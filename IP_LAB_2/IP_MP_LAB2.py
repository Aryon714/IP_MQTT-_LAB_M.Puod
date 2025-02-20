import json;

json_files = ["users1.json", "users2.json"]

python_objects = []

for json_file in json_files:
    with open(json_file, "r") as f:
        python_objects.append(json.load(f))

with open("users3.json", "w") as f:
    json.dump(python_objects, f, indent=4)