# import json
#
# import requests
#
# url = "https://dummyjson.com/auth/login"
#
# payload = {
#     "username": "emilys",
#     "password": "emilyspass"
# }
#
# res = requests.post(url, json=payload)
# data = res.json()
# token = data["accessToken"]
# print(token)
#
# headers = {"Authorization": f"Bearer {token}"}
#
# me_url = "https://dummyjson.com/auth/me"
# req_me = requests.get(me_url, headers=headers)
# data = req_me.json()
# print(data)



import requests



class AuthSession:
    def __init__(self):
        self.token = None
    def login_request(self):
        url = "https://dummyjson.com/auth/login"
        payload =  {
                "username": "emilys",
                "password": "emilyspass"
            }
        response = requests.post(url, json=payload)
        self.token = response.json()["accessToken"]
    def token_handler(self):
        if self.token is None:
            self.login_request()
        return {"Authorization": f"Bearer {self.token}"}

    def get(self, url):
        return requests.get(url, headers=self.token_handler())



se = AuthSession()
respons = se.get("https://dummyjson.com/auth/me")
print(respons.status_code)
print(respons.json())
print(respons.headers)