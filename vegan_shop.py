import os
from tabulate import tabulate
from inventory import Inventory
from commands import text_input, helper

if __name__ == "__main__":
    vegan_shop = Inventory.load_inventory() if os.path.exists("inventory.json") else Inventory()

    user_cmd = ""

    while user_cmd != "chiudi":
        user_cmd = text_input("\nInserisci un comando: ")
        try:
            match user_cmd:
                case "aggiungi":
                    vegan_shop.add_to_inventory()
                    vegan_shop.save_inventory()

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
                    vegan_shop.sell_shopping_cart()

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
