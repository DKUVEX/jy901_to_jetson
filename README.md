# jy901_to_jetson
Communication between Jetson Nano and JY901S sensor.
Code taken and adapted from WIT documentation.

## Run the code:

Execute the following steps to read data from the JY901 sensor on the Jetson Orin Nano:
1. Create a conda environment:
   
```
conda create --name <EnvName> python=3.9
conda activate <EnvName>
```

2. Install pyserial:

```
conda install pyserial
```

3. Run the main.py using sudo(make sure to include the whole path):

```
sudo /home/bluebear/miniconda3/envs/<EnvName>/bin/python3.9 main
```

4. The code will prompt you to enter the device name, Enter the following path: ``` /dev/ttyTHS0 ``` and make sure the JY901 is connected to the right pins of the Jetson
5. Make sure to change ``` <EnvName> ``` with the name set for the environment.
