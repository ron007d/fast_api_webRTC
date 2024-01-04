import asyncio
import json
import platform
import os
import cv2

from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack, RTCConfiguration, RTCIceServer
from aiortc.contrib.media import MediaPlayer, MediaRelay
from av import VideoFrame





relay = MediaRelay()
webcam = None
ice_servers = [RTCIceServer(urls='stun:stun.relay.metered.ca:80'),
               RTCIceServer(urls='turn:a.relay.metered.ca:80',
                            username='baeb547adee013b092d0efbc',
                            credential="2IpEXdau9fs7lFSY"),
               RTCIceServer(urls="turn:a.relay.metered.ca:80?transport=tcp" ,
                            username = "baeb547adee013b092d0efbc",
                            credential ="2IpEXdau9fs7lFSY" ),
               RTCIceServer(urls= "turn:a.relay.metered.ca:443",
                            username = "baeb547adee013b092d0efbc",
                            credential = "2IpEXdau9fs7lFSY"),
               RTCIceServer(urls= 'turn:a.relay.metered.ca:443?transport=tcp',
                            username = "baeb547adee013b092d0efbc",
                            credential = "2IpEXdau9fs7lFSY"),]

config = RTCConfiguration(iceServers=ice_servers)

class VideoPlayer(MediaStreamTrack):
    kind = 'video'
    
    def __init__(self,track):
        super().__init__()
        self.track = track
        
    async def recv(self):
        # print('waiting for frames to arrive')
        frame = await self.track.recv()
        
        return frame
    
def create_local_video():
    options = {'framerate':'60','video_size': '1280x720'}
    webcam = MediaPlayer('/dev/video2',options= options)
    return relay.subscribe(webcam.video)
        
    

def create_local_tracks(play_from, decode):
    global relay, webcam

    if play_from:
        player = MediaPlayer(play_from, decode=decode)
        return player.audio, player.video
    else:
        options = {"framerate": "30", "video_size": "1280x720"}
        if relay is None:
            if platform.system() == "Darwin":
                webcam = MediaPlayer(
                    "default:none", format="avfoundation", options=options
                )
            elif platform.system() == "Windows":
                webcam = MediaPlayer(
                    "video=Integrated Camera", format="dshow", options=options
                )
            else:
                webcam = MediaPlayer("/dev/video0", format="v4l2", options=options)
            relay = MediaRelay()
        return None, relay.subscribe(webcam.video)
    
    
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
            
    @peer_connection.on('track')
    def on_track(track):
        print('Recived track ',track.kind)
        if track.kind == 'video':
            # same video return 
            # peer_connection.addTrack(
            #     VideoPlayer(relay.subscribe(track))
            #     )
            video = create_local_video()
            peer_connection.addTrack(video)
            
            
    @peer_connection.on('iceconnectionstatechange')
    def on_iceconnectionstate():
        print('*'*20)
        print('ICE CONNECTION status is ',peer_connection.iceConnectionState)
        print('*'*20)
        
    @peer_connection.on('icegatheringstatechange')
    def on_icegatheringstatechange():
        print('*'*20)
        print('ICE GATHERTING CONNECTION status is ',peer_connection.iceGatheringState)
        print('*'*20)
            
            
            
    offer_data = input('Insert the offer data here = ')
    offer_data = json.loads(offer_data)
    offer_data = RTCSessionDescription(sdp=offer_data['sdp'],type=offer_data['type'])
    
    await peer_connection.setRemoteDescription(offer_data)
    answer = await peer_connection.createAnswer()
    await peer_connection.setLocalDescription(answer)
    print('\n'*3)
    # print(dict(peer_connection.localDescription))
    id = 'test1'
    answer_data = {'sdp':peer_connection.localDescription.sdp,
                   'type':peer_connection.localDescription.type}
    print(json.dumps(answer_data))
    
    
if __name__ == '__main__':
    # asyncio.run(offer())  
    loop = asyncio.get_event_loop()
    loop.run_until_complete(offer())
    loop.run_forever()  
    
    
    