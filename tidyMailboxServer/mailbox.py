#!/bin/python3
# encoding: utf8
import getpass
import json
from contextlib import contextmanager
from typing import Text

from imapclient import IMAPClient


class Mailbox(object):
    def __init__(self, conf_path):
        self.server_conf = json.load(open(conf_path, "r")).get("server")
        self.server = IMAPClient(
            self.server_conf.get("domain"),
            ssl=self.server_conf.get("security") == "SLL/TLS",
        )

    @contextmanager
    def connect(self):
        try:
            self.server.login(self.server_conf.get("user"), self._get_password())
            yield self.server
        finally:
            self.disconnect()

    def disconnect(self):
        self.server.logout()

    def _get_password(self) -> Text:
        while self.server_conf.get("password") is None:
            self.server_conf["password"] = getpass.getpass(prompt='Password for user {user} on {domain}: '.format(
                user=self.server_conf.get("user"),
                domain=self.server_conf.get("domain")
            ))
        return self.server_conf.get("password")

    def get_folders(self):
        folders = {}
        for folder_tuple in self.server.list_folders():
            name_list = folder_tuple[2]
            actual_folder = folders
            for name in name_list.split(folder_tuple[1]):
                if actual_folder.get(name) is None:
                    actual_folder[name] = {}
                actual_folder = actual_folder.get(name)
        return folders

