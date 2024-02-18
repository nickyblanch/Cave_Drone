/////////////////////////////////////////////////////////////////////////////////////////
//      AUTHOR: Nicolas Blanchard | nickyblanch@arizona.edu | 5208343191
//        INFO: This code is written as part of my master's thesis project advisted by
//              professor Sergey Shkarayev and Abhijit Mahalanobis at the University
//              of Arizona.
//        DATE: Fall 2023
// DESCRIPTION: This code accepts odometry data from the Modalai SEEKER drone and
//              broadcasts a TF using that data.
/////////////////////////////////////////////////////////////////////////////////////////


/////////////////////////////////////////////////////////////////////////////////////////
// DEPENDENCIES
/////////////////////////////////////////////////////////////////////////////////////////


#include <ros/ros.h>
#include <tf/transform_broadcaster.h>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2_ros/transform_broadcaster.h>
#include <geometry_msgs/TransformStamped.h>
#include <nav_msgs/Odometry.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl_conversions/pcl_conversions.h>
#include <sensor_msgs/PointCloud2.h>
#include <tf2_ros/static_transform_broadcaster.h>
#include <cstdio>
#include <vector>
#include <cmath>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.h>
#include <sensor_msgs/image_encodings.h>
#include <vision_msgs/Detection2DArray.h>
#include <vision_msgs/Detection2D.h>
#include <vision_msgs/BoundingBox2D.h>


/////////////////////////////////////////////////////////////////////////////////////////
// GLOBAL VARIABLES
/////////////////////////////////////////////////////////////////////////////////////////


std::string map_frame = "map";
std::string final_frame = "final";
// ros::Time start_time = ros::Time::now();


/////////////////////////////////////////////////////////////////////////////////////////
// CALLBACK FUNCTION
/////////////////////////////////////////////////////////////////////////////////////////


// SUBSCRIBES TO:
// PUBLISHES:     tf base_link -> cam_frame
//                tf final -> NED
void static_broadcaster(void) {

    // SETUP ////////////////////////////////////////////////////////////////////////////////
    static tf2_ros::StaticTransformBroadcaster static_broadcaster;
    geometry_msgs::TransformStamped static_transformStamped;
    geometry_msgs::TransformStamped static_transformStamped_NED;

    // HEADER TIMESTAMP AND TF FRAMES ///////////////////////////////////////////////////////
    // static_transformStamped.header.stamp = ros::Time::now();
    static_transformStamped.header.stamp.sec = 0;
    static_transformStamped.header.stamp.nsec = 0;
    static_transformStamped.header.frame_id = "cam_frame";
    static_transformStamped.child_frame_id = "base_link";

    static_transformStamped_NED.header.stamp.sec = 0;
    static_transformStamped_NED.header.stamp.nsec = 0;
    static_transformStamped_NED.header.frame_id = "final";
    static_transformStamped_NED.child_frame_id = "NED";

    // TRANSLATION; NO TRANSLATION //////////////////////////////////////////////////////////
    static_transformStamped.transform.translation.x = 0;
    static_transformStamped.transform.translation.y = 0;
    static_transformStamped.transform.translation.z = 0;

    static_transformStamped_NED.transform.translation.x = 0;
    static_transformStamped_NED.transform.translation.y = 0;
    static_transformStamped_NED.transform.translation.z = 0;
    
    // ORIENTATION //////////////////////////////////////////////////////////////////////////
    // See ModalAI VOXL SEEKER CAM V1 extrinsics for more information on the relationship
    // between the ToF and the VIO coordinate frames. Essentially, the yaw axes are offset
    // by 180 degrees (1 pi rads).
    tf2::Quaternion quat;
    quat.setRPY(0, 0, 3.14);
    quat.normalize();
    static_transformStamped.transform.rotation.x = quat.x();
    static_transformStamped.transform.rotation.y = quat.y();
    static_transformStamped.transform.rotation.z = quat.z();
    static_transformStamped.transform.rotation.w = quat.w();

    // Now, we need a transform from the inertial frame to a more common NED frame.
    static_transformStamped_NED.transform.rotation.x = -0.5;
    static_transformStamped_NED.transform.rotation.y = 0.5;
    static_transformStamped_NED.transform.rotation.z = 0.5;
    static_transformStamped_NED.transform.rotation.w = 0.5;

    // SEND //////////////////////////////////////////////////////////////////////////////////
    static_broadcaster.sendTransform(static_transformStamped);
    static_broadcaster.sendTransform(static_transformStamped_NED);
}


// SUBSCRIBES TO: 
// PUBLISHES:     tf base_link -> map_frame
void poseCallback(const nav_msgs::Odometry::ConstPtr& msg) {

    // RETRIEVE POSE DATA ///////////////////////////////////////////////////////////////////
    float x = msg->pose.pose.position.x;
    float y = msg->pose.pose.position.y;
    float z = msg->pose.pose.position.z;
    float x_o = msg->pose.pose.orientation.x;
    float y_o = msg->pose.pose.orientation.y;
    float z_o = msg->pose.pose.orientation.z;
    float w_o = msg->pose.pose.orientation.w;

    // TRANSFORM HANDLERS ////////////////////////////////////////////////////////////////////
    static tf2_ros::TransformBroadcaster br;
    geometry_msgs::TransformStamped transform;
    geometry_msgs::TransformStamped transform_translation;

    // FIRST (FIXED) ROTATION ////////////////////////////////////////////////////////////////
    tf2::Quaternion quat;
    // quat.setRPY(0, 0, -3.14);
    quat.setRPY(0, 0, 0);
    // quat.normalize();

    // NEW (MOVING) ROTATION /////////////////////////////////////////////////////////////////
    tf2::Quaternion q(-1.0 * x_o, -1.0 * y_o, -1.0 * z_o, 1.0 * w_o);

    // DEBUG /////////////////////////////////////////////////////////////////////////////////
    tf2::Matrix3x3 m(q);
    double roll, pitch, yaw;
    m.getRPY(roll, pitch, yaw);
    ROS_INFO("YAW: [%f], PITCH: [%f], ROLL: ]%f],", yaw*57.3, pitch*57.3, roll*57.3);
    // q.setRPY(-1.0 * roll, -1.0 * pitch, -1.0 * yaw);
    q.normalize();

    // MULTIPLy ROTATIONS TOGETHER ////////////////////////////////////////////////////////////
    // q = quat*q;
    q.normalize();

    // SEND TRANSFORM /////////////////////////////////////////////////////////////////////////
    // transform.header.stamp = ros::Time::now();
    transform.header.stamp = msg->header.stamp;
    transform.header.frame_id = "base_link";
    transform.child_frame_id = map_frame;
    // transform.transform.translation.x = -1.0 * x;
    // transform.transform.translation.y = -1.0 * y;
    // transform.transform.translation.z = -1.0 * z;
    transform.transform.translation.x = 0 * x;
    transform.transform.translation.y = 0 * y;
    transform.transform.translation.z = 0 * z;
    transform.transform.rotation.x = q.x();
    transform.transform.rotation.y = q.y();
    transform.transform.rotation.z = q.z();
    transform.transform.rotation.w = q.w();
    br.sendTransform(transform);

    transform_translation.header.stamp = msg->header.stamp;
    transform_translation.header.frame_id = map_frame;
    transform_translation.child_frame_id = final_frame;
    transform_translation.transform.translation.x = -1.0 * x;
    transform_translation.transform.translation.y = -1.0 * y;
    transform_translation.transform.translation.z = -1.0 * z;
    // transform_translation.transform.translation.x = 0 * x;
    // transform_translation.transform.translation.y = 0 * y;
    // transform_translation.transform.translation.z = 0 * z;
    transform_translation.transform.rotation.x = 0;
    transform_translation.transform.rotation.y = 0;
    transform_translation.transform.rotation.z = 0;
    transform_translation.transform.rotation.w = 1;
    br.sendTransform(transform_translation);

}

// SUBSCRIBES TO: /tof_pc
// PUBLISHES:     /restamped_pc
class pc_subscribe_and_publish {
    public:
        pc_subscribe_and_publish() {

            // TOPIC WE ARE SUBSCRIBING TO //////////////////////////////////////////////////////////
            sub = node.subscribe("/tof_pc", 10, &pc_subscribe_and_publish::pc_callback, this);

            // TOPIC WE ARE PUBLISHING //////////////////////////////////////////////////////////////
            pub = node.advertise<sensor_msgs::PointCloud2>("/restamped_pc", 100);

        }
        void pc_callback(const sensor_msgs::PointCloud2ConstPtr& msg) {

            // KEEP ALL DATA THE SAME, ONLY CHANGE TIMESTAMP ////////////////////////////////////////
            sensor_msgs::PointCloud2 msg_out;
            msg_out.header = std_msgs::Header();
            msg_out.header.frame_id = "cam_frame";
            // msg_out.header.stamp = ros::Time::now();
            msg_out.header.stamp = msg->header.stamp;
            msg_out.height = msg->height;
            msg_out.width = msg->width;
            msg_out.fields = msg->fields;
            msg_out.is_bigendian = msg->is_bigendian;
            msg_out.point_step = msg->point_step;
            msg_out.row_step = msg->row_step;
            msg_out.data = msg->data;
            msg_out.is_dense = msg->is_dense;
            pub.publish(msg_out);
        }
    private:
        ros::NodeHandle node;
        ros::Publisher pub;
        ros::Subscriber sub;
};


// SUBSCRIBES TO: /qvio/odometry
// PUBLISHES:     /rotated_odom
class odom_subscribe_and_publish {
    public:
        odom_subscribe_and_publish() {

            // TOPIC WE ARE SUBSCRIBING TO //////////////////////////////////////////////////////////
            sub = node.subscribe("/qvio/odometry", 10, &odom_subscribe_and_publish::odom_callback, this);

            // TOPIC WE ARE PUBLISHING //////////////////////////////////////////////////////////////
            pub = node.advertise<nav_msgs::Odometry>("/rotated_odom", 100);

        }
        void odom_callback(const nav_msgs::OdometryConstPtr& msg) {
            
            // CURRENTLY, ODOMETRY IS NOT ROTATED, AND IS OUTPUT WITH NO CHANGES ////////////////////
            // (BUT TO CHANGE TO A STANDED NORTH EAST DOWN FRAME, THE ODOMETRY COULD BE ROTATED HERE)
            nav_msgs::Odometry msg_out;
            msg_out.header = std_msgs::Header();
            msg_out.header.frame_id = "map";

            // msg_out.header.stamp = ros::Time::now();
            msg_out.header.stamp = msg->header.stamp;
            msg_out.twist = msg->twist;
            msg_out.pose.pose.position.x = msg->pose.pose.position.x;
            msg_out.pose.pose.position.y = msg->pose.pose.position.y;
            msg_out.pose.pose.position.z = msg->pose.pose.position.z;

            tf2::Quaternion odom_quat(msg->pose.pose.orientation.x, msg->pose.pose.orientation.y, msg->pose.pose.orientation.z, msg->pose.pose.orientation.w);
            odom_quat.normalize();
            
            geometry_msgs::Quaternion final_quat = tf2::toMsg(odom_quat);
            msg_out.pose.pose.orientation = final_quat;

            pub.publish(msg_out);
        }
    private:
        ros::NodeHandle node;
        ros::Publisher pub;
        ros::Subscriber sub;
};


// SUBSCRIBES TO: /stereo/right
// PUBLISHES:     /rgb
class im_subscribe_and_publish {
    public:
        im_subscribe_and_publish() {

            // TOPIC WE ARE SUBSCRIBING TO //////////////////////////////////////////////////////////
            sub = node.subscribe("/stereo/right", 1, &im_subscribe_and_publish::im_callback, this);

            // TOPIC WE ARE PUBLISHING //////////////////////////////////////////////////////////////
            pub = node.advertise<sensor_msgs::Image>("/rgb", 1);

        }
        void im_callback(const sensor_msgs::ImageConstPtr& msg) {

            // CREATE 3 CHANNEL IMAGE FROM 1 CHANNEL IMAGE //////////////////////////////////////////
            sensor_msgs::Image msg_out;
            msg_out.header = msg->header;
            msg_out.height = msg->height;
            msg_out.width = msg->width;
            msg_out.encoding = sensor_msgs::image_encodings::RGB8;
            msg_out.is_bigendian = msg->is_bigendian;
            msg_out.step = msg->step * 3;

            std::vector<unsigned char> new_data;
            unsigned char temp_val = 0;

            for(unsigned int i = 0; i < 921600; i++) {
                if (i % 3 == 0) {
                    temp_val = msg->data[int(i / 3)];
                }
                new_data.push_back(temp_val);
            }

            msg_out.data = new_data;
            pub.publish(msg_out);

            ROS_INFO_STREAM(" INPUT IMAGE SIZE: " << msg->data.size() << '\n');
            ROS_INFO_STREAM("OUTPUT IMAGE SIZE: " << new_data.size() << '\n');
        }
    private:
        ros::NodeHandle node;
        ros::Publisher pub;
        ros::Subscriber sub;
};


// SUBSCRIBES TO: /yolov7/yolov7
// PUBLISHES:     /direction
class detection_subscribe_and_publish {
    public:
        detection_subscribe_and_publish() {

            // TOPIC WE ARE SUBSCRIBING TO //////////////////////////////////////////////////////////
            sub = node.subscribe("/yolov7/yolov7", 1, &detection_subscribe_and_publish::detection_callback, this);

            // TOPIC WE ARE PUBLISHING //////////////////////////////////////////////////////////////
            pub = node.advertise<nav_msgs::Odometry>("/direction", 1);

        }
        void detection_callback(const vision_msgs::Detection2DArrayConstPtr& msg) {

            // RETRIEVING BOUNDING BOX LOCATIONS ////////////////////////////////////////////////////
            nav_msgs::Odometry msg_out;
            msg_out.header = msg->header;
            msg_out.header.frame_id = "base_link";
            uint16_t x = 0;
            uint16_t y = 0;

            std::vector<vision_msgs::Detection2D> detec = msg->detections;
            if (detec.size() > 0) {

                vision_msgs::BoundingBox2D box = detec[0].bbox;
                x = box.center.x;
                y = box.center.y;

                ROS_INFO_STREAM("CENTER X: " << x << '\n');
                ROS_INFO_STREAM("CENTER Y: " << y << '\n');
            }

            // CREATING TARGET ORIENTATION ///////////////////////////////////////////////////////////
            // Image size is 640x480
            const uint16_t center_x = 640 / 2;
            const uint16_t center_y = 480 / 2;
            double yaw_angle = atan2(-1.0*(double)(y-center_y), (double)(x-center_x)); // * 180.0 / (2 * 3.15159);

            tf2::Quaternion odom_quat;
            odom_quat.setRPY(0, 0, yaw_angle);
            odom_quat.normalize();
            
            geometry_msgs::Quaternion final_quat = tf2::toMsg(odom_quat);
            msg_out.pose.pose.orientation = final_quat;
            msg_out.pose.pose.position.x = 0;
            msg_out.pose.pose.position.y = 0;
            msg_out.pose.pose.position.z = 0;

            pub.publish(msg_out);

        }
    private:
        ros::NodeHandle node;
        ros::Publisher pub;
        ros::Subscriber sub;
};


/////////////////////////////////////////////////////////////////////////////////////////
// MAIN FUNCTION
/////////////////////////////////////////////////////////////////////////////////////////


int main(int argc, char** argv) {

    // SETUP ////////////////////////////////////////////////////////////////////////////////
    ros::init(argc, argv, "tof_tf_broadcaster");
    ros::NodeHandle node;

    // BASE LINK TF BROADCASTER /////////////////////////////////////////////////////////////
    ros::Subscriber sub = node.subscribe("/rotated_odom", 10, &poseCallback);

    // SENSOR FRAME TF BROADCASTER //////////////////////////////////////////////////////////
    static_broadcaster();

    // PC2 SUBSCRIBER/PUBLISHER /////////////////////////////////////////////////////////////
    pc_subscribe_and_publish sapobject;

    // ODOM SUBSCRIBER/PUBLISHER
    odom_subscribe_and_publish odom_obj;

    // IMAGE SUBSCRIBER/PUBLISHER
    im_subscribe_and_publish im_obj;

    // IMAGE SUBSCRIBER/PUBLISHER
    detection_subscribe_and_publish detec_obj;

    // RUN
    ros::spin();
    return 0;

}