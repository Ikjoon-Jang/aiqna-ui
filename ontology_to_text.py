# ontology_to_text.py

from urllib.parse import urlparse
from typing import Optional, Dict

def extract_local_name(uri: str) -> str:
    if not uri:
        return "(unknown)"
    parsed = urlparse(uri)
    return parsed.fragment if parsed.fragment else uri.split("/")[-1]

def class_to_text(cls_uri: str, label: Optional[str] = None, comment: Optional[str] = None) -> str:
    name = label if label else extract_local_name(cls_uri)
    if comment:
        return f"{name}: {comment}"
    else:
        return f"{name} is a concept in the ontology."

def object_property_to_text(prop_uri: str, domain: Optional[str], range_: Optional[str]) -> str:
    prop = extract_local_name(prop_uri)
    dom = extract_local_name(domain) if domain else "some entity"
    rng = extract_local_name(range_) if range_ else "another entity"
    return f"'{prop}' is a relationship from {dom} to {rng}."

def data_property_to_text(prop_uri: str, domain: Optional[str], range_: Optional[str]) -> str:
    prop = extract_local_name(prop_uri)
    dom = extract_local_name(domain) if domain else "some entity"
    rng = extract_local_name(range_) if range_ else "a data value"
    return f"'{prop}' is a data property of {dom} and has value type {rng}."

def swrl_rule_to_text(rule: Dict) -> str:
    label = rule.get("label", {}).get("value")
    comment = rule.get("comment", {}).get("value")
    if label and comment:
        return f"Rule {label}: {comment}"
    elif comment:
        return f"A rule: {comment}"
    elif label:
        return f"Rule {label} with no description."
    else:
        return "Unnamed rule in the ontology."