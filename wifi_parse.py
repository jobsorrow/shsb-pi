import os
os.system("sudo iwlist wlan0 scan > /home/pi/shsb-pi/wifiscan_result.txt")
wifiscan_result = open('/home/pi/shsb-pi/wifiscan_result.txt')
wifi_result = [line.strip() for line in wifiscan_result ]
cell_dict = dict()

wifiscan_result.close()
