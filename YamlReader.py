import yaml

def load_menu_from_file(file_path):
    with open(file_path, 'r') as file:
        menu_data = yaml.safe_load(file)
    return menu_data

def save_menu_to_file(menu_data, file_path):
    with open(file_path, 'w') as file:
        yaml.dump(menu_data, file)

menu_file_path = 'menuPrices.yaml' # path of the file

menu_data = load_menu_from_file(menu_file_path) # dictionary data structure

new_item = {"Coke": {"price": 3, "quantity": 10}}  # adding a new item
menu_data.update(new_item)


save_menu_to_file(menu_data, menu_file_path) # save menu to file

print(menu_data)