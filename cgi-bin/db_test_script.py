#!/usr/bin/python

from db_interface import *


#for skill in (get_skills_for_user("'john01'")):
#	print skill

#for item in (get_job_queue_for_user("'john01'")):
#	print item

#get_users_table()
#insert_new_user("brady_012",['COMP1917'])
#for user in (get_users_table()):
#	print user
#print "users"
#get_users_table()
#print "skills"
#get_skills_table()
#insert_new_user("test_subject",['COMP2042','COMP1927'])
#get_users_table()
#get_job_queue_table()
#print "new_job"
#insert_new_job(['brady_08','test subject COMP2042','COMP2042','drum09','5','YES','OK'])
#get_job_queue_table()
#print "get skills for user"
#for skill in (get_skills_for_user("test_subject")):
#	print skill
#print "get_job_queue_for_user"
#for item in (get_job_queue_for_user("test_subject")):
#	print item

#update_Job_Queue_Response("brady_03", "test")
deactivate_expired_jobs()
#print check_Job_Queue_Job_Exists("brady_05")
get_job_queue_table()
#update_Job_Queue_Response("brady_06","test")
#get_job_queue_table()
print get_my_jobs_status("brady_08")
conn.close()
