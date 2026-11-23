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
        if name.endswith(...) and os.path.isfile(path):
            ...
    return paths


def _load_json(path):
    # ouvrir le fichier en lecture (utf-8) et retourner json.load(...)  -> cours 10
    ...



def main(argv: list[str] | None = None) -> int:
    """Run the whole program and return the exit code (0, 1 or 2).

    argv is the argument list without the program name.
    None means use sys.argv[1:] (argparse does this for you).
    Do not call sys.exit() inside main(); return the code instead.
    """
    # TODO: parse arguments with argparse (-i, -d, -j, -a, -o, -q, -r).
    # TODO: load or parse the data, write the database and errors.log.
    # TODO: run the queries and write the response file.
    # Remember: remove and close the logging handler before returning,
    # also when returning early because of an error (use try/finally).
    raise NotImplementedError("main() is not written yet")


if __name__ == "__main__":
    sys.exit(main())

