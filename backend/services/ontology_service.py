import os
from rdflib import Graph, URIRef, RDF
from rdflib.plugins.sparql.processor import SPARQLResult


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