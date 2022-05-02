''' Python 3.7  for Dahua  by Dmytro Moisiuk '''
'''Script for carving video from DVR Dahua
Tested model: Dahua DHI-HCVR4104HS-S2, Dahua DHI-HCVR5108C-S3, EZ-IP NVR1A04-4P  
The following parameters should be changes at the end of the script:
f- image for analysis; 
blocksize-block size for analysis; 
quality - determine by byte with offset 0x1D in the integer from the beginning of the signature 0x44484156FD;
For all quality video use 'all' without quotation marks;
'''

import os
import sys
import hashlib
import re
import binascii
import wmi


def Time_conv(Time):
    Time_List = ['Time']
    Time_List.append(hex(Time))
    try:
        c = int(Time_List[1][4],16)
    except:
       print(error) 
    try:
        d = int(Time_List[1][5],16)
    except:
        print(error)
    try:
        b = int(Time_List[1][3],16)
    except:
        print(error)
    try:
        a = int(Time_List[1][2],16)
    except:
        print(error)
    try:    
        e = int(Time_List[1][6],16)
    except:
        print(error)    
    try:
        f = int(Time_List[1][7],16)
    except:
        print(error)
    try:
        g = int(Time_List[1][8],16)
    except:
        print(error)
    try:
        h = int(Time_List[1][9],16)
    except:
        print(error)
    #b = int(b,16)
    #print(b)
    if (((c % 4)*8 + d // 2))<10:
        dd = '0'+str(((c % 4)*8 + d // 2))
    else:
        dd = str(((c % 4)*8 + d // 2))
    if ((b % 4)*4+c//4)<10:
        mm = '0'+str((b % 4)*4+c//4)
    else:
        mm = str((b % 4)*4+c//4)
    if ((a*4) + b//4) < 10:
        yy = '0' + str((a*4) + b//4)
    else:
        yy = str((a*4) + b//4)
    if ((d%2)*16+e) < 10:
        hh = '0' + str((d%2)*16+e)
    else:
        hh = str((d%2)*16+e)
    if (f*4+g//4) < 10:
        min = '0' + str(f*4+g//4)
    else:
        min = str(f*4+g//4)
    if ((g%4)*16+h) < 10:
        ss = '0' + str((g%4)*16+h)
    else:
        ss = str((g%4)*16+h)

    data = yy + '.' + mm + '.'+ dd + '_' + hh + '_'+ min+ '_'+ ss
  #  print(data)
    return data

def carve_file(f,blocksize,quality,Spath):
    SignStr = b'\x44\x48\x41\x56\xFD'
#    SignStr = b'\x44\x48\x41\x56'
    SignEnd = b'\x64\x68\x61\x76'
    regexStr = re.compile(SignStr)
    i = 0
    k = 0
    l = -1
    c = 0
    StartOffset = 0
    EndOffset = 0
    FirstCam = b'\x00'
    m = hashlib.md5()
    SOF_List = ['start']
    EOF_List = ['start-21']
    Time_List = ['Time']
    Cam_List = ['Cam']
    Qual_List = ['Quality']
    while True:
        buf = f.read(blocksize)
        l = l + 1
        if not buf:
            break
        m.update( buf )

        for match_obj in regexStr.finditer(buf):
            offsetSt = match_obj.start()
            tmp = str(int(l * blocksize + offsetSt))
#            offsetEd = match_obj.end()
#            print "hexSt: " + hex(offsetSt)
#            print "hexEd: " + hex(offsetEd)
            if i == 0:
                StartOffset = offsetSt
                FirstCam = int.from_bytes(buf[offsetSt+6:offsetSt+8],byteorder='little')+1
                FirstDate_ = int.from_bytes((buf[offsetSt + 16:offsetSt + 20]),byteorder='little')  # int little endian
                FirstDate = int.from_bytes((buf[offsetSt + 16:offsetSt + 20]),byteorder='little') # int little endian
                FirstQual = int.from_bytes(buf[offsetSt + 29:offsetSt + 30],byteorder='big')
                i = 1
            else:
                cam = int.from_bytes(buf[offsetSt + 6:offsetSt + 8], byteorder='little') + 1

                dateK = int.from_bytes((buf[offsetSt + 16:offsetSt + 20]),byteorder='little') #int little endian
                delta = dateK - FirstDate
                Qual = int.from_bytes(buf[offsetSt + 29:offsetSt + 30],byteorder = 'big')
#                print (delta)
                if (FirstCam == cam) and (delta <= 2) and (delta > 0):
                    FirstDate = dateK
                    c = 0
                    EndOffset = offsetSt - 1
                else:
                        EndOffset = offsetSt-1
                        subdata = buf[StartOffset:EndOffset]
                        if (FirstQual == quality) or (quality == all):
                            try:
                                time_s = Time_conv(FirstDate)
                            except:
                                time_s = '000000'
                            #time_e = Time_conv(FirstDate)

                            #filename = "N:\start_"+ time_s + '_' + str(int(l * blocksize + StartOffset)) + "_" + str(int(l * blocksize + EndOffset)) + "_" + "Cam_" + str(FirstCam) + '.dav'
                            try:
                                filename = Spath +  "\Cam_"+ str(FirstCam)+ '_' + Time_conv(FirstDate_) + '-'+ Time_conv(FirstDate)+'_' + str(int(l * blocksize + StartOffset+jump)) + "_" + str(int(l * blocksize + EndOffset+jump)) + '.dav'
                            except:
                                filename = Spath +  "\Cam_"+ str(FirstCam)+ '_' + '000000' + '-'+ '000000'+'_' + str(int(l * blocksize + StartOffset+jump)) + "_" + str(int(l * blocksize + EndOffset+jump)) + '.dav'

                            copy_file = open(filename,'wb')
                            copy_file.write(subdata)
                            copy_file.close()
#                    copy_file = open('J:\Cunk_'+ str(l), 'wb')
#                    copy_file.write(buf)
#                    copy_file.close()
                            c = 1
                            print(filename)
                        StartOffset = offsetSt
                        FirstCam = int.from_bytes(buf[offsetSt + 6:offsetSt + 8], byteorder='little') + 1
                        FirstDate = int.from_bytes((buf[offsetSt + 16:offsetSt + 20]),byteorder='little')  #int little endian
                        FirstDate_ = int.from_bytes((buf[offsetSt + 16:offsetSt + 20]),byteorder='little')  #int little endian
                        FirstQual = int.from_bytes(buf[offsetSt + 29:offsetSt + 30], byteorder='big')
                        i = 1
                        k = k + 1


        if (c == 0)and (StartOffset != 0) and (EndOffset != 0) :
            if (FirstQual == quality) or (quality == all):
                subdata = buf[StartOffset:EndOffset]
                filename = Spath +  "\Cam_"+ str(FirstCam)+ '_' + Time_conv(FirstDate_)+ '-'+ Time_conv(FirstDate)+'_' + str(int(l * blocksize + StartOffset+jump)) + "_" + str(int(l * blocksize + EndOffset+jump)) +  '.dav'
                copy_file = open(filename, 'wb')
                copy_file.write(subdata)
                copy_file.close()
                StartOffset = 0
                EndOffset = 0
                k = k + 1
        print (SOF_List)
#        print (Cam_List)
#        print (Time_List)
#        print (Qual_List)
        print('chunk_' + str(l))
        print('Copy '+str(k)+ ' -s')
    return m.hexdigest()
#    return SOF_List

'''you need to make changes '''


#************* Start source block***************#

Disk_List = ['Disk List']
Disk_info = ['Disk info']
c = wmi.WMI()
for diskDrive in c.query("SELECT * FROM Win32_DiskDrive"):
    Disk_List.append(diskDrive.Name)
    Disk_info.append(diskDrive.model)
#    print(Disk_List)
l = 1
print("Available drives:")
while l < len(Disk_List):
    print(l, ".", Disk_List[l]," Model:",Disk_info[l])
    l += 1
cmd = input("Enter number: ")    
 
#f=open('\\\\.\\PhysicalDrive1','rb') #  Work with connected Drive
f=open(Disk_List[int(cmd)],'rb')
#f=open('L:\TOSHIBA HDWD110.001','rb')    # Work with RAW image  

#****************End source block*******************#


print("Enter destination path:   Example: H:\Video")
cmd = input("Enter path: ")    
Spath = cmd
#Spath = "H:\Video_Ez-IP" # Destination path   
print(Spath)

jump=0 # bytes multiple sector size (example:1174305148928)
f.seek(jump,0) #move the file pointer forward by jump bytes from start of the file
print('jump to: ', jump ,'  ok')
blocksize=2**30  # Block size
quality = all   # Quality of video frames. For all type of quality use 'all' without quotation marks.

print(carve_file(f,blocksize,quality,Spath))  #f- image for analysis; blocksize-block size for analysis; quality - determine by byte with offset 0x1D in the integer from the beginning of the signature 0x44484156FD;

