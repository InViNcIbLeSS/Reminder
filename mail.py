import imaplib,email,getpass,chardet
import bs4 as bs


unm = raw_input("Enter Gmail id: ")
pwd = getpass.getpass("Enter the pass")
M = imaplib.IMAP4_SSL("imap.gmail.com")
#M.login(unm,pwd)
M.login(unm,pwd)
rv, data = M.select('Inbox')
rv, data = M.search(None,'All')
#f = open("doc.txt","w+")

count = 0

def get_text(msg):
	text = ""
	if msg.is_multipart():
		html = None
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

for num in data[0].split():
    #if count<=4:
        
        rv, data = M.fetch(num,'(RFC822)')
        msg = email.message_from_string(data[0][1])
        print 'Message %s: %s' % (num, msg['Subject'])
        print 'Raw Date:', msg['Date']
        soup = bs.BeautifulSoup((get_text(msg)),"lxml")
        print(soup.get_text())
        #for a in soup.find_all('p'):
        #    print(a.text)
       # count = count + 1

M.close()
M.logout()
