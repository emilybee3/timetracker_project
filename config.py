# email server
import os
MAIL_SERVER = 'smtp.sendgrid.net'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ['sg_username']
print "This is my username"
print MAIL_USERNAME
MAIL_PASSWORD = os.environ['sg_password']

# administrator list
ADMINS = ['emilybee3@gmail.com']
