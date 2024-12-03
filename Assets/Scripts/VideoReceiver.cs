using Unity.WebRTC;
using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Linq;

public class VideoReceiver : MonoBehaviour
{
    public RenderTexture renderTexture; // Assign this in the inspector
    private RTCPeerConnection pc;
    private MediaStream videoStream;

    private readonly string signalingUrl = "http://192.168.2.187:12345"; // WebRTC signaling server URL

    IEnumerator Start()
    {
        // Create PeerConnection
        RTCConfiguration config = new RTCConfiguration { iceServers = new RTCIceServer[0] };
        pc = new RTCPeerConnection(ref config);

        // Handle received tracks
        pc.OnTrack = (RTCTrackEvent e) =>
        {
            if (e.Track.Kind == TrackKind.Video)
            {
                videoStream = e.Streams.FirstOrDefault();
                if (videoStream != null)
                {
                    Debug.Log("Video stream received");
                }
                else
                {
                    Debug.LogWarning("No video stream found in the track event");
                }
            }
        };

        // Start the signaling coroutine
        yield return StartCoroutine(HandleSignaling(pc));
    }


   private IEnumerator HandleSignaling(RTCPeerConnection pc)
    {
        // Create offer
        var offerOp = pc.CreateOffer();
        yield return offerOp; // Wait until the operation is complete
        RTCSessionDescription offer = offerOp.Desc; // Get the resulting offer

        // Set local description
        var localDescOp = pc.SetLocalDescription(ref offer);
        yield return localDescOp; // Wait until the operation is complete

        // Send offer to the signaling server
        yield return StartCoroutine(SendOfferToSignalingServerCoroutine(offer, pc));
    }

    private IEnumerator SendOfferToSignalingServerCoroutine(RTCSessionDescription offer, RTCPeerConnection pc)
    {
        string json = JsonUtility.ToJson(offer);
        using (UnityWebRequest request = UnityWebRequest.PostWwwForm(signalingUrl, json))
        {
            request.SetRequestHeader("Content-Type", "application/json");
            yield return request.SendWebRequest();

            if (request.result == UnityWebRequest.Result.Success)
            {
                var responseJson = request.downloadHandler.text;
                var answer = JsonUtility.FromJson<RTCSessionDescription>(responseJson);

                var remoteDescOp = pc.SetRemoteDescription(ref answer);
                yield return remoteDescOp; // Wait for remote description to be set
            }
            else
            {
                Debug.LogError($"Failed to exchange SDP with signaling server: {request.error}");
            }
        }
    }


    void OnDestroy()
    {
         if (pc != null)
        {
            pc.Close();
            pc = null;
        }
    }
}

