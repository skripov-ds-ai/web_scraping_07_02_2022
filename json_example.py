import json
from pprint import pprint


def read_json(filename):
    """
    The function for returning Python dict from json file
    :param filename: str ; it is string which contains filename
    :return: dict ; final json
    """
    new_data = {}
    with open(filename, "r") as f:
        new_data = json.load(f)
    return new_data


data = {
    "some_count": 3,
    "fruits": [
        "apple",
        "banana",
    ]
    * 10,
    "price": {
        "a": "b",
    },
}
json_data = json.dumps(data)

print(data)
print("=" * 15)
pprint(data)
print("$" * 15)
pprint(json_data)
print()

filename = "new_json_with_fruits.json"
with open(filename, "w") as f:
    # json.dump(data, f)
    json.dump(data, f, indent=4)

new_data = None
with open(filename, "r") as f:
    new_data = json.load(f)

print(new_data)
print("*" * 15)
pprint(new_data)
print()
