from os import path
import os.path
import commands
from datetime import date
import glob

hostname = commands.getoutput('hostname -a')

environment = 'Prod' #Prod  QA  test - Change the environment variable value(case sensitive) accordingly.
cert_dir1 = '/srch_share_p/ssl_certificates/'+environment+'/' #Directory where certificates are downloaded initially.
cert_dir2 = '/srch_share_p/ssl_workarea_2020/'+environment+'/' #Working-directory for extrating files from .pfx file

cert_list=(glob.glob("/srch_share_p/ssl_certificates/"+environment+"/*.pfx"))
hostname1s=[]

for i in cert_list:
        i = i.replace('/srch_share_p/ssl_certificates/'+environment+'/','')
        hostname1s=hostname1s.append(i.strip())


#print "Certificate name is "+certificate
#print "Hostname is "+hostname
#print "Hostname is "+hostname1
#print "----------------------------------------------"

#working_dir = commands.getoutput('pwd')
#print "Current directory is "+working_dir

#commands.getoutput('cp -p '+cert_dir1+hostname1+'.pfx '+cert_dir2) #Copy .pfx file to working directory

#res = os.path.isfile(cert_dir2+certificate)

#print "Copy status "+ str(res)
#print "----------------------------------------------"

for hostname1 in hostname1s:

        certificate = hostname1+'.pfx'
        commands.getoutput('cp -p '+cert_dir1+hostname1+'.pfx '+cert_dir2)
        res = os.path.isfile(cert_dir2+certificate)
        print "Copy status "+ str(res)
        print "----------------------------------------------"
        print "Certificate name is "+certificate
        #print "Hostname is "+hostname
        print "Hostname is "+hostname1
        print "----------------------------------------------"


        if res == True: #If the certificate file is available in the working directory, proceed with extraction

                print "Certificate is avaialbe in source directory"

                print "Provide credentials for extracting CERT"
                print "->"
                a=commands.getoutput\
                        ('openssl pkcs12 -in '+cert_dir2
                                +certificate+ ' -clcerts -nokeys -out '
                                       +cert_dir2+'ca-'+hostname1+'-2022-01-22.cert') #Extract CERT file from .pfx file
                print "Cert extraction result : "+a

                if "MAC verified OK" in a:
                        print "Provide credentials for extracting KEY"
                        print "->"


                        b=commands.getoutput\
                                ('openssl pkcs12 -in '+cert_dir2
                                        +certificate+ ' -nocerts -out '
                                                +cert_dir2+'ca-'+hostname1+'-2022-01-22.key') #Extract KEY file from .pfx file

                        print "Key extraction result : "+b
                else:
                        commands.getoutput('rm '+cert_dir2+hostname1+'-2022-01-22.cert')
                        print "Extraction of CERT failed"
                        exit()

                if "MAC verified OK" in b:
                        print "Provide credentials for extracting CRT"
                        print "->"

                        c=commands.getoutput\
                                ('openssl pkcs12 -in '+cert_dir2
                                        +certificate+ ' -out '
                                        +cert_dir2+'ca-'+hostname1+'-2022-01-22.crt -nodes -nokeys -cacerts') #Extract CRT file from .pfx file

                        print "CRT extraction result : "+c

                        if "MAC verified OK" in c: # If all 3 files are extracted successfuly, change the access rights using chmod.
                                print "--------------------------------------------------"
                                print "CERT, KEY and CRT files are generated successfully"
                                print "Files are available in directory : "+cert_dir2
                                print "--------------------------------------------------"

                                x1 = commands.getoutput('chmod 664 '+cert_dir2+'ca-'+hostname1+'-2022-01-22.key')
                                x2 = commands.getoutput('chmod 664 '+cert_dir2+'ca-'+hostname1+'-2022-01-22.cert')
                                x3 = commands.getoutput('chmod 775 '+cert_dir2+'ca-'+hostname1+'-2022-01-22.crt')

                                print "chmod completed for files" + x1 + "," + x2 + "," +x3
                        else:
                                commands.getoutput('rm '+cert_dir2+hostname1+'-2022-01-22.key')
                                commands.getoutput('rm '+cert_dir2+hostname1+'-2022-01-22.cert')
                                commands.getoutput('rm '+cert_dir2+hostname1+'-2022-01-22.crt')
                                print "Please run the script again with correct credentials"
                                exit()
                else:
                        commands.getoutput('rm '+cert_dir2+hostname1+'-2022-01-22.key')
                        commands.getoutput('rm '+cert_dir2+hostname1+'-2022-01-22.cert')
                        print "Extraction of KEY failed"
                        exit()

        else:
                print "Certificate is not available in the source  directory"
                exit()
