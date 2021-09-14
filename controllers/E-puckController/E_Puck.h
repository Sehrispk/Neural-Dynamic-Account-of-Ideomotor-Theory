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
        cv::Mat wheelMat;
        cv::Mat psMat;
        cv::Mat receiverMat;
        cv::Mat cameraMat;
    };
    struct CedarData
    {
        cv::Mat motorMat;
        float LEDMat;
    };
    struct MotorData
    {
        float psi_targetMat;
    };
    
    // SensorReadings and MotorCommands
    SensorData sensordata;
    CedarData cedardata;
    MotorData motordata;

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
        //Create and start the Communication Thread
        // init from config
        comThread = std::make_unique<ComLooper>();
        initFromConfig();
        comThread->run();
        // init structs
        sensordata = SensorData{cv::Mat::zeros(1,1,CV_32F), cv::Mat::zeros(8,1,CV_32F), cv::Mat::zeros(1,1,CV_32F), cv::Mat::zeros(52, 39, CV_8UC4)};
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
