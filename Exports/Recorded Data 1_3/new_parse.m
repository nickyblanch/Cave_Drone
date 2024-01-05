 data = csvread("PARSED.csv");
 figure;
 plot3(data(:, 1), data(:, 2), -1.0 * data(:, 3));
 xlabel("X");
 ylabel("Y");
 zlabel("Z");