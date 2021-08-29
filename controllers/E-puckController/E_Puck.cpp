#include <webots/Robot.hpp>
#include <webots/DistanceSensor.hpp>
#include <webots/PositionSensor.hpp>
#include <webots/Motor.hpp>
#include <webots/Camera.hpp>
#include <webots/Receiver.hpp>
#include <webots/Emitter.hpp>
#include <opencv4/opencv2/core/core.hpp>
#include <fstream>
#include <iostream>
#include <map>
using namespace webots;
#include "utilities.h"

#include "tcp_communication_looper.h"
#include "E_Puck.h"


void E_Puck::update()
{
    //auto SensorValues = readSensorValues();
    
    //sendToCedar(SensorValues);

    //auto MotorSurface = receiveFromCedar();

    //auto MotorCommands = getMotorCommands(MotorSurface);

    //applyMotorCommands(MotorCommands);
    for (auto const& [identifier, motors] : motorMap)
    {
        for (std::vector<webots::Motor*>::size_type i = 0; i < motors.size(); i++)
          {
             motors[i]->setPosition(INFINITY);
             motors[i]->setVelocity(3.14);
          }
    }
}

void E_Puck::sendToCedar(auto SensorValues)
{
    // send camera picture
    for (auto const& [identifier, camera] : cameraMap)
    {
        if (comThread->doesWriteSocketExist(identifier))
        {
            comThread->setWriteMatrix(identifier, SensorValues.cameraPicture);
        }
    }

    // send receiver readings
    for (auto const& [identifier, receiver] : recMap)
    {
        if (comThread->doesWriteSocketExist(identifier))
        {
            comThread->setWriteMatrix(identifier, SensorValues.receiverReading);
        }
    }

    // send sensor readings
    for (auto const& [identifier, sensor] : sensorMap)
    {
        if (comThread->doesWriteSocketExist(identifier))
        {
            comThread->setWriteMatrix(identifier, SensorValues.sensorReadings);
        }
    }

    // send wheel position readings
    for (auto const& [identifier, wheelsensor] : wheelsensorMap)
    {
        if (comThread->doesWriteSocketExist(identifier))
        {
            comThread->setWriteMatrix(identifier, SensorValues.wheelPosition);
        }
    }
}

auto E_Puck::receiveFromCedar()
{
    struct MotorSurface
    {
        cv::Mat motorAttractor;
        float LEDCommand;
    };

    cv::Mat motorAttractor;
    for (auto const& [identifier, motors] : motorMap)
    {
        if (comThread->doesReadSocketExist(identifier))
        {
            cv::Mat commandMatrix = comThread->getReadCommandMatrix(identifier);
            if (commandMatrix.rows == 1)
            {
                for (std::vector<webots::Motor*>::size_type i = 0; i < motors.size(); i++)
                {
                    motorAttractor = commandMatrix;
                }
            }
            else if (comThread->isReadSocketConnected(identifier) && commandMatrix.rows != 42) //I know this is kinda random, but I cannot init a Matrix with -1 and I also want to make sure that serializing went okay
            {
                std::cout << "Trying to get: " << identifier << "attractor, but read a Matrix with " << commandMatrix.rows << " entries and we have only " << 1 << " attracor." << std::endl;
            }
        }
    }
    float LEDCommand=0;

    MotorSurface return_value{motorAttractor, LEDCommand};

    return return_value;
}

auto E_Puck::readSensorValues()
{
    struct SensorValues
    {
        std::vector<float> wheelPosition;
        std::vector<float> sensorReadings;
        const void* receiverReading;
        cv::Mat cameraPicture;
    };

    // read camera picture
    cv::Mat cameraPicture;
    for (auto const& [identifier, cam] : cameraMap)
    {
        int from_to[] =
        { 0, 0, 1, 1, 2, 2 }; // for mat conversion

        cv::Mat pictureMat(cam->getHeight(), cam->getWidth(), CV_8UC4,
            const_cast<unsigned char*>(cam->getImage()));
        cameraPicture = cv::Mat(cam->getHeight(), cam->getWidth(), CV_8UC3);
        cv::mixChannels(&pictureMat, 1, &cameraPicture, 1, from_to, 3); // kill the alpha channel
    }

    // read receiver value
    const void* receiverReading;
    for (auto const& [identifier, receiver] : recMap)
    {
        receiverReading = receiver->getData();
        receiver->nextPacket();
    }

    // read distance sensor value
    std::vector<float> sensorReadings;
    for (auto const& [identifier, sensor] : sensorMap)
    {
      for (std::vector<webots::DistanceSensor*>::size_type i=0; i < sensor.size(); i++)
      {
        sensorReadings.push_back(sensor[i]->getValue());
      }
    }

    //read wheel position value
    std::vector<float> wheelPosition;
    for (auto const& [identifier, sensor] : wheelsensorMap)
    {
      for (std::vector<webots::PositionSensor*>::size_type i=0; i< sensor.size(); i++)
      {
        wheelPosition.push_back(sensor[i]->getValue());
      }
    }

    SensorValues return_values{wheelPosition, sensorReadings, receiverReading, cameraPicture}; 

    return return_values;
}

auto E_Puck::getMotorCommands(auto MotorSurface)
{
    struct MotorCommands
    {
        float psi_target;
    };
    int width;
    float fov;
    for (auto const& [identifier, camera] : cameraMap)
    {
        width = camera->getWidth();
        fov = camera->getFov();
    }
    float psi_target = (width / 2 - MotorSurface.motorAttractor) * 2 * fov / width;

    return MotorCommands(psi_target);
}

void E_Puck::applyMotorCommands(auto MotorCommands)
{
    float v[2] = MovementAttractor(MotorCommands.psi_target);
    //wb_motor_set_velocity(obj.left_motor, vL);
    //wb_motor_set_velocity(obj.right_motor, vR);
}

void E_Puck::initFromConfig()
{
    // init distance sensors
        std::cout << "Initialize distance Sensors!" << std::endl;
        // get sensors from webots
        std::vector<webots::DistanceSensor*> distance_sensors;
        distance_sensors.push_back(getDistanceSensor("ps0"));
        distance_sensors.push_back(getDistanceSensor("ps1"));
        distance_sensors.push_back(getDistanceSensor("ps2"));
        distance_sensors.push_back(getDistanceSensor("ps3"));
        distance_sensors.push_back(getDistanceSensor("ps4"));
        distance_sensors.push_back(getDistanceSensor("ps5"));
        distance_sensors.push_back(getDistanceSensor("ps6"));
        distance_sensors.push_back(getDistanceSensor("ps7"));
        // add to sensor map
        std::string SensorIdentifier = "distance_sensors";
        sensorMap[SensorIdentifier] = distance_sensors;


    // init motors 
        std::cout << "Initialize Motors!" << std::endl;
        // get motors from webots
        std::vector<webots::Motor*> motors;
        motors.push_back(getMotor("left wheel motor"));
        motors.push_back(getMotor("right wheel motor"));
        // add to motor map
        std::string MotorIdentifier = "motors";
        motorMap[MotorIdentifier] = motors;
        // add read socket
        if (configMap.find("motor_port_rcv") != configMap.end())
        {
            comThread->addReadSocket(MotorIdentifier, std::stoi(configMap["motor_port_rcv"]), std::stoi(configMap["read_buffer_size"]));
        }
        // get motor sensors from webots
        std::vector<webots::PositionSensor*> motorsensors;
        motorsensors.push_back(getPositionSensor("left wheel sensor"));
        motorsensors.push_back(getPositionSensor("right wheel sensor"));
        // add to motor sensor map
        std::string WheelSensorIdentifier = "wheelsensors";
        wheelsensorMap[WheelSensorIdentifier] = motorsensors;


    // init camera
        std::cout << "Initialize Camera!" << std::endl;
        // get camera from webots and add to camera map
        std::string cameraIdentifier = "camera";
        cameraMap[cameraIdentifier] = getCamera("camera");
        // add write socket
        if (configMap.find("camera_port_snd") != configMap.end())
        {
            comThread->addWriteSocket(cameraIdentifier, std::stoi(configMap["camera_port_snd"]), configMap["cedar_ip"]);
        }


    // init microphone -> microphone in webots is modeled with emitter and receiver
        std::cout << "Initialize Microphone!" << std::endl;
        // get receiver from webots and add to receiver map
        std::string micIdentifier = "receiver";
        recMap[micIdentifier] = getReceiver("receiver");
        // add write socket
        if (configMap.find("mic_port_snd") != configMap.end())
        {
            comThread->addWriteSocket(micIdentifier, std::stoi(configMap["mic_port_snd"]), configMap["cedar_ip"]);
        }
        // get emitter from webots and add to emitter map
        std::string emIdentifier = "emitter";
        emMap[emIdentifier] = getEmitter("emitter");
}

std::map<std::string, std::string> E_Puck::readConfiguration(std::string configFilePath)
{
    std::map<std::string, std::string> cMap;

    std::ifstream config_file(configFilePath);

    if (config_file.is_open())
    {
        std::string line;
        std::cout << "Read from Config:" << std::endl;
        while (std::getline(config_file, line))
        {
            if (line[0] != '#')
            {
                std::vector<std::string> tokens;
                split(line, ":", tokens);
                if (tokens.size() == 2)
                {
                    std::cout << "\t" << tokens[0] << " >> " << tokens[1] << std::endl;
                    cMap[tokens[0]] = tokens[1];
                }
                else
                {
                    std::cout << "Your Config File seems to be faulty. Each line should look like this >>identifier:value<< . Faulty line: " << line
                        << std::endl;
                }
            }
        }
    }
    else
    {
        std::cout << "ERROR! Could not open config file: " << configFilePath << std::endl;
    }

    config_file.close();


    return cMap;
}
