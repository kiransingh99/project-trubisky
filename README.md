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
- ADXL345 (triple-axis accelerometer): measures linear acceleration
- L3GD20H (triple axis gyroscope): measures angular velocity
- Micro SD Breakout Board: stores data onboard

This system collectes data from the two sensors and writes it to a file on the SD card. Each throw of the ball requires the corresponding data to be saved in a new file. Using user inputs, the system can be reset, and the data can be transmitted or deleted. The data is saved to a file as this is faster than transmitting it as it is measured, so this allows for a higher frequency of data readings. The accelerometer and gyroscope together track 6 degrees of freedom, which completely describes a rigid body; therefore these sensors are sufficient to fully monitor the ball's motion.

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

### Global tracker file

The global tracker file is the summary of the data of each of the throws of the ball. Each column gives the value of another metric for each file listed in the tracker. An explanation of the columns are as follows:

- **name**: the name of the raw data file, starting with its parent directory
- **health status**: a code explaining the result of the last health check done on the raw data file, where:
	- 0 means untested
	- 1 means failed
	- 2 means passed with warnings
	- 3 means passed without warnings
- **time of throw**: the total time of recording for each file (milliseconds)

## Hardware requirements
The onboard system is intended for a Arduino Nano Every, though it will work on a standard Arduino Nano. The offboard system functions without problem on an Arduino Uno. The post-processing system should function without problem on any commercial PC.

### Wiring diagram

#### Onboard system

|   Arduino Nano   |    Device name and pin    |
|------------------|---------------------------|
| **5V**           | *ADXL345* **Vin**         |
| **GND**          | *ADXL345* **GND**         |
| **A4**           | *ADXL345* **SDA**         |
| **A5**           | *ADXL345* **SCL**         |
| **3.3V**         | *L3GD20H* **Vin**         |
| **GND**          | *L3GD20H* **GND**         |
| **A4**           | *L3GD20H* **SDA**         |
| **A5**           | *L3GD20H* **SCL**         |
| **5V**           | *Micro SD Module* **5V**  |
| **GND**          | *Micro SD Module* **GND** |
| **D10**          | *Micro SD Module* **CS**  |
| **D11**          | *Micro SD Module* **DI**  |
| **D12**          | *Micro SD Module* **DO**  |
| **D13**          | *Micro SD Module* **CLK** |
| **A4**           | *Arduino Uno* **A4**      |
| **A5**           | *Arduino Uno* **A5**      |

Note that this diagram does not include the onboard power supply.

#### Offboard system

|   Arduino Uno    |    Device name and pin    |
|------------------|---------------------------|
| **5V**           | *113990010 Rx* **Vcc**    |
| **GND**          | *113990010 Rx* **GND**    |
| **D2**           | *113990010 Rx* **DATA**   |
| **A4**           | *Arduino Nano* **A4**     |
| **A5**           | *Arduino Nano* **A5**     |

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
	- create a class which converts raw data into processed data files - similar to global_tracker code. It will need to:
		- remove gravity from acceleration
		- calculate speed in x-y coordinates
		- calculate spiral rate
		- calculate position in x-y coordinates
		- calculate angle of elevation
		- calculate angle wrt direction of throw
		- include a function that updates files already listed
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
	- finish interface for main python file