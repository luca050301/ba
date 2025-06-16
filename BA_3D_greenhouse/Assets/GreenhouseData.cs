/// <summary>
/// GreenhouseData is a class that represents data coming from grafana, namely the data of the plants and the robot.
/// It contains an array of Plant objects and a RobotData object.
/// </summary>
class GreenhouseData
{

    public Plant[] series;
    public RobotData robot;

    /// <summary>
    /// Plants are represented by the Plant class, which contains the plant ID, age, and recommended action.
    /// /// </summary>
    [System.Serializable]
    public class Plant
    {
        public string plant_id;
        public string age;
        public string recommended_action;
    }

    /// <summary>
    /// RobotData is a class that represents the robot's data: the time of the last action, the action itself, and the position of the robot.
    /// </summary>
    [System.Serializable]
    public class RobotData
    {
        public string time;
        public string action;
        public string position;
    }
}

