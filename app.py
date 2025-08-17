from flask import Flask, jsonify, request
import json
import os


app = Flask(__name__)
DATA_FILE = 'data.json'

# Ler whole json file
def read_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as file:
        return json.load(file)
    
# rewrite whole json file
def write_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)


# Recover data from json file
@app.route("/products", methods=["GET"])
def get_products():
    """Get all products."""
    return jsonify(read_data())

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """Get a product by ID."""
    data = read_data()
    item = next((item for item in data if item['id'] == product_id), None)
    return jsonify(item) if item else ('', 404)


# insert data into json file
@app.route("/products", methods=["POST"])
def create_product():
    """Create a new product."""
    data = read_data()
    new_product = request.json
    new_product['id'] = max([item['id'] for item in data], default=0) + 1
    data.append(new_product)
    write_data(data)
    return jsonify(new_product)


# update data in json file
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_item(product_id):
    data = read_data()
    item = next((i for i in data if i["id"] == product_id), None)
    if not item:
        return ("Item not found", 404)
    item.update(request.json)
    write_data(data)
    return jsonify(item)


# delete data from json file
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_item(product_id):
    data = read_data()
    new_data = [item for item in data if item['id'] != product_id]

    if len(new_data) == len(data):
        return ("Item not found", 404)
    write_data(new_data)
    
    # Return no content status
    return ('', 204)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)