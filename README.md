cse-helpme
==========
Written by Stanley Hon (shon), Shannon Green & Brady Watkinson (bawa088)

## Disclaimer

This is likely fairly bug-ridden, report bugs to shon@cse.unsw.edu.au and we'll fix em some time,
alternatively, raise them on the github issue tracker.

This system also is not particularly secure, there is no real personal information or anything 
of value worth stealing - but you could make it hard for people to find help or provide it.

## Overview

cse-helpme connects people with help with a CSE course in the labs.

If you need help with a particular course, while in the labs - specify which course
and all cse-helpme users registered to help with that course will get a popup notification.

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

and the script will take care of the rest. For more information, see Requesting help.

## Install

1. cd ~
2. git clone https://github.com/stanleyhon/cse-helpme.git
3. cse-helpme/install

## Manual install

1. git clone https://github.com/stanleyhon/cse-helpme.git
2. Install python dependencies:
3. 
        $> pip install --user requests
      
3. Create ~/.xprofile and add the following

        #!/bin/sh
        nohup python ~/cse-helpme/client/csehelp.py helper-daemon&
        
    Then execute

        $> chmod 775 ~/.xprofile

4. Log out of your CSE account, then log back in!

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

     ["COMP1917","COMP1927","COMP2121","COMP2911","COMP3331","COMP3821","COMP3891",
      "COMP1911","COMP1921","COMP9242","COMP3231","COMP4128","COMP6771","COMP9243",
      "COMP9447","COMP3421","COMP3311","COMP3121"]

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

## Known bugs

- You get notifications for your own help requests if you have stated you can help with that course
