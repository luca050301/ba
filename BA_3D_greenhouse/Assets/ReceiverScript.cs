using System;
using System.Runtime.CompilerServices;
using UnityEngine;

/// <summary>
/// ReceiverScript is responsible for receiving and parsing flux query data from grafana.
/// It handles the data for plants and the robot, instantiates plant prefabs based on their age, and displays recommended actions.
/// The script also manages the robot's actions and updates the plant prefabs accordingly.
/// </summary>
public class ReceiverScript : MonoBehaviour
{
    // Define the age thresholds for different plant stages
    public TimeSpan seedlingAge = new TimeSpan(4 * 7, 0, 0, 0, 0);
    public TimeSpan plantAge = new TimeSpan(10 * 7, 0, 0, 0, 0);
    public TimeSpan fruitAge = new TimeSpan(15 * 7, 0, 0, 0, 0);


    public GameObject seedlingPrefab;
    public GameObject maturePrefab;
    public GameObject fruitPrefab;
    public GameObject ripePrefab;

    public GameObject emptyPrefab; // Prefab for empty slots
    public GameObject robot;
    private RobotController robotController;
    private DateTime timeOfLastAction = DateTime.MinValue;

    private Texture2D harvestIcon;
    private Texture2D seedIcon;
    private Texture2D waterIcon;
    private Texture2D fertilizeIcon;

    // list of plants currently in the scene
    GameObject[] plantPrefabs = null;

    void Start()
    {
        if (robot == null)
        {
            robot = GameObject.Find("robot");
        }
        robotController = robot.GetComponent<RobotController>();

        harvestIcon = Resources.Load<Texture2D>("Images/harvest");
        seedIcon = Resources.Load<Texture2D>("Images/seed");
        waterIcon = Resources.Load<Texture2D>("Images/water");
        fertilizeIcon = Resources.Load<Texture2D>("Images/fertilize");

        // tests for development purposes only
#if UNITY_EDITOR
        //ManuallyReceive();
#endif
    }
    // Test method for development purposes only
    void SecondReceive()
    {
        Receive("{\"series\":[[{\"recommended_action\":null,\"plant_id\":\"1\",\"age\":\"2025-04-02 18:32:52.381379\"},{\"recommended_action\":null,\"plant_id\":\"10\",\"age\":\"2025-04-17 10:49:47.381379\"},{\"recommended_action\":null,\"plant_id\":\"11\",\"age\":\"2025-05-07 19:00:07.381379\"},{\"recommended_action\":null,\"plant_id\":\"12\",\"age\":\"2025-04-11 17:16:54.381379\"},{\"recommended_action\":null,\"plant_id\":\"13\",\"age\":\"2025-03-19 13:29:31.381379\"},{\"recommended_action\":null,\"plant_id\":\"14\",\"age\":\"None\"},{\"recommended_action\":null,\"plant_id\":\"15\",\"age\":\"2025-05-27 16:13:31.381379\"},{\"recommended_action\":null,\"plant_id\":\"16\",\"age\":\"2025-05-04 15:54:44.381379\"},{\"recommended_action\":null,\"plant_id\":\"17\",\"age\":\"2025-05-11 07:16:41.381379\"},{\"recommended_action\":null,\"plant_id\":\"18\",\"age\":\"2025-04-22 20:28:10.381379\"},{\"recommended_action\":null,\"plant_id\":\"19\",\"age\":\"2025-04-25 04:31:42.381379\"},{\"recommended_action\":null,\"plant_id\":\"2\",\"age\":\"2025-03-24 21:51:26.381379\"},{\"recommended_action\":null,\"plant_id\":\"20\",\"age\":\"2025-04-18 11:31:49.381379\"},{\"recommended_action\":null,\"plant_id\":\"3\",\"age\":\"2025-04-27 23:02:39.381379\"},{\"recommended_action\":null,\"plant_id\":\"4\",\"age\":\"2025-05-16 16:50:40.381379\"},{\"recommended_action\":null,\"plant_id\":\"5\",\"age\":\"2025-04-22 00:42:14.381379\"},{\"recommended_action\":null,\"plant_id\":\"6\",\"age\":\"2025-05-01 09:44:19.381379\"},{\"recommended_action\":null,\"plant_id\":\"7\",\"age\":\"2025-06-29 05:14:28.381379\"},{\"recommended_action\":null,\"plant_id\":\"8\",\"age\":\"2025-06-01 22:12:35.381379\"},{\"recommended_action\":null,\"plant_id\":\"9\",\"age\":\"2025-04-23 13:59:27.381379\"}],[{\"time\":1751309115963,\"action\":\"monitor\",\"position\":1}]]}");
    }


    public void ManuallyReceive()
    {

        Receive("{\"series\":[[{\"time\":1751308304800,\"action\":\"monitoring\",\"position\":20}],[{\"plant_id\":\"1\",\"age\":\"2025-04-13 20:40:02.679555\",\"recommended_action\":null},{\"plant_id\":\"10\",\"age\":\"2025-03-16 21:15:09.679555\",\"recommended_action\":null},{\"plant_id\":\"11\",\"age\":\"2025-05-25 05:50:48.679555\",\"recommended_action\":null},{\"plant_id\":\"12\",\"age\":\"2025-03-14 04:21:06.679555\",\"recommended_action\":null},{\"plant_id\":\"13\",\"age\":\"2025-06-19 01:19:12.679555\",\"recommended_action\":null},{\"plant_id\":\"14\",\"age\":\"2025-06-25 23:10:42.679555\",\"recommended_action\":null},{\"plant_id\":\"15\",\"age\":\"2025-04-21 19:08:03.679555\",\"recommended_action\":null},{\"plant_id\":\"16\",\"age\":\"2025-03-28 21:00:53.679555\",\"recommended_action\":null},{\"plant_id\":\"17\",\"age\":\"2025-04-14 15:14:41.679555\",\"recommended_action\":null},{\"plant_id\":\"18\",\"age\":\"2025-05-31 23:29:00.679555\",\"recommended_action\":null},{\"plant_id\":\"19\",\"age\":\"2025-03-17 14:39:25.679555\",\"recommended_action\":null},{\"plant_id\":\"2\",\"age\":\"None\",\"recommended_action\":null},{\"plant_id\":\"20\",\"age\":\"2025-05-11 12:41:46.679555\",\"recommended_action\":null},{\"plant_id\":\"3\",\"age\":\"2025-04-30 22:13:49.679555\",\"recommended_action\":null},{\"plant_id\":\"4\",\"age\":\"2025-03-25 16:02:39.679555\",\"recommended_action\":null},{\"plant_id\":\"5\",\"age\":\"2025-03-29 12:57:37.679555\",\"recommended_action\":null},{\"plant_id\":\"6\",\"age\":\"2025-05-11 09:35:08.679555\",\"recommended_action\":null},{\"plant_id\":\"7\",\"age\":\"2025-06-06 20:42:20.679555\",\"recommended_action\":null},{\"plant_id\":\"8\",\"age\":\"2025-05-08 19:08:09.679555\",\"recommended_action\":null},{\"plant_id\":\"9\",\"age\":\"2025-04-14 11:00:46.679555\",\"recommended_action\":null}]]}");
        Invoke("SecondReceive", 5f);
}
    /// <summary>
    /// Receives a JSON string parameter, processes it, and updates the plant prefabs and robot actions accordingly.
    /// </summary>
    void Receive(string param)
    {
        
        if (string.IsNullOrEmpty(param))
        {
            Debug.LogError("Received empty parameter.");
            return;
        }
        // Format the JSON string to match the expected structure
        if (param.StartsWith("{\"series\":[[{\"age\"") || param.StartsWith("{\"series\":[[{\"plant_id\"") || param.StartsWith("{\"series\":[[{\"recommended_action\""))
        {
            param = param.Replace("[[", "[").Replace(",[", ",\"robot\":").Replace("]]", "");
        }
        else
        {
            param = param.Replace("\"series\":[[", "\"robot\":").Replace("],", ",\"series\":").Replace("]]", "]");
        }

        if (plantPrefabs == null)
        {
            // Initialize the plant prefabs array with a size of 100
            InitPlants(100);
        }
        try
        {
            // Parse the JSON data
            var jsonData = JsonUtility.FromJson<GreenhouseData>(param);
            if (jsonData.series.Length > 0)
            {
                // for each plant in the series, check its age and instantiate the appropriate prefab (if not already in the scene)
                // display the recommended action for each plant
                foreach (var plant in jsonData.series)
                {
                    TimeSpan? ageSpan = (plant.age != "null" && plant.age != "None") ? DateTime.Now - DateTime.Parse(plant.age) : null;

                    GameObject plantPrefab = GetPlantPrefabForAge(ageSpan);

                    int plantId = int.Parse(plant.plant_id);

                    // if no plant prefab exists for this plantId, or if the prefab is different, instantiate it
                    if (plantPrefabs[plantId] == null || plantPrefab.tag != plantPrefabs[plantId].tag)
                    {
                        if (plantPrefabs[plantId] != null)
                        {
                            Destroy(plantPrefabs[plantId]); // Destroy the old plant prefab
                        }

                        Vector3 position = new Vector3(plantId % 2 == 0 ? -1 : 1, 0, (plantId-1) / 2);
                        Quaternion rotation = Quaternion.identity; // Default rotation

                        plantPrefabs[plantId] = Instantiate(plantPrefab, position, rotation);
                        plantPrefabs[plantId].name = plant.plant_id;

                        DisplayRecommendedAction(plantPrefabs[plantId], plant.recommended_action);
                    }
                }
            }

            // Perform the robot action if it is newer than the last action
            DateTime actionTime = TimeStampStringToDateTime(jsonData.robot.time);
            if (actionTime <= timeOfLastAction)
            {
                Debug.LogWarning("Received action time is not newer than the last action time.");
                return; // Ignore actions that are not newer than the last action
            }

            timeOfLastAction = actionTime; 

            robotController.MoveToPlantAndPerformAction(jsonData.robot.action, int.Parse(jsonData.robot.position));

        }
        catch (Exception e)
        {
            Debug.LogError("Error parsing JSON: " + e);
        }
    }

    DateTime TimeStampStringToDateTime(string timestamp)
    {
        long milliseconds = long.Parse(timestamp);
        DateTime epoch = new DateTime(1970, 1, 1, 0, 0, 0, DateTimeKind.Utc);
        return epoch.AddMilliseconds(milliseconds);
    }

    GameObject GetPlantPrefabForAge(TimeSpan? ageSpan)
    {
        if (ageSpan == null)
        {
            return emptyPrefab; // Return empty prefab if ageSpan is null
        }
        else if (ageSpan < seedlingAge)
        {
            return seedlingPrefab;
        }
        else if (ageSpan < plantAge)
        {
            return maturePrefab;
        }
        else if (ageSpan < fruitAge)
        {
            return fruitPrefab;
        }
        else
        {
            return ripePrefab;
        }
    }

    /// <summary>
    /// Initializes the plant prefabs array with a specified number of plants.
    /// </summary>
    void InitPlants(int plantsCount)
    {
        plantPrefabs = new GameObject[plantsCount];
        for (int i = 0; i < plantsCount; i++)
        {
            plantPrefabs[i] = null; // Initialize with null
        }
    }

    /// <summary>
    /// Displays the recommended action for a given plant prefab based on its tag.
    /// Sets the appropriate action icon in the plant prefab's canvas.
    /// </summary>
    void DisplayRecommendedAction(GameObject plantPrefab, string recommendedAction)
    {
        var imageComponent = plantPrefab.GetComponentInChildren<UnityEngine.UI.RawImage>();

        imageComponent.enabled = true; // Make sure the image is visible
        
        if (plantPrefab.tag == "ripe")
        {
            imageComponent.texture = harvestIcon;
        }
        else if (plantPrefab.tag == "empty")
        {
            imageComponent.texture = seedIcon;
        }
        else if (recommendedAction == "water")
        {
            imageComponent.texture = waterIcon;
        }
        else if (recommendedAction == "fertilize")
        {
            imageComponent.texture = fertilizeIcon;
        }
        else if (recommendedAction == "")
        {
            imageComponent.enabled = false; // Hide the image if no action is recommended
        }
        else
        {
            Debug.LogWarning("Unknown recommended action: " + recommendedAction);
            imageComponent.enabled = false; // Hide the image if the action is unknown
        }
    }
}
