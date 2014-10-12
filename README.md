cse-helpme
==========

for the cse hackathon

## Install

1. cd ~
2. git clone https://github.com/stanleyhon/cse-helpme.git
3. cse-helpme/install

## Manual install

1. git clone https://github.com/stanleyhon/cse-helpme.git
2. Install python dependencies:
3. 
        $ pip install requests
      
3. Create ~/.xprofile and add the following

        #!/bin/sh
        nohup python ~/cse-helpme/client/csehelp.py helper-daemon&
        
    Then execute

        chmod 775 ~/.xprofile

4. Log out of your CSE account, then log back in!

## Requesting help
TBA

## Helping someone
TBA
