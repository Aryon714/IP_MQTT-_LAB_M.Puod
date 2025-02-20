a = '{"firstName":"Martynas","lastName":"Puodziunas","city":"Vilnius"}'
b={
    "age":"24"
}

c = json.loads(a)

c.update(b)

print(c)
