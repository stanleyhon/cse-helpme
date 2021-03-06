#!/usr/bin/env python
import os
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

    jsondata = r.json()
    if jsondata["status"] == "OK":
        print "Help request submitted."
    else:
        print "Sorry, help request not accepted. Reason: %s" % jsondata["status"]

def get_info():
    user = run_command("whoami").strip()
    machine = run_command("hostname").strip()

    if not user or not machine:
        exit("Couldn't work out your user/machine. Seek help immediately.")

    return user, machine

def run_command(command):
    child = subprocess.Popen(command, stdout=subprocess.PIPE)
    return child.communicate()[0]

def complete(args):
    # close a help request

    user, _ = get_info()

    params = {"action": "complete", "id": user}

    try:
        r = requests.post(SERVER, params=params)
    except requests.exceptions.RequestException:
        exit("Something went wrong and we couldn't connect to the server, sorry :(")

    jsondata = r.json()
    if jsondata["status"] == "OK":
        print "Request closed. Have a nice day :)"
    else:
        print "Sorry, request not closed. Reason: %s" % jsondata["status"]


def new_notification(jobid, course, location, description, jobsLeft):
    message = "CSE-HELPME: " + jobid + " needs help with " + course + "@" + location + " \\\"" + description + "\\\""
    if jobsLeft > 0:
        message = message + "\nYou have " + str(jobsLeft) + " more relevant jobs, dismiss to see next"


    returncode = os.system( "echo -e \"" + message + "\"|xmessage -buttons dismiss:0,assist\\ " + jobid + ":1 -file -")
    # don't know why return value is 1*256 but ok
    if returncode == 256: # This guy wants to assist.
        respond(jobid)

def new_info(message):
    os.system("xmessage %s" % message)

def show_all(args):
    
    user, _ = get_info()
    params = {"action": "poll", "id": user}
    try:
        r = requests.get(SERVER, params=params)
    except requests.exceptions.RequestException:
        # Don't exit the daemon, just fail silently
        exit("Something went wrong and we couldn't connect to the server, sorry :(")

    jsondata = r.json()
    if "jobs" in jsondata:
        for job in jsondata["jobs"]:
            print "- %s on %s wants help with %s" % (job["id"], job["location"], job["course"])
            if job["description"]:
                print "\t (\"%s\")" % job["description"]

def helper_daemon(args):
    user, _ = get_info()
    seen_jobs = []
    fresh_jobs = []
    all_jobs = []
    myjob_old_status = ""
    message = ""

    while True:
        # Poll
        print >>sys.stderr, "Polling..."

        params = {"action": "poll", "id": user}
        try:
            r = requests.get(SERVER, params=params)
        except requests.exceptions.RequestException:
            # Don't exit the daemon, just fail silently
            pass

        #print >>sys.stderr, "Received data:"
        jsondata = r.json()
        #print jsondata

        if "status" in jsondata and jsondata["status"] == "OK":
            # Keep track of fresh jobs and seen jobs
            fresh_jobs = [job for job in jsondata["jobs"] if job["id"] not in seen_jobs]
            seen_jobs = [job["id"] for job in jsondata["jobs"]]

            process_jobs(fresh_jobs)

            # Watch the status of any of our job requests
            status = jsondata["myjob"]
            if myjob_old_status != status and status not in ["ready","expired"]:
                print "Accepted"
                new_info("'Good news - your help request was accepted by user(s) %s'" % jsondata["myjob"])
                
            myjob_old_status = status
            
            # Watch the status of new messages
            if "message" in jsondata and jsondata["message"] and jsondata["message"] != message:
                message = jsondata["message"]
                new_info(jsondata["messages"])

        time.sleep(args.interval)

def process_jobs(fresh_jobs):
        # TODO: database needs to provide us with jobid, course, description, etc
        # Received a poll response
        for i, job in enumerate(fresh_jobs):
            print "- %s " % job["id"]
            new_notification(job["id"], job["course"], job["location"], job["description"], len(fresh_jobs) - (i+1))

def respond(job):
    user, _ = get_info()
    params = {"action": "respond", "id": user, "job": job}
    try:
        r = requests.post(SERVER, params=params)
    except requests.exceptions.RequestException:
        exit("Something went wrong and we couldn't connect to the server, sorry :(")
        
    jsondata = r.json()
    
    if jsondata["status"] == "OK":
        print "Response submitted. Go help that guy!"
    else:
        print "Sorry, response not accepted. Reason: %s" % jsondata["status"]

def register(args):
    user, machine = get_info()
    print "Registering your specialties..."

    courses = ",".join(args.courses).upper()

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

def manual_respond(args):
    respond(args.user)

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

    helpedby_parser = subparsers.add_parser("helped", help="Close your help request")
    # helpedby_parser.add_argument("user", metavar="USER", help="The user who helped you")
    helpedby_parser.set_defaults(func=complete)

    helperdaemon_parser = subparsers.add_parser("helper-daemon", help="Run the helper service")
    helperdaemon_parser.add_argument("--interval", "-i", default=7, metavar="wait", type=int, help="Poll every _wait_ seconds")
    helperdaemon_parser.set_defaults(func=helper_daemon)

    helpedby_parser = subparsers.add_parser("register", help="Register as a helper")
    helpedby_parser.add_argument("courses", metavar="COURSES", nargs="+", help="What courses can you help with?")
    helpedby_parser.set_defaults(func=register)

    showall_parser = subparsers.add_parser("showall", help="Display all current help requests")
    showall_parser.set_defaults(func=show_all)
    
    respond_parser = subparsers.add_parser("respond", help="Manually respond to a user's help request")
    respond_parser.add_argument("user", metavar="USER", help="User's request to accept")
    respond_parser.set_defaults(func=manual_respond)

    args = parser.parse_args()
    args.func(args)
