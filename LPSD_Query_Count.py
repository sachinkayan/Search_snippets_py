import smtplib
import string
import sqlite3
from sqlite3 import Error
import commands
from datetime import datetime

str1 = ""

currentMonth = int(datetime.now().month)
currentYear = int(datetime.now().year)


if currentMonth == 1:
    lastMonth = 12
else:
    lastMonth = currentMonth-1


smtpServer = '*****.****.cat.com'  # SMTP server that handles email requests
host = commands.getoutput('hostname')
fromaddr = 'Latest query report' + '@' + host
toaddr=['******@cat.com']
subj = 'Latest query report for '+str(currentYear)+'-'+str(lastMonth)

fpath = '/tardis2/sachin/sqldb_report_log' #A file located in tardis mount to log the report generation
lfile = open(fpath, mode='r')

reportDate = str(lastMonth)+str(currentYear)

for line in lfile:                          # Check whether the report is already generated for the server.
        if reportDate+"-"+host in line:
                print "Report already generated for this server"
                exit()
else:
        print "Generating report...."

try:
        if lastMonth in (10,11,12):
                lastMonth = lastMonth
        else:
                lastMonth = str(0)+str(lastMonth)

        path='/vivisimo/velocity/data/reporting/'+str(currentYear)+'-'+str(lastMonth)
        print "Path is "+str(path)
        conn = sqlite3.connect(path)
        #print conn
        curs = conn.cursor()
        curs.execute("SELECT count(*) FROM reporting;")
        for data1 in curs.fetchall():
                a="Latest Query count for "+str(currentYear)+ " Month "+str(lastMonth)+" is :" +str(data1)+" --  "

        lfile = open(fpath, mode='a')
        lfile.write(reportDate+"-"+host+ "\n")
        print a
        body=a

        def email(toaddr, fromaddr, subj, body, smtpServer):
                msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n" % (fromaddr, string.join(toaddr, ", "), subj))
                server = smtplib.SMTP(smtpServer)
                server.sendmail(fromaddr, toaddr, msg + body)
                server.quit()

        email(toaddr, fromaddr, subj, body, smtpServer)

except Error:
        print "Database file is not available "+str(Error)
        exit()
