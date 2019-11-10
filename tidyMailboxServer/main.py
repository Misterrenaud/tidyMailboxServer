#!/bin/python3
# encoding: utf8
import logging

from mailbox import Mailbox

logging.basicConfig(level=logging.INFO)


def print_hierarchy(folders, level=0):
    for name, children in folders.items():
        print("\t" * level + name)
        print_hierarchy(children, level=level + 1)


mb = Mailbox("../conf/rloiseleux@skapane.com.json")
with mb.connect():
    print_hierarchy(mb.get_folders())

