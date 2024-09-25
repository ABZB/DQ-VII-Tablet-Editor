from ctypes.wintypes import BYTE
import os
from tkinter.filedialog import askopenfilename



def standalone_checksum():
    source_file = askopenfilename(title = 'Select Save File')

    savedata = []

    with open(source_file,"r+b") as f:
        #get file length
        f.seek(0, os.SEEK_END)
        file_end = f.tell()
        f.seek(0, 0)
        block = f.read(file_end)
    
        #kth byte is kth entry in list
        for ch in block:
            savedata.append(ch)
        

        checksum = 0

        for x in range(16,len(savedata) - 1):
            #interpret the byte as a signed 1-byte integer
            if((savedata[x] & 128) == 128):
                checksum += (savedata[x] & 127) - 128
            else:
                checksum += savedata[x]
        
        output_bytes = []
        for x in range(4):
            output_bytes.append(checksum & 0xFF)
            checksum = checksum >> 8

        f.seek(0, 0)

        for x in output_bytes:
            f.write(BYTE(x))

        print(output_bytes)
        

def write_checksum(savedata):
    checksum = 0

    for x in range(16,len(savedata) - 1):
     #interpret the byte as a signed 1-byte integer
        if((savedata[x] & 128) == 128):
            checksum += (savedata[x] & 127) - 128
        else:
            checksum += savedata[x]
        
    
    for x in range(4):
        savedata[x] = checksum & 0xFF
        checksum = checksum >> 8

    return(savedata)


def main():
    standalone_checksum()

if __name__ == '__main__':
	main()