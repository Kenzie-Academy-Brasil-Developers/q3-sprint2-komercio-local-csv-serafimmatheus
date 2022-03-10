from csv import DictReader, DictWriter
from http import HTTPStatus

def open_csv_reading(file):
    with open(file, "r") as f:
        list_products_dict = DictReader(f)
        # return [product for product in list_products_dict]

        list_teste = []
        for product in list_products_dict:
            product["id"] = int(product["id"])
            product["price"] = float(product["price"])
            list_teste.append(product)

        return list_teste


def open_csv_append(file, data, cont_list):
    with open(file, "a") as f:
        fieldnames = ["id", "name", "price"]
        file_open = DictWriter(f, fieldnames=fieldnames)
        file_open.writerow({"id": int(cont_list[::-1][0]) + 1, "name": data["name"], "price": data["price"]})


def open_csv_writer(file, list_writer):
    with open(file, "w") as f:
        fieldnames = ["id", "name", "price"]
        file_writer = DictWriter(f, fieldnames=fieldnames)
        file_writer.writeheader()
        file_writer.writerows(list_writer)

