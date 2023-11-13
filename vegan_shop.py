""" Vegan grocieries shop"""
import json
import os
from datetime import datetime
from tabulate import tabulate


COMMANDS = {
    "aggiungi": "aggiungi un prodotto al magazzino",
    "elenca": "elenca i prodotto in magazzino",
    "vendi": "registra una vendita effettuata",
    "profitti": "mostra i profitti totali",
    "aiuto": "mostra i possibili comandi",
    "chiudi": "esci dal programma",
}


class Product:
    def __init__(
        self, name: str, quantity: int, buy_price: float = 0.0, sell_price: float = 0.0
    ):
        self.name = name
        self.quantity = quantity
        self.sell_price = float(sell_price)
        self.buy_price = float(buy_price)

    def __repr__(self) -> str:
        return self.name

    def __getitem__(self, item):
        return [self.quantity, self.buy_price, self.sell_price]


class Inventory:
    def __init__(self):
        self.inventory = {}
        self.gross_income = 0.0
        self.net_income = 0.0
        self.cost = 0.0

    def __repr__(self) -> str:
        product_list = "\n".join(
            [
                f"{product.name}\t|\t{product.quantity}\t|\t{product.sell_price}"
                for product in sorted(self.inventory.values(), key=lambda x: x.name)
            ]
        )
        return str(product_list)

    def __dict__(self) -> dict:
        sorted_inventory = sorted(self.inventory.values(), key=lambda x: x.name)
        return {
            item.name: [item.quantity, item.buy_price, item.sell_price]
            for item in sorted_inventory
        }

    def __list__(self) -> list:
        products = []
        for product_name, product in vegan_shop.inventory.items():
            products.append([product_name, product.quantity, product.sell_price])
        return products

    def update_net_income(self, product, quantity: int) -> float:
        self.net_income += self.update_gross_income(
            product, quantity
        ) - self.calculate_cost(product, quantity)
        return self.net_income

    def update_gross_income(self, product, quantity: int) -> float:
        sold_product = vegan_shop.inventory[product.name]
        self.gross_income += sold_product.sell_price * quantity
        return self.gross_income

    def calculate_cost(self, product: Product, quantity: int) -> None:
        self.cost += product.buy_price * quantity
        return self.cost

    def update_inventory(self, product: Product) -> None:
        if product.name in self.inventory:
            self.update_quantity(product)
        else:
            self.add_product(product)

    def add_product(self, product: Product) -> None:
        self.inventory[product.name] = product

    def sell_product(self, product, quantity: int) -> None:
        # TODO, aggiorna quantità in modo corretto, rileggi le specifiche per capire cosa serve e ragiona sul flusso di cassa
        """
        aggiorna quantità
        aggiorna net_income
        """
        if quantity <= 0:
            raise AssertionError("La quantità deve essere maggiore di 0")
        product = self.inventory[product]
        self.update_quantity(product, -quantity)
        self.update_net_income(product, quantity)

    def update_quantity(self, product: Product, quantity) -> None:
        if abs(quantity) > self.inventory[product.name].quantity:
            raise AssertionError(
                "Quantità superiore alla quantità in magazzino, operazione annuallata"
            )
        if quantity == self.inventory[product.name].quantity:
            self.inventory.pop(product.name)
        else:
            self.inventory[product.name].quantity += quantity

    def save_inventory(self) -> None:
        now = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        inventory_dict = {"last_save": now}
        inventory_dict["product format"] = {
            "name": ["quantity", "buy_price", "sell_price"]
        }
        inventory_dict["gross_income"] = self.gross_income
        inventory_dict["net_income"] = self.net_income
        inventory_dict["products"] = self.__dict__()
        with open("inventory.json", "w") as f:
            json.dump(inventory_dict, f, indent=4)

    def product_exist(self, product_name: str) -> bool:
        if product_name in self.inventory:
            return True
        else:
            return False


def load_inventory():
    with open("inventory.json", "r") as f:
        inventory_dict = json.load(f)
    inventory = Inventory()
    for product, values in inventory_dict["products"].items():
        inventory.add_product(Product(product, values[0], values[1], values[2]))
    inventory.gross_income = inventory_dict["gross_income"]
    inventory.net_income = inventory_dict["net_income"]
    return inventory


def helper():
    print("I comandi disponibili sono i seguenti: ")
    for cmd, help in COMMANDS.items():
        print(f"{cmd}: {help}")


def get_user_input(message, data_type):
    while True:
        user_input = input(f"{message}")
        try:
            value = data_type(user_input)
            return value
        except ValueError:
            if data_type == int:
                print("Quantità non valida, devi inserire un numero intero")
            elif data_type == float:
                print("Quantità non valida, devi inserire un numero decimale")


if __name__ == "__main__":
    vegan_shop = load_inventory() if os.path.exists("inventory.json") else Inventory()

    user_cmd = ""

    while user_cmd != "chiudi":
        user_cmd = input("\nInserisci un comando: ").lower()
        try:
            match user_cmd:
                case "aggiungi":
                    product_name = input("Inserisci il nome del prodotto: ")
                    product_quantity = get_user_input("Inserisci la quantità: ", int)

                    if not vegan_shop.product_exist(product_name):
                        product_buy_price = float(
                            get_user_input("Inserisci il prezzo di acquisto: ", float)
                        )
                        product_sell_price = float(
                            get_user_input("Inserisci il prezzo di vendita: ", float)
                        )
                        product = Product(
                            product_name,
                            product_quantity,
                            product_buy_price,
                            product_sell_price,
                        )

                    else:
                        product = Product(product_name, product_quantity)
                    vegan_shop.update_inventory(product)

                case "elenca":
                    headers = ["PRODOTTO", "QUANTITA'", "PREZZO"]
                    print(
                        tabulate(
                            vegan_shop.__list__(),
                            headers=headers,
                            tablefmt="simple_outline",
                        )
                    )

                case "vendita":
                    product_list = []
                    add_product = "si"
                    while add_product == "si":
                        input_product_name = input("Inserisci il nome del prodotto: ")
                        if not vegan_shop.product_exist(input_product_name):
                            raise AssertionError("Prodotto non presente in magazzino")
                        if input_product_name in [
                            product["product"] for product in product_list
                        ]:
                            input_product_quantity = get_user_input(
                                "Inserisci la quantità: ", int
                            )
                            product_list[input_product_name][
                                "quantity"
                            ] += input_product_quantity
                            product_list[input_product_name]["partial"] += (
                                vegan_shop.inventory[input_product_name].sell_price
                                * input_product_quantity
                            )
                        else:
                            input_product_quantity = get_user_input(
                                "Inserisci la quantità: ", int
                            )
                            # TODO sistemre il metodo append e renderlo coerente con la vendita
                            # cerca di fare un oggetto, aggiungilo alla lista e vendi gli oggetti della lista
                            # magari con prodotto e incrementandone solo la quantità con un metodo apposito
                            product_list.append(
                                {
                                    input_product_name: {
                                        "quantity": input_product_quantity,
                                        "partial": vegan_shop.inventory[
                                            input_product_name
                                        ].sell_price
                                        * input_product_quantity,
                                    }
                                }
                            )

                        add_product = input("Aggiungere un altro prodotto? (si/NO): ")

                    for product in product_list:
                        vegan_shop.sell_product(product["product"], product["quantity"])

                    print("VENDITA REGISTRATA")
                    for product in product_list:
                        print(
                            f"{product['quantity']} X {product['product']}: €{product['partial']}"
                        )
                    print(
                        f"Totale: €{sum([product['partial'] for product in product_list])}"
                    )

                case "profitti":
                    print(
                        f"Profitto: lordo=€{vegan_shop.gross_income} netto=€{vegan_shop.net_income}"
                    )

                case "aiuto":
                    helper()

                case "chiudi":
                    vegan_shop.save_inventory()

                case _:
                    print("Comando non valido")
                    helper()

        except ValueError:
            print(
                "Il valore inserito non è valido, quantità, prezzo di acquisto e di vendita devono essere numeri"
            )
        except Exception as e:
            print(e)
