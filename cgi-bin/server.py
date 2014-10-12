#!/usr/bin/python
import cgi
import cgitb
import json
import db_interface
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

    #TODO change location
    insert_new_job([myID,description,course,'drum08',duration,'YES','OK'])
    print "Your id is " + myid + ". Your course is " + course + ". Your duration is " + str(duration) + ". Your description is " + description + "."

    statusOK()

# --- POLL ---
elif form["action"].value == "poll":
    
    job_queue = get_job_queue_for_user(myID)
    relevant_jobs = []
    
    #returns job queue in format: job_id|time_start|username|request_desc|course|location|time_length|active|responders
    for job in job_queue:
        info = job.split('|')
               
        newjob = {"id" : info[2], "course" : info[4], "Location" : info[5], "Description" : info[3]}
        relevant_jobs.append (newjob)
     
    
    myStatus = sdaflkj()
            
    response = {"status" : "ok", "jobs" : relevant_jobs, "myjob" : myStatus, "messages" : ""}  

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

    insert_new_user(myid,skills) #added by Brady

    statusOK()

# --- RESPOND ---
elif form["action"].value == "respond":
    exists = True
    if not exists:
        response = {"status" : "Unknown responder"}
        print json.dumps(response)
        exit()

    if "job" not in form:
        response = {"status" : "Missing job"}
        print json.dumps(response)
        exit()

    job = form["job"].value
    exists = check_Job_Queue_Job_Exists(job) #added by Brady
    if not exists:
        response = {"status" : "Can't find specified job"}
        print json.dumps(response)
        exit()

    update_Job_Queue_Response(job,myID) #added by Brady
    statusOK()

# --- COMPLETE ---
elif form["action"].value == "complete":
    exists = check_Job_Queue_Job_Exists(myId)
    if exists is False:
        response = {"status" : "No Job to complete"}
        print json.dumps(response)
        exit()

    update_Job_Queue_Queue_Complete(myId)

    statusOK()
    
conn.close()
