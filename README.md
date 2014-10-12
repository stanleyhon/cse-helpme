cse-helpme
==========
Written by Stanley Hon (shon), Shannon Green (sgreen) & Brady Watkinson (bawa088)

## Disclaimer

This is likely fairly bug-ridden, report bugs to shon@cse.unsw.edu.au and we'll fix em some time,
alternatively, raise them on the github issue tracker.

This system also is not particularly secure, there is no real personal information or anything 
of value worth stealing - but you could make it hard for people to find help or provide it.

## Overview

cse-helpme connects people with help with a CSE course in the labs.

If you need help with a particular course, while in the labs - specify which course
and all cse-helpme users registered to help with that course will get a popup notification 
if they are logged in on a CSE machine - in any lab.

If you want to help others in the labs, register the courses you can help with
and anyone needing help with those courses will send you a popup notifying you of
which lab machine they are at and other useful information.

## Detail

Installing this system on your CSE account simply adds our script to your startup
scripts (meaning it runs when you log in). The script polls our server periodically
for anyone who needs help. Additionally, it adds a symbolic link to your ~/bin folder
so you can invoke the script directly.

If you need help, you manually invoke the script and specify:

1. the course you need help with
2. a short description if desired

And the script will take care of the rest. For more information, see Requesting help.

The script sends queries and polls a server (included in this repo under cgi-bin/server.py
which responds with JSON objects which the client script interprets.

It uses environment variables to figure out who you are, and where you are at CSE.

## I'm a judge and I want to demo this

Hi there! You can't test this on your own because the system is designed not to show you your own requests. Here's what you'll need to do.
0. Find at least one friend. Good luck. (If you can't do this, then you will need several CSE accounts)
1. Be at CSE, on lab machines.
2. Each person should run install steps as below.
3. Register your specialities with the script (also below).
4. Get someone to request help and watch as notifications come in! You can respond to those notifications using the buttons that pop up, and the student-in-distress should receive a notification back.
5. Give all prizes to Brady, Stanley and Shannon.

## Install (RECOMMENDED)

1. cd ~
2. git clone https://github.com/stanleyhon/cse-helpme.git
3. cse-helpme/install

If you are having trouble installing the system, see Manual Install.

## Requesting help

If you need help, call the script like this:

     csehelp.py help COMP1917

You can also specify two other additional parameters:
 
Description is designed for you to provide some information (if desired) to people responding.
Note you should try to avoid putting punctuation in the description unless you know how to 
escape it properly.
     
     csehelp.py help COMP1917 --description "a description goes here"

Duration indicates how long you plan on having the help request be active. There is an upper limit of
60 minutes, and the job will remove itself from the system after that time.
     
     csehelp.py help COMP1917 --duration 60

After someone has successfully helped you, or you no longer need help you can remove the job
from the system by using the following command.

     csehelp.py helped

If you do not remove the job, people may still come and try to help you - but the job will eventually
expire.

If you request help again, before your first job has expired, it will replace your first help request.

## Helping someone

If you want to help people, make sure you install the script first, so you can receive
notifications. Then you need to register with the system by typing the following command:

     csehelp.py register COMP1917 COMP1927 COMP2911 COMP3331 COMP3891 COMP1911 COMP1921

The courses we current support are:

     courses = ["COMP1000","COMP1000","COMP1400","COMP1400","COMP1911","COMP1911","COMP1917","COMP1917","COMP1921","COMP1921","COMP1927",
     "COMP1927","COMP2041","COMP2041","COMP2111","COMP2111","COMP2121","COMP2121","COMP2911","COMP2911","COMP3121","COMP3121","COMP3131",
     "COMP3131","COMP3141","COMP3141","COMP3151","COMP3151","COMP3153","COMP3153","COMP3161","COMP3161","COMP3211","COMP3211","COMP3222",
     "COMP3222","COMP3231","COMP3231","COMP3311","COMP3311","COMP3331","COMP3331","COMP3411","COMP3411","COMP3421","COMP3421","COMP3431",
     "COMP3431","COMP3441","COMP3441","COMP3511","COMP3511","COMP3601","COMP3601","COMP3821","COMP3821","COMP3891","COMP3891","COMP3901",
     "COMP3901","COMP3902","COMP3902","COMP4001","COMP4001","COMP4121","COMP4121","COMP4128","COMP4128","COMP4141","COMP4141","COMP4161",
     "COMP4161","COMP4181","COMP4181","COMP4335","COMP4335","COMP4336","COMP4336","COMP4337","COMP4337","COMP4411","COMP4411","COMP4418",
     "COMP4418","COMP4431","COMP4431","COMP4432","COMP4432","COMP4601","COMP4601","COMP4904","COMP4904","COMP4905","COMP4905","COMP4906",
     "COMP4906","COMP4910","COMP4910","COMP4911","COMP4911","COMP4920","COMP4920","COMP4930","COMP4930","COMP4931","COMP4931","COMP4941",
     "COMP4941","COMP6714","COMP6714","COMP6721","COMP6721","COMP6731","COMP6731","COMP6741","COMP6741","COMP6752","COMP6752","COMP6771",
     "COMP6771","COMP9018","COMP9018","COMP9242","COMP9242","COMP9243","COMP9243","COMP9315","COMP9315","COMP9318","COMP9318","COMP9319",
     "COMP9319","COMP9321","COMP9321","COMP9322","COMP9322","COMP9323","COMP9323","COMP9332","COMP9332","COMP9333","COMP9333","COMP9334",
     "COMP9334","COMP9417","COMP9417","COMP9444","COMP9444","COMP9447","COMP9447","COMP9517","COMP9517","COMP9844","COMP9844"]

You can include all of the courses if you like.

If someone needs help with a course you've specified you can help with, you will see a popup
notifying you of who needs help, where they are, and a short description if they have included it.

The popup has two buttons, "dismiss" and "help X". Clicking help will notify the person that 
you are on the way. dismiss will hide the popup.

If you want to see dismissed jobs, you can use the command:

     csehelp.py showall

If you see someone you want to help in this list, simply invoke:

     csehelp.py respond <user-id>

Where user-id is the person who you want to help.

## Manual install (ADVANCED)

1. git clone https://github.com/stanleyhon/cse-helpme.git
      
2. Create ~/.xprofile and add the following

        #!/bin/sh
        nohup python ~/cse-helpme/client/csehelp.py helper-daemon&
        
    Then execute

        $> chmod 775 ~/.xprofile

4. Log out of your CSE account, then log back in!

## Developer setup

Use these instructions to setup your own database and server, note you will need to modify the 
scripts in order to have them contact your server instead of the default hardcoded server.

1. git clone the repo
2. run make\_DB.py
3. put cgi-bin files in cgi-bin for your webserver.

## Stuff we would have done if we had time
- Be smarter about notifications; only notify people in nearby labs
- Game mechanics (earn points for helping people. Compete!)
- Security

## Known bugs

- You get notifications for your own help requests if you have stated you can help with that course

## Removal

To remove the system, simply remove the startup code from ~/.xprofile and delete related files.
To temporarily disable the system, you can comment out the startup code from ~/.xprofile.
