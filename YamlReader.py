import yaml

with open("menuPrices.yaml", "r")as f:
    data = yaml.safe_load(f)

def find (name):
    
    if name not in data.keys():
        print("Error")
    else: 
        for i in data:
            if i == name:
                for k in data[i]:
                    if k == 'price':
                        print(f"Dish name: {name}")
                        print(f"Price: {data[i][k]}")
                    elif k == 'quantity':
                        print(f"Quantity: {data[i][k]}")
                break

find("Burger")