## Running Tootbot on Windows

Running Tootbot from the command line is simple. First, make sure your path is set to Tootbot's folder. For example, if the files are stored in a 'Tootbot' folder your desktop, you would run this:

```
cd Desktop\Tootbot
```

Then start up Tootbot with this command:

```
python tootbot.py
```

### Starting Tootbot on boot

To automatically start Tootbot when you log in, you have to create a simple batch file and place it in the Startup Items for your user account. First, open Notepad and paste the following script (replace `C:\Tootbot` with the actual path to your Tootbot folder):

```
@echo off
cd "C:\Tootbot"
:python
py ./tootbot.py
goto python
```

This script sets the current directory to your Tootbot folder and runs Tootbot in a loop. This way, if Tootbot crashes for some reason, it will automatically restart. Save the script to your desktop, with the ending `.bat` instead of `.txt`.

Next, open the Windows Run dialog (`WIN + R` or right-click on Start button and select 'Run'), type the below command, and press Enter:

```
shell:startup
```

This will open the Startup folder for your Windows account. Simply drag the batch file you made with Notepad into this folder. The next time you log in, Tootbot should start automatically in a CMD window!

## Running Tootbot on Mac/Linux

Running Tootbot from the Terminal is simple. First, make sure your path is set to Tootbot's folder. For example, if the files are stored in a 'Tootbot' folder your desktop, you would run this:

```
cd ~/Desktop/Tootbot
```

Then start up Tootbot with this command:

```
python tootbot.py
```