import serial
import requests
import math
import threading
import time

start_seq = '$START '
end_seq = ' $END'

#target_ip = 'http://192.168.4.1/'
target_ip = 'http://localhost/'

datastream = serial.Serial(port='COM13', baudrate=9600)

btn1, btn2, joybtn, axis0_raw, axis1_raw = False, False, False, 512, 512

def SerialMonitorThread():
    global btn1, btn2, joybtn, axis0_raw, axis1_raw
    while True:
        try:
            data = datastream.readline().decode().strip()
            if data[:len(start_seq)] == start_seq and data[-len(end_seq):] == end_seq:
                data = data.removeprefix(start_seq)
                data = data.removesuffix(end_seq)
                btn1, btn2, joybtn, axis0_raw, axis1_raw = map(int, data.split(' '))
        except UnicodeError:
            pass

def RequestsThread():
    is_stop = True
    while True:
        axis0 = axis0_raw / 512 - 1
        axis1 = axis1_raw / 512 - 1

        magnitude = min(math.sqrt((axis0 ** 2) + (axis1 ** 2)) * 100, 100)
        angle = math.degrees(math.atan2(axis0, axis1))
        angle = angle % 360

        magnitude = int(magnitude)
        angle = int(angle)

        if magnitude > 50:
            if btn1:
                is_stop = False
                print('Drive spin left')
                requests.get(target_ip + 'setspeeddirrot?speed=' + str(magnitude) +
                             '&direction=' + str(angle) + '&rotation=-20')
            elif btn2:
                is_stop = False
                print('Drive spin right')
                requests.get(target_ip + 'setspeeddirrot?speed=' + str(magnitude) +
                             '&direction=' + str(angle) + '&rotation=20')
            elif joybtn:
                is_stop = False
                print('Orientation')
                requests.get(target_ip + 'setspeeddir?speed=10&direction=' + str(angle))
            else:
                is_stop = False
                print('Drive')
                requests.get(target_ip + 'setspeeddir?speed=' + str(magnitude) + '&direction=' + str(angle))

        elif btn1:
            is_stop = False
            print("Spin left")
            requests.get(target_ip + '/drive_cmd/spinleft')
        elif btn2:
            is_stop = False
            print("Spin right")
            requests.get(target_ip + '/drive_cmd/spinright')
        elif not is_stop:
            print("Stop")
            requests.get(target_ip + '/drive_cmd/stop')
            is_stop = True

        time.sleep(0.01)


def main():
    t = threading.Thread(target=SerialMonitorThread)
    t.start()
    RequestsThread()




if __name__ == '__main__':
    main()