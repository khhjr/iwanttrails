
import re
import sys
import time
import requests
import datetime


r = re.compile(r"(?P<ip>[\d\.]+).*\[(?P<utc>[\w/:]+)\s\+0000\]\s+(?P<op>.*)\s\d+\s\d+\s.*?\((?P<agent>.*)\)")


ip_tbl = {}
starlink = "153.66.9"


bots = [
    "gptbot",
    "openai",
    "robot",
    "bot.html"
]


count = 1
def ip_lookup(ipaddr, line):

    def geo_lu(url):
        global count
        if count > 45:
            print("limit exceeded, sleeping", file=sys.stderr)
            time.sleep(62)
            count = 1
        data = None
        try:
            print(f"ip lookup {count}", file=sys.stderr)
            count += 1
            response = requests.get(url)
            data = response.json()
        except Exception as e:
            print(line)
            print(e, file=sys.stderr)
        return data

    if ipaddr in ip_tbl:
        return ip_tbl[ipaddr]

    if ipaddr.startswith(starlink):
        ip_tbl[ipaddr] = "starlink"
        return "starlink"

    for s in bots:
        if s in line:
            ip_tbl[ipaddr] = "bot"
            return "bot"

    url = f"http://ip-api.com/json/{ipaddr}"
    data = geo_lu(url)

    if data and data['status'] == 'success':
        v = f"{data['regionName']} {data['city']}"
    else:
        v = "??"
    ip_tbl[ipaddr] = v
    return v


def utc_convert(ustr):
    utc = datetime.datetime.strptime(ustr, "%d/%b/%Y:%H:%M:%S")
    return (utc + datetime.timedelta(hours=-5))


def main(log):

    with open(log, "r") as f:
        lines = f.readlines()
        for l in lines:
            m = r.search(l)
            if m:
                ipl = ip_lookup(m.group("ip"), l)
                est = utc_convert(m.group("utc"))
                print(f"{m.group("ip"):<16} {ipl:<25} {est} {m.group("op")} {m.group("agent")}")

if __name__ == "__main__":
    main(sys.argv[1])

