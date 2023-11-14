COMMANDS = {
    "aggiungi": "aggiungi un prodotto al magazzino",
    "elenca": "elenca i prodotto in magazzino",
    "vendi": "registra una vendita effettuata",
    "profitti": "mostra i profitti totali",
    "aiuto": "mostra i possibili comandi",
    "chiudi": "esci dal programma",
}


def helper() -> None:
    print("I comandi disponibili sono i seguenti: ")
    for cmd, help in COMMANDS.items():
        print(f"{cmd}: {help}")


def text_input(msg):
    return input(msg).lower().strip()


def get_user_input(message, data_type) -> int or float:
    while True:
        user_input = input(f"{message}")
        try:
            value = data_type(user_input)
            if value < 0:
                raise ValueError("Il valore deve essere maggiore di 0")
            else:
                return value
        except ValueError:
            if data_type == int:
                print("Quantità non valida, devi inserire un numero intero")
            elif data_type == float:
                print("Quantità non valida, devi inserire un numero decimale")


