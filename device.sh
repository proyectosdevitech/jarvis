#!/bin/bash

echo "Disconnecting old connections..."
adb disconnect

echo "Setting up connected device..."
adb tcpip 5555

echo "Waiting for device to initialize..."
sleep 3

# Obtener la IP del dispositivo conectado por adb
ipfull=$(adb shell ip addr show wlan0 | grep "inet " | awk '{print $2}')
ip=${ipfull%%/*}

echo "Connecting to device with IP $ip..."
adb connect "$ip"

# Configuración manual para conexión a un dispositivo específico
DEVICE_IP="192.168.1.7"
ADB_PORT="5555"

echo "Restarting the ADB server..."
adb kill-server
adb start-server

echo "Connecting to the Android device over Wi-Fi..."
adb connect "$DEVICE_IP:$ADB_PORT"
