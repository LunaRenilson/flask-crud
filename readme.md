# Projeto Flask + Docker com CRUD em JSON

Este guia ensina como configurar um projeto **Flask** dentro de um container **Docker**, com rotas básicas de CRUD para manipular um arquivo JSON.

---

## Estrutura do projeto

```
flask-crud-docker/
│── app.py
│── data.json
│── requirements.txt
│── Dockerfile
```

---

## 1. Criar o arquivo `data.json`

```json
[
  {
    "id": 1,
    "name": "Item exemplo"
  }
]
```

---

## 2. Criar o `app.py`

```python
from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)
DATA_FILE = "data.json"

def read_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# Rotas de recuperação de dados
@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(read_data())

@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    data = read_data()
    item = next((i for i in data if i["id"] == item_id), None)
    return jsonify(item) if item else ("Item not found", 404)


# Rotas de inserção de dados
@app.route("/items", methods=["POST"])
def create_item():
    data = read_data()
    new_item = request.json
    new_item["id"] = max([i["id"] for i in data], default=0) + 1
    data.append(new_item)
    write_data(data)
    return jsonify(new_item), 201


# Rotas de modificação de dados
@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = read_data()
    item = next((i for i in data if i["id"] == item_id), None)
    if not item:
        return ("Item not found", 404)
    item.update(request.json)
    write_data(data)
    return jsonify(item)


# Rotas de remoção
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    data = read_data()
    new_data = [i for i in data if i["id"] != item_id]
    if len(new_data) == len(data):
        return ("Item not found", 404)
    write_data(new_data)
    return ("", 204)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)