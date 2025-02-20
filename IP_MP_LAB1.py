import json;

a = {
    "firstName":"Martynas",
    "lastName":"Puodziunas",
    "city":"Vilnius",
    "age":"24"
}

b = json.dumps(a)

print(b)