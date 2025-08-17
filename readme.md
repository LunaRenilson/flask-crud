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
        "name": "Celular",
        "price": 1200.00,
        "description": "Smartphone with 128GB storage and 6GB RAM"
    },
    {
        "id": 2,
        "name": "Laptop",
        "price": 2500.00,
        "description": "15-inch laptop with Intel i7 processor and 16GB RAM"
    },
    {
        "id": 3,
        "name": "Tablet",
        "price": 800.00,
        "description": "10-inch tablet with 64GB storage and Wi-Fi connectivity"
    },
    {
        "id": 4,
        "name": "Smartwatch",
        "price": 300.00,
        "description": "Smartwatch with heart rate monitor and GPS"
    },
    {
        "id": 5,
        "name": "Headphones",
        "price": 150.00,
        "description": "Wireless headphones with noise cancellation"
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

@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(read_data())

@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    data = read_data()
    item = next((i for i in data if i["id"] == item_id), None)
    return jsonify(item) if item else ("Item not found", 404)

@app.route("/items", methods=["POST"])
def create_item():
    data = read_data()
    new_item = request.json
    new_item["id"] = max([i["id"] for i in data], default=0) + 1
    data.append(new_item)
    write_data(data)
    return jsonify(new_item), 201

@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = read_data()
    item = next((i for i in data if i["id"] == item_id), None)
    if not item:
        return ("Item not found", 404)
    item.update(request.json)
    write_data(data)
    return jsonify(item)

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
```

---

## 3. Dependências (`requirements.txt`)

```
flask==3.0.3
```

---

## 4. Criar o `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

---

## 5. Build e execução com Docker

### Build da imagem:
```bash
docker build -t flask-crud .
```

### Rodar o container:
```bash
docker run -p 5000:5000 flask-crud
```

---

## 6. Testando as rotas

- **Listar itens**
  ```http
  GET http://localhost:5000/items
  ```

- **Criar item**
  ```http
  POST http://localhost:5000/items
  Content-Type: application/json

  {
    "name": "Novo item"
  }
  ```

- **Atualizar item**
  ```http
  PUT http://localhost:5000/items/1
  Content-Type: application/json

  {
    "name": "Item atualizado"
  }
  ```

- **Excluir item**
  ```http
  DELETE http://localhost:5000/items/1
  ```

---

## 7. Depuração de erros comuns

Se aparecer o erro **`ModuleNotFoundError: No module named flask`**:

1. Certifique-se de que o `requirements.txt` está correto.
2. Refaça o build sem cache:
   ```bash
   docker build --no-cache -t flask-crud .
   ```
3. Verifique dentro do container se o Flask foi instalado:
   ```bash
   docker run -it flask-crud bash
   pip list | grep Flask
   ```

Se não aparecer nada, significa que o `pip install` não rodou corretamente.

---
