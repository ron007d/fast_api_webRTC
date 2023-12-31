import asyncio
import json
import platform
import os
import cv2

from aiortc import RTCPeerConnection, RTCSessionDescription,RTCConfiguration,RTCIceServer, MediaStreamTrack
from aiortc.contrib.media import MediaPlayer, MediaRelay
from av import VideoFrame

import requests

server_url = 'http://116.193.133.227:5000/'
def send_offer(data):
    data = {'user_name':'pi_video_server',
            'offer':data}
    response = requests.post(url = f'{server_url}offer_data',params=data)
    print(response)
    
def get_answer():
    try:
        while True:
            pass
    except:
        print('Keyboard error')
            
    
relay = MediaRelay()
ice_servers = [RTCIceServer(urls='stun:___________________'),
               RTCIceServer(urls='turn:___________________',
                            username='____________________',
                            credential="___________________"),
               RTCIceServer(urls="turn:____________________________" ,
                            username = "__________________________",
                            credential ="_________________________" ),
               RTCIceServer(urls= "turn:________________________",
                            username = "__________________________",
                            credential = "_________________________"),
               RTCIceServer(urls= 'turn:____________________________',
                            username = "__________________________",
                            credential = "_________________________"),]


config = RTCConfiguration(iceServers=ice_servers)

google_ice = [RTCIceServer(urls='stun:stun.l.google.com:19302')]

config2 = RTCConfiguration(google_ice)

def create_local_video():
    options = {'framerate':'60','video_size':'1280x720'}
    webcam = MediaPlayer('/dev/video0',options=options)
    return relay.subscribe(webcam.video)


async def offer():
    print('Starting RTC connection')
    
    peer_connection = RTCPeerConnection(configuration=config)
    
    @peer_connection.on('connectionstatechange')
    def connection_status():
        print('*'*20)
        print('Connection status is ',peer_connection.connectionState)
        print('*'*20)
    
    
    
    
    @peer_connection.on('datachannel')
    def datachannel_event(channel):
        
        print('data channel created > ',channel)
        
        @channel.on('open')
        async def on_open(message):
            print('Connection Opened ',message)
            
        @channel.on('message')
        async def on_message(message):
            print('Got mesage > ',message)
            
        @channel.on('close')
        def on_close(message):
            print("Connection Closed ",message)

    
    video = create_local_video()
    peer_connection.addTrack(video)
    offer_decription = await peer_connection.createOffer()
    await peer_connection.setLocalDescription(offer_decription)
    
    offer_data = {'sdp':peer_connection.localDescription.sdp,
                  'type':peer_connection.localDescription.type}
    print(json.dumps(offer_data))
    print('\n'*2)
    
    answer = input('ENTER THE ANSWER : ')
    
    answer_data = json.loads(answer)
    answer_data = RTCSessionDescription(sdp= answer_data['sdp'],
                                        type= answer_data['type'])
    await peer_connection.setRemoteDescription(answer_data)
    
if __name__ == '__main__':
    # asyncio.run(offer())  
    loop = asyncio.get_event_loop()
    loop.run_until_complete(offer())
    loop.run_forever()  
    