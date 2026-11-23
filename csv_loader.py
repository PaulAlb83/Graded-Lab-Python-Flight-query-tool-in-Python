"""Reading CSV files into flight records and error messages."""

import csv
import os   # demandé à l'IA : seulement pour os.path.basename

from validator import validate_row, to_record


def parse_files(paths: list[str], airports: set[str]) -> tuple[list[dict], list[str]]:
    """Process the CSV files in the order given.

    Return (records, errors):
      records - valid flight records, in input order
      errors  - one message per invalid row, in input order, formatted as
                "<file name>:<line number>: <ERROR_CODE> | <free text>"
                (base file name only, no timestamp or level, no newline)

    Also performs the DUPLICATE_FLIGHT check across all the files.
    Does not write any files and does not log anything itself.
    """
    records = []
    errors = []
    seen = set()   # couples (flight_id, departure_datetime) des lignes VALIDES déjà vues

    for path in paths:
        # demandé à l'IA : os.path.basename("data/db.csv") renvoie "db.csv"
        filename = os.path.basename(path)

        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for number, line in enumerate(lines, start=1):
            # 1. Ligne 1 = en-tête -> passer à la ligne suivante
            # À COMPLÉTER (if ... : continue)
            if number == 1:
                continue

            # 2. Ligne vide / que des espaces, ou commentaire
            text = line.strip()
            if text == "" or text.startswith("#"):
                continue

            # 3. Enlever seulement le "\n" de fin (pour le message d'erreur)
            line = line.rstrip("\r\n")

            # 4. Découper la ligne avec le module csv
            fields = list(csv.reader([line]))[0]

            # 5. Contrôles 1 à 11
            code = validate_row(fields, airports)

            # 6. Si valide : record + vérification du doublon
            if code is None:
                record = to_record(fields)
                key = (record["flight_id"], record["departure_datetime"])
                if key in seen:
                    code = "DUPLICATE_FLIGHT"
                else:
                    seen.add(key)
                    records.append(record)

            # 7. Si invalide : ajouter le message à errors
            if code is not None:
                errors.append(
                    filename + ":" + str(number) + ": " + code + " | " + line.strip()
                )

    return records, errors
