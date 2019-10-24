#!/bin/python
# encoding: utf8
import email
import getpass
import imaplib
import json


class Mailbox(object):
    def __init__(self, conf_path):
        self.server_conf = json.load(open(conf_path, "r")).get("server")
        self.password = None

    def connect(self):
        server = imaplib.IMAP4_SSL(self.server_conf.get("domain"))
        try:
            server.login(self.server_conf.get("user"), self._get_password())
        except Exception as e:
            raise e
        else:
            # Print list of mailboxes on server
            code, mailboxes = server.list()
            for mailbox in mailboxes:
                print(mailbox.decode("utf-8"))
            # Select mailbox
            print(server.select("INBOX", readonly=True))

            result, data = server.uid('search', None, "ALL")
            if result == 'OK':
                for num in data[0].split()[-10:]:
                    result, data = server.uid('fetch', num, '(RFC822)')
                    if result == 'OK':
                        email_message = email.message_from_bytes(data[0][1])
                        print('From:' + email_message['From'])
                        print('To:' + email_message['To'])
                        print('Date:' + email_message['Date'])
                        print('Subject:' + str(email_message['Subject']))
                        print('Content:' + str(email_message.get_payload()[0]))

            # Cleanup
            server.close()

    def _get_password(self):
        while self.password is None:
            self.password = getpass.getpass(prompt='Password for user {user} on {domain}: '.format(
                user=self.server_conf.get("user"),
                domain=self.server_conf.get("domain")
            ))
        return self.password
