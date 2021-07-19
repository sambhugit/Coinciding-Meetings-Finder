# Coinciding-Meetings-Finder
A python tool to find coinciding online meetings.
###
Are you facing this problem! \
\
Got fed up of a number of meeings everyday and headaches due to multiple meetings coinciding.\
\
This python tool will help you find the coinciding meetings you have everyday.\
\
Run this at start of a day and it will show your 'gonna clash' meetings.
### Step 1: Create the app
For the current project, I have only took Zoom meetings as it is more popular nowadays.\
* To ping the api, first we need to create an OAuth or JWT or any access granting app with enough scope to get you the list of meetings.
* Refer to the API documentation of your online meeting provider for knowing how to create an app. For Zoom alone, you can just visit [Zoom Marketplace](https://marketplace.zoom.us/) and create your app. In this project, we will be sticking to JWT app as it is more easier.
* Once you created the app, copy the "token" and save it somewhere. Make sure you grant enough expire time for your token.
### Step 2: Ping the API's
* To ping the api, lets use http client module inbuild in python. You can also use 'requests' module for the same. 
```
import http.client
token = "bbbbbb'Your token here!'bbbbbbbbbbbbbbbbbbbbbbbaaaaaaaaaaabbbbbbbbbbb"

conn = http.client.HTTPSConnection("api.zoom.us") #Give base url of your meeting povider here..

headers = {
    'authorization': "Bearer" + token,
    'content-type': "application/json"
}   
conn.request("GET", "/v2/users/{Give your zoom user id}/meetings", headers=headers) #The REST API should be formatted as per your meeting provider API

res_m = conn.getresponse()
```
* The above code will download the meeting list in your Zoom id. Now lets encode it in "utf-8" format and save it as a JSON so that we can easily work in it.
```
data_m = res_m.read()

data_m = data_m.decode("utf-8")
f_m = open("meetings_list.json",'w')
f_m.write(data_m)
f_m.close()
```
### Step 3: Sort the meetings
* Since we have the meetings, lets sort them out to find the conciding ones.
* Lets open the "meetings_list.json" first.
```
with open("meeting_list.json",'r') as file_read:
    data = json.load(file_read)

meetings_start_time = []
meetings_end_time = []
meetings_topic = []
```
* Now lets sort the meetings. Two meetings are coinciding if the start time of one meeting is earlier than the end time of another meeting. 
* Didn't get it. Rethink about it. If one meeting starts at 11.00 am and ends at 12.00 pm and the second one starts at 11.30 am and ends at 12.15 pm, they are coinciding!
* Here we will be using pyhon 'datetime' module to sort the meetings and find the ones coinciding.
```
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
```
* So cool. Now we have list of start and end time of all meetings in the present day for the user along with meeting topic.
* Lets shuffle the lists together and sort them in ascending order of meeting_start_time.
```
meetings_start_time,meetings_end_time,meetings_topic=  zip(*sorted(zip(meetings_start_time, meetings_end_time, meetings_topic)))
```
* Now to find the ones coinciding, all we have to do is to check the start and end times of meetings in the list.
```
for checker in range(0,len(meetings_start_time)):
    if meetings_end_time[checker] > meetings_start_time[checker + 1]:
        print("\nMeeting with topic ","'%s'"%meetings_topic[checker]," and meeting with topic ","'%s'"%meetings_topic[checker+1]," are coinciding!\n")
```
* Done! Now we have the coinciding meetings.
* Remember, this code will fail to find meetings that ends and start past midnight. For eg. One meetings starts at 2021/07/19 11.00 pm, ends at 2021/07/20 12.30 am and the next meeting starts at 2021/07/20 12.15 am, ends at 2021/07/20 1.00 am, our code is going to classify 2nd meeting as future meeting and wont care about it. 
* For trial, I have uploaded a small 'meeting_list.json' file as an example. Clone this repo and run 'sorter.py' to get a demo of the code.
