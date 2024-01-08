clear; clc; close all;
data = readmatrix("leader_follower_light_1_8_318.csv");
waypoints = readmatrix("leader_follower_light_waypoints_1_8_318.csv");
%changed cvsread because of warning to readmatrix
figure;

plot3(data(:, 1), data(:, 2), -1.0 * data(:, 3));   % leader
hold on;
plot3(data(:,4),data(:, 5), -1.0 * data(:, 6));     % follower
hold on;
plot3(waypoints(:, 1), waypoints(:, 2), -1.0 * waypoints(:, 3), '*');
title('Drone Positions','Color',[0 0 1],'FontSize', 15)
xlabel("X-Axis","FontSize",10,"Color",[0 0 1]);
ylabel("Y-Axis","FontSize",10,"Color",[0 0 1]);
zlabel("Z-Axis","FontSize",10,"Color",[0 0 1]);
set(gca, 'YDir', 'reverse');
xlim([-1 5]);
ylim([-3 3]);
zlim([0 2]);
grid on