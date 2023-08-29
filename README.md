# Cave_Drone
**Cave Drones for Autonomous Exploration In GPS Denied Environments**

*Research sponsored by the Micro Air Vehicle (MAV) Lab at the University of Arizona.*

## Intro
'Follower' is currently the main working folder. It contains code for the follower drones; the Python script enables the drones to navigate to waypoints that are already pre-programmed or sent in real time via UDP.
The MATLAB code enables visualization of recorded telemetry logs; basically, after the drones has been flown, we can re-create it's path using recorded 'local_position_NED" MAVLINK messages stored in the telemetry
files that QGroudncontrol saves.

'Beacon' contains code to turn an ESP32 microcontroller into a WiFi bridge, theoretically enabling ESP32 devices to be used as telemtry repeaters throughout the flight of the drones. This is a WIP.

'Exports' contains collected data including video and telemetry. This data is used to post-flight analysis.

'References' contains academic papers on the topic that may be useful.

# Contact
Please email nickyblanch@arizona.edu for questions about code OR usage.
