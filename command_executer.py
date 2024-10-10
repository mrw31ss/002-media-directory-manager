import os

# open the commands file into buffer
with open("commands.txt", "r") as file:
    commands = file.readlines()
    file.close()

# change the directory to that of the config file
os.chdir("/Volumes/SCHNEIDER_002/005_media/Movies")

# run the commands 
for line in commands:
    os.system(f"{line}")