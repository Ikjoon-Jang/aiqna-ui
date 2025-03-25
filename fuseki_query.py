# fuseki_query.py

import requests
from typing import List, Dict

FUSEKI_ENDPOINT = "http://3.36.178.68:3030/dataset/query"  # 수정: 실제 데이터셋 이름 사용

def run_sparql_query(query: str) -> List[Dict]:
    headers = {"Accept": "application/sparql-results+json"}
    response = requests.post(FUSEKI_ENDPOINT, data={"query": query}, headers=headers)
    response.raise_for_status()
    return response.json()["results"]["bindings"]

def get_classes() -> List[Dict]:
    query = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?class ?label ?comment
    WHERE {
      ?class a owl:Class .
      OPTIONAL { ?class rdfs:label ?label }
      OPTIONAL { ?class rdfs:comment ?comment }
    }
    """
    results = run_sparql_query(query)
    return [
        {
            "uri": r.get("class", {}).get("value"),
            "label": r.get("label", {}).get("value"),
            "comment": r.get("comment", {}).get("value"),
        }
        for r in results
    ]

def get_object_properties() -> List[Dict]:
    query = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?property ?domain ?range
    WHERE {
      ?property a owl:ObjectProperty .
      OPTIONAL { ?property rdfs:domain ?domain }
      OPTIONAL { ?property rdfs:range ?range }
    }
    """
    results = run_sparql_query(query)
    return [
        {
            "uri": r.get("property", {}).get("value"),
            "domain": r.get("domain", {}).get("value"),
            "range": r.get("range", {}).get("value"),
        }
        for r in results
    ]

def get_data_properties() -> List[Dict]:
    query = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?property ?domain ?range
    WHERE {
      ?property a owl:DatatypeProperty .
      OPTIONAL { ?property rdfs:domain ?domain }
      OPTIONAL { ?property rdfs:range ?range }
    }
    """
    results = run_sparql_query(query)
    return [
        {
            "uri": r.get("property", {}).get("value"),
            "domain": r.get("domain", {}).get("value"),
            "range": r.get("range", {}).get("value"),
        }
        for r in results
    ]

def get_individuals_with_literals() -> List[Dict]:
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?individual ?type ?prop ?value
    WHERE {
      ?individual a ?type .
      FILTER(?type != owl:Class && ?type != owl:ObjectProperty && ?type != owl:DatatypeProperty)
      OPTIONAL {
        ?individual ?prop ?value .
        FILTER(isLiteral(?value))
      }
    }
    """
    results = run_sparql_query(query)
    individuals = {}
    for r in results:
        uri = r.get("individual", {}).get("value")
        if not uri:
            continue
        if uri not in individuals:
            individuals[uri] = {
                "uri": uri,
                "type": r.get("type", {}).get("value"),
                "literals": []
            }
        if "prop" in r and "value" in r:
            individuals[uri]["literals"].append({
                "prop": r["prop"].get("value"),
                "value": r["value"].get("value")
            })
    return list(individuals.values())

def get_swrl_rules() -> List[Dict]:
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX swrl: <http://www.w3.org/2003/11/swrl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX swrla: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#>

    SELECT ?rule ?label ?comment ?body ?head ?isEnabled
    WHERE {
      ?rule rdf:type swrl:Imp .
      OPTIONAL { ?rule rdfs:label ?label }
      OPTIONAL { ?rule rdfs:comment ?comment }
      OPTIONAL { ?rule swrla:isRuleEnabled ?isEnabled }
      OPTIONAL { ?rule swrl:body ?body }
      OPTIONAL { ?rule swrl:head ?head }
    }
    """
    results = run_sparql_query(query)
    return [
        {
            "uri": r.get("rule", {}).get("value"),
            "label": r.get("label", {}),
            "comment": r.get("comment", {}),
            "body": r.get("body", {}).get("value"),
            "head": r.get("head", {}).get("value"),
            "isEnabled": r.get("isEnabled", {}).get("value"),
        }
        for r in results
    ]
