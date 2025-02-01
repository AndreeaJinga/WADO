import rdflib
from rdflib import Graph, URIRef, Literal, RDFS, RDF, Namespace, XSD
import requests

DBPEDIA_SPARQL = "https://dbpedia.org/sparql"
PROGRAMMING_LANGUAGE_CLASS = rdflib.URIRef("http://example.org/ProgrammingLanguage")

BASE_URI = "http://example.org/"
WEBDEV = Namespace(BASE_URI)

def query_dbpedia_for_label(label, lang="en"):
    sparql_query = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dbo:  <http://dbpedia.org/ontology/>
    PREFIX dbp:  <http://dbpedia.org/property/>
    PREFIX dct:  <http://purl.org/dc/terms/>

    SELECT ?language ?abstract ?designer ?paradigm ?developer ?year
    WHERE {{
        BIND(<http://dbpedia.org/resource/{label}> AS ?language)

        OPTIONAL {{
            ?language dbo:abstract ?abstract .
            FILTER (LANG(?abstract) = "en")
        }}

        OPTIONAL {{ ?language dbo:designer ?designer . }}
        OPTIONAL {{ ?language dbp:designer ?designer . }}

        OPTIONAL {{ ?language dbo:paradigm ?paradigm . }}
        OPTIONAL {{ ?language dbp:paradigm ?paradigm . }}

        OPTIONAL {{ ?language dbo:developer ?developer . }}
        OPTIONAL {{ ?language dbp:developer ?developer . }}

        OPTIONAL {{ ?language dbo:released ?year . }}
        OPTIONAL {{ ?language dbo:year ?year . }}
    }}
    """
    
    response = requests.get(DBPEDIA_SPARQL, params={'query': sparql_query, 'format': 'application/sparql-results+json'})
    data = response.json()
    results = data['results']['bindings']
    
    if results:
        return results[0]
    return None


def process_dbpedia_resource(resource_name, resource, g):
    resource_uri = URIRef(f"{BASE_URI}ProgrammingLanguage#{resource_name}")
    language_uri = resource.get("language", {}).get("value")
    g.add((resource_uri, WEBDEV.hasURL, Literal(language_uri, datatype=XSD.anyURI)))
    
    abstract = resource.get("abstract", {}).get("value") if "abstract" in resource else None
    if abstract:
        g.add((resource_uri, WEBDEV.hasDescription, Literal(abstract, datatype=XSD.string)))
    
    designer = resource.get("designer", {}).get("value") if "designer" in resource else None
    if designer:
        g.add((resource_uri, WEBDEV.hasDesigner, Literal(designer, datatype=XSD.string)))
        
    developer = resource.get("developer", {}).get("value") if "developer" in resource else None
    if developer:
        g.add((resource_uri, WEBDEV.hasDeveloper, Literal(developer, datatype=XSD.string)))
        
    year = resource.get("year", {}).get("value") if "year" in resource else None
    if year:
        g.add((resource_uri, WEBDEV.hasReleaseYear, Literal(year, datatype=XSD.gYear)))
            

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
        if dbpedia_uri:
            print(f"Found DBpedia resource: {label_value}")
            
            process_dbpedia_resource(label_value, dbpedia_uri, g)
            

    g.serialize(destination="updated_ontology.owl", format="xml")
    print("Updated ontology saved to updated_ontology.owl")


if __name__ == "__main__":
    main()
