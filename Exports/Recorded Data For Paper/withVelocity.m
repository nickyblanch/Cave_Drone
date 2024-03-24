%% AUTHORS: Nick Blanchard, Amber Parker, Arturo Lopez

% Clear workspace
clear; clc; close all;

% Flags
mode = 0;    % 0 FOR LIGHT, 1 FOR DARK

%% Load Data

if mode
    data = readmatrix("./Leader_Follower_Dark/coordinates2024_3_22_xx_xx_xx_xx_xx.csv");
    waypoints = readmatrix("./Leader_Follower_Dark/waypoints2024_3_22_xx_xx_xx_xx_xx.csv");
else
    data = readmatrix("./Leader_Follower_Light/coordinates2024_3_12_15_12_15_29_40.csv");
    waypoints = readmatrix("./Leader_Follower_Light/waypoints2024_3_12_15_12_15_29_40.csv");
end

drone1_pos = data(:, 1:3); % Data for drone 1 (x, y, z)
drone2_pos = data(:, 4:6); % Data for drone 2 (x, y, z)
drone1_vel = data(:, 7:9); % Data for drone 1 (vx, vy, vz)
drone2_vel = data(:, 10:12); % Data for drone 2 (vx, vy, vz)

%%  Plot the pos data
figure;
hold on;
plot3(drone1_pos(:, 1), drone1_pos(:, 2), drone1_pos(:, 3), 'LineWidth', 1, 'Color', 'Blue');    % Drone 1
plot3(drone2_pos(:, 1), drone2_pos(:, 2), drone2_pos(:, 3), 'LineWidth', 1, 'Color', 'Red');     % Drone 2
plot3(waypoints(:, 1), waypoints(:, 2), waypoints(:, 3), '.black', 'MarkerSize', 10);               % Waypoints
if mode
    title('Recorded Flight Path of Vehicle Train, Fully Dark Conditions', 'Color', 'Black', 'FontSize', 15)
else
    title('Recorded Flight Path of Vehicle Train, Fully Lit Conditions', 'Color', 'Black', 'FontSize', 15)
end

xlabel("North (m)", "FontSize", 14, 'fontweight', 'bold');
ylabel("East (m)", "FontSize", 14, 'fontweight', 'bold');
zlabel("Down (m)", "FontSize", 14, 'fontweight', 'bold');
set(gca, 'YDir', 'reverse');
set(gca, 'ZDir', 'reverse');
legend('Drone 1', 'Drone 2', 'Waypoints', 'location', 'northeast')
xlim([-1 5]);
ylim([-3 3]);
zlim([-2 0]);
grid on;

%%  Plot the vel data
figure;
hold on;
if mode
    title('Recorded Velocities of Vehicle Train, Fully Dark Conditions','Color','Black','FontSize', 15)
else
    title('Recorded Velocities of Vehicle Train, Fully Lit Conditions','Color','Black','FontSize', 15)
end
plot(vecnorm(transpose(drone1_vel)), 'LineWidth', 1,'Color', 'Blue');               % leader
plot(vecnorm(transpose(drone2_vel)), 'LineWidth', 1,'Color', 'Blue');               % follower
xlabel("North (m)","FontSize",14, 'fontweight', 'bold');
ylabel("East (m)","FontSize",14, 'fontweight', 'bold');
legend('Leader Vehicle', 'Follower Vehicle', 'location', 'northeast');
ylim([-5 5]);

%% Individual vel plots
ylimit = [-5 5];

% Leader
figure;
subplot(3, 1, 1);
plot(data(:, 7));
if mode
    title("X, Y, Z Velocities of Leader Vehicle, Fully Dark Conditions");
else
    title("X, Y, Z Velocities of Leader Vehicle, Fully Lit Conditions");
end
ylabel("X Velocity (m/s)");
xlabel("Time");
ylim(ylimit);

subplot(3, 2, 2);
plot(data(:, 8));
ylabel("Y Velocity (m/s)");
xlabel("Time");
ylim(ylimit);

subplot(3, 2, 3);
plot(data(:, 9));
ylabel("Z Velocity (m/s)");
xlabel("Time");
ylim(ylimit);

% Follower
figure;
subplot(3, 1, 1);
plot(data(:, 7));
if mode
    title("X, Y, Z Velocities of Follower Vehicle, Fully Dark Conditions");
else
    title("X, Y, Z Velocities of Follower Vehicle, Fully Lit Conditions");
end
ylabel("X Velocity (m/s)");
xlabel("Time");
ylim(ylimit);

subplot(3, 2, 2);
plot(data(:, 8));
ylabel("Y Velocity (m/s)");
xlabel("Time");
ylim(ylimit);

subplot(3, 2, 3);
plot(data(:, 9));
ylabel("Z Velocity (m/s)");
xlabel("Time");
ylim(ylimit);
