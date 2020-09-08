import socket
import logging 
import time
import sys
import math
import subprocess
from emoji import demojize

oauth = 'oauth:ga1k0354tbhq3afzk7gu4ts1mnc86w'
server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'sjxf'
channel = f'{sys.argv[1]}'

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s — %(message)s',
                    datefmt='%Y-%m-%d_%H:%M:%S',
                    handlers=[logging.FileHandler(f'logs/chat.log.{channel}', encoding='utf-8')])

subprocess.Popen(f'tail -f logs/chat.log.{channel}', shell=True)

sock = socket.socket()
sock.settimeout(120)
sock.connect((server, port))
sock.send(f'PASS {oauth}\n'.encode('utf-8'))
sock.send(f'NICK {nickname}\n'.encode('utf-8'))
sock.send(f'JOIN #{channel}\n'.encode('utf-8'))

count = 0.0
rate = 0.0

start_time = time.time()

while True:
    resp = sock.recv(2048).decode('utf-8')
    if resp.startswith('PING'):
        sock.send('PONG\n'.encode('utf-8'))
        #logging.info(resp)
    
    elif len(resp) > 0:
        logging.info(demojize(resp))
    
    if (count%4 == 0): 
        #time.sleep(0.1)
        end_time = time.time()
        rate = 4/(end_time-start_time)
        start_time = end_time
        
    logging.info(f"Calls = {count}, Messages Sent Per Second = {rate}")
    count += 1

sock.close()

        