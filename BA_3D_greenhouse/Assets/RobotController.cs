using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// RobotController is responsible for controlling the robot's movement and actions towards plants.
/// It handles the robot's movement towards a target plant, performs actions like watering, fertilizing, harvesting, monitoring, and seeding
/// Also manages the arm controller's rotation to target the plant.
/// </summary>
public class RobotController : MonoBehaviour
{
    private ArmController armController;

    public float moveSpeed = 0.4f; // Speed at which the robot moves towards the plant
    public float actionDuration = 2f; // Duration of the action performed on the plant

    float moveProgress = 1f; // Progress of the movement towards the plant 
    Vector3 initialPosition; // Initial position of the robot
    Vector3 targetPosition; // Target position of the robot (plant position)
    Vector3 armPositionOnRobot; // Position of the arm controller

    string currentAction; // Current action to perform on the plant
    int currentPlantId; // Current plant ID to perform the action on
    Texture2D harvestIcon;
    Texture2D waterIcon;
    Texture2D fertilizeIcon;
    Texture2D monitorIcon;
    Texture2D seedIcon;

    RawImage iconHolder;

    void Start()
    {
        armController = GetComponentInChildren<ArmController>();
        armPositionOnRobot = GameObject.Find("arm").transform.localPosition;

        harvestIcon = Resources.Load<Texture2D>("Images/harvest");
        waterIcon = Resources.Load<Texture2D>("Images/water");
        fertilizeIcon = Resources.Load<Texture2D>("Images/fertilize");
        monitorIcon = Resources.Load<Texture2D>("Images/monitor");
        seedIcon = Resources.Load<Texture2D>("Images/seed");

        iconHolder = GetComponentInChildren<RawImage>();

        iconHolder.enabled = false; // Initially disable the icon holder

    }

    /// <summary>
    /// Updates the robot's position towards the target plant every frame if movement is in progress.
    /// Performs the action on the plant once the robot reaches the target position.
    /// </summary>
    void Update()
    {
        if (moveProgress < 1f)
        {
            // Move towards the target position
            moveProgress += Time.deltaTime * moveSpeed;
            moveProgress = Mathf.Clamp01(moveProgress);
            transform.position = Vector3.Lerp(initialPosition, new Vector3(initialPosition.x, initialPosition.y, targetPosition.z), moveProgress);

            // Check if the robot has reached the target position
            if (moveProgress >= 1f)
            {
                // Perform the action on the plant
                armController.RotateToTarget(GameObject.Find(currentPlantId.ToString()).transform);
                PerformActionOnPlant();
            }
        }

    }
    /// <summary>
    /// Initiates the robot's movement towards a specified plant and performs the given action.
    /// </summary>
    public void MoveToPlantAndPerformAction(string action, int plantId)
    {
        // Set the current action and plant ID
        currentAction = action;
        currentPlantId = plantId;

        // Find the plant by ID
        GameObject plant = GameObject.Find(currentPlantId.ToString());
        if (plant == null)
        {
            Debug.LogError("Plant with ID " + currentPlantId + " not found.");
            return;
        }

        // Set the target position to the plant's position adjusted for the arm controller
        targetPosition = plant.transform.position - armPositionOnRobot; // Adjust position for arm controller
        initialPosition = transform.position;
        moveProgress = 0f; // Reset progress for new action

        armController.ResetRotations(); // Reset arm rotations before moving to the plant
        DisableIconHolder(); // Ensure icon holder is disabled before starting a new action
    }

    /// <summary>
    /// Performs the action on the plant based on the current action set.
    /// This method is called when the robot reaches the target position.
    /// </summary>
    void PerformActionOnPlant()
    {
        Debug.Log("Performing action: " + currentAction + " on plant at position: " + targetPosition);

        // switch based on the action
        switch (currentAction)
        {
            case "water":
                WaterPlant();
                break;
            case "fertilize":
                FertilizePlant();
                break;
            case "harvest":
                HarvestPlant();
                break;
            case "monitor":
                MonitorPlant();
                break;
            case "seed":
                SeedPlant();
                break;

            default:
                iconHolder.enabled = false; // Disable icon holder if action is not recognized
                break;
        }
        // after 10 secs disable the icon holder
        Invoke("DisableIconHolder", 10f);
    }

    void WaterPlant()
    {
        iconHolder.texture = waterIcon;
        iconHolder.enabled = true;
        Debug.Log("Watering plant at position: " + targetPosition);
    }
    void FertilizePlant()
    {
        iconHolder.texture = fertilizeIcon;
        iconHolder.enabled = true;
        Debug.Log("Fertilizing plant at position: " + targetPosition);
    }
    void HarvestPlant()
    {
        iconHolder.texture = harvestIcon;
        iconHolder.enabled = true;
        Debug.Log("Harvesting plant at position: " + targetPosition);
    }
    void MonitorPlant()
    {
        iconHolder.texture = monitorIcon;
        iconHolder.enabled = true;
        Debug.Log("Monitoring plant at position: " + targetPosition);
    }
    void SeedPlant()
    {
        iconHolder.texture = seedIcon;
        iconHolder.enabled = true;
        Debug.Log("Seeding plant at position: " + targetPosition);
    }

    void DisableIconHolder()
    {
        iconHolder.enabled = false; // Disable the icon holder after action is performed
    }
}
