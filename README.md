# EchoTales

SETUP
Please follow the below steps to execute the project file.

1. Access the zip file Echo tales using any IDE: Open the extracted zip file in any IDE
like Visual studio or IntelliJ

3. Install Python3: Make sure that you have python3 installed in your system. You might
face issues if you have multiple versions of python installed in your system. So, it’s better
to make sure you only have python3 installed.
which python – Run this command in the terminal to see which python version is
downloaded.

4. Run file Echotales.py – you will come across the following errors, saying that modules
have not been installed or python is not available
Open the terminal in the path of the project file and run below command
python3 echotales.py
if this doesn’t work try,
python3_path_in_your_system echotales.py_path_in_your_system

5. If the systems asks you to download any tools please go ahead.
   
6. Now you have install few python libraries, before that lets make sure that you have pip
installed and it is updated. To check this, please run below commands
python3 -m ensurepip
python3 -m pip install --upgrade pip

7. Now install below libraries
python3 -m pip install pysofaconventions
python3 -m pip install scipy

8. Now to install pyaudio, you need to install homebrew and portaudio first
python3 -m pip install pyaudio , If you run this command you will get few errors which
are expected to get rid of the errors, execute below command
/bin/bash -c "$(curl -fsSL
https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
Note: After you execute this command, your terminal will give you Nextsteps , in which
you have to execute 2 commands. Please go ahead and execute those 2 commands.
Then execute the below command to install Port Audio
brew install portaudio
Now try installing pyAudio by using below command and it should start installing
python3 -m pip install pyaudio

9. Install pygame using below command.
python3 -m pip install pysofaconventions
10. Run the file Echotales.py now and it should run successfully.
python3 echotales.py




Once the UI comes up,
PRESS 1 – 4 keys to play audio
ALSO
PRESS 1 – 4 keys to PAUSE audio as well.
PRESS 1 – 4 keys to PAUSE audio as well.
