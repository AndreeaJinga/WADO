import os
import requests
from dotenv import load_dotenv # type: ignore
from rdflib import Graph, Namespace, URIRef, RDF, RDFS, Literal, XSD # type: ignore
from datetime import datetime

FILE_VERSION = 1

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("Missing GITHUB_TOKEN in .env")

BASE_URI = "http://example.org/"
WEBDEV = Namespace(BASE_URI)

ontology_file = f"v{FILE_VERSION}.owl"
g = Graph()
g.parse(ontology_file, format="xml")


def safe_string(uri_str):
    safe_uri = uri_str.replace(" ", "_")        # avoid spaces
    safe_uri = safe_uri.replace("'", "")        # avoid quotes
    safe_uri = safe_uri.replace('"', "")        # avoid double-quotes
    safe_uri = safe_uri.replace("#", "_sharp")  # avoid hashtag
    return safe_uri


def fetch_repos_by_topic(topic: str, min_stars: int = 10000, limit: int = 50):
    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

    query_string = f"topic:{topic} stars:>={min_stars} sort:stars-desc"

    graphql_query = """
    query($queryString: String!, $limit: Int!) {
      search(query: $queryString, type: REPOSITORY, first: $limit) {
        edges {
          node {
            ... on Repository {
              name
              description
              url
              createdAt
              licenseInfo {
                name
              }
              primaryLanguage {
                name
              }
            }
          }
        }
      }
    }
    """

    variables = {
        "queryString": query_string,
        "limit": limit
    }

    response = requests.post(url, json={"query": graphql_query, "variables": variables}, headers=headers)
    if response.status_code != 200:
        raise Exception(f"GitHub GraphQL query failed: {response.status_code}\n{response.text}")

    data = response.json()
    edges = data["data"]["search"]["edges"]
    return [edge["node"] for edge in edges]


def has_year(repo):
    created_at = repo.get("createdAt")
    if created_at:
        dt = datetime.fromisoformat(created_at.replace("Z",""))
        return str(dt.year)
    return None


def insert_repos_into_ontology(repos, topic: str):
    for repo in repos:
        safe_name = safe_string(repo["name"])

        repo_uri = URIRef(f"{BASE_URI}{topic}#{safe_name}")

        g.add((repo_uri, RDF.type, getattr(WEBDEV, topic)))
        g.add((repo_uri, RDFS.label, Literal(repo["name"], datatype=XSD.string)))

        if repo.get("description"):
            g.add((repo_uri, WEBDEV.hasDescription, Literal(repo["description"], datatype=XSD.string)))

        if repo.get("url"):
            g.add((repo_uri, WEBDEV.hasURL, Literal(repo["url"], datatype=XSD.anyURI)))

        year_str = has_year(repo)
        if year_str !=  None:
            g.add((repo_uri, WEBDEV.hasReleaseYear, Literal(year_str, datatype=XSD.gYear)))

        license_str =  repo.get("licenseInfo", {})
        if license_str != None:
            license_str = safe_string(license_str.get("name").lower())
            license_uri = URIRef(f"http://example.org/License#{license_str}")  

            if not (license_uri, RDF.type, WEBDEV.License) in g:
                print(f"Adding new license: {license_str}")
                g.add((license_uri, RDF.type, WEBDEV.License))
                g.add((license_uri, RDFS.label, Literal(license_str, datatype=XSD.string)))

            g.add((repo_uri, WEBDEV.isLicenseUnder, license_uri))

        primary_lang_str = repo.get("primaryLanguage", {})
        if primary_lang_str != None:
            primary_lang_str = safe_string(primary_lang_str.get("name").lower())
            primary_lang_uri = URIRef(f"http://example.org/ProgrammingLanguage#{primary_lang_str}")  

            if not (primary_lang_uri, RDF.type, WEBDEV.ProgrammingLanguage) in g:
                print(f"Adding new ProgrammingLanguage: {primary_lang_str}")
                g.add((primary_lang_uri, RDF.type, WEBDEV.ProgrammingLanguage))
                g.add((primary_lang_uri, RDFS.label, Literal(primary_lang_str, datatype=XSD.string)))

            g.add((repo_uri, WEBDEV.usesLanguage, primary_lang_uri))


def main():
    map_topic_search = {
        "framework": "Framework",
        "aop": "AOPFramework",
        "backend": "BackendFramework",
        "frontend": "FrontendFramework",
        "ml": "MachineLearningFramework",
        "orm": "ORMFramework",
        "spa": "SPAFramework",
        "template-engine": "TemplateEngine",
        "ide": "IDE",
        "interpreter": "Interpreter",
        "library": "Library",
        "os": "OperatingSystem",
        "programming-language": "ProgrammingLanguage",
        "sdk": "SDK",
    }
    map_topic_star ={
        "framework": 10000,
        "aop": 1000,
        "backend": 5000,
        "frontend": 5000,
        "ml": 5000,
        "orm": 5000,
        "spa": 2000,
        "template-engine": 2000,
        "ide": 5000,
        "interpreter": 5000,
        "library": 5000,
        "os": 3000,
        "programming-language": 10000,
        "sdk": 10000,
    }

    for key in map_topic_search.keys():
        print()
        print(f"Fetching top repositories for topic '{key}'...")
        repos = fetch_repos_by_topic(key, min_stars=map_topic_star[key], limit=100)

        print(f"Found {len(repos)} repositories for topic '{key}'.")
        insert_repos_into_ontology(repos, map_topic_search[key])
        print("DONE")
        print()

    new_version = FILE_VERSION + 1
    g.serialize(destination=f"v{new_version}.owl", format="xml")


if __name__ == "__main__":
    main()
