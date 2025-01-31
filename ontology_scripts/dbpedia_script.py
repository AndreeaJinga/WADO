import rdflib
from rdflib import Graph, URIRef, Literal, RDFS, RDF
import requests

DBPEDIA_SPARQL = "https://dbpedia.org/sparql"
PROGRAMMING_LANGUAGE_CLASS = rdflib.URIRef("http://example.org/ProgrammingLanguage")

def query_dbpedia_for_label(label, lang="en"):
    # sparql_query = f"""
    # PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    # SELECT ?resource
    # WHERE {{
    #   ?resource rdfs:label "{label}"@{lang} .
    #   FILTER (STRSTARTS(STR(?resource), "http://dbpedia.org/resource/"))
    # }}
    # LIMIT 1
    # """
    sparql_query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbo:  <http://dbpedia.org/ontology/>
        PREFIX dbp:  <http://dbpedia.org/property/>
        PREFIX dct:  <http://purl.org/dc/terms/>

        SELECT ?language 
            ?abstract 
            ?designer 
            ?paradigm 
            ?influencedBy 
            ?influenced 
            ?typing 
            ?latestReleaseVersion
        WHERE {{
            BIND(<http://dbpedia.org/resource/{label}> AS ?language) .
        }}
    
    """
    
    response = requests.get(DBPEDIA_SPARQL, params={'query': sparql_query, 'format': 'application/sparql-results+json'})
    data = response.json()
    print("heeere")
    print(data)
    return None
    results = data['results']['bindings']
    
    if results:
        return results[0]['resource']['value']
    return None


def get_dbpedia_triples(resource_uri, limit=5):
    """
    Retrieves the first `limit` properties of the given DBpedia resource URI.
    Returns a list of (subject, predicate, object) in string or literal form.
    """
    sparql_query = f"""
    SELECT ?p ?o
    WHERE {{
      <{resource_uri}> ?p ?o .
    }}
    LIMIT {limit}
    """
    response = requests.get(DBPEDIA_SPARQL, params={'query': sparql_query, 'format': 'json'})
    data = response.json()
    results = data['results']['bindings']
    
    triples = []
    for binding in results:
        p = binding['p']['value']  # predicate is always a URI
        o_info = binding['o']
        
        # If 'o' is a URI, we'll keep it as a URI, else as a literal
        if o_info['type'] == 'uri':
            o = o_info['value']  # e.g. http://dbpedia.org/resource/XYZ
        else:
            # It's a literal or typed literal
            o = o_info['value']
        triples.append((resource_uri, p, o))
    
    return triples

def main():
    g = rdflib.Graph()
    g.parse("v2.owl", format="xml")
    
    for pl_instance in g.subjects(RDF.type, PROGRAMMING_LANGUAGE_CLASS):
        print(f"Processing instance: {pl_instance}")
        label_value = None
        for lbl in g.objects(pl_instance, RDFS.label):
            label_value = str(lbl)
            break

        if not label_value:
            print(f"No rdfs:label found for {pl_instance}, skipping DBpedia lookup.")
            continue

        dbpedia_uri = query_dbpedia_for_label(label_value)
        if not dbpedia_uri:
            print(f"No DBpedia resource found for '{label_value}'.")
            continue
        
        print(f"Found DBpedia resource: {dbpedia_uri}")
        return None

    #     new_triples = get_dbpedia_triples(dbpedia_uri, limit=5)

    #     # 6. Insert those triples into the local graph
    #     for s, p, o in new_triples:
    #         s_node = URIRef(s)
    #         p_node = URIRef(p)

    #         # Check if 'o' looks like a URI
    #         if isinstance(o, str) and o.startswith("http"):
    #             o_node = URIRef(o)
    #         else:
    #             # Otherwise treat as literal
    #             o_node = Literal(o)

    #         g.add((s_node, p_node, o_node))
    
    # g.serialize(destination="updated_ontology.owl", format="xml")
    # print("Updated ontology saved to updated_ontology.owl")

if __name__ == "__main__":
    main()
