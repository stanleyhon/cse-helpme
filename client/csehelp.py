#!/usr/bin/env python

import argparse
import requests
import subprocess
import time
import sys

SERVER = "http://www.cse.unsw.edu.au/~shon/cgi-bin/server.py"

def request_help(args):
    user, machine = get_info()

    print("Sending for help...")

    params = {"action": "help", "id": user, "course": args.course.upper(),
        "location": machine.lower(), "duration": args.duration, "description": args.description}
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

def get_info():
    user = run_command("whoami").strip()
    machine = run_command("hostname").strip()

    if not user or not machine:
        exit("Couldn't work out your user/machine. Seek help immediately.")

    return user, machine

def run_command(command):
    child = subprocess.Popen(command, stdout=subprocess.PIPE)
    return child.communicate()[0]

def helped_by(args):
    # close a help request and store who completed it etc
    pass

def new_notification(jobid, course, location, description, jobsLeft):
    # TODO: pull detailed information
    message = "CSE-HELPME: " + job + " needs help with " + course + "@" + location + ":" + description
    if jobsLeft > 0:
        message = message + "\nYou have " + str(jobsLeft) + " more relevant jobs, dismiss to see next"

    child = subprocess.Popen("echo -e " + message + "|xmessage -buttons dismiss:0,assist\ " + jobid + ":1 -file -")
    returncode = child.returncode
    if returncode is 1: # This guy wants to assist.
        # TODO: Call assist on jobid
        rubbish = 5

def helper_daemon(args):
    user, machine = get_info()

    while True:

        # Poll
        print >>sys.stderr, "Polling..."

        # TODO: database needs to provide us with jobid, course, description, etc
        # Received a poll response
        seen_jobs = []
        fresh_jobs = ["sgreen", "emmaw"]
        for job in fresh_jobs:
            if job not in seen_jobs:
                seen_jobs.append (job)

                # do a notification
                new_notification (job, "COMP1917", "drum07", "really good", 5)
        time.sleep(args.interval)

def register(args):
    user, machine = get_info()
    print "Registering your specialties..."

    courses = ",".join(args.courses)

    params = {"action": "start", "id": user, "skills": courses}
    try:
        r = requests.post(SERVER, params=params)
    except requests.exceptions.RequestException:
        exit("Something went wrong and we couldn't connect to the server, sorry :(")

    jsondata = r.json()
    if jsondata["status"] == "OK":
        print "Registration accepted, thanks! \n\nTip: Make sure you have the daemon running to get notifications."
    else:
        print "Sorry, registration not accepted. Reason: %s" % jsondata["status"]



if __name__ == "__main__":
    desc = """
    Receive or provide help on UNSW CSE courses.
    """
    parser = argparse.ArgumentParser(description=desc)
    subparsers = parser.add_subparsers()

    help_parser = subparsers.add_parser("help", help="Ask for help with a course")
    help_parser.add_argument("course", metavar="COURSE", help="The course you want help with, in the format COMP1234")
    help_parser.add_argument("--duration", "-t", metavar="t", default=60, type=int, help="Time your request will remain open, in minutes (default 60)")
    help_parser.add_argument("--description", "-d", metavar="\"<text>\"", default="", help="Short description (to pass to your helpers)")
    help_parser.set_defaults(func=request_help)

    helpedby_parser = subparsers.add_parser("helpedby", help="Tell us who helped you out!")
    helpedby_parser.add_argument("user", metavar="USER", help="The user who helped you")
    helpedby_parser.set_defaults(func=helped_by)

    helperdaemon_parser = subparsers.add_parser("helper-daemon", help="Run the helper service")
    helperdaemon_parser.add_argument("--interval", "-i", default=30, metavar="wait", type=int, help="Poll every _wait_ seconds")
    helperdaemon_parser.set_defaults(func=helper_daemon)

    helpedby_parser = subparsers.add_parser("register", help="Register as a helper")
    helpedby_parser.add_argument("courses", metavar="COURSES", nargs="+", help="What courses can you help with?")
    helpedby_parser.set_defaults(func=register)


    args = parser.parse_args()
    args.func(args)
