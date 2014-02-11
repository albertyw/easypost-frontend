"""
This is the part of the website that manages records of shipments
"""
import smtplib

from email.mime.text import MIMEText

def email_shipment_info(status, email):
    from_email = "poomailer@internal.openbiome.com"
    body = "Your shipping label has been created.\n"
    body += "Tracking Code: %s\n" % (status['message']['tracking_code'],)
    body += "Download Label: %s\n" % (status['message']['label_url'],)
    msg = MIMEText(body)

    msg['Subject'] = 'Poomailer Label'
    msg['From'] = from_email
    msg['To'] = email

    s = smtplib.SMTP('localhost')
    s.sendmail(from_email, [email], msg.as_string())
    s.quit()
    return True
