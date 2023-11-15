import os
from inventory import Inventory
from commands import get_text_input, helper

if __name__ == "__main__":
    vegan_shop = Inventory.load_inventory() if os.path.exists("inventory.json") else Inventory()
    vegan_shop.save_inventory()

    user_cmd = ""

    while user_cmd != "chiudi":
        user_cmd = get_text_input("\nInserisci un comando: ")
        try:
            match user_cmd:
                case "aggiungi":
                    vegan_shop.add_to_inventory()
                    vegan_shop.save_inventory()

                case "elenca":
                    print(vegan_shop)

                case "vendita":
                    vegan_shop.sell_shopping_cart()
                    vegan_shop.save_inventory()

                case "profitti":
                    print(
                        f"Profitto: lordo=€{vegan_shop.gross_income} netto=€{vegan_shop.net_income}"
                    )

                case "aiuto":
                    print(helper())

                case "chiudi":
                    vegan_shop.save_inventory()

                case _:
                    print("Comando non valido")
                    print(helper())

        except Exception as e:
            # eccezioni sono gestite nelle funzioni 
            print(e)
