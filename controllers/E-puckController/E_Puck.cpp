#include "E_Puck.h"
#include <map>

void E_Puck::run()
{
    std::cout << "RUN! >CAREN TCP Controller< RUN!" << std::endl;

    initFromConfig();

    int timeStep = (int)this->getBasicTimeStep();

    comThread->run();

    while (this->step(timeStep) != -1)
    {
        readAndApplyMotorCommands();

        sendCurrentMotorStatus();

        sendCameraPictures();
    }

    comThread->stop();
    comThread = nullptr;

}


void E_Puck::initFromConfig()
{
    std::cout << "RUN! >CAREN TCP Controller< RUN!" << std::endl;
}

void E_Puck::sendCurrentMotorStatus()
{
    std::cout << "RUN! >CAREN TCP Controller< RUN!" << std::endl;
}

void E_Puck::readAndApplyMotorCommands()
{
    std::cout << "RUN! >CAREN TCP Controller< RUN!" << std::endl;
}

void E_Puck::sendCameraPictures();
{
    std::cout << "RUN! >CAREN TCP Controller< RUN!" << std::endl;
}

cv::Mat E_Puck::getCameraPicture(webots::Camera* cam)
{
    std::cout << "RUN! >CAREN TCP Controller< RUN!" << std::endl;
}

std::map<std::string, std::string> E_Puck::readConfiguration(std::string configFilePath)
{
    std::cout << "RUN! >CAREN TCP Controller< RUN!" << std::endl;
}