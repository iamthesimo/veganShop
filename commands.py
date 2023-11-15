COMMANDS = {
    "aggiungi": "aggiungi un prodotto al magazzino",
    "elenca": "elenca i prodotto in magazzino",
    "vendi": "registra una vendita effettuata",
    "profitti": "mostra i profitti totali",
    "aiuto": "mostra i possibili comandi",
    "chiudi": "esci dal programma",
}


def helper() -> str:
    cmd_list = ["I comandi disponibili sono i seguenti: "]
    for cmd, help in COMMANDS.items():
        cmd_list.append(f"{cmd}: {help}")
    return '\n'.join(cmd_list)


def get_text_input(msg) -> str:
    return input(msg).lower().strip()


def get_number_input(message, data_type) -> int or float:
    # controllo che il valore inserito sia un numero e provoa a fare il casting a data_type
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
