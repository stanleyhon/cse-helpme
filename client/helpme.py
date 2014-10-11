#!/usr/bin/env python

import argparse
import requests
import subprocess

SERVER = "http://www.cse.unsw.edu.au/~shon/cgi-bin/server.py"

def helpee(args):
    user = run_command("whoami").strip()
    machine = run_command("hostname").strip()

    if not user or not machine:
        exit("Couldn't work out your user/machine. Seek help immediately.")

    print "Sending for help..."

    params = {"action": "help", "id": user, "course": args.course,
        "location": machine, "duration": args.duration, "description": args.description}
    try:
        r = requests.post(SERVER, params=params)
    except requests.exceptions.RequestException:
        exit("Something went wrong and we couldn't connect to the server, sorry :(")
    print r.text

    #jsondata = r.json()
    #if jsondata["status"] == "OK":
    #    print "Help request submitted."
    #else:
    #    print "Sorry, help request not accepted. Reason: %s" % jsondata["status"]

def run_command(command):
    child = subprocess.Popen(command, stdout=subprocess.PIPE)
    return child.communicate()[0]

def helper(args):
    # Register with server
    # Start the helper service
    pass

if __name__ == "__main__":
    desc = """
    Receive or provide help on UNSW CSE courses.
    (Hackathon 2014)
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("course", metavar="COURSE", help="The course you want help with, in the format COMP1234")
    parser.add_argument("--duration", "-t", metavar="t", default=60, help="Time your request will remain open, in minutes (default 60)")
    parser.add_argument("--description", "-d", metavar="\"<text>\"", default=60, help="Short description (to pass to your helpers)")

    args = parser.parse_args()
    helpee(args)