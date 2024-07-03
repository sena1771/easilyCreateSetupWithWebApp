

import socket
import os
import zipfile
import sys
import tkinter as tk
import shutil
from tkinter import ttk
import threading
import queue
import time
#import shutil


ip_address = "127.0.0.1"
port = "9271"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

version = "0.1.4"

folder_path = 'C:\\IPP Platform Configuration Tool' #TODO: will change as IPP Platform Configuration Tool while delivering

if getattr(sys,'frozen',False):
    import pyi_splash
    script_directory =sys._MEIPASS
else:
    script_directory = os.path.dirname(os.path.abspath(__file__))


zip_path = os.path.join(script_directory,'IPP Platform Configuration Tool.zip')

icon_path = os.path.join(script_directory,'plane2.ico')


stop_extracting = threading.Event()
update_queue = queue.Queue()

def extract_files():
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
       
    if os.path.exists(zip_path):
        with zipfile.ZipFile(zip_path,'r') as zp:
            total_files = len(zp.namelist())
            root.after(0,lambda : progress_bar.config(maximum = total_files)) 
           
            extracted_count = 0

            update_interval = 10
            for file_index, file in enumerate(zp.namelist()):

                    if stop_extracting.is_set():
                        break

      
                    file_path= os.path.join(folder_path,file)
                    directory = os.path.dirname(file_path)
                    
                    if not os.path.exists(directory):
                        
                        os.makedirs(directory)
                        root.after(0,lambda : current_file_label.config(text = f"New directory created : {directory}")) 
                       


                    if len(file_path) >= 260 :
                        file_path = r'\\?\ ' + file_path
                    try :
                        
                        with zp.open(file) as file_data, open(file_path, 'wb') as output_file:
                            
                            shutil.copyfileobj(file_data,output_file)
                            extracted_count += 1

                                                     
                            #root.after(0,lambda :extracting_file_label.config(text=f"Extracting: {file}"))
                            #root.after(0,lambda : progress_bar.config(value = file_index + 1))
                      
                            root.update_idletasks()
                                
                  
                      
                                          
                    except Exception as ex:
                            #current_file_label.config(text =f"Failed to extract {file}: {ex}")
                            root.after(0,lambda :current_file_label.config(text= f"Failed to extract {file} "))
                           
                    #finally:
                            #root.after(0,extractinComplete)  
                        
                             #root.after(0,cancel_button.pack_forget)
                    #download_button.pack_forget()
                    root.after(0,lambda : extracting_file_label.config(text = f"Extracting: {file}"))                   
                    root.after(0,lambda : progress_bar.config(value = file_index + 1))
                    #simulate_extraction(file)
                    root.update_idletasks()

    if not stop_extracting.is_set():        
        info_label.config(state='normal')
        info_label.delete(1.0,tk.END)
        info_label.insert(tk.END,"New version downloaded successfully")
        info_label.config(state='disabled')
        progress_bar.pack_forget()
        extracting_file_label.pack_forget()
        ok_button.pack(side=tk.LEFT, pady=10,padx=10)
        
        cancel_button.pack_forget()
                    #simulate_extraction(file)
                   
                    #time.sleep(1)
                    #if not stop_extracting.is_set():
                        #root.after(0,extractinComplete)
                    #extractinComplete()
            
        #info_text = f" {extracted_count} files downloaded or updated."
                   
                       
def simulate_extraction(file):

    for _ in range(10):
        if stop_extracting.is_set():
            return
        root.after(0,extractinComplete)
        #root.update_idletasks()
def start_extracting():
     
    
     stop_extracting.clear()
     progress_bar.pack()
     extracting_file_label.pack()
     

     threading.Thread(target=extract_files).start()
     download_button.pack_forget()

     

def extractinComplete():
     
     info_label.config(state='normal')
     info_label.delete(1.0,tk.END)
     info_label.insert(tk.END,"New version downloaded successfully")
     info_label.config(state='disabled')
     download_button.pack_forget()
     progress_bar.pack_forget()            
     extracting_file_label.pack_forget()
     ok_button.pack(side=tk.LEFT, pady=10,padx=10)
     progress_bar['value'] = progress_bar['maximum']
     cancel_button.pack_forget()
   
def cancel_extracting() :
     stop_extracting.set()
     
     info_label.config(state = 'normal')
     info_label.delete(1.0,tk.END)
     info_label.insert(tk.END,"Extraction cancelled")
     info_label.config(state = 'disabled')
     ok_button.pack(side=tk.LEFT, pady=10,padx=10)
       
     progress_bar.pack_forget()
     download_button.pack_forget()
     cancel_button.pack_forget()
     current_file_label.pack_forget()
     extracting_file_label.pack_forget()

    
def close_screen():
    #thread close
    stop_extracting.set()
    info_label.config(state = 'normal')
    info_label.delete(1.0,tk.END)
    info_label.insert(tk.END,"Extraction cancelled")
    info_label.config(state = 'disabled')
    progress_bar.pack_forget()
    download_button.pack_forget()
    cancel_button.pack_forget()
    current_file_label.pack_forget()
    extracting_file_label.pack_forget()
    root.destroy()

  
root= tk.Tk()
root.resizable(width=False,height=False)
root.iconbitmap(icon_path)
root.eval('tk::PlaceWindow . center') #centers window
root.geometry('550x400')
root.title("IPP Platform Configuration Tool")

root.configure(background='steel blue')


title_label = tk.Label(root,text="Installer",width=40,font=("Ink Free",25,'bold'),bg="steel blue",fg="gold")
title_label.pack(side =tk.TOP,padx=30)

info_text = "IPP Platform Configuration Tool --- Version:" +version+" "+"will be downloaded.\nNew Updates;\n-DTN Interrack Switch Configuration\n-HSN Configuration\n-Report File Creation" 
info_label = tk.Text(root,height= 10, width = 50)
info_label.insert(tk.END, info_text)
info_label.pack(pady=10,padx=10)
info_label.config(state = 'disabled')


current_file_label = tk.Label(root,text = "Waiting to start...", anchor ="w")
frame_buttons = tk.Frame(root)
frame_buttons.pack(side = tk.BOTTOM, fill = tk.X)

download_button = tk.Button(frame_buttons,text ="Install/Update", command= start_extracting,bg="steel blue",fg="white",width=23)
download_button.pack(side=tk.RIGHT,padx=20, pady=20)

cancel_button = tk.Button(frame_buttons,text= "Cancel", command = cancel_extracting,bg="steel blue",fg="white",width=25)
cancel_button.pack(side=tk.LEFT,padx =20,pady=20)

ok_button = tk.Button(frame_buttons,text="OK", command = close_screen,width=25,bg="steel blue",fg="white")

progress_label_frame = tk.Frame(root,bg="steel blue")
progress_label_frame.pack(pady=5,expand=True)


progress_bar = ttk.Progressbar(progress_label_frame,orient='horizontal', mode= 'determinate', length=300)


extracting_file_label = tk.Label(progress_label_frame,text="",fg="white",bg="steel blue")


if getattr(sys,'frozen',False):
     pyi_splash.close()
  
    
root.mainloop()




