import sendgrid

# MAKE A SECURE CONNECTION TO SENDGRID
# Fill in the variables below with your SendGrid
# username and password.
#========================================================#
sg_username = "emilybee3"
sg_password = "glassman66"

# CREATE THE SENDGRID MAIL OBJECT
#========================================================#
sg = sendgrid.SendGridClient(emilybee3, glassman66)
message = sendgrid.Mail()

# ENTER THE EMAIL INFORMATION
#========================================================#
message.set_from("emilybee3@gmail.com")
message.set_subject("test email")
message.set_text("Hello,\n\nThis is a test message from SendGrid. We have sent this to you because you requested a test message be sent from your account.\n\nThis is a link to my website: http://localhost:5000/\nThis is a link to apple.com: http://www.apple.com\nThis is a link to sendgrid.com: http://www.sendgrid.com\n\nThank you for reading this test message.\n\nLove,\nYour friends at SendGrid")
message.set_html("<table style=\"border: solid 1px #000; background-color: #666; font-family: verdana, tahoma, sans-serif; color: #fff;\"> <tr> <td> <h2>Hello,</h2> <p>This is a test message from SendGrid.    We have sent this to you because you requested a test message be sent from your account.</p> <a href=\"http://www.google.com\" target=\"_blank\">This is a link to google.com</a> <p> <a href=\"http://www.apple.com\" target=\"_blank\">This is a link to apple.com</a> <p> <a href=\"http://www.sendgrid.com\" target=\"_blank\">This is a link to sendgrid.com</a> </p> <p>Thank you for reading this test message.</p> Love,<br/> Your friends at SendGrid</p> <p> <img src=\"http://cdn1.sendgrid.com/images/sendgrid-logo.png\" alt=\"SendGrid!\" /> </td> </tr> </table>")
message.add_to("emilybee3@gmail.com")



# SEND THE MESSAGE
#========================================================#
status, msg = sg.send(message)

print msg