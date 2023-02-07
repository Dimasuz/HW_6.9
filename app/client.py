import time

import requests

response = requests.post(
    "http://127.0.0.1:8000/users/",
    json={
        "name": f"user_{time.time()}",
        "email": f"user_{time.time()}@em.em",
        "password": "123",
    },
)


print(response.status_code)
# print(response.json())
print(response.text)
#
# response = requests.get('http://127.0.0.1:8000/users/2/')
#
# print(response.status_code)
# print(response.text)


# response = requests.delete('http://127.0.0.1:8000/users/2')
#
# print(response.status_code)
# print(response.text)
#
# response = requests.get('http://127.0.0.1:8000/users/2')
#
# print(response.status_code)
# print(response.text)


# response = requests.post('http://127.0.0.1:8000/adv/',
#                         json={f'title': 'title_{time.time()}',
#                               f'descr': 'descr_{time.time()}',
#                               'user_id': 2,
#                               'password': '123',
#                               }
#                         )
#
#
# print(response.status_code)
# print(response.json())
# print(response.text)


# response = requests.patch('http://127.0.0.1:8000/adv/1/',
#                         json={'descr': 'descr_1_patch1.2',
#                               'user_id': 1,
#                               'password': '123',
#                               }
#                         )
# print(response.status_code)
# # print(response.json())
# print(response.text)
# #
#

response = requests.get("http://127.0.0.1:8000/adv/1/")

print(response.status_code)
# print(response.text)

response = requests.delete(
    "http://127.0.0.1:8000/adv/1/",
    json={
        "user_id": 1,
        "password": "12",
    },
)

print(response.status_code)
# print(response.json())

# #
#
#
# response = requests.get("http://127.0.0.1:8000/adv/1/")
#
# print(response.status_code)
# print(response.text)
