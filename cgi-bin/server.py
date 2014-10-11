#!/usr/bin/python
import cgi
import cgitb
import json
cgitb.enable()

#cgi.test()

courses = ["COMP1917"]

print "Content-Type: text/html"
print

form = cgi.FieldStorage()

if "action" not in form:
    response = {"status" : "Action Missing"}
    print json.dumps(response)
    exit()

string = form['course'].value
print string

# SOMEONE NEEDS HELP
if form["action"].value == "help":
    # TODO: Validate ID
    myid = form["id"].value
    
    # Ensure course is legit
    if form["course"].value not in courses:
        response = {"status" : "Invalid course"}
        print json.dumps(response)
        exit()
    course = form["course"].value
    # Ensure duration is legit
    try:
        duration = int(form["duration"].value)
        if (duration > 60 or duration <= 0):
            response = {"status" : "Duration invalid"}
            print json.dumps(response)
            exit()
    except ValueError:
        response = {"status" : "Duration invalid"}
        print json.dumps(response)
        exit()
    # We now have duration in minutes in the variable 'duration'
    description = ""
    if "description" in form:
        description = form["description"].value
    # We now have description in description

    # DB insertion with all that stuff
    print "Your id is " + myid + ". Your course is " + course + ". Your duration is " + str(duration) + ". Your description is " + description + "."

# SOMEONE POLLING TO LOOK FOR JOBS
elif form["action"].value == "poll":
    # TODO: Validate ID
    print "oops"
    

