%% AUTHORS: Nick Blanchard, Amber Parker, Arturo Lopez

% Clear workspace
clear; clc; close all;

% Flags
mode = 0;    % 0 FOR LIGHT, 1 FOR DARK
ML = 1;      % Maching Learning Test
FPV = 0;     % FPV Test

%% Load Data

if mode
    data = readmatrix("./Leader_Follower_Dark/coordinates2024_3_22_13_54_23_truncated.csv");
    waypoints = readmatrix("./Leader_Follower_Dark/waypoints2024_3_22_13_54_23_truncated.csv");
else
    data = readmatrix("./Leader_Follower_Light/coordinates2024_3_12_15_12_15_29_40_truncated.csv");
    waypoints = readmatrix("./Leader_Follower_Light/waypoints2024_3_12_15_12_15_29_40_truncated.csv");
end

drone1_pos = data(:, 1:3); % Data for Leader (x, y, z)
drone2_pos = data(:, 4:6); % Data for Follower (x, y, z)
drone1_vel = data(:, 7:9); % Data for Leader (vx, vy, vz)
drone2_vel = data(:, 10:12); % Data for Follower (vx, vy, vz)

%%  Plot the pos data
figure;
hold on;
plot3(drone1_pos(:, 1), drone1_pos(:, 2), drone1_pos(:, 3), 'LineWidth', 1, 'Color', 'Blue');    % Leader
plot3(drone2_pos(:, 1), drone2_pos(:, 2), drone2_pos(:, 3), 'LineWidth', 1, 'Color', 'Red');     % Follower
plot3(waypoints(:, 1), waypoints(:, 2), waypoints(:, 3), '.black', 'MarkerSize', 14);               % Waypoints
if mode
    title('Flight Path of Vehicle Train, Dark', 'Color', 'Black', 'FontSize', 15);
else
    title('Flight Path of Vehicle Train, Lit', 'Color', 'Black', 'FontSize', 15);
end

xlabel("North (m)", "FontSize", 14, 'fontweight', 'bold');
ylabel("East (m)", "FontSize", 14, 'fontweight', 'bold');
zlabel("Down (m)", "FontSize", 14, 'fontweight', 'bold');
set(gca, 'YDir', 'reverse');
set(gca, 'ZDir', 'reverse');
legend('Leader', 'Follower', 'Waypoints', 'location', 'northeast')
xlim([-1 5]);
ylim([-3 3]);
zlim([-2 0]);
grid on;

%%  Plot the vel data
ylimit = [-1.75 1.75];
ylimit_abs = [0 2];
xlimit = [0 length(drone1_vel)];

figure;
hold on;
if mode
    title('Velocities of Vehicle Train, Dark','Color','Black','FontSize', 15);
else
    title('Velocities of Vehicle Train, Lit','Color','Black','FontSize', 15);
end
plot(vecnorm(transpose(drone1_vel)), 'LineWidth', 1,'Color', 'Blue');               % leader
plot(vecnorm(transpose(drone2_vel)), 'LineWidth', 1,'Color', 'Red');               % follower
xlabel("Time","FontSize",14, 'fontweight', 'bold');
ylabel("Velocity (m/s)","FontSize",14, 'fontweight', 'bold');
legend('Leader Vehicle', 'Follower Vehicle', 'location', 'northeast');
ylim(ylimit_abs);
xlim(xlimit);

%% Individual vel plots

% Leader
figure;
subplot(3, 1, 1);
plot(drone1_vel(:, 1));
if mode
    title("Velocities of Leader Vehicle, Dark",'Color','Black','FontSize', 15);
else
    title("Velocities of Leader Vehicle, Lit",'Color','Black','FontSize', 15);
end
ylabel("X Velocity (m/s)", "FontSize", 10, 'fontweight', 'bold');
xlabel("Time", "FontSize", 10, 'fontweight', 'bold');
ylim(ylimit);
xlim(xlimit);

subplot(3, 1, 2);
plot(drone1_vel(:, 2));
ylabel("Y Velocity (m/s)", "FontSize", 10, 'fontweight', 'bold');
xlabel("Time", "FontSize", 10, 'fontweight', 'bold');
ylim(ylimit);
xlim(xlimit);

subplot(3, 1, 3);
plot(drone1_vel(:, 3));
ylabel("Z Velocity (m/s)", "FontSize", 10, 'fontweight', 'bold');
xlabel("Time", "FontSize", 10, 'fontweight', 'bold');
ylim(ylimit);
xlim(xlimit);

% Follower
figure;
subplot(3, 1, 1);
plot(drone2_vel(:, 1));
if mode
    title("Velocities of Follower Vehicle, Dark",'Color','Black','FontSize', 15);
else
    title("Velocities of Follower Vehicle, Lit",'Color','Black','FontSize', 15);
end
ylabel("X Velocity (m/s)", "FontSize", 10, 'fontweight', 'bold');
xlabel("Time", "FontSize", 10, 'fontweight', 'bold');
ylim(ylimit);
xlim(xlimit);

subplot(3, 1, 2);
plot(drone2_vel(:, 2));
ylabel("Y Velocity (m/s)", "FontSize", 10, 'fontweight', 'bold');
xlabel("Time", "FontSize", 10, 'fontweight', 'bold');
ylim(ylimit);
xlim(xlimit);

subplot(3, 1, 3);
plot(drone2_vel(:, 3));
ylabel("Z Velocity (m/s)", "FontSize", 10, 'fontweight', 'bold');
xlabel("Time", "FontSize", 10, 'fontweight', 'bold');
ylim(ylimit);
xlim(xlimit);

%% Additional section for machine learning testing that Nick has been working on

if ML

    % Load data
    data = readmatrix("C:\Users\nicky\Downloads\coordinates_file_new.csv");
    waypoints = readmatrix("C:\Users\nicky\Downloads\waypoints_file_new.csv");
    drone1_pos = data(:, 1:3); % Data for Leader (x, y, z)
    drone1_vel = data(:, 4:6); % Data for Leader (vx, vy, vz)
    
    % Position data
    figure;
    hold on;
    plot3(drone1_pos(:, 1), drone1_pos(:, 2), drone1_pos(:, 3), 'LineWidth', 1, 'Color', 'Blue');    % Leader
    plot3(waypoints(:, 1), waypoints(:, 2), waypoints(:, 3), '.black', 'MarkerSize', 14);               % Waypoints
    title('Path During Autonomous Flight', 'Color', 'Black', 'FontSize', 15);
    xlabel("North (m)", "FontSize", 14, 'fontweight', 'bold');
    ylabel("East (m)", "FontSize", 14, 'fontweight', 'bold');
    zlabel("Down (m)", "FontSize", 14, 'fontweight', 'bold');
    set(gca, 'YDir', 'reverse');
    set(gca, 'ZDir', 'reverse');
    legend('Leader', 'Waypoints', 'location', 'northeast')
    xlim([-1 6]);
    ylim([-2 5]);
    zlim([-2 0]);
    grid on;

    % Velocity data
    ylimit = [-0.25 0.25];
    xlimit = [0 length(drone1_vel)];
    figure;
    subplot(3, 1, 1);
    plot(drone1_vel(:, 1));
    title("Velocities During Autonomous Flight",'Color','Black','FontSize', 15);
    ylabel("X Velocity (m/s)", "FontSize", 10, 'fontweight', 'bold');
    xlabel("Time", "FontSize", 10, 'fontweight', 'bold');
    ylim(ylimit);
    xlim(xlimit);
    
    subplot(3, 1, 2);
    plot(drone1_vel(:, 2));
    ylabel("Y Velocity (m/s)", "FontSize", 10, 'fontweight', 'bold');
    xlabel("Time", "FontSize", 10, 'fontweight', 'bold');
    ylim(ylimit);
    xlim(xlimit);
    
    subplot(3, 1, 3);
    plot(drone1_vel(:, 3));
    ylabel("Z Velocity (m/s)", "FontSize", 10, 'fontweight', 'bold');
    xlabel("Time", "FontSize", 10, 'fontweight', 'bold');
    ylim(ylimit);
    xlim(xlimit);


end

%% Additional section for FPV testing

if FPV
    % Load data
    data_light = readmatrix("C:\Users\nicky\OneDrive\Documents\GitHub\Cave_Drone\Exports\Recorded Data For Paper\Drone_1_Light_1_16_433.txt");
    data_dark = readmatrix("C:\Users\nicky\OneDrive\Documents\GitHub\Cave_Drone\Exports\Recorded Data For Paper\Drone1_Dark_1_16_436.txt");

    % Lit
    figure;
    plot3(data_light(:, 1), data_light(:, 2), 1.0 * data_light(:, 3), 'Color', 'Blue');    % leader
    hold on;
    title('FPV Flight, Lit','Color','Black','FontSize', 15)
    xlabel("North (m)","FontSize",12, 'fontweight', 'bold');
    ylabel("East (m)","FontSize",12, 'fontweight', 'bold');
    zlabel("Down (m)","FontSize",12, 'fontweight', 'bold');
    set(gca, 'YDir', 'reverse');
    set(gca, 'ZDir', 'reverse');
    legend('FPV Drone', 'location', 'northeast')
    xlim([-1 5]);
    ylim([-3 3]);
    zlim([-2 0]);
    grid on;
    hold off;
    
    % Dark
    figure;
    plot3(data_dark(:, 1), data_dark(:, 2), 1.0 * data_dark(:, 3), 'Color', 'Blue');    % leader
    hold on;
    title('FPV Flight, Dark','Color','Black','FontSize', 15)
    xlabel("North (m)","FontSize",12, 'fontweight', 'bold');
    ylabel("East (m)","FontSize",12, 'fontweight', 'bold');
    zlabel("Down (m)","FontSize",12, 'fontweight', 'bold');
    set(gca, 'YDir', 'reverse');
    set(gca, 'ZDir', 'reverse');
    legend('FPV Drone', 'location', 'northeast')
    xlim([-1 5]);
    ylim([-3 3]);
    zlim([-2 0]);
    grid on;
    
end

