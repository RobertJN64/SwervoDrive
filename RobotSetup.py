import os

def install():
    wifiname = input("Enter wifi name: ")
    wifipass = input("Enter wifi passcode (8-64 chars): ")
    if not (8 <= len(wifipass) <= 64):
        print("Wifi pass does not meet length requirements. Installer terminated.")
        return

    print("Installing crontab lib")
    os.system("sudo pip3 install python-crontab")

    print("Enabling i2c")
    os.system("sudo raspi-config nonint do_i2c 0")

    #print("Installing explorerhat lib")
    #os.system("sudo apt-get install python3-explorerhat")

    print("Installing flask")
    os.system("sudo pip install flask")

    print("Installing hostapd")
    os.system('sudo apt install hostapd')

    print("Installing dnsmasq")
    os.system("sudo apt install dnsmasq")

    print("Enabling hostapd")
    os.system("sudo systemctl unmask hostapd")
    os.system("sudo systemctl enable hostapd")

    print("Editing dhcpd.conf file")
    with open("/etc/dhcpcd.conf", "a") as f:
        f.write("interface wlan0" + '\n')
        f.write("static ip_address=192.168.4.1/24" + '\n')
        f.write("nohook wpa_supplicant" + '\n')

    print("Copying dnsmasq.conf file to dnsmasq.conf.orig")
    with open("/etc/dnsmasq.conf") as f:
        with open("/etc/dnsmasq.conf.orig", "w+") as f2:
            for line in f.readlines():
                f2.write(line)

    print("Editing dnsmasq.conf file")
    with open("/etc/dnsmasq.conf", "a") as f:
        f.write("interface=wlan0 # Listening interface" + '\n')
        f.write("dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h" + '\n')
        f.write("                # Pool of IP addresses served via DHCP" + '\n')
        f.write("domain=wlan     # Local wireless DNS domain" + '\n')
        f.write("address=/gw.wlan/192.168.4.1")
        f.write("                # Alias for this router" + '\n')

    print("Editing hostpad.conf file")
    with open("/etc/hostapd/hostapd.conf", "w+") as f:
        f.write("country_code=US" + '\n')
        f.write("interface=wlan0" + '\n')
        f.write("ssid=" + wifiname + '\n')
        f.write("hw_mode=g" + '\n')
        f.write("channel=7" + '\n')
        f.write("macaddr_acl=0" + '\n')
        f.write("auth_algs=1" + '\n')
        f.write("ignore_broadcast_ssid=0" + '\n')
        f.write("wpa=2" + '\n')
        f.write("wpa_passphrase=" + wifipass + '\n')
        f.write("wpa_key_mgmt=WPA-PSK" + '\n')
        f.write("wpa_pairwise=TKIP" + '\n')
        f.write("rsn_pairwise=CCMP" + '\n')

    try:
        print("Editing crontab")
        from crontab import CronTab
        cron = CronTab(user='pi')  # current users cron
        directory = '/home/pi/Desktop/SwervoDrive/'
        command = 'cd ' + directory +' && sudo python3 main.py > ' + directory + 'logs.txt 2>&1'
        job = cron.new(command='sudo cp ' + directory + 'logs.txt ' + directory + 'logsold.txt',
                 comment='Backup 2 versions of log files.')
        job.every_reboot()
        job = cron.new(command=command, comment='Run Robot Script')
        job.every_reboot()
        cron.write() #save crontab

    except ImportError:
        print("ERROR: Crontab module not found. Crontab is necessary and should have been",
              "installed automatically. Try installing it manually and run the installer again.")
        return


    print("Installing finished! Please reboot your device. If a wifi network is not created,"
          "check the config files. For questions, contact robertjnies+swervedrive@gmail.com")


print("WARNING! This installer will make permanent changes to your computer!",
      "Only run if you are on a RaspberryPi running linux and connected to wifi.",
      "This script must be run with root permissions (sudo)",
      "After the installer finishes, please reboot the computer.")

if input("Continue y/n: ") == 'y':
    install()
else:
    print("Installer canceled.")