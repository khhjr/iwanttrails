#!/usr/bin/env python3

import re
import sys
import time
import requests
import datetime


class AccessLogEntry(object):

    pat = r'(?P<ipaddr>\d{1,3}(?:\.\d{1,3}){3}).*\[(?P<utc>[\w/:]+)\s\+0000\]\s+"(?P<op>[^"]+)"\s(?P<status>\d+)\s'
    pat += r'(?P<size>\d+)\s"(?P<referer>[^"]*)"\s"(?P<agent>[^"]+)"\s"(?P<forwarded>\d{1,3}(?:\.\d{1,3}){3})"\s(?P<response>.*)'
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
        self.load_attrs()

    def __getattr__(self, name):
        return self.unknown


    def __str__(self):
        return f"{self.est}   {self.ipaddr:<16} {self.location:<40.38} {self.status:<5.3} {self.referer:<30.28} {self.op:<50.48} {self.agent:<50.50}"

    @property
    def url(self):
        return f"http://ip-api.com/json/{self.ipaddr}"

    def load_attrs(self):
        m = self.regex.search(self.log_entry)
        if m:
            for k, v in m.groupdict().items():
                setattr(self, k, v)

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
            print(AccessLogEntry(l))

if __name__ == "__main__":
    main(sys.argv[1])

