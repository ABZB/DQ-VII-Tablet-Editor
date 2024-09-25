from tkinter.filedialog import asksaveasfilename
from dqviichecksum import *
from tkinter import asksaveasfilename, askopenfilename

def export_to_CSV():
    
    game_file_path = askopenfilename("Select your save file (Save000.bin is Quicksave, 001-003 are Adventure Logs)")

    csv_file_path = asksaveasfilename("Save exported data as CSV", defaultextension=".csv", filetypes=(("CSV file", "*.csv"),))

    savedata = []

    with open(game_file_path,"r+b") as f:
        #get file length
        f.seek(0, os.SEEK_END)
        file_end = f.tell()
        f.seek(0, 0)
        block = f.read(file_end)
    
        #kth byte is kth entry in list
        for ch in block:
            savedata.append(ch)
    
    save_size = len(savedata)

    #check to see if we're really in the right spot
    if(savedata[0x32C0] == 0x53 and savedata[0x32C1] == 0x55 and savedata[0x32C2] == 0x52 and savedata[0x32C3] == 0x45):
        cur = 0x32CC
    else:
        print('Did not find expected Tablet header in location, searching')
        cur = 0
        while True:
            if(cur + 3 == save_size):
                print('Something is wrong, exiting')
                break
            elif(savedata[cur] == 0x53 and savedata[cur + 1] == 0x55 and savedata[cur + 2] == 0x52 and savedata[cur + 3] == 0x45):
                cur += 0x0C
                
    #first 16 are 0x34 bytes each, and are your found tablets
    
    








while True:
    option = int(input("Export Tablets to CSV (C) or Write CSV to Save (S)"))
    if(option in {'C', 'c'}):
        export_to_CSV()
        break
    elif(option in {'S', 's'}):
        export_to_Save()
        break