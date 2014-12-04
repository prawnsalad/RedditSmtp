import smtpd
import asyncore
from email.parser import Parser
import praw

class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data):
    	message = Parser().parsestr(data)
    	reddit_user = rcpttos[0].split('@')[0]

    	if self.debug:
	        print 'Receiving message from:', peer
	        print 'Message addressed from:', mailfrom
	        print 'Message addressed to  :', rcpttos
	        print 'Message length        :', len(data)
	        print 'Reddit user           :', reddit_user
	        print 'Message               :', get_message_text(message)

        r.send_message(reddit_user, message['subject'], get_message_text(message))

        return


def get_message_text(msg):
	text = ""
	if msg.is_multipart():
	    for part in msg.get_payload():
	        if part.get_content_charset() is None:
	            charset = chardet.detect(str(part))['encoding']
	        else:
	            charset = part.get_content_charset()
	        if part.get_content_type() == 'text/plain':
	            text = unicode(part.get_payload(decode=True),str(charset),"ignore").encode('utf8','replace')
	        if part.get_content_type() == 'text/html':
	            html = unicode(part.get_payload(decode=True),str(charset),"ignore").encode('utf8','replace')
	    if html is None:
	        return text.strip()
	    else:
	        return html.strip()
	else:
	    text = unicode(msg.get_payload(decode=True),msg.get_content_charset(),'ignore').encode('utf8','replace')
	    return text.strip()



r = praw.Reddit(user_agent='messages')
r.login('account_username', 'account_password')

server = CustomSMTPServer(('0.0.0.0', 25), None)
server.debug = True

asyncore.loop()
