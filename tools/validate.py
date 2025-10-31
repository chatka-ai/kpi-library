import json, sys, yaml
from jsonschema import validate

with open("schema/kpi_schema.json") as f:
    schema = json.load(f)

def check(path):
    with open(path) as f:
        doc = yaml.safe_load(f)
    validate(instance=doc, schema=schema)
    print("OK:", path)

if __name__ == "__main__":
    for p in sys.argv[1:]:
        check(p)
