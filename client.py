import requests

BASE_URL = "http://localhost:5000"

def list_items():
    response = requests.get(f"{BASE_URL}/products")
    print("Itens:", response.json())


def get_item(item_id):
    response = requests.get(f"{BASE_URL}/products/{item_id}")
    if response.status_code == 200:
        print("Item encontrado:", response.json())
    else:
        print("Item não encontrado")


def create_item(name, price=0.0):
    response = requests.post(f"{BASE_URL}/products", json={"name": name, "price": price})
    print("Item criado:", response.json())


def update_item(item_id, name, price=0.0):
    response = requests.put(f"{BASE_URL}/products/{item_id}", json={"name": name, "price": price})
    if response.status_code == 200:
        print("Item atualizado:", response.json())
    else:
        print("Item não encontrado")


def delete_item(item_id):
    response = requests.delete(f"{BASE_URL}/products/{item_id}")
    if response.status_code == 204:
        print(f"Item {item_id} removido com sucesso")
    elif response.status_code == 404:
        print("Item não encontrado")


if __name__ == "__main__":
    # Exemplos de uso
    
    list_items()
    # create_item("Fancy Hat", 800)
    # delete_item(7)
