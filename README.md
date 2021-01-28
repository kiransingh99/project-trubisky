
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
- Seeed 113990010: RF transmitter

This system collectes data from the two sensors and writes it to a file on the SD card. Each throw of the ball requires the corresponding data to be saved in a new file. Using user inputs, the system can be reset, and the data can be transmitted or deleted. The data is saved to a file as this is faster than transmitting it as it is measured, so this allows for a higher frequency of data readings. The accelerometer and gyroscope together track 6 degrees of freedom, which completely describes a rigid body; therefore these sensors are sufficient to fully monitor the ball's motion.

### Offboard system
This system is not connected to the ball, but is connected to a PC. It is comprised of:
- Arduino Uno: processor
- Seeed 113990010: RF receiver
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

## Hardware requirements
The onboard system is intended for a Arduino Nano Every, though it has yet to be tested on one. It will not work in its current state on a standard Arduino Nano as the inbuilt storage is not sufficient, and some parts of the code do not fit in the available space. It may be theoretically possible to compress the compiled code to make it fit but currently this has not been done. An Arduino Uno would not solve the memory issue, as it has the same storage capacity as an Arduino Nano. An Arduino Mega does solve this problem, but significantly increases the mass of the onboard system.

The offboard system functions without problem on an Arduino Uno.

The post-processing system should function without problem on any commercial PC.

### Wiring diagram

#### Onboard system

| Arduino Nano | Device name and pin |
|--------------|---------------------|
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
| **5V**           | *113990010 Tx* **Vcc**    |
| **GND**          | *113990010 Tx* **GND**    |
| **D5**           | *113990010 Tx* **DATA**   |

Note that you can add a 17cm antenna onto the transmitter. This diagram does not include the onboard power supply.

#### Offboard system

| Arduino Uno | Device name and pin |
|-------------|---------------------|
| **5V**          | *113990010 Rx* **Vcc**    |
| **GND**         | *113990010 Rx* **GND**    |
| **D2**          | *113990010 Rx* **DATA**   |

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
	- **data/** *#both raw and processed data are saved here*
	- **src/** *#code is stored here*
	- **.gitignore**
	- **README.md**

## To Do
- Off board code
- Post processing code
	- check if file is okay as a csv (i.e. it is healthy) - print out any issues - only check previously unchecked files
	- get individual metrics and write them to a global tracker file (track file names too) - only check healthy files
	- figure out how to add different types of information to global tracker (and ensure that any files added later also collect this information)
	- figure out how to add info from more files to global tracker
	- use global tracker to 