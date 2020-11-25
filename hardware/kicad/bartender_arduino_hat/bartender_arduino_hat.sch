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
L Connector:Conn_01x03_Female J3
U 1 1 610130DF
P 5650 4050
F 0 "J3" V 5496 4198 50  0000 L CNN
F 1 "JST" V 5587 4198 50  0000 L CNN
F 2 "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" H 5650 4050 50  0001 C CNN
F 3 "~" H 5650 4050 50  0001 C CNN
	1    5650 4050
	0    1    1    0   
$EndComp
$Comp
L Connector:Conn_01x04_Male J4
U 1 1 61014290
P 6150 3700
F 0 "J4" H 6122 3582 50  0000 R CNN
F 1 "Arduino_Right" H 6122 3673 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" H 6150 3700 50  0001 C CNN
F 3 "~" H 6150 3700 50  0001 C CNN
	1    6150 3700
	-1   0    0    1   
$EndComp
$Comp
L Connector:Conn_01x06_Male J2
U 1 1 610150C3
P 5650 3150
F 0 "J2" V 5712 3394 50  0000 L CNN
F 1 "Arduino_Top" V 5803 3394 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical" H 5650 3150 50  0001 C CNN
F 3 "~" H 5650 3150 50  0001 C CNN
	1    5650 3150
	0    1    1    0   
$EndComp
$Comp
L Connector:Conn_01x06_Male J1
U 1 1 61015A81
P 5050 3650
F 0 "J1" H 5158 4031 50  0000 C CNN
F 1 "Arduino_Left" H 5158 3940 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical" H 5050 3650 50  0001 C CNN
F 3 "~" H 5050 3650 50  0001 C CNN
	1    5050 3650
	1    0    0    -1  
$EndComp
Text Label 5650 3750 1    50   ~ 0
GND
Text Label 5550 3750 1    50   ~ 0
5V
Text Label 5750 3750 1    50   ~ 0
D9
Wire Wire Line
	5650 3350 5650 3550
Wire Wire Line
	5650 3550 5750 3550
Wire Wire Line
	5750 3550 5750 3850
Wire Wire Line
	5250 3550 5600 3550
Wire Wire Line
	5600 3550 5600 3600
Wire Wire Line
	5600 3600 5650 3600
Wire Wire Line
	5650 3600 5650 3850
Wire Wire Line
	5250 3450 5550 3450
Wire Wire Line
	5550 3450 5550 3850
$EndSCHEMATC
