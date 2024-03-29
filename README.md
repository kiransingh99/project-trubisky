# Project Trubisky
Git repo for Masters project - Modelling Dynamics of an American Football

## About
The aim of this project is to collect data from an American football during flight, and use it to learn more about the dynamics of the ball when being thrown.

The codename 'Project Trubisky' refers to Mitchell Trubisky, the Quarterback of the Chicago Bears between 2017 and 2021. Whilst he was a promising young prospect coming out of college, his lack of accuracy was one of the reasons he struggled in the NFL. This project is named to pay homage to him.

This project is made up of three parts:
- On-board:        the system embedded in to the football to collect data
- Off-board:       the system that receives the data transmitted from the on-board system
- Post-processing: handles the data once saved to the computer, and generates meaningful output for the user

All software used in this project is available in this Github repository

### On-board system
This system is embedded into the ball. It is comprised of:
- Arduino Nano: processor
- BNO055 (9 DOF IMU) measures linear acceleration, angular velocity, orientation
- Micro SD Breakout Board: stores data on-board

This system collectes data from the sensor and writes it to a file on the SD card. Each throw of the ball requires the corresponding data to be saved in a new file. Using user inputs, the system can be reset, and the data can be transmitted or deleted. The data is saved to a file as this is faster than transmitting it as it is measured, so this allows for a higher frequency of data readings. The accelerometer and gyroscope together track 6 degrees of freedom, which, when combined with a 3 axis magnetometer, whcih gives us information about orientation (which is required in a gravitational field) completely describes a rigid body; therefore these sensors are sufficient to fully monitor the ball's motion.

### Off-board system
This system is not connected to the ball, but is connected to a PC. It is comprised of:
- Arduino Uno: processor
- PC: stores data for future processing

This system simply receives the transmitted data and writes it to the Serial monitor. A python script running on the same PC reads the serial port, and writes the data received to csv files.

### Post-processing system
This system is just made up of Python scripts running on a PC, with access to all the csv files mentioned above. It takes the raw sensor data and produces useful and meaningful output to the user. Potential outputs include:
- Data about individual throws
	- A flight path (horizontal and vertical distance)
	- Metrics such as:
		- distance travelled
		- maximum height reached
		- rotation rate of spiral
		- stability of spiral
- Graphs of all the data, such as:
	- Distance thrown against angle of attack and launch velocity
	- Stability of spiral against launch velocity

Each file can be passed to a function which generates data about the throws and adds relevant data to another csv file, which summarises all the data, so it doesnt need to be recalculated every time a graph summarising all the data is generated.

## Software

### Dependencies
The external libraries used by this software are: 

- On-board
	- Adafruit_Sensor
	- Adafruit_BNO055
	- utility/imumaths
	- SD
	- Wire
- Off-board
	- C++ (run on Arduino)
		- Wire
	- python (run on PC)
		- datetime
		- os
		- serial
		- signal
- Post-processing
	- csv
	- matplotlib
	- numpy
	- os
	- sys

### Structure of repository

- **project-trubisky/** *#root directory*
	- **.vscode/** *#config files for running system from VS Code*
	- **data/** *#both raw and processed data are saved here*
	- **src/** *#code is stored here*
	- **.gitignore**
	- **README.md**


## Interpreting the data

### Raw data files

The raw data files are in CSV file formats, and the file names begin with the prefix "RAW-". In case they were not transmitted accurately, they are 'health checked' before they get added to the tracker file (mentioned below). They have the following columns:

- time - timestamp of each reading, given in milliseconds
- acc (e_r) - linear acceleration in the direction of the major axis (m/s^2)
- acc (e_theta) - linear acceleration in the direction of the first minor axis (m/s^2)
- acc (e_phi) - linear acceleration in the direction of the second minor axis (m/s^2)
- w (e_r) - angular velocity in the direction of the major axis (deg/s)
- w (e_theta) - angular velocity in the direction of the first minor axis (deg/s)
- w (e_phi) - angular velocity in the direction of the second minor axis (deg/s)
- euler (alpha) - change in yaw since sensors initialised (deg)
- euler (beta) - pitch (deg)
- euler (gamma) - roll (deg)

This file should not be given too much focus as the processed data files contain the same information and more.

### Processed data files
The processed data files have the same first columns as the raw data files, but each of the headings are prefixed by '[raw] '. They are complete replications of the raw data files, except the units of measurement have been converted to more usable ones, where appropriate (using radians instead of degrees). The next column contains the time in milliseconds between each sample. The next columns contain the same sensor data, but after having been smoothened (low pass filtered). The order of these columns should not be changed

Following that, the columns contain data at each timestep of the throw as listed below. Note that these columns can be in any order, provided they follow the first set of columns:

- velocities (e_r), (e_theta), (e_phi) - the velocity of the ball in ball-centred coordinates. The origin of this axis is the centre of the ball, and this orthonormal set rotates with the ball.
- velocities (x), (y), (z) - the velocity of the ball in cartesian coordinates. This is relative to a stationary observer.

### Global tracker file

The global tracker file is the summary of the data of each of the throws of the ball. Each column gives the value of another metric for each file listed in the tracker. An explanation of the columns are as follows:

- **name**: the name of the raw data file, starting with its parent directory
- **health status**: a code explaining the result of the last health check done on the raw data file, where:
	- 0 means untested
	- 1 means failed
	- 2 means passed with warnings
	- 3 means passed without warnings
- **processed file**: name of the processed data file corresponding to the raw data file
- **time of throw**: the total time of recording for each file (milliseconds)

## Hardware requirements
The on-board system is intended for a Arduino Nano Every, though it will work on a standard Arduino Nano. The off-board system functions without problem on an Arduino Uno. The post-processing system should function without problem on any commercial PC.

### Wiring diagram

#### On-board system

|   Arduino Nano   |    Device name and pin    |
|------------------|---------------------------|
| **5V**           | *BNO055* **Vin**          |
| **GND**          | *BNO055* **GND**          |
| **A4**           | *BNO055* **SDA**          |
| **A5**           | *BNO055* **SCL**          |
| **5V**           | *Micro SD Module* **5V**  |
| **GND**          | *Micro SD Module* **GND** |
| **D10**          | *Micro SD Module* **CS**  |
| **D11**          | *Micro SD Module* **DI**  |
| **D12**          | *Micro SD Module* **DO**  |
| **D13**          | *Micro SD Module* **CLK** |

Note that this diagram does not include the on-board power supply.

The off-board system has a Molex connector, which allows control of the system within the ball. The connections are as folows:

| #  | Colour |  Connection on-board  |         Connection          |            Function           |
|----|--------|-----------------------|-----------------------------|-------------------------------|
| 1  | blue   | **A4**                | **A4** on off-board system  | Tx data wire                  |
| 2  | purple | **A5**                | **A5** on off-board system  | Tx data wire                  |
| 3  | grey   | **GND**               | **GND** on off-board system | Ground reference for Tx       |
| 4  | white  | **Delete pin (D4)**   | #5                          | Triggers delete function      |
| 5  | black  | **GND**               | Either #4 or #6             | Pulls #4 or #6 down to ground |
| 6  | brown  | **Transmit pin (D5)** | #5                          | Triggers transmit function    |
| 7  | red    | **Vin**               | #8a                         | Power circuit                 |
| 8a | orange | **Battery (+ve)**     | #7                          | Power circuit                 |
| 8b | orange | **Battery (+ve)**     | Battery charger (+ve)       | Charge battery                |

Note that when charging, the negative terminal of the battery should be connected to either of the ground pins.

#### Off-board system

|   Arduino Uno    |    Device name and pin    |
|------------------|---------------------------|
| **5V**           | *113990010 Rx* **Vcc**    |
| **GND**          | *113990010 Rx* **GND**    |
| **D2**           | *113990010 Rx* **DATA**   |
| **A4**           | *On-board system* **A4**  |
| **A5**           | *On-board system* **A5**  |
| **GND**          | *On-board system* **GND** |

### Effect of mass of additional components
Adding components with finite mass to the ball will affect the mechanics. The main concerns include the changes in the ball's mass, centre of mass, and its moment of inertia.

As per the NFL regulations, the inflated ball must have a mass between 14 and 15oz (396-425g). The electronics weigh around 66g and therefore increase the mass of the ball by about 15%. However, by slightly underinflating the ball, the significance of this change in mass can be reduced. A difference this small is not noticeable to some NFL players, let alone the average user of this product.

To maintain the ball's centre of mass, the electronics shall be installed with even mass distribution, and positioned at the centre of the ball.

By modelling the ball as a prolate spheroid, the moment of inertia of the original ball is:

$I_\text{ball}=\frac{1}{5}mb^2\left(1+\frac{a^2}{b^2}\right)$
where $m$, $a$ and $b$ are the mass, the semi-major axis and the semi-minor axis of the ball respectively 
$I_\text{ball}=\frac{1}{5}\cdot0.4\cdot 0.086^2\cdot\left(1+\frac{0.141^2}{0.086^2}\right)$
$I_\text{ball}=2.18\times10^{-3}\text{kgm}^{-1}$

The increase in moment of inertia will be almost completely due to the PP3 battery, and will be equal to:
$I_\text{elec}\simeq I_\text{battery}=\frac{1}{12}m\left(w^2+d^2\right)$
where $m$, $w$ and $d$ are the mass, width and thickness of the battery, respectively
$I_\text{elec}\simeq\frac{1}{12}\cdot0.046\cdot\left(0.027^2+0.018^2\right)$
$I_\text{elec}\simeq4.03\times10^{-6}\text{kgm}^{-1}$

This is only an increase of 0.18%, and therefore will have a negligible effect on the results.

## To Do
- Post processing code
	- add more metrics - dependent on processed data operations
		- time of launch (when acceleration (without g) stops increasing / when spiral reaches ~80% of max)
		- launch speed
		- spiral rating (normalised variance of spiral)
		- angle of attack (at launch)
	- plot metrics in tracker (ensemble class)