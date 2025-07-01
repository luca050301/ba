
using System.Runtime.InteropServices;
using UnityEngine;

/// <summary>
/// ObjectClicker is responsible for detecting mouse clicks on objects in the scene.
/// The script captures mouse clicks and performs a raycast to detect objects.
/// It sends the name of the clicked object to a WebGL application.
/// Also, it disables keyboard input capture in WebGL builds.
/// </summary>
public class ObjectClicker : MonoBehaviour
{
    // Import the WebGL function to send data
#if UNITY_WEBGL && !UNITY_EDITOR
        [DllImport("__Internal")]
        private static extern void GetData(string deviceId);
#else
    private static void GetData(string deviceId)
    {
        Debug.Log("ERROR");
    }
#endif

    void Start()
    {
        // Disable keyboard input capture in WebGL builds
#if !UNITY_EDITOR && UNITY_WEBGL
               UnityEngine.WebGLInput.captureAllKeyboardInput = false;
#endif
    }

    void Update()
    {
        // Check for mouse click, raycast at clicked position, and send the name of the clicked object
        if (Input.GetMouseButtonDown(0))
        {
            RaycastHit hit;
            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            if (Physics.Raycast(ray, out hit, 100.0f))
            {
                if (hit.transform != null)
                {
                    GameObject go = hit.transform.gameObject;
                    SendEventWithId(go);
                }
            }
        }
    }
    /// <summary>
    /// Sends the name of the clicked GameObject to the WebGL application.
    /// Only sends data if the GameObject is not null and the name is a number.
    /// </summary>
    void SendEventWithId(GameObject go)
    {
        if (go != null && int.TryParse(go.name, out _))
        {
            try
            {
                GetData(go.name);
            }
            catch (System.Exception e)
            {
                Debug.LogError($"Error sending data: {e.Message}");
            }
        }
    }
}
