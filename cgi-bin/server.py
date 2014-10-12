#!/usr/bin/python
import cgi
import cgitb
import json
cgitb.enable()

#cgi.test()

def statusOK ():
    response = {"status" : "OK"}
    print json.dumps(response)
    exit()

courses = ["COMP1917","COMP1927","COMP2121","COMP2911","COMP3331","COMP3821","COMP3891",
           "COMP1911","COMP1921","COMP9242","COMP3231","COMP4128","COMP6771","COMP9243",
           "COMP9447","COMP3421","COMP3311","COMP3121"]

print "Content-Type: text/html"
print

form = cgi.FieldStorage()

if "action" not in form:
    response = {"status" : "Action Missing"}
    print json.dumps(response)
    exit()

# TODO: Validate ID
if "id" in form:
    myid = form["id"].value
else:
    response = {"status" : "ID Missing"}
    print json.dumps(response)
    exit()


# --- HELP ---
if form["action"].value == "help":    
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

    statusOK()

# --- POLL ---
elif form["action"].value == "poll":
    
    # TODO: Look up skills of this guy
    # TODO: Look up applicable jobs for this guy
    # TODO: Send it
    response = {"status" : "OK", "job1" : {"id" : "shon", "course" : "COMP1917", "expiry" : "136", "Location" : "drum07", "Description" : "im bad", "status" : "in progress"}}
    print json.dumps(response)

# --- START ---
elif form["action"].value == "start":
    if "skills" not in form:
        response = {"status" : "Missing skills"}
        print json.dumps(response)
        exit()

    skills = form["skills"].value.split(',')
    # Step through and make sure all the courses are in the master courselist
    for skill in skills:
        if skill not in courses:
            response = {"status" : "Invalid skill"}
            print json.dumps(response)
            exit()
    
    # All skills are valid

    # TODO: Call DB new user with myid and skills

    statusOK()

# --- RESPOND ---
elif form["action"].value == "respond":
    # TODO: Check this user already exists
    exists = True
    if not exists:
        response = {"status" : "Unknown responder"}
        print json.dumps(response)
        exit()

    # TODO: Check who they're responding to
    if "job" not in form:
        response = {"status" : "Missing job"}
        print json.dumps(response)
        exit()

    job = form["job"].value
    # TODO: Check to see if this job is in existance
    exists = True
    if not exists:
        response = {"status" : "Can't find specified job"}
        print json.dumps(response)
        exit()

    # TODO: mark job as responding
    statusOK()

# --- COMPLETE ---
elif form["action"].value == "complete":
    # TODO: Check the user actually has a valid job
    exists = True
    if exists is False:
        response = {"status" : "No Job to complete"}
        print json.dumps(response)
        exit()

    # TODO: Make database call to complete job. 

    statusOK()
    
