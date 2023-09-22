####################################################################################
#       Author: Nicolas Blanchard | nickyblanch@arizona.edu | (520) 834-3191
#         Date: 9/20/23
#      Purpose: 
# Dependencies: 
####################################################################################
# Libraries
####################################################################################


import tkinter as tk
from tkinter import ttk
from tkinter import *


####################################################################################
# Global variables
####################################################################################


drone_1_IP = "192.168.1.1"
drone_2_IP = "192.168.1.2"
drone_1_UDP = 1
drone_2_UDP = 1
window_width = 750
window_height = 450


####################################################################################
# Function definitions
####################################################################################


def setup():

    # DEBUG
    # print("Setup")

    # Use global window function
    global window
    global drone_1_IP_entry
    global drone_2_IP_entry
    global drone_1_UDP_entry
    global drone_2_UDP_entry
    global drone_1_x_entry
    global drone_1_y_entry
    global drone_1_z_entry
    global drone_2_x_entry
    global drone_2_y_entry
    global drone_2_z_entry

    # Create window
    window = Tk()

    # Set size of window
    window.geometry(str(window_width) + "x" +  str(window_height))

    # Create canavs
    mars = PhotoImage(file = r"C:\Users\nicky\OneDrive\Pictures\mars_blurred_resized.png", master=window)
    canvas = tk.Canvas(window, width=window_width, height=window_height)
    canvas.pack()
    canvas.background = mars
    bg = canvas.create_image(0, 0, anchor=tk.NW, image=mars)

    # # Create frames WITH BACKGROUND COLORS
    # top_frame = Frame(window, bg='cyan', width=1920, height=window_height/5)
    # left_frame = Frame(window, bg='red', width=window_width/2, height=window_height*2/5)
    # left_frame_bottom = Frame(window, bg='purple', width=window_width/2, height=window_height*1/10)
    # left_frame_bottom_coords = Frame(window, bg='gray', width=window_width/2, height=window_height*1/10)
    # right_frame = Frame(window, bg='yellow', width=window_width/2, height=window_height*2/5)
    # right_frame_bottom = Frame(window, bg='white', width=window_width/2, height=window_height*1/10)
    # right_frame_bottom_coords = Frame(window, bg='pink', width=window_width/2, height=window_height*1/10)
    # bottom_frame = Frame(window, bg='blue', width=window_width/2, height=window_height/5)

    top_frame = Frame(window, width=1920, height=window_height/5, bg='')
    left_frame = Frame(window, width=window_width/2, height=window_height*2/5, bg='')
    left_frame_bottom = Frame(window, width=window_width/2, height=window_height*1/10, bg='')
    left_frame_bottom_coords = Frame(window, width=window_width/2, height=window_height*1/10)
    right_frame = Frame(window, width=window_width/2, height=window_height*2/5)
    right_frame_bottom = Frame(window, width=window_width/2, height=window_height*1/10)
    right_frame_bottom_coords = Frame(window, width=window_width/2, height=window_height*1/10)
    bottom_frame = Frame(window, width=window_width/2, height=window_height/5)
    
    # Organize frames
    top_frame.grid(row=0, columnspan=2)
    left_frame.grid(row=1, column=0, sticky='nsew')
    left_frame_bottom.grid(row=2, column=0, sticky='nsew')
    left_frame_bottom_coords.grid(row=3, column=0, sticky='nsew')
    right_frame.grid(row=1, column=1, sticky="nsew")
    right_frame_bottom.grid(row=2, column=1, sticky='nsew')
    right_frame_bottom_coords.grid(row=3, column=1, sticky='nsew')
    bottom_frame.grid(row=4, columnspan=2, sticky="ew")

    # Formatting frames
    top_frame.grid_propagate(False)
    top_frame.pack_propagate(False)
    left_frame.grid_propagate(False)
    left_frame.pack_propagate(False)
    left_frame.columnconfigure(0, weight=2)
    left_frame.columnconfigure(1, weight=0)
    left_frame.columnconfigure(2, weight=1)
    left_frame_bottom.grid_propagate(False)
    left_frame_bottom.pack_propagate(False)
    left_frame_bottom.columnconfigure(0, weight=1)
    left_frame_bottom.columnconfigure(1, weight=1)
    left_frame_bottom.columnconfigure(2, weight=1)
    left_frame_bottom.columnconfigure(3, weight=1)
    left_frame_bottom.columnconfigure(4, weight=1)
    left_frame_bottom_coords.grid_propagate(False)
    left_frame_bottom_coords.pack_propagate(False)
    left_frame_bottom_coords.columnconfigure(0, weight=1)
    left_frame_bottom_coords.columnconfigure(3, weight=1)
    right_frame.grid_propagate(False)
    right_frame.pack_propagate(False)
    right_frame.columnconfigure(0, weight=2)
    right_frame.columnconfigure(1, weight=0)
    right_frame.columnconfigure(2, weight=1)
    right_frame_bottom.grid_propagate(False)
    right_frame_bottom.pack_propagate(False)
    right_frame_bottom.columnconfigure(0, weight=1)
    right_frame_bottom.columnconfigure(1, weight=1)
    right_frame_bottom.columnconfigure(2, weight=1)
    right_frame_bottom.columnconfigure(3, weight=1)
    right_frame_bottom.columnconfigure(4, weight=1)
    right_frame_bottom_coords.grid_propagate(False)
    right_frame_bottom_coords.pack_propagate(False)
    right_frame_bottom_coords.columnconfigure(0, weight=1)
    right_frame_bottom_coords.columnconfigure(3, weight=1)
    bottom_frame.grid_propagate(False)
    bottom_frame.pack_propagate(False)
    bottom_frame.columnconfigure(0, weight=1)
    bottom_frame.columnconfigure(1, weight=1)
    bottom_frame.columnconfigure(2, weight=1)
    bottom_frame.columnconfigure(3, weight=1)
    bottom_frame.columnconfigure(4, weight=1)
    bottom_frame.columnconfigure(5, weight=1)
    bottom_frame.rowconfigure(0, weight=1)
    
    # Title
    title = Label(top_frame, text='CAVE DRONE GCS', font=('Arial 26'))
    title.pack()

    # Titles
    drone_1_title = Label(left_frame, text="Leader Drone", font=('Arial 20'))
    drone_1_title.grid(row=0, column=0, sticky='w')
    drone_2_title = Label(right_frame, text="Follower Drone", font=('Arial 20'))
    drone_2_title.grid(row=0, column=0, sticky='w')

    # IP Entry Widgets
    drone_1_IP_entry = Entry(left_frame, width=12, font=('Arial 16'))
    drone_1_IP_entry.grid(row=1, column=0, padx=5, pady=10, sticky='e')
    drone_2_IP_entry = Entry(right_frame, width=12, font=('Arial 16'))
    drone_2_IP_entry.grid(row=1, column=0, padx=5, pady=10, sticky='e')

    # UDP Entry Widgets
    drone_1_UDP_entry = Entry(left_frame, width=5, font=('Arial 16'))
    drone_1_UDP_entry.grid(row=1, column=1, pady=10, sticky='w')
    drone_2_UDP_entry = Entry(right_frame, width=5, font=('Arial 16'))
    drone_2_UDP_entry.grid(row=1, column=1, pady=10, sticky='w')

    # IP Buttons
    photo = PhotoImage(file = r"C:\Users\nicky\OneDrive\Pictures\wifi_small.png")

    drone_1_IP_button = Button(left_frame, image=photo, command=update_drone_1_IP)
    drone_1_IP_button.image = photo
    drone_1_IP_button.grid(row=1, column=2, padx=5, pady=10, sticky='w')
    drone_2_IP_button = Button(right_frame, image=photo, command=update_drone_2_IP)
    drone_2_IP_button.image = photo
    drone_2_IP_button.grid(row=1, column=2, padx=5, pady=10, sticky='w')

    # Arm buttons
    drone_1_arm_button = Button(left_frame, text="Arm Leader", width=20, command=lambda: arm_drone("1"))
    drone_1_arm_button.grid(row=2, column=0, padx=4, pady=2, sticky='e')
    drone_2_arm_button = Button(right_frame, text="Arm Follower", width=20, command=lambda: arm_drone("2"))
    drone_2_arm_button.grid(row=2, column=0, padx=4, pady=2, sticky='e')

    # Disarm buttons
    drone_1_disarm_button = Button(left_frame, text="Disarm Leader", width=20, command=lambda: disarm_drone("1"))
    drone_1_disarm_button.grid(row=2, column=1, columnspan=2, padx=4, pady=2, sticky='w')
    drone_2_disarm_button = Button(right_frame, text="Disarm Follower", width=20, command=lambda: disarm_drone("2"))
    drone_2_disarm_button.grid(row=2, column=1, columnspan=2, padx=4, pady=2, sticky='w')

    # Takeoff buttons
    drone_1_takeoff_button = Button(left_frame, text="Takeoff Leader", width=20, command=lambda: takeoff_drone("1"))
    drone_1_takeoff_button.grid(row=3, column=0, padx=4, pady=2, sticky='e')
    drone_2_takeoff_button = Button(right_frame, text="Takeoff Follower", width=20, command=lambda: takeoff_drone("2"))
    drone_2_takeoff_button.grid(row=3, column=0, padx=4, pady=2, sticky='e')

    # Land buttons
    drone_1_land_button = Button(left_frame, text="Land Leader", width=20, command=lambda: land_drone("1"))
    drone_1_land_button.grid(row=3, column=1, columnspan=2, padx=4, pady=2, sticky='w')
    drone_2_land_button = Button(right_frame, text="Land Follower", width=20, command=lambda: land_drone("2"))
    drone_2_land_button.grid(row=3, column=1, columnspan=2, padx=4, pady=2, sticky='w')

    # Mode buttons
    drone_1_off_button = Button(left_frame_bottom, text="OFF", width=7, command=lambda: update_flight_mode("1", "4"))
    drone_1_off_button.grid(row=1, column=0, padx=4, pady=2, sticky='w')
    drone_1_test_button = Button(left_frame_bottom, text="TEST", width=7, command=lambda: update_flight_mode("1", "0"))
    drone_1_test_button.grid(row=1, column=1, padx=4, pady=2, sticky='w')
    drone_1_manual_button = Button(left_frame_bottom, text="MANUAL", width=7, command=lambda: update_flight_mode("1", "1"))
    drone_1_manual_button.grid(row=1, column=2, padx=4, pady=2, sticky='w')
    drone_1_demo_button = Button(left_frame_bottom, text="DEMO", width=7, command=lambda: update_flight_mode("1", "3"))
    drone_1_demo_button.grid(row=1, column=3, padx=4, pady=2, sticky='w')
    drone_1_autonomous_button = Button(left_frame_bottom, text="AUTO", width=7, command=lambda: update_flight_mode("1", "2"))
    drone_1_autonomous_button.grid(row=1, column=4, padx=4, pady=2, sticky='w')
    drone_2_off_button = Button(right_frame_bottom, text="OFF", width=7, command=lambda: update_flight_mode("2", "4"))
    drone_2_off_button.grid(row=1, column=0, padx=4, pady=2, sticky='w')
    drone_2_test_button = Button(right_frame_bottom, text="TEST", width=7, command=lambda: update_flight_mode("2", "0"))
    drone_2_test_button.grid(row=1, column=1, padx=4, pady=2, sticky='w')
    drone_2_manual_button = Button(right_frame_bottom, text="MANUAL", width=7, command=lambda: update_flight_mode("2", "1"))
    drone_2_manual_button.grid(row=1, column=2, padx=4, pady=2, sticky='w')
    drone_2_demo_button = Button(right_frame_bottom, text="DEMO", width=7, command=lambda: update_flight_mode("2", "3"))
    drone_2_demo_button.grid(row=1, column=3, padx=4, pady=2, sticky='w')
    drone_2_autonomous_button = Button(right_frame_bottom, text="AUTO", width=7, command=lambda: update_flight_mode("2", "2"))
    drone_2_autonomous_button.grid(row=1, column=4,padx=4, pady=2, sticky='w')

    # Manual coordinate entries
    drone_1_x_entry = Entry(left_frame_bottom_coords, width=5, font=('Arial 16'))
    drone_1_x_entry.grid(row=1, column=0, pady=10, sticky='e')
    drone_1_y_entry = Entry(left_frame_bottom_coords, width=5, font=('Arial 16'))
    drone_1_y_entry.grid(row=1, column=1, pady=10)
    drone_1_z_entry = Entry(left_frame_bottom_coords, width=5, font=('Arial 16'))
    drone_1_z_entry.grid(row=1, column=2, pady=10)
    drone_2_x_entry = Entry(right_frame_bottom_coords, width=5, font=('Arial 16'))
    drone_2_x_entry.grid(row=1, column=0, pady=10, sticky='e')
    drone_2_y_entry = Entry(right_frame_bottom_coords, width=5, font=('Arial 16'))
    drone_2_y_entry.grid(row=1, column=1, pady=10)
    drone_2_z_entry = Entry(right_frame_bottom_coords, width=5, font=('Arial 16'))
    drone_2_z_entry.grid(row=1, column=2, pady=10)

    # Manual coordinate entry button
    drone_1_coords_button = Button(left_frame_bottom_coords, text='✓', width=5, command=lambda: update_coords("1"))
    drone_1_coords_button.grid(row=1, column=3, columnspan=2, padx=4, pady=2, sticky='w')
    drone_2_coords_button = Button(right_frame_bottom_coords, text='✓', width=5, command=lambda: update_coords("2"))
    drone_2_coords_button.grid(row=1, column=3, columnspan=2, padx=4, pady=2, sticky='w')

    # Current coordinate feedback
    drone_1_x_coord = Label(bottom_frame, text='1.01', font=('Arial 16'))
    drone_1_x_coord.grid(row = 0, column = 0)
    drone_1_y_coord = Label(bottom_frame, text='0.75', font=('Arial 16'))
    drone_1_y_coord.grid(row = 0, column = 1)
    drone_1_z_coord = Label(bottom_frame, text='-0.88', font=('Arial 16'))
    drone_1_z_coord.grid(row = 0, column = 2)
    drone_2_x_coord = Label(bottom_frame, text='1.01', font=('Arial 16'))
    drone_2_x_coord.grid(row = 0, column = 3)
    drone_2_y_coord = Label(bottom_frame, text='0.75', font=('Arial 16'))
    drone_2_y_coord.grid(row = 0, column = 4)
    drone_2_z_coord = Label(bottom_frame, text='-0.88', font=('Arial 16'))
    drone_2_z_coord.grid(row = 0, column = 5)
    drone_1_x_lab = Label(bottom_frame, text='X', font=('Arial 16'))
    drone_1_x_lab.grid(row = 1, column = 0)
    drone_1_y_lab = Label(bottom_frame, text='Y', font=('Arial 16'))
    drone_1_y_lab.grid(row = 1, column = 1)
    drone_1_z_lab = Label(bottom_frame, text='Z', font=('Arial 16'))
    drone_1_z_lab.grid(row = 1, column = 2)
    drone_2_x_lab = Label(bottom_frame, text='X', font=('Arial 16'))
    drone_2_x_lab.grid(row = 1, column = 3)
    drone_2_y_lab = Label(bottom_frame, text='Y', font=('Arial 16'))
    drone_2_y_lab.grid(row = 1, column = 4)
    drone_2_z_lab = Label(bottom_frame, text='Z', font=('Arial 16'))
    drone_2_z_lab.grid(row = 1, column = 5)

    # TODO:
    # Add current x,y,z coordinates in bottom frame

    # Configure grid
    window.rowconfigure(9)
    window.columnconfigure((0, 1), weight = 1, uniform="column")


def update_drone_1_IP():
   
    global drone_1_IP
    global drone_1_IP_entry
    global drone_1_UDP
    global drone_1_UDP_entry

    temp = drone_1_IP_entry.get()

    if temp != "":
        drone_1_IP = temp

    temp = drone_1_UDP_entry.get()

    if temp != "":
        drone_1_UDP = temp

    print(str(drone_1_IP) + ":" + str(drone_1_UDP))


def update_drone_2_IP():
   
    global drone_2_IP
    global drone_2_IP_entry
    global drone_2_UDP
    global drone_2_UDP_entry

    temp = drone_2_IP_entry.get()

    if temp != "":
        drone_2_IP = temp

    temp = drone_2_UDP_entry.get()

    if temp != "":
        drone_2_UDP = temp

    print(str(drone_2_IP) + ":" + str(drone_2_UDP))


def arm_drone(drone_number):
    print("DRONE " + drone_number + " ARMED")


def disarm_drone(drone_number):
    print("DRONE " + drone_number + " DISARMED")


def takeoff_drone(drone_number):
    print("DRONE " + drone_number + " TAKEOFF")


def land_drone(drone_number):
    print("DRONE " + drone_number + " LAND")


def update_flight_mode(drone_number, mode):
    print("DRONE " + drone_number + " FLIGHT MODE: " + mode)


def update_coords(drone_number):
    if drone_number == "1":
        print("DRONE " + drone_number + " TARGET COORDS: " + drone_1_x_entry.get() + " " + drone_1_y_entry.get() + " " + drone_1_z_entry.get())
    else:
        print("DRONE " + drone_number + " TARGET COORDS: " + drone_2_x_entry.get() + " " + drone_2_y_entry.get() + " " + drone_2_z_entry.get())


def main():

    setup()

    window.mainloop()


####################################################################################
# Main
####################################################################################


main()