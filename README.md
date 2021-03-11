# Project Trubisky
Git repo for Masters project - Modelling Dynamics of an American Football

## About
The aim of this project is to collect data from an American football during flight, and use it to learn more about the dynamics of the ball when being thrown.

The codename 'Project Trubisky' refers to Mitchell Trubisky, the Quarterback of the Chicago Bears between 2017 and 2021. Whilst he was a promising young prospect coming out of college, his lack of accuracy was one of the reasons he struggled in the NFL. This project is named to pay homage to him.

This project is made up of three parts:
- Onboard:         the system embedded in to the football to collect data
- Offboard:        the system that receives the data transmitted from the onboard system
- Post-processing: handles the data once saved to the computer, and generates meaningful output for the user

All software used in this project is available in this Github repository

### Onboard system
This system is embedded into the ball. It is comprised of:
- Arduino Nano: processor
- BNO055 (9 DOF IMU) measures linear acceleration, angular velocity, orientation
- Micro SD Breakout Board: stores data onboard

This system collectes data from the two sensors and writes it to a file on the SD card. Each throw of the ball requires the corresponding data to be saved in a new file. Using user inputs, the system can be reset, and the data can be transmitted or deleted. The data is saved to a file as this is faster than transmitting it as it is measured, so this allows for a higher frequency of data readings. The accelerometer and gyroscope together track 6 degrees of freedom, which, when combined with a 3 axis magnetometer, whcih gives us information about orientation (which is required in a gravitational field) completely describes a rigid body; therefore these sensors are sufficient to fully monitor the ball's motion.

### Offboard system
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

## Interpreting the data

### Raw data files

The raw data files are in CSV file formats, and the file names begin with the prefix "RAW-". In case they were not transmitted accurately, they are 'health checked' before they get added to the tracker file (mentioned below). They have the following columns:

- time - timestamp of each reading, given in milliseconds
- acc (e_r) - linear acceleration in the direction the ball points in (along the major axis)
- acc (e_1) - linear acceleration along one of the minor axes
- acc (e_2) - linear acceleration along the other minor axis
- w (e_r) - angular velocity in the direction of the major axis
- w (e_1) - angular velocity in the direction of the first minor axis
- w (e_2) - angular velocity in the direction of the second minor axis
- euler (alpha) - change in bearing since sensors initialised
- euler (beta) - change in elevation/ pitch since sensors initialised
- euler (gamma) - change in orientation since sensors intiialised

This file should not be given too much focus as the processed data files contain the same information and more.

### Processed data files
TO DO

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
The onboard system is intended for a Arduino Nano Every, though it will work on a standard Arduino Nano. The offboard system functions without problem on an Arduino Uno. The post-processing system should function without problem on any commercial PC.

### Wiring diagram

#### Onboard system

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

Note that this diagram does not include the onboard power supply.

The offboard system has a Molex connector, which allows control of the system within the ball. The connections are as folows:

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

#### Offboard system

|   Arduino Uno    |    Device name and pin    |
|------------------|---------------------------|
| **5V**           | *113990010 Rx* **Vcc**    |
| **GND**          | *113990010 Rx* **GND**    |
| **D2**           | *113990010 Rx* **DATA**   |
| **A4**           | *Onboard system* **A4**   |
| **A5**           | *Onboard system* **A5**   |
| **GND**          | *Onboard system* **GND**  |

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

## Structure of repository

- **project-trubisky/** *#root directory*
	- **.vscode/** *#config files for running system from VS Code*
	- **data/** *#both raw and processed data are saved here*
	- **src/** *#code is stored here*
	- **.gitignore**
	- **README.md**

## To Do
- Post processing code
	- raw data files
		- delete raw data file when it's removed from tracker - delete processed data file too
	- processed data files
		- dereference processed data file from tracker if it gets deleted
		- remove offsets and convert units (m/s/s, rad/s, rad)
		- low pass filter/smoother - set parameters at beginning of method
		- remove any given column
		- discard zero readings as sensors haven't been set up properly
		- calculate speed in ball centred coordinates
		- calculate speed in x-y coordinates
		- calculate position in x-y coordinates
		- spiral rating (variance of spiral)
		- calculate angle of elevation
		- calculate angle wrt direction of throw
		- include a function that updates files already listed
		- graph any variables against each other (unspecified number of independent and dependent variables)
	- add more operations (metrics) - dependent on processed data
		- time of launch (when acceleration (without g) stops increasing)
		- launch speed
		- spiral rate
		- angle of attack (at launch)
		- angle wrt direction of throw (at launch)
	- add more functions for individual file analysis
		- plot speed against time
		- plot path in x-y coordinates
		- angle of attack
	- comments and docstrings (assume all docstrings are wrong - especially RE raw vs processed data)
	- finish interface for main python file