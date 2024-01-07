% Specify the file path
file_path = 'DRONE_3_SOLO_LIGHT.txt';

% Open the file and read its contents
fid = fopen(file_path, 'rt');

% Initialize arrays to store x, y, and z coordinates
x = [];
y = [];
z = [];

% Read the file line by line
while ~feof(fid)
    line = fgetl(fid);
    
    % Check if the line contains "Drone 1" data
    if contains(line, 'Drone 1:')
        % Extract the numeric values from the line
        values = sscanf(line, 'Drone 1: (%f, %f, %f)');
        
        % Check if the values were successfully extracted
        if numel(values) == 3
            x = [x; values(1)];
            y = [y; values(2)];
            z = [z; values(3)];
        end
    end
end

% Close the file
fclose(fid);

% Create a 3D scatter plot with all points
figure;
scatter3(x, y, z, 'filled');
title('Location of Drone 1');
xlabel('X-Axis');
ylabel('Y-Axis');
zlabel('Z-Axis');
grid on;
