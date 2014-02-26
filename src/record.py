"""
This is the part of the website that manages records of shipments
"""
import smtplib
from email.mime.text import MIMEText

import settings

def email_shipment_info(status):
    from_email = "poomailer@internal.openbiome.com"
    subject = 'Poomailer Label'
    body = "Your shipping label has been created.\n"
    body += "Tracking Code: %s\n" % (status['message']['tracking_code'],)
    body += "Download Label: %s\n" % (status['message']['label_url'],)
    body += "Amount paid: %s\n" % (status['message']['price'],)
    msg = MIMEText(body)

    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = ', '.join(settings.SHIPMENT_EMAILS)

    if settings.DEBUG:
        print "Sent email To %s; From %s" % (str(settings.SHIPMENT_EMAILS), from_email)
        print "Subject: %s" % subject
        print "Body: %s" % body
    else:
        s = smtplib.SMTP('localhost')
        s.sendmail(from_email, settings.SHIPMENT_EMAILS, msg.as_string())
        s.quit()
    return True
