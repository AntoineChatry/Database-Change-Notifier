import urllib.request
import json
import smtplib
from email.message import EmailMessage
import time


class DatabaseWatcher:
    def __init__(self):
        self.api_url = "yourapi.com/yourscript.php"
        self.sender_email = "sender@example.com"
        self.sender_password = "senderpassword"
        self.receiver_email = "receiver@example.com"
        self.subject = "Database Update!"
        self.content = "Hi, \n\n Your database has been updated. \n Here's the details: \n\n"
        self.rows = self.get_rows()

    def get_rows(self):
        try:
            headers = {"X-API-KEY": "yourapikey"}
            req = urllib.request.Request(self.api_url, headers=headers)
            x = urllib.request.urlopen(req)
            raw_data = x.read()
            print(raw_data)
            encoding = x.info().get_content_charset("utf8")  
            data = json.loads(raw_data.decode(encoding))  
            print("Fetched {} rows".format(len(data)))
            return data
        except Exception as e:
            print("An error occurred: {}".format(e))
            return None

    def send_email(self, new_rows):
        print("New rows found, sending email...")
        msg = EmailMessage()
        msg["From"] = self.sender_email
        msg["To"] = self.receiver_email
        msg["Subject"] = self.subject
        # Find the new rows
        new_data = [row for row in new_rows if row not in self.rows]
        msg.set_content(
            self.content
            + "Old rows: {}\nNew rows: {}\nNew data: {}".format(
                len(self.rows), len(new_rows), new_data
            )
        )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
        print("Email sent!")

        self.rows = new_rows

    def watch_for_updates(self):
        while True:
            print("Checking for updates...")
            new_rows = self.get_rows()
            if new_rows is not None and new_rows != self.rows:
                self.send_email(new_rows)
            print("Sleeping for 20 minutes...")
            time.sleep(20*60)


if __name__ == "__main__":
    watcher = DatabaseWatcher()
    watcher.watch_for_updates()
