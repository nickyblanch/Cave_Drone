clear; clc; close all;
data = readmatrix("leader_follower_light_1_8_318_shortened.csv");
waypoints = readmatrix("leader_follower_light_waypoints_1_8_318.csv");
%changed cvsread because of warning to readmatrix
figure;

plot3(data(:, 1), data(:, 2), 1.0 * data(:, 3), 'Color', 'Blue');    % leader
hold on;
plot3(data(:,4),data(:, 5), 1.0 * data(:, 6), 'Color', 'Red');       % follower
hold on;
plot3(waypoints(:, 1), waypoints(:, 2), 1.0 * waypoints(:, 3), '.black', 'MarkerSize', 12); % waypoints
title('Recorded Flight Path of Vehicle Train, Fully Lit Conditions','Color','Black','FontSize', 15)
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