# Year3_IP
Individual Project for MEng Electronic Engineering with AI, Part III

File Structure:
-AprilVersion:
  - contains some predecessor version to the final design, initially used AprilTags then got switched to ArUco
-ArucoTags:
  - contains the libraries developed with python which are to be tested
-FinalDesign
  - contains all testing and implementation programs
-Serial
  - contains the serial read function to test the UART connection


USE:
The file "FinalAruco.py" is all that is required without needing root access, to run final version.
To run navigate to directory in terminal and execute
python FinalAruco.py

To get Unicorn Hat implementation, use "ArucoMainNew.py" in combination with "UnicornControl.py"
Navigate to directory and execute
sudo python ArucoMainNew.py
