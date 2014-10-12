#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('helpMe_DB.db')

#===Select * from table=====
def get_users_table():
    cursor = conn.execute("SELECT * from USERS")
    for row in cursor:
        print '%s' % (row[0])

def get_skills_table():
    cursor = conn.execute("SELECT * from SKILLS")
    for row in cursor:
        print '%s %s' % (row[0], row[1])

def get_job_queue_table():    
    cursor = conn.execute("SELECT * from JOB_QUEUE")
    job_queue = []
    for row in cursor:
        job_queue.append(" | ".join(row))
        print job_queue[len(job_queue)-1]

#===Get skills for User====
def get_skills_for_user(id):
    user_skills = []
    sql = """SELECT USERNAME, COURSE_HELP
                FROM SKILLS
                 WHERE USERNAME = '""" + id + "'" 
    cursor = conn.execute(sql)
    for row in cursor:
        user_skills.append(row[1])
    return user_skills

#===Insert New User===
def insert_new_user(user_id,skills):
    sql = "DELETE FROM USERS WHERE USERNAME = ?"
    conn.execute(sql, (user_id,))
    sql = "DELETE FROM SKILLS WHERE USERNAME = ?"
    conn.execute(sql, (user_id,))
    sql = "INSERT INTO USERS VALUES(?)"
    conn.execute(sql, (user_id,))
    for skill in skills:
        sql = "INSERT INTO SKILLS VALUES(?,?)"
        conn.execute(sql, (user_id, skill))
    conn.commit()

#===deactivate users===
def deactivate_expired_jobs():
    sql = "UPDATE JOB_QUEUE SET ACTIVE = 'NO' WHERE (strftime('%s','now','localtime') - strftime('%s',TIME_START)) > TIME_LENGTH * 60"
    conn.execute(sql)
    conn.commit()
    
#===Make New Job===
def insert_new_job(job):
    user_id = job[0]
    sql = "UPDATE JOB_QUEUE SET ACTIVE = 'NO' WHERE USERNAME = ?"
    conn.execute(sql, (user_id,))
    
    job[4] = str(job[4])
    sql = "INSERT INTO JOB_QUEUE VALUES(NULL,datetime('now','localtime'),'"+"','".join(job)+"')"
    
    conn.execute(sql)
    conn.commit()

#===Get Job Queue for User===
def get_job_queue_for_user(user_id):
    job_queue = []
    for skill in (get_skills_for_user(user_id)):
        sql = """SELECT *
                    FROM JOB_QUEUE
                    WHERE COURSE_NAME = ?
                    AND (strftime('%s','now','localtime') - strftime('%s',TIME_START)) < TIME_LENGTH * 60
                    AND ACTIVE = 'YES'"""
        cursor = conn.execute(sql, (skill,))
        for row in cursor:
            #print "|".join(row)
            job_queue.append("|".join([str(c) for c in row]))
    return job_queue

#===Get my job status===
def get_my_jobs_status(user_id):
    sql = "SELECT RESPONDERS FROM JOB_QUEUE WHERE USERNAME = ? AND ACTIVE = 'YES'"
    cursor = conn.execute(sql, (user_id,))
    status = ""
    for row in cursor:
        status += row[0]
    if status == "OK":
        return "ready"
    elif status == "":
        return "expired"
    else:
        return status
    
#===Check Job Exists===
def check_job_queue_job_exists(job_user_id):
    sql = """SELECT * FROM JOB_QUEUE
                WHERE USERNAME = ?
                AND ACTIVE = 'YES'"""
    cursor = conn.execute(sql, (job_user_id,))
    bool = False
    for row in cursor:
        bool = True
    return bool

#===Update Job Queue Response===
def update_job_queue_response(job_user_id, user_id):
    sql = "SELECT RESPONDERS FROM JOB_QUEUE WHERE USERNAME = ? AND ACTIVE = 'YES'"
    cursor = conn.execute(sql, (job_user_id,))
    status = ""
    for row in cursor:
        status += row[0]
    if status == "OK":
        sql = "UPDATE JOB_QUEUE SET RESPONDERS = ? WHERE USERNAME = ? AND ACTIVE = 'YES'"
    else:
        sql = "UPDATE JOB_QUEUE SET RESPONDERS = RESPONDERS || ', ' || ? WHERE USERNAME = ? AND ACTIVE = 'YES'"
    cursor = conn.execute(sql, (user_id, job_user_id))
    conn.commit()    

#===Complete Job===
def update_job_queue_queue_complete(job_user_id):
    sql = "UPDATE JOB_QUEUE SET ACTIVE = 'NO' WHERE USERNAME = ?"
    cursor = conn.execute(sql, (job_user_id,))
    conn.commit()    
