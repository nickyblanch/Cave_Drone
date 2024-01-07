# Author: Nick B
# Purpose: Parse output from the GCS and remove all text, formatting data into a .csv file.

def main():

    source = open("DRONE_3_SOLO_LIGHT.txt", "r")
    output = open("PARSED.csv", "w")
    # output.write("X,Y,Z\n")

    for line in source:
        words = line.split() # Split on whitespace
        print(words)         # Debug

        if len(words) > 1:
            if words[1].replace(":", "") == "1":
                output.write(words[2].replace("(", "") + words[3] + words[4].replace(")", "") + "\n")
        
    source.close()
    output.close()

main()