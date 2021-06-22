import requests
import json
from tabulate import tabulate
import time

holders_url = "https://wax.api.atomicassets.io/atomicassets/v1/accounts?collection_name=novarallywax&page=1&limit=100&order=desc"
holders_response = requests.get(holders_url)

common_snake = 1000
uncommon_snake = 3500
rare_snake = 12500
classic_snake = 35000
sketch_snake = 100000

holders_dict = {}
final_table_list = []

raw_holders_data = json.loads(holders_response.content)

print("Do note that the account in position after 100 maybe higher than the others, i have just fetched the first 100 addresses and sorted them out")
print("You would be waiting here the entire day if i were to sort every single address (blame the API)")
print("This is going to take a while.........")

# print(holders_list)
def getAssets(owner):
    complete_raw_data = []
    page = 1
    checkComplete = 0
    while checkComplete == 0:
        response = requests.get(f"https://wax.api.atomicassets.io/atomicassets/v1/assets?owner={owner}&collection_name=novarallywax&page={page}&limit=1000&order=desc&sort=asset_id")
        raw_data = json.loads(response.content)
        complete_raw_data += raw_data["data"]
        if len(raw_data["data"]) == 1000:
            # print(page)
            page += 1      
        else:
            checkComplete = 1
    return complete_raw_data

def snakeoil(owner):
    complete_raw_data = getAssets(owner)
    common_count = 0
    uncommon_count = 0
    rare_count = 0
    classic_count = 0
    sketch_count = 0
    for i in range(len(complete_raw_data)):
        try:
            rarity = complete_raw_data[i]["template"]["immutable_data"]["Rarity"]
            if rarity == "Common":
                common_count += 1
            if rarity == "Uncommon":
                uncommon_count += 1
            if rarity == "Rare":
                rare_count += 1
            if rarity == "Classic":
                classic_count += 1
            if rarity == "Sketch":
                sketch_count += 1
        except:
            pass

    total_snake = (common_count*common_snake) + (uncommon_count*uncommon_snake) + (rare_count*rare_snake) + (classic_count*classic_snake) + (sketch_count*sketch_snake)
    return dict({owner:total_snake})

# dict1 = snakeoil("k3bri.wam")
# dict2 = {'hello':5689}

# dict2.update(dict1)

# print(dict2)

for i in range(100):
    owner = raw_holders_data["data"][i]["account"]
    holders_dict.update(snakeoil(owner))

# print(holders_dict)

sorted_holders_dict = dict(sorted(holders_dict.items(), key=lambda item: item[1],reverse=True))

sorted_holders_dict_keys = list(sorted_holders_dict.keys())
sorted_holders_dict_values = list(sorted_holders_dict.values())

for i in range(100):
    final_table_list.append(list((i+1,sorted_holders_dict_keys[i],sorted_holders_dict_values[i],int(sorted_holders_dict_values[i]/10))))

# print(final_table_list)

table = tabulate(final_table_list, headers=["Rank","Account Name","Snaking Power","Snaking Power Pre-launch"], tablefmt='orgtbl')

print(table)

print("\nMade by TheViralClovers/k3bri.wam")

while True:
    time.sleep(1000)