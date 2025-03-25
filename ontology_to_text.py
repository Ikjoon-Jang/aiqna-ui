# ontology_to_text.py
from urllib.parse import urlparse
from typing import Optional, Dict, List

def extract_local_name(uri: Optional[object]) -> str:
    if not uri:
        return "(unknown)"
    if isinstance(uri, dict):
        uri = uri.get("value", "")
    if not isinstance(uri, str):
        return "(unknown)"
    parsed = urlparse(uri)
    return parsed.fragment if parsed.fragment else uri.split("/")[-1]

def class_to_text(cls_uri, label: Optional[Dict] = None, comment: Optional[Dict] = None) -> str:
    name = label.get("value") if label and "value" in label else extract_local_name(cls_uri)
    if comment and "value" in comment:
        return f"{name}: {comment['value']}"
    else:
        return f"{name} is a concept in the ontology."

def object_property_to_text(prop_uri, domain, range_) -> str:
    prop = extract_local_name(prop_uri)
    dom = extract_local_name(domain)
    rng = extract_local_name(range_)
    return f"'{prop}' is a relationship from {dom} to {rng}."

def data_property_to_text(prop_uri, domain, range_) -> str:
    prop = extract_local_name(prop_uri)
    dom = extract_local_name(domain)
    rng = extract_local_name(range_)
    return f"'{prop}' is a data property of {dom} and has value type {rng}."

def individual_to_text(ind_uri, type_uri, literals: Optional[List[Dict]] = None) -> str:
    name = extract_local_name(ind_uri)
    type_name = extract_local_name(type_uri)
    if literals:
        literals_text = "; ".join(
            [f"{extract_local_name(lit.get('prop'))} = {lit.get('value')}" for lit in literals if 'prop' in lit and 'value' in lit]
        )
        return f"{name} is an individual of type {type_name} with values: {literals_text}."
    else:
        return f"{name} is an individual of type {type_name}."

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

def ontology_elements_to_sentences(classes, object_props, data_props, individuals, rules):
    sentences = []

    # 클래스
    for cls in classes:
        uri = cls.get("uri")
        label = cls.get("label")
        comment = cls.get("comment")
        sentences.append(class_to_text(uri, label, comment))

    # 객체 속성
    for prop in object_props:
        sentences.append(object_property_to_text(prop.get("uri"), prop.get("domain"), prop.get("range")))

    # 데이터 속성
    for prop in data_props:
        sentences.append(data_property_to_text(prop.get("uri"), prop.get("domain"), prop.get("range")))

    # 인디비주얼
    for ind in individuals:
        uri = ind.get("uri")
        type_ = ind.get("type")
        literals = ind.get("literals", [])
        sentences.append(individual_to_text(uri, type_, literals))

    # SWRL 룰
    for rule in rules:
        sentences.append(swrl_rule_to_text(rule))

    return sentences
