class E_Puck : public Robot
{
    // IP and Buffersize load from Config
    std::string caren_ip_address;
    int read_buffer_size;
    // Ports loaded from the Config
    int arm_port_rcv;
    int arm_port_snd;
    int head_port_rcv;
    int head_port_snd;
    int cam_port_snd;

    std::map<std::string, std::string> configMap;
    std::map<std::string, std::vector<webots::Motor*>> motorMap;
    std::map<std::string, webots::Camera*> cameraMap;
    std::unique_ptr<ComLooper> comThread;

private:
    void initFromConfig();

    void sendCurrentMotorStatus();

    void readAndApplyMotorCommands();

    void sendCameraPictures();

    cv::Mat getCameraPicture(webots::Camera* cam);

    std::map<std::string, std::string> readConfiguration(std::string configFilePath);

public:
    E_Puck(std::string
           configFilePath) 
    {
        std::cout << "Create TCP_Caren_Controller with ConfigFile: " << configFilePath << std::endl;

        configMap = readConfiguration(configFilePath);
        //Create the Communication Thread
        comThread = std::make_unique<ComLooper>();

        auto camCenter = getCamera("camera_center");
        int camTimeStep = 4 * (int)this->getBasicTimeStep();
        camCenter->enable(camTimeStep);
    }

    ~E_Puck()
    {
        if (comThread->isRunning())
        {
            comThread->stop();
            comThread = nullptr;
        }
    }

    void run();
};
