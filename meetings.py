import json
import http.client

def api_call(token)

    conn = http.client.HTTPSConnection("api.zoom.us") #Give base url of your meeting povider here..
    
    headers = {
        'authorization': "Bearer" + token,
        'content-type': "application/json"
    }   
    conn.request("GET", "/v2/users/{Give your zoom user id}/meetings", headers=headers) #The REST API should be formatted as per your meeting provider API
    
    res_m = conn.getresponse()
    
    data_m = res_m.read()
    
    data_m = data_m.decode("utf-8")
    f_m = open("meetings_list.json",'w')
    f_m.write(data_m)
    f_m.close()
    

if __name__=="__main__":
    
    token= "bbbbbb'Your token here!'bbbbbbbbbbbbbbbbbbbbbbbaaaaaaaaaaabbbbbbbbbbb"
    
    api_call(token)

