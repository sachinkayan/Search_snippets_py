import os.path
from os import path
import os.path
import commands
from datetime import date

hostname = commands.getoutput('hostname -a')
hostname1 = commands.getoutput('hostname')
certificate = hostname1+'.pfx'
environment = 'test'
cert_dir1 = '/tardis2/ssl_certificates/'+environment #source directory where raw SSL certificates are located
cert_dir2 = '/tardis2/sachin/certificates/PROD/certificates/'+environment #destination directory where key, cert, crt files will be extracted to


print "Certificate name is "+certificate
#print "Hostname is "+hostname
print "Hostname is "+hostname1
print "----------------------------------------------"

working_dir = commands.getoutput('pwd')

#print "Current directory is "+working_dir

commands.getoutput('cp -p /tardis2/ssl_certificates/test/'+hostname1+'.pfx '+'./certificates/PROD/')

res = os.path.isfile('/tardis2/sachin/certificates/PROD/'+certificate)

print "Copy status "+ str(res)
print "----------------------------------------------"

if res == True:

        print "Certificate is avaialbe in source directory"

        print "Provide credentials for extracting CERT"
        print "->"
        a=commands.getoutput\
        ('openssl pkcs12 -in /tardis2/sachin/certificates/'
                   'PROD/'+certificate+ ' -clcerts -nokeys -out /tardis2/sachin/'
                                        'certificates/PROD/ca-'+hostname1+'-03-15-2022.cert')
        print "Cert extraction result : "+a

        if "MAC verified OK" in a:
                print "Provide credentials for extracting KEY"
                print "->"
                b=commands.getoutput\
                ('openssl pkcs12 -in /tardis2/sachin/certificates/'
                   'PROD/'+certificate+ ' -nocerts -out /tardis2/sachin/'
                                        'certificates/PROD/ca-'+hostname1+'-03-15-2022.key')
                print "Key extraction result : "+b
        else:
                commands.getoutput('rm /tardis2/sachin/certificates/PROD/ca-'+hostname1+'-03-15-2022.cert')
                print "Extraction of CERT failed"
                exit()

        if "MAC verified OK" in b:
                print "Provide credentials for extracting KEY"
                print "->"
                c=commands.getoutput\
                ('openssl pkcs12 -in /tardis2/sachin/certificates/'
                   'PROD/'+certificate+ ' -out /tardis2/sachin/'
                                        'certificates/PROD/ca-'+hostname1+'-03-15-2022.crt -nodes -nokeys -cacerts')

                print "CRT extraction result : "+c

                if "MAC verified OK" in c:
                        print "--------------------------------------------------"
                        print "CERT, KEY and CRT files are generated successfully"
                        print "--------------------------------------------------"
                else:
                        commands.getoutput('rm /tardis2/sachin/certificates/PROD/ca-'+hostname1+'-03-15-2022.key')
                        commands.getoutput('rm /tardis2/sachin/certificates/PROD/ca-'+hostname1+'-03-15-2022.cert')
                        commands.getoutput('rm /tardis2/sachin/certificates/PROD/ca-'+hostname1+'-03-15-2022.crt')
                        print "Please run the script again with correct credentials"
                        exit()
        else:
                commands.getoutput('rm /tardis2/sachin/certificates/PROD/ca-'+hostname1+'-03-15-2022.key')
                commands.getoutput('rm /tardis2/sachin/certificates/PROD/ca-'+hostname1+'-03-15-2022.cert')
                print "Extraction of KEY failed"
                exit()

else:
        print "Certificate is not available in the source  directory"
        exit()

