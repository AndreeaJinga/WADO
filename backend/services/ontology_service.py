import os
from rdflib import Graph, URIRef, RDF
from rdflib.plugins.sparql.processor import SPARQLResult
from flask import current_app

class OntologyService:
    def __init__(self, ontology_path):
        self.graph = Graph()
        if os.path.exists(ontology_path):
            self.graph.parse(ontology_path, format='xml')  # or 'turtle' as needed


    def get_instances_of_class(self, class_uri):
        """Return instances (subjects) that have rdf:type == class_uri."""
        instances = []
        for s in self.graph.subjects(RDF.type, URIRef(class_uri)):
            instances.append(str(s))
        return instances


    def get_concept_info(self, concept_uri):
        """Return a dict of all predicates and objects for the concept."""
        concept_info = {}
        concept_ref = URIRef(concept_uri)
        for p, o in self.graph.predicate_objects(concept_ref):
            concept_info[str(p)] = str(o)
        return concept_info


    def get_frameworks_for_language(self, language):
        """retunrs the frameworks for a given language"""
        frameworks = []

        query = f"""
        PREFIX ns1: <{current_app.config["BASE_URL"]}> 
        SELECT ?Framework WHERE {{ 
            ?Framework ns1:usesLanguage <{current_app.config["BASE_URL"]}ProgrammingLanguage#{language}> .
            ?Framework rdf:type ns1:Framework .
            }}
        """
        result = None
        try:
            result = self.graph.query(query)
            for row in result:
                frameworks.append(str(row[0]))
        except Exception as e:
            print(f"SPARQL query error: {e}")
        return frameworks
        
        
        
    def run_sparql_query(self, sparql_query):
        """
        Execute the SPARQL query string on the RDF graph and return a list of dicts.
        Each dict represents one row of the SPARQL results with variable bindings.
        """
        try:
            result: SPARQLResult = self.graph.query(sparql_query)
            # Convert each row in the result to a dict: { var_name: "value" }
            results_list = []
            for row in result:
                row_dict = {
                    var: str(value) for var, value in row.asdict().items()
                }
                results_list.append(row_dict)
            return results_list

        except Exception as e:
            print(f"SPARQL query error: {e}")
            return None
        
    def get_my_classes(self):
        classes = set()
        for s in self.graph.subjects(RDF.type):
            if str(s).startswith(current_app.config['BASE_URL']):
                if "#" in str(s):
                    classes.add(str(s).split("#")[0])
        classes = list(classes)
        return classes