
import re
import sys
import time
import requests
import datetime


class AccessLogEntry(object):

    pat = r'(?P<ip>\d{1,3}(?:\.\d{1,3}){3}).*\[(?P<utc>[\w/:]+)\s\+0000\]\s+"(?P<op>[^"]+)"\s'
    pat += r'(?P<status>\d+)\s(?P<size>\d+)\s"(?P<referer>[^"]*)"\s"(?P<agent>[^"]+)"'
    regex = re.compile(pat)
    location_tbl = {}
    starlink = "153.66.9"
    bots = [
        "gptbot",
        "openai",
        "robot",
        "bot.html"
    ]
    _lookup_count = 1
    unknown = "unknown"

    def __init__(self, line):
        self.log_entry = line
        self.ipaddr = None
        self._location = None
        self.utc = self.unknown
        self.op = self.unknown
        self.status = self.unknown
        self.referer = self.unknown
        self.agent = self.unknown
        self.load_attrs()

    @property
    def url(self):
        return f"http://ip-api.com/json/{self.ipaddr}"

    def load_attrs(self):
        m = self.regex.search(self.log_entry)
        if m:
            self.ipaddr = m.group("ip")
            self.utc = m.group("utc")
            self.op = m.group("op")
            self.status = m.group("status")
            self.referer = m.group("referer")
            self.agent = m.group("agent")
        else:
            self.ipaddr = self.unknown

    @property
    def location(self):
        if self.ipaddr not in self.location_tbl:
            if not self._get_location():
                # Retry once in case we exceeded max lookups per minute.
                print("limit possibly exceeded, sleeping", file=sys.stderr)
                time.sleep(62)
                AccessLogEntry._lookup_count = 1
                self._get_location()
        return self.location_tbl[self.ipaddr]

    def _get_location(self):
        success = None
        data = None
        print(f"ip location lookup {AccessLogEntry._lookup_count}", file=sys.stderr)
        try:
            AccessLogEntry._lookup_count += 1
            response = requests.get(self.url)
            data = response.json()
            success = True
        except Exception as e:
            print(self.log_entry, file=sys.stderr)
            print(e, file=sys.stderr)
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
            print(f"{self.est}   {self.ipaddr:<16} {self.location:<40.38} {self.status:<5.3} {self.referer:<30.28} {self.op:<50.48} {self.agent:<50.50}")

    @property
    def est(self):
        if self.utc == self.unknown:
            return self.unknown
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

