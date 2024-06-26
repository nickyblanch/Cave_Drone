clear; clc; close all;
data = readmatrix("Drone3_drone1_success_dark_1_19_202.csv");
waypoints = readmatrix("Drone3_drone1_success_dark_1_19_202_waypoints.csv");
%changed cvsread because of warning to readmatrix
figure;

plot3(data(:, 1), data(:, 2), 1.0 * data(:, 3), 'Color', 'Blue');    % leader
hold on;
plot3(data(:,4),data(:, 5), 1.0 * data(:, 6), 'Color', 'Red');       % follower
hold on;
plot3(waypoints(:, 1), waypoints(:, 2), 1.0 * waypoints(:, 3), '.black', 'MarkerSize', 12); % waypoints
title('Recorded Flight Path of Vehicle Train, Fully Dark Conditions','Color','Black','FontSize', 15)
xlabel("North (m)","FontSize",12, 'fontweight', 'bold');
ylabel("East (m)","FontSize",12, 'fontweight', 'bold');
zlabel("Down (m)","FontSize",12, 'fontweight', 'bold');
set(gca, 'YDir', 'reverse');
set(gca, 'ZDir', 'reverse');
legend('Leader', 'Follower', 'Waypoints', 'location', 'northeast')
xlim([-1 5]);
ylim([-3 3]);
zlim([-2 0]);
grid on

%%
clear; clc; close all;
data = readmatrix("Drone_1_Light_1_16_433.txt");
figure;

plot3(data(:, 1), data(:, 2), 1.0 * data(:, 3), 'Color', 'Blue');    % leader
hold on;
title('Recorded Flight Path of FPV Flight, Fully Lit Conditions','Color','Black','FontSize', 15)
xlabel("North (m)","FontSize",12, 'fontweight', 'bold');
ylabel("East (m)","FontSize",12, 'fontweight', 'bold');
zlabel("Down (m)","FontSize",12, 'fontweight', 'bold');
set(gca, 'YDir', 'reverse');
set(gca, 'ZDir', 'reverse');
legend('FPV Drone', 'location', 'northeast')
xlim([-1 5]);
ylim([-3 3]);
zlim([-2 0]);
grid on

%%
clear; clc; close all;
data = readmatrix("Drone1_Dark_1_16_436.txt");
figure;

plot3(data(:, 1), data(:, 2), 1.0 * data(:, 3), 'Color', 'Blue');    % leader
hold on;
title('Recorded Flight Path of FPV Flight, Fully Dark Conditions','Color','Black','FontSize', 15)
xlabel("North (m)","FontSize",12, 'fontweight', 'bold');
ylabel("East (m)","FontSize",12, 'fontweight', 'bold');
zlabel("Down (m)","FontSize",12, 'fontweight', 'bold');
set(gca, 'YDir', 'reverse');
set(gca, 'ZDir', 'reverse');
legend('FPV Drone', 'location', 'northeast')
xlim([-1 5]);
ylim([-3 3]);
zlim([-2 0]);
grid on