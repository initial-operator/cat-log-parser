import ipaddress
import logging
import re
import uuid

class LogParser:

    PORT_IDENTIFIER: str = '(port)+(:)?+(")?+(\s)?+((6553[0-5])|(655[0-2][0-9])|(65[0-4][0-9]{2})|(6[0-4][0-9]{3})|([1-5][0-9]{4})|([0-5]{0,5})|([0-9]{1,4}))+(")?'

    def __init__(self):
        logging.info("Initializing file parsing capability.")
        self._search_criteria: str = self.PORT_IDENTIFIER

    def parse(self, logfile: str) -> dict:
        logging.info("Initiating log file parsing.")
        logging.info("Accessing log file.")
        matches: list = []
        with open(logfile, "r") as file:
            logging.info("Parsing log file contents.")
            for line in file:
                possible_match = re.search(self._search_criteria, line, re.IGNORECASE)
                if possible_match: 
                    port_number: int = None
                    primary_match = possible_match.group(0)

                    if ":" in primary_match:
                        match_split = primary_match.split(":")
                        port_number = int(match_split[1].replace("\"", ""))
                    else:
                        match_split = primary_match.split(" ")
                        port_number = int(match_split[1])

                    record: dict = {"uid": str(uuid.uuid4()), "contents": line, "port_number": port_number}
                    matches.append(record)
                else:
                    pass
            logging.info("Completed parsing log file contents.")
        logging.info("Closed access to log file.")
        logging.info("Initiated results consolidation.")
        narrative: dict = {
            "uid": str(uuid.uuid4()),
            "search_criteria": self._search_criteria,
            "number_of_matches": len(matches),
            "results": matches,
        }
        logging.info("Completed log file parsing.")
        return narrative
