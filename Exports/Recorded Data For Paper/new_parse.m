clear; clc; close all;
data = readmatrix("coordinates_1_7_306.csv");
%changed cvsread because of warning to readmatrix
figure;

plot3(data(:, 1), data(:, 2), -1.0 * data(:, 3));
plot3(data(:,4),data(:, 5), -1.0 * data(:, 6));
title('Drone Positions','Color',[0 0 1],'FontSize', 15)
xlabel("X-Axis","FontSize",10,"Color",[0 0 1]);
ylabel("Y-Axis","FontSize",10,"Color",[0 0 1]);
zlabel("Z-Axis","FontSize",10,"Color",[0 0 1]);
xlim([-4 15]);
ylim([-4 15]);
zlim([-50 15]);
grid on