import logging

from argparse import ArgumentParser
from json import dumps
from pathlib import Path

from __config__ import CONFIG
from logparser import LogParser


def parse_arguments() -> dict:
    arguments_dict: dict = {}
    parser = ArgumentParser(description="Simple command line application to find port information in log files.")
    parser.add_argument("logfile", type=str, help="Absolute path to log file intended for parsing.")
    args = parser.parse_args()

    if args.logfile:
        logging.info("Required argument {logfile} successfully identified.")

        log_file_path: Path = Path(args.logfile)

        if not log_file_path.exists():
            error: str = "LogParser received bad parameter. {logfile} parameter does point to valid filesystem object."
            logging.critical(error)
            exit(error)

        if not log_file_path.is_file():
            error: str = "LogParser received bad parameter. {logfile} parameter must be a file, operator provided a directory."
            logging.critical(error)
            exit(error)

        logging.info("Required argument {logfile} sucessfully validated.")
        arguments_dict.update({"path": log_file_path, "abs_path": log_file_path.absolute()})
        logging.info("Required argument {logfile} sucessfully added to application configuration.")
    else:
        error: str = "LogParser {logfile} parameter was not provided and is required for proper application operation."
        logging.critical(error)
        exit(error)

    return arguments_dict


def main():
    print("Catepillar LogParser")
    print(dumps(CONFIG, indent=4))
    print()

    logging.basicConfig(format="%(process)d - %(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG)
    logging.info("LogParser initialization started.")

    logging.info("LogParser arguments verification started.")
    arguments: dict = parse_arguments()
    logging.info("LogParser arguments verification complete.")
    print()
    print("LogParser Configuration")
    print("{logifle}:", arguments.get("abs_path"))
    print()
    logging.info("LogParser initialization complete.")

    logparser: LogParser = LogParser()
    narrative: dict = logparser.parse(arguments.get("abs_path"))

    print("LogParser Execution Summary")
    print(f"Search Criteria: { {narrative.get('search_criteria')} }")
    print(f"Number of Matches: {narrative.get('number_of_matches')}")
    print()

    count: int = 1
    for record in narrative.get("results"):
        print(f"Record: {count}/{narrative.get('number_of_matches')}")
        print(f"Identifier: {record.get('uid')}")
        print(f"Port Identified: {record.get('port_number')}")
        print(f"Contents: {record.get('contents')}")
        count = count + 1

    logging.info("LogParser execution complete.")
    exit(0)


main()
