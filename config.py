# email server
import os
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ['MAIL_USERNAME']
print "This is my username"
print MAIL_USERNAME
MAIL_PASSWORD = os.environ['MAIL_PASSWORD']

# administrator list
ADMINS = ['emilybee3@gmail.com']
