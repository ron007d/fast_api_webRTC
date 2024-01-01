import asyncio
import json
import platform
import os
import cv2

from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack
from aiortc.contrib.media import MediaPlayer, MediaRelay
from av import VideoFrame

relay = MediaRelay()

def create_local_video():
    options = {'framerate':'60','video_size':'1280x720'}
    webcam = MediaPlayer('/dev/video0',options=options)
    return relay.subscribe(webcam.video)


async def offer():
    print('Starting RTC connection')
    
    peer_connection = RTCPeerConnection()
    
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
    