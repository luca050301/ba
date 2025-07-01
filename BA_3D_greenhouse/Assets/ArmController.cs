using UnityEngine;
using System.Runtime.InteropServices;

/// <summary>
/// ArmController is responsible for controlling the rotation of a robotic arm.
/// It allows the arm to rotate towards a target position and sends the arm's position to a WebGL application.
/// The arm consists of four parts: Base, Shoulder, Elbow, and Wrist.
/// </summary>
public class ArmController : MonoBehaviour
{
    // Import the WebGL function to send arm position
#if UNITY_WEBGL && !UNITY_EDITOR
        [DllImport("__Internal")]
        private static extern void GetArmPos(string position);
#else
    private static void GetArmPos(string position)
    {
        Debug.Log("ERROR");
    }
#endif

    public GameObject Base; // rotate around Y-axis
    public GameObject Shoulder; // rotate up and down
    public GameObject Elbow; // rotate up and down
    public GameObject Wrist; // rotate up and down

    Quaternion initialBaseRotation, initialShoulderRotation, initialElbowRotation, initialWristRotation;


    Quaternion targetBaseRotation, targetShoulderRotation, targetElbowRotation, targetWristRotation;

    Vector3 baseWristPosition;

    public float rotationSpeed = 1f;

    float rotationProgress = 1f;

    /// <summary>
    /// Sets the arm's initial rotations.
    /// </summary>
    void Start()
    {
        initialBaseRotation = Base.transform.localRotation;
        initialShoulderRotation = Shoulder.transform.localRotation;
        initialElbowRotation = Elbow.transform.localRotation;
        initialWristRotation = Wrist.transform.localRotation;

        targetBaseRotation = initialBaseRotation;
        targetShoulderRotation = initialShoulderRotation;
        targetElbowRotation = initialElbowRotation;
        targetWristRotation = initialWristRotation;

        baseWristPosition = Wrist.transform.position;
    }

    /// <summary>
    /// Updates the arm's rotation towards the target position every frame if a rotation is in progress.
    /// </summary>
    void Update()
    {
        if (rotationProgress < 1f)
        {
            rotationProgress += Time.deltaTime * rotationSpeed;
            rotationProgress = Mathf.Clamp01(rotationProgress);

            // Interpolate rotations
            Base.transform.localRotation = Quaternion.Lerp(initialBaseRotation, Quaternion.Euler(0, 0, targetBaseRotation.eulerAngles.z), rotationProgress);
            Shoulder.transform.localRotation = Quaternion.Lerp(initialShoulderRotation, Quaternion.Euler(targetShoulderRotation.eulerAngles.x, 0, 0), rotationProgress);
            Elbow.transform.localRotation = Quaternion.Lerp(initialElbowRotation, Quaternion.Euler(targetElbowRotation.eulerAngles.x, 0, 0), rotationProgress);
            Wrist.transform.localRotation = Quaternion.Lerp(initialWristRotation, Quaternion.Euler(targetWristRotation.eulerAngles.x, 0, 0), rotationProgress);

            if (rotationProgress >= 1f)
            {
                try 
                {
                    // Send the final arm position to WebGL
                    sendArmPositionToWebGL((Wrist.transform.position - baseWristPosition).ToString());
                }
                catch (System.Exception e)
                {
                    Debug.LogError($"Error sending arm position: {e.Message}");
                }
            }
        }
    }

    /// <summary>
    /// Initiates the rotation of the arm towards a target position.
    /// </summary>
    public void RotateToTarget(Transform target)
    {
        // Set initial rotations
        initialBaseRotation = Base.transform.localRotation;
        initialShoulderRotation = Shoulder.transform.localRotation;
        initialElbowRotation = Elbow.transform.localRotation;
        initialWristRotation = Wrist.transform.localRotation;

        // Calculate target rotations based on the target position
        Vector3 directionToTarget = (target.position - Base.transform.position).normalized;
        Debug.Log($"Base Position: {Base.transform.position}");
        Debug.Log($"Target Position: {target.position}, Direction to Target: {directionToTarget}");

       targetBaseRotation = Quaternion.Euler(0f, 0f, directionToTarget.x < 0 ? 0f : 180f); // Rotate around Y-axis

        //targetShoulderRotation = Quaternion.Euler(30f, 0f, 0f); // Example angle for shoulder
       // targetElbowRotation = Quaternion.Euler(-50f, 0f, 0f); // Example angle for elbow
       // targetWristRotation = Quaternion.Euler(20f, 0f, 0f); // Example angle for wrist

        rotationProgress = 0f;
    }

    /// <summary>
    /// Resets the arm's rotations to their initial state.
    /// </summary>
    public void ResetRotations()
    {
        // Reset rotations to initial state
        targetBaseRotation = initialBaseRotation;
        targetShoulderRotation = initialShoulderRotation;
        targetElbowRotation = initialElbowRotation;
        targetWristRotation = initialWristRotation;

        initialBaseRotation = Base.transform.localRotation;
        initialShoulderRotation = Shoulder.transform.localRotation;
        initialElbowRotation = Elbow.transform.localRotation;
        initialWristRotation = Wrist.transform.localRotation;

        rotationProgress = 0f; // Reset progress for new rotation
    }

    void sendArmPositionToWebGL(string position)
    {
        GetArmPos(position);
    }
}
