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

    // list of plants currently in the scene
    GameObject[] plantPrefabs = null;

    void Start()
    {
        if (robot == null)
        {
            robot = GameObject.Find("robot");
        }
        robotController = robot.GetComponent<RobotController>();

        // tests for development purposes only
#if UNITY_EDITOR
        Receive(
            "{\"series\":[[{\"time\":1749983188297,\"action\":\"water\",\"position\":3}],[{\"age\":\"null\",\"plant_id\":\"1\"},{\"age\":\"2025-03-11 20:35:42.027785\",\"plant_id\":\"10\"},{\"age\":\"2025-05-10 04:26:08.027785\",\"plant_id\":\"11\"},{\"age\":\"2025-06-15 09:35:42.027785\",\"plant_id\":\"12\"},{\"age\":\"2025-03-20 15:35:20.027785\",\"plant_id\":\"13\"},{\"age\":\"2025-03-06 22:09:46.027785\",\"plant_id\":\"14\"},{\"age\":\"2025-04-06 18:16:06.027785\",\"plant_id\":\"15\"},{\"age\":\"2025-05-22 17:08:09.027785\",\"plant_id\":\"16\"},{\"age\":\"2025-05-24 03:30:13.027785\",\"plant_id\":\"17\"},{\"age\":\"2025-05-29 21:15:00.027785\",\"plant_id\":\"18\"},{\"age\":\"2025-02-25 16:45:17.027785\",\"plant_id\":\"19\"},{\"age\":\"2025-04-11 06:00:18.311827\",\"plant_id\":\"2\"},{\"age\":\"2025-03-10 03:19:45.324483\",\"plant_id\":\"3\"},{\"age\":\"2025-06-11 06:34:11.335699\",\"plant_id\":\"4\"},{\"age\":\"2025-03-02 20:35:02.354614\",\"plant_id\":\"5\"},{\"age\":\"2025-05-07 05:56:42.373575\",\"plant_id\":\"6\"},{\"age\":\"2025-03-23 07:31:14.027785\",\"plant_id\":\"7\"},{\"age\":\"2025-03-01 14:39:44.027785\",\"plant_id\":\"8\"},{\"age\":\"2025-06-05 23:04:20.027785\",\"plant_id\":\"9\"}]]}"
        );

        // call receive after 10 secs with param "asd
        Invoke("Test", 10f);
#endif
    }
    // Test method for development purposes only
    void Test()
    {
        Receive(
            "{\"series\":[[{\"time\":1749983188297,\"action\":\"seed\",\"position\":13}],[{\"age\":\"null\",\"plant_id\":\"1\"},{\"age\":\"2025-03-11 20:35:42.027785\",\"plant_id\":\"10\"},{\"age\":\"2025-05-10 04:26:08.027785\",\"plant_id\":\"11\"},{\"age\":\"2025-06-15 09:35:42.027785\",\"plant_id\":\"12\"},{\"age\":\"2025-03-20 15:35:20.027785\",\"plant_id\":\"13\"},{\"age\":\"2025-03-06 22:09:46.027785\",\"plant_id\":\"14\"},{\"age\":\"2025-04-06 18:16:06.027785\",\"plant_id\":\"15\"},{\"age\":\"2025-05-22 17:08:09.027785\",\"plant_id\":\"16\"},{\"age\":\"2025-05-24 03:30:13.027785\",\"plant_id\":\"17\"},{\"age\":\"2025-05-29 21:15:00.027785\",\"plant_id\":\"18\"},{\"age\":\"2025-02-25 16:45:17.027785\",\"plant_id\":\"19\"},{\"age\":\"2025-04-11 06:00:18.311827\",\"plant_id\":\"2\"},{\"age\":\"2025-03-10 03:19:45.324483\",\"plant_id\":\"3\"},{\"age\":\"2025-06-11 06:34:11.335699\",\"plant_id\":\"4\"},{\"age\":\"2025-03-02 20:35:02.354614\",\"plant_id\":\"5\"},{\"age\":\"2025-05-07 05:56:42.373575\",\"plant_id\":\"6\"},{\"age\":\"2025-03-23 07:31:14.027785\",\"plant_id\":\"7\"},{\"age\":\"2025-03-01 14:39:44.027785\",\"plant_id\":\"8\"},{\"age\":\"2025-06-05 23:04:20.027785\",\"plant_id\":\"9\"}]]}"
        );
    }
    /// <summary>
    /// Receives a JSON string parameter, processes it, and updates the plant prefabs and robot actions accordingly.
    /// </summary>
    void Receive(string param)
    {
        Debug.Log("Received parameter: " + param);

        if (string.IsNullOrEmpty(param))
        {
            Debug.LogError("Received empty parameter.");
            return;
        }
        // Format the JSON string to match the expected structure
        if (param.StartsWith("{ \"series\":[[{ \"age\""))
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
                    TimeSpan? ageSpan = plant.age != "null" ? DateTime.Now - DateTime.Parse(plant.age) : null;

                    GameObject plantPrefab = GetPlantPrefabForAge(ageSpan);

                    int plantId = int.Parse(plant.plant_id);

                    // if no plant prefab exists for this plantId, or if the prefab is different, instantiate it
                    if (plantPrefabs[plantId] == null || plantPrefab.tag != plantPrefabs[plantId].tag)
                    {
                        if (plantPrefabs[plantId] != null)
                        {
                            Destroy(plantPrefabs[plantId]); // Destroy the old plant prefab
                        }

                        Vector3 position = new Vector3(plantId % 2 == 0 ? -1 : 1, 0, plantId / 2);
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
        if (plantPrefab.tag == "empty")
        {
            recommendedAction = "seed";
        }
        else if (plantPrefab.tag == "ripe")
        {
            recommendedAction = "harvest";
        }
        // load png from Resources folder

        Texture2D actionIcon = Resources.Load<Texture2D>("Images/" + recommendedAction);

        var imageComponent = plantPrefab.GetComponentInChildren<UnityEngine.UI.RawImage>();

        if (actionIcon == null)
        {
            // make invisible
            imageComponent.enabled = false;
            return;
        }


        imageComponent.texture = actionIcon;
        imageComponent.enabled = true; // Make sure the image is visible
    }
}
