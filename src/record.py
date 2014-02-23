"""
This is the part of the website that manages records of shipments
"""
import smtplib
from email.mime.text import MIMEText

from keys import DEBUG

def email_shipment_info(status, to_email):
    from_email = "poomailer@internal.openbiome.com"
    subject = 'Poomailer Label'
    body = "Your shipping label has been created.\n"
    body += "Tracking Code: %s\n" % (status['message']['tracking_code'],)
    body += "Download Label: %s\n" % (status['message']['label_url'],)
    msg = MIMEText(body)

    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    if DEBUG:
        print "Sent email To %s; From %s" % (from_email, to_email)
        print "Subject: %s" % subject
        print "Body: %s" % body
    else:
        s = smtplib.SMTP('localhost')
        s.sendmail(from_email, [to_email], msg.as_string())
        s.quit()
    return True
