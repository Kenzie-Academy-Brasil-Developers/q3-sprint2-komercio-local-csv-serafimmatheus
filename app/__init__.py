import numbers
from flask import Flask, jsonify, request
import os
import csv
from http import HTTPStatus
from app.products import open_csv_append, open_csv_reading, open_csv_writer

app = Flask(__name__)

route = os.getenv("MY_VARIABLE_ROTA")

@app.get("/products")
def get_products():
    try:
        list_products = open_csv_reading(route)
        per_page = request.args.get("per_page", 0)
        page = request.args.get("page", 0)
        
        total = len(list_products[int(0):int(per_page)])
        inicial = (int(page) - 1) * int(total)
        final = int(per_page) * int(page)

        if per_page == 0:
            final = 3        

        return {"data": list_products[inicial:final]}, HTTPStatus.OK
    except:
        return {"msg": "Algo deu errado!"}, HTTPStatus.BAD_REQUEST


@app.get("/products/<product_id>")
def get_product_id(product_id):

    try:
        list_dict_products = open_csv_reading(route)

        list_products = [i for i in list_dict_products if int(i["id"]) == int(product_id)]

        return {"data": list_products}
                
        
    except:
        return {"error": f"id {product_id} não encontrado"}, HTTPStatus.BAD_REQUEST


@app.post("/products")
def post_products():

    try:
        data = request.get_json()

        expected_keys = {"name", "price"}
        body_keys_set = set(data.keys())
        invalid_keys = body_keys_set - expected_keys
        if invalid_keys:
            return {
                "error": "invalid_keys",
                "expected": list(expected_keys),
                "received": list(body_keys_set)

            }, HTTPStatus.BAD_REQUEST

        cont_list = []
        lendo = open_csv_reading(route)
        for i in lendo:
            cont_list.append(i["id"])
        
        open_csv_append(route, data, cont_list)
        
        return {"id": int(cont_list[::-1][0]) + 1, "name": data["name"], "price": data["price"]}, HTTPStatus.CREATED
            

    except:
        return {"msg": "algo deu errado!"}, HTTPStatus.BAD_REQUEST


@app.patch("/products/<product_id>")
def patch_products(product_id):
    data = request.get_json()

    expected_keys = {"name", "price"}
    body_keys_set = set(data.keys())
    invalid_keys = body_keys_set - expected_keys
    if invalid_keys:
        return {
        "error": "invalid_keys",
        "expected": list(expected_keys),
        "received": list(body_keys_set)

    }, HTTPStatus.BAD_REQUEST

    lendo = open_csv_reading(route)
    list_filtered = []
    for i in lendo:
        if i["id"] == product_id:
            i = {"id": i["id"], "name": data["name"], "price": data["price"]}
        
        list_filtered.append(i)


    if len(list_filtered) == 0:
        return {"error": f"product id {product_id} not found"}, HTTPStatus.BAD_REQUEST

    open_csv_writer(route, list_filtered)

    product_obj = [product for product in list_filtered if product["id"] == product_id] 

    if len(product_obj) == 0:
        return {"error": f"product id {product_id} not found"}, HTTPStatus.BAD_REQUEST

    return {"data": product_obj}



@app.delete("/products/<product_id>")
def delete_products(product_id):
    leitura = open_csv_reading(route)

    list_filtered = [i for i in leitura if i["id"] != product_id]

    open_csv_writer(route, list_filtered)

    return {"msg": f"id {product_id} removido"}
    
    
  
