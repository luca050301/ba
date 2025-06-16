using UnityEngine;

/// <summary>
/// CameraController is responsible for controlling the camera movement.
/// Movement options are:
/// - Left click to move the camera
/// - Right click to rotate the camera
/// - Zoom using the mouse wheel
/// The camera will always look at a GameObject named "robot" in the scene.
/// </summary>
public class CameraController : MonoBehaviour
{
    public float moveSpeed = 50f;
    public float rotateSpeed = 1000f;
    public float zoomSpeed = 20f;
    public float minZoom = 5f;

    GameObject robot;
    void Start()
    {
        // Find the robot GameObject in the scene
        robot = GameObject.Find("robot");
        if (robot == null)
        {
            Debug.LogError("Robot GameObject not found in the scene.");
        }

        transform.LookAt(robot.transform.position);
    }


    void Update()
    {
        // Move the camera with left mouse button
        if (Input.GetMouseButton(0))
        {
            // move
            float moveX = Input.GetAxis("Mouse X") * moveSpeed * Time.deltaTime;
            float moveY = Input.GetAxis("Mouse Y") * moveSpeed * Time.deltaTime;
            transform.Translate(-moveX, -moveY, 0);

            // Ensure camera is always above ground
            Vector3 position = transform.position;
            position.y = Mathf.Max(position.y, 1f); // Adjust the height as needed
            transform.position = position;
        }

        // Rotate the camera with right mouse button, Rotate around the robot
        if (Input.GetMouseButton(1))
        {
            // rotate
            float rotateX = Input.GetAxis("Mouse X") * rotateSpeed * Time.deltaTime;
            float rotateY = Input.GetAxis("Mouse Y") * rotateSpeed * Time.deltaTime;
            transform.RotateAround(robot.transform.position, Vector3.up, rotateX);
            transform.RotateAround(robot.transform.position, transform.right, -rotateY);

            // Ensure camera is always above ground
            Vector3 position = transform.position;
            position.y = Mathf.Max(position.y, 1f); // Adjust the height as needed
            transform.position = position;

            // slowly look at the robot
            Vector3 direction = robot.transform.position - transform.position;
            Quaternion lookRotation = Quaternion.LookRotation(direction);
            transform.rotation = Quaternion.Slerp(transform.rotation, lookRotation, Time.deltaTime * 2f);
        }

        // Zoom the camera with mouse wheel
        float scroll = Input.GetAxis("Mouse ScrollWheel");
        if (scroll != 0)
        {
            // zoom
            Camera.main.fieldOfView -= scroll * zoomSpeed;
            // Clamp the zoom level
            Camera.main.fieldOfView = Mathf.Clamp(Camera.main.fieldOfView, minZoom, 60f);
        }

    }
}
