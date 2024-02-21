clear; clc; close all;
data = readmatrix("coordinates2024_2_19_12_19_12_50_45.csv");
waypoints = readmatrix("waypoints2024_2_19_12_19_12_50_45.csv");

% Extract data for each drone
drone1_data = data(:, 1:3); % Data for drone 1 (x, y, z)
drone2_data = data(:, 4:6); % Data for drone 2 (x, y, z)

% Plot the data
figure;
plot3(drone1_data(:, 1), drone1_data(:, 2), drone1_data(:, 3), 'LineWidth', 1, 'Color', 'Blue'); % Drone 1
hold on;
plot3(drone2_data(:, 1), drone2_data(:, 2), drone2_data(:, 3), 'LineWidth', 1, 'Color', 'Red'); % Drone 2
plot3(waypoints(:, 1), waypoints(:, 2), waypoints(:, 3), '.black', 'MarkerSize', 10); % Waypoints

title('Recorded Flight Path of Vehicle Train, Fully Dark Conditions', 'Color', 'Black', 'FontSize', 15)
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
%% 
%% Plot velocity data for drone 1
figure;

plot3(data(:, 7), data(:, 8), 1.0 * data(:, 9), 'LineWidth', 1,'Color', 'Blue');    % leader
hold on;
title('Recorded Flight Path of FPV Flight, Fully Lit Conditions Velocity','Color','Black','FontSize', 15)
xlabel("North (m)","FontSize",14, 'fontweight', 'bold');
ylabel("East (m)","FontSize",14, 'fontweight', 'bold');
zlabel("Down (m)","FontSize",14, 'fontweight', 'bold');
set(gca, 'YDir', 'reverse');
set(gca, 'ZDir', 'reverse');
legend('FPV Drone', 'location', 'northeast')
xlim([-1 4]);
ylim([-3 1]);
zlim([-1 2]);
grid on