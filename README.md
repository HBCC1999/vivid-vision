# Vivid Vision By HBCC1999
A program that helps you with measures against myopia. It enforces pop-up notifications every 20 minutes (or the interval you specify) and sends you notification of either silent or critical intensity. Great if you want your eyes to not be affected as much during screen times.

# Setup
The program comes with a compiled installation wizard (VividVisionSetup.exe), that is compiled version of installation_wizard.iss (uses Inno setup to compile), and then it asks user for configuration (interval, intensity) to procede to another compiled exe (installer.exe), which installs config.json and uninstall.exe in localappdata and also puts the main program (VividVision.exe) in shell:startup, where it will run automatically at startup. However, windows defender is very strict about making changes to shell:startup and aborts this process while in execution. To avoid this, once you run the exe, go to Windows Secuity->Protection Hisotry->Quanrantined/Removed programs-> Restore VividVision.exe and installer.exe.

# Installation
Since most users wont bother with windows defender, an easier way is to copy the exe in dist/ and paste it in to your startup directory (Locate by C:\Users\UserName\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup or  by running shell:script command in Win + R). I really wanted this project to be very straight-forward, but Windows Defender's coming in the way.
