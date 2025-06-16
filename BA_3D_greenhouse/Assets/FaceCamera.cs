using UnityEngine;

/// <summary>
/// FaceCamera is responsible for making a GameObject face the camera at all times.
/// </summary>
public class FaceCamera : MonoBehaviour
{
    public Camera cam;

    void Start()
    {
        if (cam == null)
        {
            cam = Camera.main; // Fallback to the main camera if none is assigned
        }
    }

    void Update()
    {
        transform.LookAt(transform.position + cam.transform.rotation * Vector3.forward,
                         cam.transform.rotation * Vector3.up);
    }
}