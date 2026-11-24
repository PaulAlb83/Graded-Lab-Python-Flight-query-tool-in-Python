import argparse
import json
import logging
import os
import sys
from datetime import datetime

from validator import load_airports
from csv_loader import parse_files
from query import run_queries


"""Flight Schedule Parser and Query Tool - command-line entry point.

Run from the project folder, for example:
    python flight_parser.py -i data/db.csv -a data/airports.txt
"""
import sys

# TODO: fill in your details: plain ASCII, no spaces or underscores.
STUDENT_ID = "260ADB178"
FIRST_NAME = "Paul"
LAST_NAME = "Alberti"

def _build_parser():
    # write my prompt
    parser = argparse.ArgumentParser(description="Flight schedule parser and query tool")
    # une seule source obligatoire parmi -i / -d / -j (sinon argparse sort avec le code 2)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("-i", metavar="FILE", help="parse a single CSV file")
    source.add_argument("-d", metavar="FOLDER", help="parse all .csv files in a folder")
    source.add_argument("-j", metavar="FILE", help="load an existing JSON database")
    parser.add_argument("-a", metavar="FILE", help="airport list (required with -i/-d)")
    parser.add_argument("-o", metavar="FILE", help="output JSON database (default: db.json)")
    parser.add_argument("-q", metavar="FILE", help="JSON file with queries")
    parser.add_argument("-r", metavar="FOLDER", default=".", help="folder for the response file")
    return parser


def _list_csv_files(folder):
    # write my prompt
    paths = []
    for name in sorted(os.listdir(folder)):
        path = os.path.join(folder, name)
        # garder seulement les fichiers qui finissent par ".csv" (pas les sous-dossiers)
        if name.endswith(".csv") and os.path.isfile(path):
            paths.append(path)
    return paths


def _load_json(path):
    # ouvrir le fichier en lecture (utf-8) et retourner json.load(...)  -> cours 10
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


import argparse
import json
import logging
import os
import sys
from datetime import datetime

from validator import load_airports
from csv_loader import parse_files
from query import run_queries

# (tes constantes STUDENT_ID, FIRST_NAME, LAST_NAME restent ici)


def _build_parser():
    # demandé à l'IA : argparse (imposé par le sujet)
    parser = argparse.ArgumentParser(description="Flight schedule parser and query tool")
    # une seule source obligatoire parmi -i / -d / -j (sinon argparse sort avec le code 2)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("-i", metavar="FILE", help="parse a single CSV file")
    source.add_argument("-d", metavar="FOLDER", help="parse all .csv files in a folder")
    source.add_argument("-j", metavar="FILE", help="load an existing JSON database")
    parser.add_argument("-a", metavar="FILE", help="airport list (required with -i/-d)")
    parser.add_argument("-o", metavar="FILE", help="output JSON database (default: db.json)")
    parser.add_argument("-q", metavar="FILE", help="JSON file with queries")
    parser.add_argument("-r", metavar="FOLDER", default=".", help="folder for the response file")
    return parser


def _list_csv_files(folder):
    # demandé à l'IA : os.listdir (noms du dossier), os.path.join, os.path.isfile
    paths = []
    for name in sorted(os.listdir(folder)):
        path = os.path.join(folder, name)
        # garder seulement les fichiers qui finissent par ".csv" (pas les sous-dossiers)
        if name.endswith(".csv") and os.path.isfile(path):
            paths.append(path)
    return paths


def _load_json(path):
    # ouvrir le fichier en lecture (utf-8) et retourner json.load(...)  -> cours 10
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main(argv: list[str] | None = None) -> int:
    # 1. argv = None -> prendre les arguments de la ligne de commande
    if argv is None:
        argv = sys.argv[1:]

    # 2. Lire les arguments. argparse fait sys.exit en cas d'erreur d'usage :
    #    on attrape SystemExit pour RETOURNER le code (0 pour -h, 2 sinon)
    parser = _build_parser()
    try:
        args = parser.parse_args(argv)
        # -a obligatoire avec -i ou -d
        if (args.i is not None or args.d is not None) and args.a is None:
            parser.error("-a is required with -i or -d")
        # -o interdit avec -j
        if args.j is not None and args.o is not None:
            parser.error("-o cannot be used with -j")
    except SystemExit as e:
        return e.code

    logger = logging.getLogger("flight_parser")
    handler = None
    try:
        if args.j is not None:
            # 3a. Mode -j : charger la base, qui doit être une liste de dictionnaires
            db = _load_json(args.j)
            if not isinstance(db, list):
                raise ValueError("database must be a JSON array")
            for item in db:
                if not isinstance(item, dict):
                    raise ValueError("database must contain only objects")
        else:
            # 3b. Mode -i / -d : liste des chemins des CSV
            if args.i is not None:
                paths = [args.i]
            else:
                paths = _list_csv_files(args.d)
                if len(paths) == 0:   # aucun .csv trouvé
                    raise ValueError("no .csv files in folder " + args.d)

            airports = load_airports(args.a)

            # chemin de la base : -o s'il est donné, sinon "db.json"
            if args.o is not None:
                db_path = args.o
            else:
                db_path = "db.json"
            # errors.log dans le même dossier que la base (demandé à l'IA : os.path.dirname)
            log_path = os.path.join(os.path.dirname(db_path), "errors.log")

            # configuration imposée par le sujet
            logger.setLevel(logging.INFO)
            handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
            handler.setFormatter(logging.Formatter(
                "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
            logger.addHandler(handler)

            db, errors = parse_files(paths, airports)
            # un WARNING par message d'erreur, dans l'ordre
            for message in errors:
                logger.warning(message)
            # écrire db dans db_path avec json.dump (cours 10, slide 12)
            with open(db_path, "w", encoding="utf-8") as f:
                json.dump(db, f)

        # 4. Requêtes (-q) : objet ou liste, sinon erreur
        if args.q is not None:
            queries = _load_json(args.q)
            if not isinstance(queries, (dict, list)):
                raise ValueError("queries must be a JSON object or array")
            responses = run_queries(db, queries)
            # demandé à l'IA : datetime.now().strftime -> heure locale "YYYYMMDD_HHMM"
            stamp = datetime.now().strftime("%Y%m%d_%H%M")
            name = f"response_{STUDENT_ID}_{FIRST_NAME}_{LAST_NAME}_{stamp}.json"
            # écrire responses dans os.path.join(args.r, name) avec json.dump
            with open(os.path.join(args.r, name), "w", encoding="utf-8") as f:
                json.dump(responses, f)

        return 0

    except (OSError, ValueError) as e:
        # fichier introuvable / illisible, JSON invalide, mauvaise structure -> code 1
        # demandé à l'IA : file=sys.stderr écrit sur la sortie d'erreur
        print(f"Error: {e}", file=sys.stderr)
        return 1

    finally:
        # TOUJOURS retirer et fermer le handler, même après une erreur (imposé par le sujet)
        if handler is not None:
            logger.removeHandler(handler)
            handler.close()


if __name__ == "__main__":
    sys.exit(main())

