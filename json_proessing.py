import json

with open("data.json","r") as f:
    data = json.load(f)

print(data)

# print all employee names with designation
departments = data["company"]["departments"]


for department in departments:
    print(f"{department['manager']['name']} -----> {department['manager']['contact']['email']}")
    for team in department["teams"]:
        print(f"{team['teamId']}")
        for menber in team["members"]:
            print(f"{menber['name']}")

