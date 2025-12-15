from optparse import Values
from tkinter.filedialog import asksaveasfilename
from turtle import update
from dqviichecksum import *
from tkinter import *
from tkinter import ttk
from constants import *
from string import capwords

def load_save_file():
    #load data
    global savedata
    savedata = []
    with open(askopenfilename(title = 'Select Save File'),"r+b") as f:
        #get file length
        f.seek(0, os.SEEK_END)
        file_end = f.tell()
        f.seek(0, 0)
        block = f.read(file_end)
        
        #kth byte is kth entry in list
        for ch in block:
            savedata.append(ch)
    return()


def write_save_file():
    global savedata
    global original_dlc_haven_list
    dlc_haven_count = 0
    for tablet_number in range(24):
        #sum up number of non-Empties
        new_tablet_name = dlc_haven_wdgs[tablet_number].get()
        if(new_tablet_name != 'Empty'):
            dlc_haven_count += 1

        #if name changed, update appropriately
        if(original_dlc_haven_list[tablet_number] != new_tablet_name):
            temp_pointer = 0x3610 + tablet_number*0x54

            for byte_index in range(0x54):
                savedata[temp_pointer + byte_index] = int(dlc_haven_tablet_hex_dict[new_tablet_name] [byte_index*2 : byte_index*2 + 2], base = 16)
    
    #update count of tablets
    savedata[0x3E04] = dlc_haven_count
    
    #update checksum
    savedata = write_checksum(savedata)


    #write file
    with open(asksaveasfilename(title = 'Select Save File'),"w+b") as f:
        
        for x in savedata:
            f.write(BYTE(x))


def update_all_fields():
    global savedata
    global original_dlc_haven_list

    #set string variables
    player_tablets_count_text.set('Player Tablet Count: ' + str(savedata[0x3E00]))
    fixed_tablets_count_text.set('Other Tablet Count: ' + str(savedata[0x3E04]))


    #update fixed tablets
    for i in range(24):
        temp_pointer = 0x3610 + i*0x54
        found_match_bool = False
        temp_name = ''
        
        for tabletname in dlc_haven_tablet_hex_dict.keys():
            for byte_index in range(0x54):
                #0xE and 0x32 are times-cleared
                if(int(dlc_haven_tablet_hex_dict[tabletname] [byte_index*2 : byte_index*2 + 2], base = 16) != savedata[temp_pointer + byte_index] and byte_index != 0xE and byte_index != 0x32):
                    found_match_bool = False
                    break
                else:
                    found_match_bool = True
                    temp_name = tabletname
            #if here and found_match_bool is true, we found a correct match, we want to set the corresponding button to the key
            if(found_match_bool):

                dlc_haven_wdgs[i].set(temp_name)
                original_dlc_haven_list.append(temp_name)
                break
            else:
                if(savedata[temp_pointer] == savedata[temp_pointer +1] == savedata[temp_pointer + 2] == savedata[temp_pointer + 3] == savedata[temp_pointer + 4] == savedata[temp_pointer + 5] == 0):
                    dlc_haven_wdgs[i].set('')
                    original_dlc_haven_list.append('')
                else:
                    dlc_haven_wdgs[i].set('Streetpass Tablet')
                    original_dlc_haven_list.append('Streetpass Tablet')
    return()





def search_combobox_event(event, value, name):

    if(value == ''):
        name['value'] = dlc_haven_tablet_names_list

    else:
        data = []

        for item in dlc_haven_tablet_names_list:
            if(value.lower() in item.lower()):
                data.append(item)
            #sets combobox selected value if equal
            if(value.lower() == item.lower()):
                name.set(capwords(value.title()))
            name['value'] = data



def fixed_tablet_box_search(event):
    value = event.widget.get()
    search_combobox_event(event, value, event.widget)



root = Tk()
root.title("DQVII Traveler's Tablet Editor V." + str(version))
root.geometry('350x350')

player_tablets_count_text = StringVar()

fixed_tablets_count_text = StringVar()

player_tablets_count_text.set('NA')
fixed_tablets_count_text.set('NA')

player_tablets_label = Label(root, textvariable=player_tablets_count_text)
player_tablets_label.grid(row = 0, column = 0, sticky="ew")

fixed_tablets_label = Label(root, textvariable=fixed_tablets_count_text)
fixed_tablets_label.grid(row = 0, column = 1, sticky="ew")

load_save_file_button = Button(root, text = 'Load Save File', command = lambda: [load_save_file(), update_all_fields()], height = 2, width = 18, pady = 5, padx = 7)
load_save_file_button.grid(row = 1, column = 0, sticky="ew")


write_save_file_button = Button(root, text = 'Write Save File', command = lambda: [write_save_file()], height = 2, width = 18, pady = 5, padx = 7)
write_save_file_button.grid(row = 1, column = 1, sticky="ew")



initial_row = 2
dhc_count = 0

dlc_haven_vars = []
dlc_haven_wdgs = []


for i in range(24):

    var = StringVar(value = '')
    dlc_haven_vars.append(var)

    combo = ttk.Combobox(root, value = [], width = 18)
    
    combo['values'] = dlc_haven_tablet_names_list
    
    dlc_haven_wdgs.append(combo)
    

    combo.grid(row = initial_row + dhc_count//2, column = dhc_count%2, sticky="new")

    combo.bind('<KeyRelease>', fixed_tablet_box_search)
    dhc_count +=1



root.mainloop()





