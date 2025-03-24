from fuseki_query import (
    get_classes,
    get_object_properties,
    get_data_properties,
    get_individuals,
    get_swrl_rules
)

from ontology_to_text import (
    class_to_text,
    object_property_to_text,
    data_property_to_text,
    swrl_rule_to_text
)

def print_sentences(title, sentences):
    print(f"\n===== {title} (Natural Language) =====")
    for s in sentences:
        print(f"- {s}")

if __name__ == "__main__":
    # 1. 클래스 → 자연어
    class_results = get_classes()
    class_sentences = [
        class_to_text(
            c["class"]["value"],
            c.get("label", {}).get("value"),
            c.get("comment", {}).get("value")
        )
        for c in class_results
    ]
    print_sentences("Classes", class_sentences)

    # 2. 오브젝트 속성 → 자연어
    obj_results = get_object_properties()
    obj_sentences = [
        object_property_to_text(
            o["property"]["value"],
            o.get("domain", {}).get("value"),
            o.get("range", {}).get("value")
        )
        for o in obj_results
    ]
    print_sentences("Object Properties", obj_sentences)

    # 3. 데이터 속성 → 자연어
    data_results = get_data_properties()
    data_sentences = [
        data_property_to_text(
            d["property"]["value"],
            d.get("domain", {}).get("value"),
            d.get("range", {}).get("value")
        )
        for d in data_results
    ]
    print_sentences("Data Properties", data_sentences)

    # 4. SWRL 룰 → 자연어
    swrl_results = get_swrl_rules()
    swrl_sentences = [swrl_rule_to_text(r) for r in swrl_results]
    print_sentences("SWRL Rules", swrl_sentences)
