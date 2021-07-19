import json
import datetime


def sort_me(data):
    
    meetings_start_time = []
    meetings_end_time = []
    meetings_topic = []

    for meeting in data['meetings']:
        datetime_object = datetime.datetime.strptime(meeting['start_time'], '%Y-%m-%dT%H:%M:%SZ') # Format the meeting start time representation.
        if datetime_object < datetime.datetime.now(): #Check whether the meeting is in the present/future. We have no use with past meetings.
            continue
        if (datetime_object - datetime.datetime.now()) <= datetime.timedelta(days=0,hours = 24, seconds=0, microseconds=0):# In the present/future meetings, lets take present/todays meetings.
            meetings_start_time.append(datetime_object.time()) #Extract the start time of meeting.
            meetings_end_time.append((datetime_object+ datetime.timedelta(hours = (meeting['duration']/60))).time()) #Extract end time of meeting.
            meetings_topic.append(meeting['topic']) #Extract meeting topic.
        else:
          continue
      
    meetings_start_time,meetings_end_time,meetings_topic=  zip(*sorted(zip(meetings_start_time, meetings_end_time, meetings_topic)))
    
    for checker in range(0,len(meetings_start_time)):
        if meetings_end_time[checker] > meetings_start_time[checker + 1]:
            print("\nMeeting with topic ","'%s'"%meetings_topic[checker]," and meeting with topic ","'%s'"%meetings_topic[checker+1]," are coinciding!\n")

if __name__=="__main__":
    
    with open("meeting_list.json",'r') as file_read:
        data = json.load(file_read)
        
    sort_me(data)