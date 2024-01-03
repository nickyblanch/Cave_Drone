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
#include <tf2/LinearMath/Quaternion.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.h>


/////////////////////////////////////////////////////////////////////////////////////////
// GLOBAL VARIABLES
/////////////////////////////////////////////////////////////////////////////////////////


std::string map_frame = "map";
// ros::Time start_time = ros::Time::now();


/////////////////////////////////////////////////////////////////////////////////////////
// CALLBACK FUNCTION
/////////////////////////////////////////////////////////////////////////////////////////


// SUBSCRIBES TO:
// PUBLISHES:     tf base_link -> cam_frame
void static_broadcaster(void) {

    // SETUP ////////////////////////////////////////////////////////////////////////////////
    static tf2_ros::StaticTransformBroadcaster static_broadcaster;
    geometry_msgs::TransformStamped static_transformStamped;

    // HEADER TIMESTAMP AND TF FRAMES ///////////////////////////////////////////////////////
    // static_transformStamped.header.stamp = ros::Time::now();
    static_transformStamped.header.stamp.sec = 0;
    static_transformStamped.header.stamp.nsec = 0;
    static_transformStamped.header.frame_id = "cam_frame";
    static_transformStamped.child_frame_id = "base_link";

    // TRANSLATION; NO TRANSLATION //////////////////////////////////////////////////////////
    static_transformStamped.transform.translation.x = 0;
    static_transformStamped.transform.translation.y = 0;
    static_transformStamped.transform.translation.z = 0;
    tf2::Quaternion quat;
    
    // ORIENTATION //////////////////////////////////////////////////////////////////////////
    // See ModalAI VOXL SEEKER CAM V1 extrinsics for more information on the relationship
    // between the ToF and the VIO coordinate frames. Essentially, the yaw axes are offset
    // by 180 degrees (1 pi rads).
    quat.setRPY(0, 0, 3.14);
    quat.normalize();
    static_transformStamped.transform.rotation.x = quat.x();
    static_transformStamped.transform.rotation.y = quat.y();
    static_transformStamped.transform.rotation.z = quat.z();
    static_transformStamped.transform.rotation.w = quat.w();

    // SEND //////////////////////////////////////////////////////////////////////////////////
    static_broadcaster.sendTransform(static_transformStamped);
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
    transform.transform.translation.x = -1.0 * x;
    transform.transform.translation.y = -1.0 * y;
    transform.transform.translation.z = -1.0 * z;
    transform.transform.rotation.x = q.x();
    transform.transform.rotation.y = q.y();
    transform.transform.rotation.z = q.z();
    transform.transform.rotation.w = q.w();
    br.sendTransform(transform);

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

    // RUN
    ros::spin();
    return 0;

}