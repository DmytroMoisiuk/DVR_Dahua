### DVR_Dahua_Python
Python 3.7
Script for recovering video from DHFS4.1

#### Tested devices:

- Dahua DHI-HCVR4104HS-S2
- Dahua DHI-HCVR5108C-S3
- EZ-IP NVR1A04-4P


#### Usage:

#### Step 1:
- Change variables at the end of the script;

    (f- RAW image or connected Drive; 
  blocksize-block size for analysis; 
  quality - determine by byte with offset 0x1D in the integer from the beginning of the signature 0x44484156FD. For all video use 'all' without quotation marks ) 

#### Step 2:
- Execute the script.

Executing the script is very easy: Simply open a terminal (on Windows: [Win] + [R] -> enter "cmd" and press enter). At first you have to switch to the directory where the script is located and then you can fire up the Python interpreter.

 Linux:
cd /path/to/script/
python Python_3.7_Dahua_07.05.19.py 

 Windows:
cd C:\Path\to\script\
python Python_3.7_Dahua_07.05.19.py



#### Homepage and Contact:

Dmytro Moisiuk  
e-mail:dm.moisiuk@gmail.com
https://github.com/DmytroMoisiuk/DVR_Dahua

Feel free to contact me if you have any additional suggestions or you've found a bug. Feedback is always welcome! 
