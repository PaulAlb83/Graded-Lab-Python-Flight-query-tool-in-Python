"""Row validation: airport list loading, single-row checks, record building."""
# j'ai demandé à claude si j'avais besoin d'importer des bibliothès et m'a proposé celle ci
# et j'ai demanddé de verifé si c'était autorisé par l'ennoncé voici sa réponse:
#Oui, tu peux les ajouter. La consigne interdit les bibliothèques tierces, c’est-à-dire celles
#  qu’on installe avec pip comme pandas. Elle impose la bibliothèque standard, celle qui est
#  livrée avec Python. math et datetime en font partie, comme csv, json, logging, argparse et re
import math
from datetime import datetime
# I ask if have had need of other function and he give create detetime_format and valid datetime
# I completed the body of these functions
def _has_datetime_format(text):
    if len(text) != 16:
        return False
    for i in range(16):
        ch = text[i]
        if i == 4 or i == 7:
            if ch != "-":
                return False
        elif i == 10:
            if ch != " ":
                return False
        elif i == 13:
            if ch != ":":
                return False
        else:
            if not ("0" <= ch <= "9"):
                return False
    return True


def _is_valid_datetime(text):
    if not _has_datetime_format(text):
        return False
    try:
        datetime.strptime(text, "%Y-%m-%d %H:%M")
    except ValueError:
        return False
    return True
# I tried to run the code but I forgot certain function and 
# claude said me to add that (He give me only structure and I completed):
def _is_ascii_letters_digits(text):
    # Parcourir chaque caractère de text
    for ch in text:
        # Si ch n'est ni une lettre a-z, ni une lettre A-Z, ni un chiffre 0-9 -> False
        if not (...):
            return False
    return True


def _is_ascii_letters_digits(text):
    # Parcourir chaque caractère de text
    for ch in text:
        # Si ch n'est ni une lettre a-z, ni une lettre A-Z, ni un chiffre 0-9 -> False
        if not ("a" <= ch <= "z" or "A" <= ch <= "Z" or "0" <= ch <= "9"):
            return False
    return True


def _is_airport_code(code, airports):
    # Un code d'aéroport a exactement 3 caractères
    if len(code) != 3:
        return False
    # Chaque caractère doit être une lettre majuscule A-Z
    for ch in code:
        if not ("A" <= ch <= "Z"):
            return False
    # Enfin, le code doit exister dans la liste des aéroports
    return code in airports

def load_airports(path: str) -> set[str]:
    """Read an airport list file and return the set of codes.

    One code per line. Strip whitespace; skip blank lines and lines
    starting with '#'.
    """
  
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f]
    return {l for l in lines if l != "" and l[0] != "#"}

# voici le prompte demandé : « Sans écrire de code, donne-moi la structure de validate_row :
#  l’ordre des étapes, ce que chacune vérifie, et le code d’erreur renvoyé. »
#« Découpe validate_row en petites fonctions auxiliaires et dis-moi laquelle écrire en premier. »
#« Donne-moi un squelette avec uniquement les if et des commentaires # TODO, je remplis les conditions moi-même. »
def validate_row(fields: list[str], airports: set[str]) -> str | None:
    """Check one CSV row (fields as returned by csv.reader, not yet stripped).

    Return None if the row is valid, otherwise the error code of the
    FIRST failing check (checks 1-11 in the specification, in order).
    Does not check for duplicates.
    """
      
        # 1. Le nombre de champs doit être exactement 6
    if len(fields) != 6:
        return "WRONG_FIELD_COUNT"

    # Nettoyer les champs (strip) dans une nouvelle liste values
    values = [field.strip() for field in fields]

    # 2. Aucun champ ne doit être vide après nettoyage
    for v in values:
        if v == "":
            return "MISSING_FIELD"

    # Donner un nom à chaque valeur
    flight_id, origin, destination, departure, arrival, price = values

    # 3. flight_id : entre 2 et 8 caractères, uniquement lettres/chiffres ASCII
    if not (2 <= len(flight_id) <= 8 and _is_ascii_letters_digits(flight_id)):
        return "INVALID_FLIGHT_ID"

    # 4. origin : code d'aéroport valide
    if not _is_airport_code(origin, airports):
        return "INVALID_ORIGIN"

    # 5. destination : code d'aéroport valide
    if not _is_airport_code(destination, airports):
        return "INVALID_DESTINATION"

    # 6. origin et destination doivent être différents
    if origin == destination:
        return "SAME_ORIGIN_DESTINATION"  
      
      
       # 7
    if not _is_valid_datetime(departure):
        return "INVALID_DEPARTURE"
    # 8
    if not _is_valid_datetime(arrival):
        return "INVALID_ARRIVAL"
    # 9
    if arrival <= departure:
        return "ARRIVAL_NOT_AFTER_DEPARTURE"
    # 10
    try:
        price_value = float(price)
    except ValueError:
        return "INVALID_PRICE"
    if not math.isfinite(price_value):
        return "INVALID_PRICE"
    # 11
    if price_value <= 0:
        return "NON_POSITIVE_PRICE"

    return None


#ok donne moi le squelette de to_record pour que je puisse le compléter moi même s'il te plaît
#claude give the squelette and I adding the body

def to_record(fields: list[str]) -> dict:
    """Turn a valid row into a flight record dictionary.

    Keys: flight_id, origin, destination, departure_datetime,
    arrival_datetime (stripped strings) and price (float).
    """
    # 1. Nettoyer les 6 champs : enlever les espaces au début et à la fin de chacun
    values = [field.strip() for field in fields]

    # 2. Construire le dictionnaire avec les 6 clés exactes du sujet
    record = {
        "flight_id": values[0],
        "origin": values[1],
        "destination": values[2],
        "departure_datetime": values[3],
        "arrival_datetime": values[4],
        "price": float(values[5]),   # attention : ce doit être un nombre, pas une chaîne
    }

    # 3. Retourner le dictionnaire
    return record