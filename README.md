# Pokedex
## Pokemon Index w/ Type weakness

Executable is for Windows.

Python 3.4 w/ wxPython.

Some features will not work with Linux.

For executable to run properly, keep Pokedex folder structure as is.

### **To Run the pokedex.exe file:**
1. Download the following items:
  * Images Directory
  * pokedata.cfg
  * pokedata.default.cfg
  * pokedex.exe
2. Keep structure level the same
  * *This is because the paths are relative in the code*
3. Run the exe


### **To Run the pokedex.py file:**
1. Download Python 3.4: https://www.python.org/downloads/
2. Go to http://wxpython.org/Phoenix/snapshot-builds/ and copy link address of the correct file for your Python version
  * Example:
    * _wxPython_Phoenix-3.0.3.\<ignore this\>-cp34-none-win_amd64.whl_ would by Python 3.4 (cp34) 64-bit (amd64).
    * _wxPython_Phoenix-3.0.3.\<ignore this\>-cp34-none-win32.whl_ would by Python 3.4 (cp34) 32-bit (win32).
3. Go to Python directory contain "python.exe" in command prompt and run the following:
  >python.exe -m ensurepip
  
  >python.exe -m pip install \<paste link\>
  
  
### **Note if you get these errors:**
* **vcvarsall.bat doesn't exist:**
  * Go and Download Visual C++ 2010 @ http://www.microsoft.com/en-us/download/details.aspx?id=5555



* **module <name> doesn't exist:**
  >python.exe -m pip install \<name\>

  * If that doens't work, google "\<name\> python" and download the correct library
