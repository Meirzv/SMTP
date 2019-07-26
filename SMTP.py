##########################################################
#   Title   : SMTP Programming Assignment 3
#   Name    : Meir Zeevi
#   File    : SMTP.py
#   NYU ID  : N11290134
#   Version : 1.0.0
#   Python 3 interpreter
##########################################################
import ssl
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from socket import *

def get_and_print_server_response(codeNumber,print_):
    # Check server response for each step of the SMTP protocol
    recv = clientSocket.recv(1024).decode()
    if recv[:3] != codeNumber:
        print(codeNumber+ ' reply not received from server.')
        clientSocket.close()
        exit(print_)
    print("S: " + recv)

################## Receving Gmail input information for the user #########################
emailAddress = input("Enter your Email Address: ")
password = input("Enter your Email Password: ")
############## End of Receving Gmail input information for the user ######################

# Choose a mail server (e.g. Google mail server) and call it mailserver
#Fill in start
server = gethostbyname("smtp.gmail.com")
server_port = 587
#Fill in end

# Create socket called clientSocket and establish a TCP connection with mailserver
#Fill in start
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.settimeout(5)
clientSocket.connect((server,server_port))
#Should receive -- 220 smtp.gmail.com ESMTP b5-v6sm22941298qkf.4 - gsmtp
get_and_print_server_response('220',"Error with the connection. Try a different server")
#Fill in end

###############################################
# Send EHLO command and print server response.
# Should receive:
# 250-SIZE 35882577
# 250-8BITMIME
# 250-STARTTLS
# 250-ENHANCEDSTATUSCODES
# 250-PIPELINING
# 250-CHUNKING
# 250 SMTPUTF8
##############################################
clientSocket.send(b'EHLO gmail.com\r\n')
get_and_print_server_response('250',"Error with EHLO command")

################### STARTTLS and Wrap socket with TLS ########################
clientSocket.send(b'STARTTLS\r\n')  #STARTTLS command
while True: #waiting for TLS response "220 2.0.0 Ready to start TLS"
    starttlsCmd = clientSocket.recv(1024).decode()
    if starttlsCmd.split()[0] == '220':
        break
    elif starttlsCmd.split()[0] == '502':
        print("S: " + "502 5.5.1 Unrecognized command")
        exit("STARTTLS command in unrecognized")
print("S: " + starttlsCmd)
#Wrap the socket with TLS
clientSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_TLSv1_2, do_handshake_on_connect=True)
############################### END ##########################################

############ One Line Authentication ##################
base64encoded = base64.b64encode(("\x00"+emailAddress+"\x00"+password).encode())
clientSocket.send("AUTH PLAIN ".encode()+base64encoded+"\r\n".encode())
# 235 2.7.0 Accepted
get_and_print_server_response('235',"Authentication Faild, Please enter your password correctly")
################ End Authentication ####################


################ Create Mime Message for extra credit ##################
msgMime = MIMEMultipart('related')
msgMime['Subject'] = "Computer Networks Assignment Plus Extra Credit"
msgMime['From'] = "maorzv@gmail.com"
msgMime['To'] = "mz2530@nyu.edu"
image_ = open("nyu.jpg", 'rb').read()
msgImage = MIMEImage(image_, 'jpg')
msgImage.add_header('Content-Disposition', 'inline', filename="nyu.jpg")
body = 'I love computer networks!'
msgText = MIMEText(body, 'plain')
msgMime.attach(msgText)
msgMime.attach(msgImage)
############################# End of Mime ##############################


################# Sending information by SMTP procotol #########################
# Send MAIL FROM command and print server response.
# Fill in start
clientSocket.send(b'MAIL FROM:<maorzv@gmail.com>\r\n')
# 250 2.1.0 OK i2-v6sm20879112qkf.42 - gsmtp
get_and_print_server_response('250',"Problem with MAIL FROM")
# Fill in end
# Send RCPT TO command and print server response.
# Fill in start
clientSocket.send(b'RCPT TO:<mz2530@nyu.edu>\r\n')
# 250 2.1.5 OK i2-v6sm20879112qkf.42 - gsmtp
get_and_print_server_response('250',"Problem with RCPT TO")
# Fill in end
# Send DATA command and print server response.
# Fill in start
clientSocket.send(b'DATA\r\n')
# 354  Go ahead i2-v6sm20879112qkf.42 - gsmtp
get_and_print_server_response('354',"Problem with DATA")
# Fill in end
# Send message data.
# Fill in start

# Without the extra credit
# body = b"\r\n I love computer networks!"
# clientSocket.send(body)

######### Sending email data including image ############
clientSocket.send(msgMime.as_bytes())
#########################################################
# Fill in end
# Message ends with a single period.
# Fill in start
endmsg = b'\r\n.\r\n'
clientSocket.send(endmsg)
# Fill in end
# Send QUIT command and get server response.
# Fill in start
quitCommand = b'QUIT\r\n'
clientSocket.send(quitCommand)
# 250 2.0.0 OK 1540240026 i2-v6sm20879112qkf.42 - gsmtp
get_and_print_server_response('250',"Problem with QUIT")
# Fill in end
################# End of Sending information by SMTP procotol ###################
clientSocket.close()