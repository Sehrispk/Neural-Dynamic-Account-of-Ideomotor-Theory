class E_Puck : public Robot
{
      // IP and Buffersize load from Config
    std::string caren_ip_address;
    int read_buffer_size;
    // Ports loaded from the Config
    int camera_port_snd;
    int mic_port_snd;
    int motor_port_rcv;

    // devices and ComThread
    std::map<std::string, std::string> configMap;
    std::map<std::string, std::vector<webots::Motor*>> motorMap;
    std::map<std::string, std::vector<webots::PositionSensor*>> wheelsensorMap;
    std::map<std::string, webots::Camera*> cameraMap;
    std::map<std::string, std::vector<webots::DistanceSensor*>> sensorMap;
    std::map<std::string, webots::Receiver*> recMap;
    std::map<std::string, webots::Emitter*> emMap;
    std::unique_ptr<ComLooper> comThread;
    
    // Command and Sensor Structs
    struct SensorData
    {
        cv::Mat wheelPosition;
        cv::Mat sensorReadings;
        cv::Mat receiverReading;
        cv::Mat cameraPicture;
    };
    struct CedarData
    {
        cv::Mat motorCommand;
        float LEDCommand;
    };
    struct MotorData
    {
        float psi_target;
    };
    
    // SensorReadings and MotorCommands
    SensorData SensorReadings;
    CedarData MotorSurface;
    MotorData MotorCommands;

private:
    void ComThreadUpdate();
    void initFromConfig();
    void readSensorValues();
    void getMotorCommands();
    void applyMotorCommands();
    std::map<std::string, std::string> readConfiguration(std::string configFilePath);

public:
    E_Puck(std::string
           configFilePath) 
    {
        std::cout << "Create E-Puck with ConfigFile: " << configFilePath << std::endl;
        // read config
        configMap = readConfiguration(configFilePath);
        //Create the Communication Thread
        comThread = std::make_unique<ComLooper>();
        // init from config
        initFromConfig();
    };

    ~E_Puck()
    {
        if (comThread->isRunning())
        {
            comThread->stop();
            comThread = nullptr;
        }
    };

    void update();
};
