import pandas as pd
import re 
import sys
import matplotlib.pyplot as plt
from datetime import datetime

def instantiate_dataframe(file):
    msgs = []
    data = []

    with open(file, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
        
        for line in lines:
            if line:
                try:
                    time_logged = line.split('—')[0].strip()
                    time_logged = datetime.strptime(time_logged, '%Y-%m-%d_%H:%M:%S')
                    
                    response = line.split('—')[1:]
                    response = '—'.join(response).strip()
                    if 'Calls =' in response and 'Messages Sent Per Second =' in response:
                        calls, usr_engmt = re.search(
                            'Calls = (.*), Messages Sent Per Second = (.*)', response
                        ).groups()

                        d = {
                            'dt': time_logged,
                            'calls': calls,
                            'user_engagement': usr_engmt
                        }

                        data.append(d)

                    else:
                        username, channel_msg = re.search(
                            ':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*)', response
                        ).groups()

                        channel = channel_msg.split()[0].strip()
                        message = channel_msg.split(':')[1:]
                        message = ':'.join(message).strip()

                        m = {
                            'dt': time_logged,
                            'channel': channel,
                            'username': username,
                            'message': message
                        }

                        msgs.append(m)
                    
                except Exception:
                    pass

    return pd.DataFrame().from_records(msgs), pd.DataFrame().from_records(data)

def get_rate(data):
    return data['user_engagement'].drop_duplicates()
    
if __name__ == "__main__":
    msgs, data = instantiate_dataframe(f'logs/chat.log.{sys.argv[1]}')
    msgs.set_index('dt', inplace=True)
    data.set_index('dt', inplace=True)
    
    plt.figure(1)
    msgs['username'].value_counts().head(10).plot(kind='bar', title='Most active users for latest extraction')
    
    plt.figure(2)
    msgs['message'].value_counts().head(10).plot(kind='bar', title='Most used emotes for latest extraction')
    
    plt.figure(3)
    rate = get_rate(data)
    rate = rate.astype(float)
    rate.plot(title='Rate of messages sent per second (user engagement)')
    plt.xlabel('Date/Time')
    
    plt.figure(4)
    data = data.astype(float)
    data.plot(title='Total number of messages sent')
    plt.xlabel('Date/Time')

    plt.show()
    #data.to_csv('test2.csv')
    #msgs.to_csv('test1.csv')

    # Acquired data:
    # dataframe for calls made over stream = data['calls']
    # dataframe for messages sent per second over stream = data['user_engagement'].drop_duplicates()
    # N most active users = msgs['username'].value_counts().head(N)
    # N most sent messages = msgs['message'].value_counts().head(N)
    # most sent message msgs.describe()['message'].loc('Top')
    # number of times most sent message was sent msgs.describe()['message'].loc('Freq')
    # most active user msgs.describe()['username'].loc('Top')
    # number of msgs sent by most active user msgs.describe()['username'].loc('Freq')

    # ToDo: 
    # (Wordcloud of) most used words/emotes
    # Sentiment analysis on chat 
    # Create report 
