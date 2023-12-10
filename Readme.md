# FAST API FOR WEBRTC

The implementation flows and learning flow works like this.

---
## Implementation flow
1. FAST API will work as a signalling server.
2. Currently it will follow only request response model but in later time websocket or socket io will be implemented.
3. There will be two user call and answer.
    
    a. Call will create username/room
    
    b. answer will check all the username/room list and select one and will try to connect to that.


## workdone
| Index | Work | Under Planning | Under Progress | Testing | Completeds | Comments |
|:--:|:---|:---:|:--:|:---:|:---:|:--|
|1|Create a simple page with two redirects call and answer | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | |
|2| In the call page create a SDP (Session description) and send it to the fast api | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | Sending to `localhost:8080/offer_data` as post request |
|3| Add Java script to get the answer response from another points | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | Added java script which request from `localhost:8080/get_answer/<username>` if anyone answers from answer page then it will take it and connect with the client |
|4| create answer page where the offers will be shown and user can select those | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | took the keys from the `offers` directionay and passed it to jinja compiler |
|5| Get the offer from the selected user and create `answer SDP`  and pass it to the  `answer_data`| :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | Done |
|6| Check the whole flow and test if it working |:white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | text is being transmitted and ICE candidate is working :blush:
|7| Create a simple HTML page and transmit video using WEB RTC | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | Created using miniwebrtc github and working |
|8| Test the video transmission in LAN | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | LAN CONNECTION WORKING WITH VIDEO TRANSMISSION |
|9| Test the video in NAT transmission | :white_check_mark: | :white_check_mark: | :x: | :bangbang: | Only text data channel is working but video transmission is not working |




### Issues

1. only `Text mode is working in LAN and WAN` where the ice candiadates are getting success but in `video mode only LAN` ice candidate is working.
2. Added turn server but still its not working properly.
