# Text_Based_Browser

This tool will enable the user to view their favorite websites without
the distracting ads and pictures. Just enter the desired URL and
get to reading!

## Installation:
The user has two options to run this browser:
1.  System Installation
2.  Virtual Environment (Recommended)

### System Installation
This repository includes a "requirements.txt" file which contains all the required modules to run the project. The project was built using Python 3.8.2, so if any issue occur due to incompitable function the user may have to switch to this version. To install the required modules simply run the following command in the project's root directory.
```
pip3 install -r requirements.txt
```

### Virtual Environment
This repository also includes a python virtual environment in the **"tbb"** directory. This environment holds a 3.8.2 version of Python with all the necessary modules already installed. This method is recommended because it does not require the user to install any additional modules onto their personal version of python. However, it is important to note that the user will have to activate the virtual environmemnt every time their open a new **terminal** session. The commands to run the environment on Windows and Unix based systems can be found below.

**Unix Based (MacOs/Linux):**
```
source tbb/Scripts/activate
```
**Windows:**
```
tbb\Scripts\activate.bat
```

If the user wishes to close the environment without closing their session they can run the following:

**Unix Based (MacOs/Linux) and Windows:**
```
deactivate
```

## Execution:
To run the program simply enter:
```
python browser.py tabs
```
If you are not using the virtual environment, you must specify **"python3"** in the above command.

When running the program you will be greeted with a welcome message that explains how to use the browser. You will then be prompted for either a command or URL. If you enter a URL the brower will search for the corresponding website and print the content. The additional commands available can be viewd in the table below.

Commands | Description
----- | ------
history | prints the stored history for your session
back | will reprint the last site in your history
bookmarks | enters bookmark sub-menu
exit | ends the session
help | prints help text



*Daniel Pelis, EE 551 Final Project*
