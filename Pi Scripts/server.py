import asyncio
import cv2
import json
from aiortc import VideoStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.signaling import TcpSocketSignaling
from websockets import serve
#import servo

angles = [0.00]*3

# WebRTC Video Stream Track
class VideoStreamTrack(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)

        async def recv(self):
            frame = await asyncio.to_thread(self.__read_frame)
            return frame

        def _read_frame(self):
            ret, frame = self.cap.read()
            if not ret:
                raise RuntimeError("Failed to read frame from camera")
            return frame

# WebRTC Handler
async def webrtc_handler(signaling):
    peer_connection = RTCPeerConnection()
    peer_connection.addTrack(VideoStreamTrack())

    offer = await signaling.receive()
    await peer_connection.setRemoteDescription(offer)

    answer = await pc.createAnswer()
    await peer_connection.setLocalDescription(answer)
    await signaling.send(peer_connection.localDescription)

    await peer_connection.close()

async def websocket_handler(websocket, path):
    while True:
        try:

            if "angles" in command:
                # Extract angles and save to the angles array as floats
                angles[0], angles[1], angles[2] = map(float, command["angles"])
                print(f"Updated angles: {angles}")

            # Send a response back to the client indicating success
            await websocket.send(json.dumps({"status": "received"}))

        except Exception as e:
            print(f"WebSocket error: {e}")
            break

async def main():
    signaling = TcpSocketSignaling("127.0.0.1", 12345)

    webrtc_task = asyncio.create_task(webrtc_handler(signaling))
    websocket_task = serve(websocket_handler, "0.0.0.0", 8765)

    await asyncio.gather(webrtc_task, websocket_task)

if __name__ == "__main__":
        asyncio.run(main())

        #set_all_servos()

        #print("Servos set to fixed angles: 0°, 90°, 180°")

        time.sleep(2)
