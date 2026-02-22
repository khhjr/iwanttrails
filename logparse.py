
import re
import sys
import time
import requests
import datetime


class AccessLogEntry(object):

    regex = re.compile(r"(?P<ip>[\d\.]+).*\[(?P<utc>[\w/:]+)\s\+0000\]\s+(?P<op>.*)\s\d+\s\d+\s.*?\((?P<agent>.*)\)")
    location_tbl = {}
    starlink = "153.66.9"
    bots = [
        "gptbot",
        "openai",
        "robot",
        "bot.html"
    ]

    def __init__(self, line):
        self.log_entry = line
        self._lookup_count = 1
        self._ipaddr = None
        self._location = None
        self.op = "unknown"
        self.agent = "unknown"

    @property
    def url(self):
        return f"http://ip-api.com/json/{self.ipaddr}"

    @property
    def ipaddr(self):
        if not self._ipaddr:
            m = self.regex.search(self.log_entry)
            if m:
                self._ipaddr = m.group("ip")
                self.utc = m.group("utc")
                self.op = m.group("op")
                self.agent = m.group("agent")
        return self._ipaddr

    @property
    def location(self):
        if self.ipaddr not in self.location_tbl:
            while not self._get_location():
                print(f"ip location lookup {self._lookup_count}", file=sys.stderr)
        return self.location_tbl[self.ipaddr]

    def _get_location(self):
        success = None
        data = None
        try:
            self._lookup_count += 1
            response = requests.get(self.url)
            data = response.json()
            success = True
        except Exception as e:
            print(self.log_entry, file=sys.stderr)
            print(e, file=sys.stderr)
            print("limit possibly exceeded, sleeping", file=sys.stderr)
            time.sleep(62)
            self._lookup_count = 1
        if data and data['status'] == 'success':
            v = f"{data['regionName']} {data['city']}"
        else:
            v = "??"
        if self.ipaddr.startswith(self.starlink):
            v = f"***STARLINK {v}"
        for s in self.bots:
            if s in self.log_entry:
                v = f"***BOT {v}"
                break
        self.location_tbl[self.ipaddr] = v
        return success

    def print(self):
            print(f"{self.ipaddr:<16} {self.location:<40} {self.est} {self.op} {self.agent}")

    @property
    def est(self):
        utc = datetime.datetime.strptime(self.utc, "%d/%b/%Y:%H:%M:%S")
        return (utc + datetime.timedelta(hours=-5))


def main(log):

    with open(log, "r") as f:
        lines = f.readlines()
        for l in lines:
            ale = AccessLogEntry(l)
            ale.print()

if __name__ == "__main__":
    main(sys.argv[1])

