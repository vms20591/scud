#!/usr/bin/env python3

import argparse
import sys
import os
import getpass
import json
from json.decoder import JSONDecodeError

DEFAULT_SCUD_FILE = os.path.join(os.path.expanduser("~"), ".config", "scud.json")

def setup_arg_parser():
    parser = argparse.ArgumentParser(prog="scud")
    subparsers = parser.add_subparsers()
    parser.add_argument("-f", "--file", default=DEFAULT_SCUD_FILE, help="Location to scud file")

    parser_commit = subparsers.add_parser("commit", help="Add server details to scud file")
    parser_commit.set_defaults(func=ScudWrapper.commit)

    parser_checkout = subparsers.add_parser("checkout", help="Get server details from scud file")
    parser_checkout.add_argument("search_text", help="Search text to filter from server details")
    parser_checkout.set_defaults(func=ScudWrapper.checkout)

    parser_log = subparsers.add_parser("log", help="List all server details from scud file")
    parser_log.set_defaults(func=ScudWrapper.log)

    return parser

def main():
   parser = setup_arg_parser()

   if len(sys.argv) == 1:
       parser.print_help(sys.stderr)
       return 1

   args = parser.parse_args()

   try:
      return args.func(args)
   except Exception as exp:
       print("Fatal error occurred: {0}".format(str(exp)))
       return 1

class Utils:
    @staticmethod
    def get_input(prompt="> ", is_password=False, capture_until_right=False):
        first = True
        user_input = ""

        while first or capture_until_right:
            first = False

            if is_password:
                user_input = getpass.getpass(prompt)
            else:
                user_input = input(prompt)

            capture_until_right = capture_until_right and not user_input

        return user_input

class ScudWrapper:
    @staticmethod
    def commit(args):
        scud = Scud.new(args.file)

        scud.commit()

        return 0

    @staticmethod
    def checkout(args):
        scud = Scud.new(args.file)

        scud.checkout(args.search_text)

        return 0

    @staticmethod
    def log(args):
        scud = Scud.new(args.file)

        scud.log()

        return 0

class Scud:
    def __init__(self, scud_file):
        self.file = scud_file

    def _load_from_file(self, ignore_new_file=False):
        scud_info = []

        try:
            with open(self.file) as f:
                scud_info = json.load(f)

            return scud_info
        except JSONDecodeError as jd_error:
            raise Exception("Invalid scud file!")
        except FileNotFoundError as fnf_error:
            if ignore_new_file:
                return scud_info

            raise Exception("File doesn't exist!")

    @staticmethod
    def new(scud_file):
        return Scud(scud_file)

    def _capture_details(self):
        name = Utils.get_input("Nickname? ", capture_until_right=True)
        host = Utils.get_input("Server hostname or IP: ")
        port = Utils.get_input("Server port: ")
        username = Utils.get_input("Server username: ")
        password = Utils.get_input("Server password: ", is_password=True)
        key_file = Utils.get_input("Server identity file: ")

        details = {
            "name": name,
            "host": host,
            "port": port,
            "username": username,
            "password": password,
            "key_file": key_file
        }

        return details

    def _pretty_print(self, scud):
        print("Name: {0}\nHost: {1}\nPort: {2}\nUsername: {3}\nPassword: {4}\nKey File: {5}".format(scud.get("name", ""), scud.get("host", ""), scud.get("port", ""), scud.get("username", ""), scud.get("password", ""), scud.get("key_file", "")))

    def commit(self):
        details = self._capture_details()
        scud_info = self._load_from_file(True)
        scud_info.append(details)

        with open(self.file, "w") as f:
            json.dump(scud_info, f)

    def checkout(self, search_text=""):
        scud_info = self._load_from_file()
        search_text = (search_text or "").lower()

        def _filter(item):
            name = item.get("name", "").lower().find(search_text)
            host = item.get("host", "").lower().find(search_text)
            username = item.get("username", "").lower().find(search_text)

            return (name + host + username) > -3

        matches = list(filter(_filter, scud_info)) if search_text else scud_info

        print("Found {0} match(es)!".format(len(matches)))

        for scud in matches:
            self._pretty_print(scud)
            print("-" * 50)

        print("")

    def log(self):
        scud_info = self._load_from_file()

        print("Found {0} scuds!".format(len(scud_info)))

        for scud in scud_info:
            self._pretty_print(scud)
            print("-" * 50)

        print("")

if __name__ == "__main__":
    sys.exit(main())

