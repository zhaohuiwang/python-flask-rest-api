import requests
import json


response = requests.get('https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow')
print(response) # <Response [200]>
print(response.json()) # all the items

print(response.json().keys)
print(response.json()['items']) # just a list now

for value in response.json()['items']:
    if value['answer_count'] == 0:
        print(value['title'])
    else:
        print()