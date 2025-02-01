from flask import Blueprint, jsonify, request, current_app
from services.ontology_service import OntologyService
from services.user_service import UserService
from services.email_service import EmailService

ontology_blueprint = Blueprint('ontology', __name__)


# @ontology_blueprint.before_app_request
# def init_ontology_service():
#     """Load the ontology once when the app starts."""
#     ontology_path = 'ontology.owl'  # Adjust the path if needed
#     current_app.config['ONTOLOGY_SERVICE'] = OntologyService(ontology_path)


def token_required(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Missing or invalid Authorization header"}), 401
        token = auth_header.split()[1]
        user_service: UserService = current_app.config['USER_SERVICE']
        username = user_service.validate_token(token)
        if not username:
            return jsonify({"message": "Invalid or expired token"}), 401
        
        # Store the username in the request context if needed
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__  # Keep function name for Flask
    return wrapper


@ontology_blueprint.route('/class/<path:class_uri>/instances', methods=['GET'])
@token_required
def get_class_instances(class_uri):
    """
    Example call: GET /api/ontology/class/http://example.org/MyClass/instances
    (encoded URI)
    """
    ontology_service: OntologyService = current_app.config['ONTOLOGY_SERVICE']
    instances = ontology_service.get_instances_of_class(class_uri)
    return jsonify({"class_uri": class_uri, "instances": instances})


@ontology_blueprint.route('/concept', methods=['GET'])
def get_concept_info():
    """
    GET /api/ontology/concept?uri=<concept_uri>
    """
    concept_uri = request.args.get('uri')
    if not concept_uri:
        return jsonify({"message": "Missing concept URI"}), 400
    
    ontology_service: OntologyService = current_app.config['ONTOLOGY_SERVICE']
    concept_info = ontology_service.get_concept_info(concept_uri)
    return jsonify({"concept_uri": concept_uri, "info": concept_info})


@ontology_blueprint.route('/sparql', methods=['POST'])
@token_required
def run_sparql():
    ontology_service: OntologyService = current_app.config['ONTOLOGY_SERVICE']
    
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"message": "No SPARQL query provided"}), 400
    
    sparql_query = data['query']
    email_bool = data['email_bool']
    
    results = ontology_service.run_sparql_query(sparql_query)
    if results is None:
        return jsonify({"message": "Error executing SPARQL query"}), 500
    
    json_results = jsonify({"results": results})
    if email_bool:
        email_service: EmailService = current_app.config['EMAIL_SERVICE']
        auth_header = request.headers.get('Authorization')
        token = auth_header.split()[1]
        user_service: UserService = current_app.config['USER_SERVICE']
        username = user_service.validate_token(token)
        email_service.send_email(username,"WADO app query", f"{sparql_query}\n\n{results}")
    return json_results, 200