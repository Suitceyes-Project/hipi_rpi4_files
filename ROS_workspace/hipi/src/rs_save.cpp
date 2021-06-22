#include <ros/ros.h>
#include <sensor_msgs/Image.h>
#include <std_msgs/String.h>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgcodecs.hpp>
#include <cv_bridge/cv_bridge.h>
#include <iostream>
#include <iomanip>
#include <ctime>
#include <chrono>
#include <stdio.h>


//std::string timestamp();
void timestamp();

char mbstr[24];

void imageCallback(const sensor_msgs::ImageConstPtr& msg)
{
   try
   {
  	//cv::imshow("viewImage", cv_bridge::toCvShare(msg, "bgr8")->image);
  	timestamp();
    std::string rgb_image = "/home/leedssc/save_folder/rgb_" + std::string(mbstr) + ".jpg";
    //cv::imwrite(rgb_image);
  	cv::imwrite(rgb_image, cv_bridge::toCvShare(msg, "bgr8")->image);
   	//cv::waitKey(30);
   }
   catch (cv_bridge::Exception& e)
   {
  	ROS_ERROR("Could not convert from '%s' to 'bgr8'.", msg->encoding.c_str());
   }
}


void depthCallback(const sensor_msgs::ImageConstPtr& msg)
{
   try
   {
    std::string depth_image = "/home/leedssc/save_folder/depth_reg_" + std::string(mbstr) + ".png";
    //cv::imwrite(depth_image);
  	cv::imwrite(depth_image, cv_bridge::toCvShare(msg, "16UC1")->image);
  	//cv::imshow("viewDepth", cv_bridge::toCvShare(msg, "16UC1")->image);
   	//cv::waitKey(30);
   }
   catch (cv_bridge::Exception& e)
   {
  	ROS_ERROR("Could not convert from '%s' to '16UC1'.", msg->encoding.c_str());
   }
}


//std::string timestamp()
void timestamp()
{
    std::time_t t = std::time(nullptr);
    //std::cout << "UTC:   " << std::put_time(std::gmtime(&t), "%c %Z") << '\n';
    
    
    std::chrono::system_clock::time_point t2 = std::chrono::system_clock::now();
    const std::chrono::duration<double> tse = t2.time_since_epoch();
    std::chrono::seconds::rep milliseconds = std::chrono::duration_cast<std::chrono::milliseconds>(tse).count() % 1000000;
    //std::cout << milliseconds << '\n';
    
    
    if (std::strftime(mbstr, sizeof(mbstr), "%d_%m_%y_%H_%M_%S_", std::gmtime(&t))) {
        //std::cout << mbstr << '\n';
    }
    
    char  buf[6];
    
    sprintf(buf, "%ld", milliseconds);
    //td::cout << buf<< '\n';
    for (int i=18; i<=23; i++) {
        mbstr[i] = buf[i-18];
    }
    
    std::cout << mbstr << '\n';
}

int main(int argc, char **argv)
{
	ros::init(argc, argv, "rs_save");
	ros::NodeHandle nh;
	ros::Rate loop_rate(1);
	//cv::namedWindow("viewImage");
	//cv::namedWindow("viewDepth");
	ros::Publisher tstamp_pub = nh.advertise<std_msgs::String>("tstamp", 50);
	 
    ros::Subscriber image_sub = nh.subscribe("/camera/color/image_raw_t", 1, imageCallback);
	ros::Subscriber depth_sub = nh.subscribe("/camera/depth/image_rect_raw_t", 1, depthCallback);
	
	while (ros::ok())
    {
    
        std_msgs::String msg;
        msg.data = std::string(mbstr);
        tstamp_pub.publish(msg);
        ros::spinOnce();
        loop_rate.sleep();
    }
	//ros::spin();
	
	//cv::destroyWindow("viewImage");
	//cv::destroyWindow("viewDepth");
	
	return 0;
}
