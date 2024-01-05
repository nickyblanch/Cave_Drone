clear; clc; close all;
data = csvread("waypoints.csv");
figure;
plot3(data(:, 1), data(:, 2), -1.0 * data(:, 3));
title('Drone Positions','Color',[0 0 1],'FontSize', 15)
xlabel("X-Axis","FontSize",10,"Color",[0 0 1]);
ylabel("Y-Axis","FontSize",10,"Color",[0 0 1]);
zlabel("Z-Axis","FontSize",10,"Color",[0 0 1]);
xlim([-3 4]);
ylim([-3 4]);
zlim([-3 4]);
grid on