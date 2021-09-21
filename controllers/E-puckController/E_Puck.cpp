#include <webots/Robot.hpp>
#include <webots/DistanceSensor.hpp>
#include <webots/PositionSensor.hpp>
#include <webots/Motor.hpp>
#include <webots/Camera.hpp>
#include <webots/Receiver.hpp>
#include <webots/Emitter.hpp>
#include <webots/LED.hpp>
#include <opencv4/opencv2/core/core.hpp>
#include <fstream>
#include <iostream>
#include <map>
using namespace webots;
#include "utilities.h"

#include "tcp_communication_looper.h"
#include "E_Puck.h"
#include "MovementAttractor.cpp"

void E_Puck::update()
{
    readSensorValues();
    
    ComThreadUpdate();

    applyMotorCommands();
}

void E_Puck::ComThreadUpdate()
{
///////////////////////////////////sendToCedar////////////////////////////////////////////////
// send camera picture
    for (auto const& [identifier, camera] : cameraMap)
    {
        if (comThread->doesWriteSocketExist(identifier))
        {
            comThread->setWriteMatrix(identifier, sensordata.cameraMat);
        }
    }

    // send receiver readings
    for (auto const& [identifier, receiver] : recMap)
    {
        if (comThread->doesWriteSocketExist(identifier))
        {
            comThread->setWriteMatrix(identifier, sensordata.receiverMat);
        }
    }
 
//////////////////////////////////receiveFromCedar/////////////////////////////////////////////////////
    for (auto const& [identifier, motors] : motorMap)
    {
        if (comThread->doesReadSocketExist(identifier))
        {
            cv::Mat commandMatrix = comThread->getReadCommandMatrix(identifier);
            if (commandMatrix.rows == 1)
            {
                for (std::vector<webots::Motor*>::size_type i = 0; i < motors.size(); i++)
                {
                    cedardata.motorMat = commandMatrix;
                }
            }
            else{cedardata.motorMat = cv::Mat::zeros(1,1,CV_32F);}
        }
    }
    
    if (comThread->doesReadSocketExist("break"))
    {
      cv::Mat commandMatrix = comThread->getReadCommandMatrix("break");
      if (commandMatrix.rows == 1)
      {
        cedardata.breakMat = commandMatrix;
      }
      else{cedardata.breakMat = cv::Mat::zeros(1,1,CV_32F);}
    }
    
    for (auto const& [identifier, LEDs] : LEDMap)
    {
      if (comThread->doesReadSocketExist(identifier))
      {
        cv::Mat commandMatrix = comThread->getReadCommandMatrix(identifier);
        if (commandMatrix.rows == 4)
        {
          for (std::vector<webots::LED*>::size_type i = 0; i < LEDs.size(); i++)
          {
            cedardata.LEDMat = commandMatrix;
          }
        }
        else{cedardata.LEDMat = cv::Mat::zeros(8,1,CV_32F);}
       }
      }
}



void E_Puck::readSensorValues()
{
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
    sensordata.cameraMat = cameraPicture;
    
    // read distance sensor value
    std::vector<float> sensorReadings;
    for (auto const& [identifier, sensor] : sensorMap)
    {
      for (std::vector<webots::DistanceSensor*>::size_type i=0; i < sensor.size(); i++)
      {
        sensorReadings.push_back(sensor[i]->getValue());
      }
    }
    transform2Distance(sensorReadings);
    for (int i=0; i<8; i++)
    {
      sensordata.psMat.at<float>(i) = sensorReadings[i];
    }
    

    // read receiver value
    for (auto const& [identifier, receiver] : recMap)
    {
        sensordata.receiverMat = cv::Mat::zeros(10,1,CV_32F);
        if (receiver->getQueueLength() > 0)
        {
          std::string packet((const char *)receiver->getData());
          float pitch(std::stof(packet));
          sensordata.receiverMat.at<float>((int)pitch) = 1.;
          receiver->nextPacket();
        }
        std::cout << sensordata.receiverMat << std::endl;
    }
}

void E_Puck::applyMotorCommands()
{
    int width = 0;
    float fov = 0;
    for (auto const& [identifier, camera] : cameraMap)
    {
        width = camera->getWidth();
        fov = camera->getFov();
    }
    
    float psi_target = ((float)width / 2 - cedardata.motorMat.at<float>(0)) * 2 * fov / width;
    float v[2] = {0, 0};
    
    if (cedardata.breakMat.at<float>(0) >= 0.75)
    {
      v[0] = 0;
      v[1] =0;
    }
    else if (cedardata.breakMat.at<float>(0) < 0.75)
    {
      MovementAttractor(E_Puck::sensordata.psMat, psi_target, v);
    }
    
    for (auto const& [identifier, motor] : motorMap)
    {
      for (std::vector<webots::DistanceSensor*>::size_type i=0; i<motor.size(); i++)
      {
        motor[i]->setPosition(INFINITY);
        motor[i]->setVelocity(v[i]);
      }
    }
    
    for (auto const& [identifier, led] : LEDMap)
    {
      for (std::vector<webots::LED*>::size_type i=0; i<led.size()/2; i++)
      {
        led[2*i]->set(cedardata.LEDMat.at<float>(i) >= 0.75);
        led[2*i+1]->set(cedardata.LEDMat.at<float>(i) >= 0.75);
      }
    }
}

void E_Puck::initFromConfig()
{
    // init LEDs
        std::cout << "Initialize LEDs!" << std::endl;
        // get sensors from webots
        std::vector<webots::LED*> LEDs;
        LEDs.push_back(getLED("led0"));
        LEDs.push_back(getLED("led1"));
        LEDs.push_back(getLED("led2"));
        LEDs.push_back(getLED("led3"));
        LEDs.push_back(getLED("led4"));
        LEDs.push_back(getLED("led5"));
        LEDs.push_back(getLED("led6"));
        LEDs.push_back(getLED("led7"));
        
        std::string LEDIdentifier = "LED";
        LEDMap[LEDIdentifier] = LEDs;
        if (configMap.find("LED_port_rcv") != configMap.end())
        {
            comThread->addReadSocket(LEDIdentifier, std::stoi(configMap["LED_port_rcv"]), std::stoi(configMap["read_buffer_size"]));
        }
        
    // init distance Sensors
        std::cout << "Initialize distance Sensors!" << std::endl;
        // get LEDs from webots
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
        for (auto const& [identifier, sensor] : sensorMap)
        {
          for (std::vector<webots::DistanceSensor*>::size_type i=0; i < sensor.size(); i++)
          {
            sensor[i]->enable(this->getBasicTimeStep());
          }
        }

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
        if (configMap.find("break_port_rcv") != configMap.end())
        {
          comThread->addReadSocket("break", std::stoi(configMap["break_port_rcv"]), std::stoi(configMap["read_buffer_size"]));
        }

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
        for (auto const& [identifier, cam] : cameraMap)
        {
          cam->enable(this->getBasicTimeStep());
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
        for (auto const& [identifier, rec] : recMap)
        {
          rec->setChannel(2);
          rec->enable(this->getBasicTimeStep());
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
