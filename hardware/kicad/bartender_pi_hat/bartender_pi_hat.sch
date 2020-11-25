EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Connector:Raspberry_Pi_2_3 J1
U 1 1 60B0BE25
P 2700 3650
F 0 "J1" H 2700 5131 50  0000 C CNN
F 1 "Raspberry_Pi" H 2700 5040 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_2x20_P2.54mm_Vertical" H 2700 3650 50  0001 C CNN
F 3 "https://www.raspberrypi.org/documentation/hardware/raspberrypi/schematics/rpi_SCH_3bplus_1p0_reduced.pdf" H 2700 3650 50  0001 C CNN
	1    2700 3650
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x04_Female J4
U 1 1 60B185D5
P 7000 5200
F 0 "J4" H 7028 5176 50  0000 L CNN
F 1 "Scale Connector" H 7028 5085 50  0000 L CNN
F 2 "Connector_JST:JST_XH_B4B-XH-A_1x04_P2.50mm_Vertical" H 7000 5200 50  0001 C CNN
F 3 "~" H 7000 5200 50  0001 C CNN
	1    7000 5200
	1    0    0    -1  
$EndComp
Wire Wire Line
	3000 4950 3350 4950
Wire Wire Line
	1900 3650 1700 3650
Wire Wire Line
	1700 3650 1700 5250
Wire Wire Line
	1700 5250 5050 5250
Wire Wire Line
	5050 5250 5050 3300
Wire Wire Line
	5050 3300 6800 3300
Wire Wire Line
	1650 5300 5100 5300
Wire Wire Line
	5100 5300 5100 3400
Wire Wire Line
	5100 3400 6800 3400
Wire Wire Line
	1600 5350 5150 5350
Wire Wire Line
	5150 5350 5150 3500
Wire Wire Line
	5150 3500 6800 3500
Wire Wire Line
	1550 5400 5200 5400
Wire Wire Line
	5200 5400 5200 3600
Wire Wire Line
	5200 3600 6800 3600
Wire Wire Line
	1500 5450 5250 5450
Wire Wire Line
	5250 5450 5250 3700
Wire Wire Line
	5250 3700 6800 3700
Wire Wire Line
	5300 5500 5300 3800
Wire Wire Line
	5300 3800 6800 3800
Wire Wire Line
	5350 5550 5350 3900
Wire Wire Line
	5350 3900 6800 3900
Wire Wire Line
	3500 4350 3950 4350
Wire Wire Line
	5400 5600 5400 4000
Wire Wire Line
	5400 4000 6800 4000
Wire Wire Line
	5450 5650 5450 4100
Wire Wire Line
	5450 4100 6800 4100
Wire Wire Line
	1900 4350 1150 4350
Wire Wire Line
	5500 5700 5500 4200
Wire Wire Line
	5500 4200 6800 4200
Wire Wire Line
	4800 4950 5550 4950
Wire Wire Line
	5550 4950 5550 4400
Connection ~ 4800 4950
$Comp
L power:GND #PWR0101
U 1 1 60BC753B
P 3350 5000
F 0 "#PWR0101" H 3350 4750 50  0001 C CNN
F 1 "GND" H 3355 4827 50  0000 C CNN
F 2 "" H 3350 5000 50  0001 C CNN
F 3 "" H 3350 5000 50  0001 C CNN
	1    3350 5000
	1    0    0    -1  
$EndComp
Wire Wire Line
	3350 5000 3350 4950
Connection ~ 3350 4950
Wire Wire Line
	3350 4950 4800 4950
Wire Wire Line
	4400 2150 4400 6000
Wire Wire Line
	4400 6000 6000 6000
Wire Wire Line
	6000 6000 6000 5100
Wire Wire Line
	6000 5100 6800 5100
Wire Wire Line
	4800 4950 4800 6250
Wire Wire Line
	4800 6250 6150 6250
Wire Wire Line
	6150 6250 6150 5400
Wire Wire Line
	6150 5400 6800 5400
Wire Wire Line
	3500 3450 4300 3450
Wire Wire Line
	4300 3450 4300 6100
Wire Wire Line
	4300 6100 6050 6100
Wire Wire Line
	6050 6100 6050 5200
Wire Wire Line
	6050 5200 6800 5200
Wire Wire Line
	3500 3550 4200 3550
Wire Wire Line
	4200 3550 4200 6150
Wire Wire Line
	4200 6150 6100 6150
Wire Wire Line
	6100 6150 6100 5300
Wire Wire Line
	6100 5300 6800 5300
Wire Wire Line
	5300 5500 3950 5500
Wire Wire Line
	3950 5500 3950 4350
Wire Wire Line
	1250 5550 5350 5550
Wire Wire Line
	1200 5600 5400 5600
Wire Wire Line
	3500 3350 3900 3350
$Comp
L Connector:Conn_01x02_Female J5
U 1 1 60C169B2
P 7350 4650
F 0 "J5" H 7378 4626 50  0000 L CNN
F 1 "12V Output" H 7378 4535 50  0000 L CNN
F 2 "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical" H 7350 4650 50  0001 C CNN
F 3 "~" H 7350 4650 50  0001 C CNN
	1    7350 4650
	1    0    0    -1  
$EndComp
Wire Wire Line
	6500 4400 6500 4750
Wire Wire Line
	6500 4750 7150 4750
Connection ~ 6500 4400
Wire Wire Line
	6500 4400 6800 4400
Text Label 6300 3300 0    50   ~ 0
Pump1
Text Label 6300 3400 0    50   ~ 0
Pump2
Text Label 6300 3500 0    50   ~ 0
Pump3
Text Label 6300 3600 0    50   ~ 0
Pump4
Text Label 6300 3700 0    50   ~ 0
Pump5
Text Label 6300 3800 0    50   ~ 0
Pump6
Text Label 6300 3900 0    50   ~ 0
Pump7
Text Label 6300 4000 0    50   ~ 0
Pump8
Text Label 6300 4100 0    50   ~ 0
Pump9
Text Label 6300 4200 0    50   ~ 0
Pump10
Text Label 6300 4300 0    50   ~ 0
12v
Text Label 6300 4400 0    50   ~ 0
GND
Wire Wire Line
	5550 4400 6500 4400
Wire Wire Line
	6150 4300 6150 4650
Wire Wire Line
	6150 4300 6800 4300
Wire Wire Line
	6150 4650 7150 4650
Text Label 6550 5100 0    50   ~ 0
3v3
Text Label 6550 5200 0    50   ~ 0
DT
Text Label 6400 5300 0    50   ~ 0
Scale_SCK
Text Label 6550 5400 0    50   ~ 0
GND
Wire Wire Line
	2800 2150 2800 2350
Wire Wire Line
	2800 2150 4400 2150
$Comp
L Connector:Conn_01x12_Female J3
U 1 1 60B19650
P 7000 3900
F 0 "J3" H 7028 3876 50  0000 L CNN
F 1 "Pump Connector" H 7028 3785 50  0000 L CNN
F 2 "Connector_JST:JST_XH_B12B-XH-A_1x12_P2.50mm_Vertical" H 7000 3900 50  0001 C CNN
F 3 "~" H 7000 3900 50  0001 C CNN
	1    7000 3900
	1    0    0    1   
$EndComp
Wire Wire Line
	1150 4350 1150 5650
Wire Wire Line
	3900 3350 3900 5700
Wire Wire Line
	5450 5650 1150 5650
Wire Wire Line
	3900 5700 5500 5700
Wire Wire Line
	1250 3850 1900 3850
Wire Wire Line
	1250 3850 1250 5550
Wire Wire Line
	1200 5600 1200 3950
Wire Wire Line
	1200 3950 1900 3950
Wire Wire Line
	1500 3050 1900 3050
Wire Wire Line
	1500 3050 1500 5450
Wire Wire Line
	1550 5400 1550 3450
Wire Wire Line
	1550 3450 1900 3450
Wire Wire Line
	1600 3550 1900 3550
Wire Wire Line
	1600 3550 1600 5350
Wire Wire Line
	1650 5300 1650 4250
Wire Wire Line
	1650 4250 1900 4250
$EndSCHEMATC
