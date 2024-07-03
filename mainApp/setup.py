
import os
import zipfile
import sys
import tkinter as tk
import shutil
from tkinter import ttk
import threading
#from django.http import JsonResponse
import logging
import subprocess
import zipfile




if __name__ == "__main__":

    print('is working?')
    logging.basicConfig(filename = 'setup_log.txt',level = logging.DEBUG,format = '%(asctime)s %(levelname)s:%(message)s')
    logging.info('script started')

  

  
    #download_dir = sys.argv[2]

    #version = sys.argv[3]
    #update_info = sys.argv[4]
    path_directory = os.path.dirname(os.path.abspath(__file__))
    

    zip_path = os.path.join(path_directory,'Example_Archive_Folder.zip')
    

    project_directory_download_folder = os.path.join(path_directory,'setupDownload')
    

    logging.info(f'project directory download folder: {project_directory_download_folder}')

    info_file_path = os.path.join(path_directory,'info.txt')
    version = ""
    update_info = ""

    if os.path.exists(info_file_path):
        logging.info(f'Reading from info.txt:{info_file_path}')
        with open(info_file_path,'r') as info_file :
            for line in info_file:
                logging.info(f'Reading line:{line.strip()}')
                if line.startswith("version = "):
                    version = line.split("=",1)[1].strip()
                    logging.info(f"version:{version}")
                elif line.startswith("update_info="):
                    update_info = line.split("=",1)[1].strip()
                    logging.info(f"update_inff:{update_info}") 
    if not version or not update_info:
        logging.info(f"version:{version},updateInfo:{update_info}")
        logging.error("Version or update info not found in info.txt file")
        sys.exit(1)                   

    #folder_path = download_dir

    

    folder_path = 'C:\\Example-Folder-Place' 

    if getattr(sys,'frozen',False):
        import pyi_splash
        script_directory =sys._MEIPASS
    else:
        script_directory = os.path.dirname(os.path.abspath(__file__))

    

    

    icon_path = os.path.join(script_directory,'example-pic.ico')


    if not os.path.exists(project_directory_download_folder ):
            os.makedirs(project_directory_download_folder)
            logging.info(f'Crated directory: {project_directory_download_folder}')

    logging.info(f'icon path is : {icon_path}')
    logging.info(f'folder path is : {folder_path}')

    stop_extracting = threading.Event()


    def extract_files():
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        if os.path.exists(zip_path):
            with zipfile.ZipFile(zip_path,'r') as zp:
                total_files = len(zp.namelist())
                root.after(0,lambda : progress_bar.config(maximum = total_files)) 
    

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
                                #extracted_count += 1

                                                        
                            
                                root.update_idletasks()
                                    
                    
                        
                                            
                        except Exception as ex:
                            
                                root.after(0,lambda :current_file_label.config(text= f"Failed to extract {file} "))
                            
                        #finally:
                                #root.after(0,extractinComplete)  
                            
                                #root.after(0,cancel_button.pack_forget)
                    
                        root.after(0,lambda : extracting_file_label.config(text = f"Extracting: {file}"))                   
                        root.after(0,lambda : progress_bar.config(value = file_index + 1))
                    
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
                    
                
            #info_text = f" {extracted_count} files downloaded or updated."
                    
                        

        
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
    root.title("Setup Downloader")

    root.configure(background='steel blue')


    title_label = tk.Label(root,text="Installer",width=40,font=("Ink Free",25,'bold'),bg="steel blue",fg="gold")
    title_label.pack(side =tk.TOP,padx=30)

   
    info_label = tk.Text(root,height= 10, width = 50)
    info_label.insert(tk.END, f"Example Archive --- Version:{version}\nNew Updates:\n{update_info}")
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



    #logging.info(f"Running the pyinstaller command: {''.join(pyinstaller_command)}")

def createSetupExeFile():
    script_directory = os.path.dirname(os.path.abspath(__file__))
 
    zip_path = os.path.join(script_directory,'..\media\Example_Archive_Folder.zip')
    
    info_file_path = os.path.join(script_directory,'..\media\info.txt')

    path_directory = os.path.dirname(os.path.abspath(__file__))
    project_directory_download_folder = os.path.join(path_directory,'setupDownload')
    icon_path = os.path.join(script_directory,'icon\example-pic.ico')    
    pyinstaller_path ='C:\\Users\\ayseexamplename.examplesurname\\Desktop\\setupCreatorWebApp\\setupCreator\\Yilan\\Scripts\\pyinstaller.exe'
    commandPyinstaller = f"""{pyinstaller_path} --noconfirm --onedir --console --name setupExample --windowed --add-data "{zip_path};." --add-data "{info_file_path};." --add-binary "{icon_path};." --icon "{icon_path}" --distpath "{project_directory_download_folder}" "{os.path.abspath(__file__)}\""""
    

    try:
        result =subprocess.run(commandPyinstaller,capture_output=True,text=True,shell=True) 
        if result.returncode == 0:
            print("Exe created successfully")
            #return JsonResponse({'status': 'error','message':'Successssss'})
            logging.info("Created successfully the exe")

            #zip_pathOfDownload = os.path.join(path_directory,'setupDownload.zip')
            #zip_directory(project_directory_download_folder,zip_pathOfDownload)

            return result

        else:
            print(f"Failed to create exe:{result.stderr}")
            logging.error(f"Failed while creating the exe : {result.stderr}")
            #return JsonResponse({'status': 'error','message':'There is no archive file found'})
    except Exception as e :
            print("Failed ") 
            logging.error(f"Failed while creating the exe : {str(e)}")
            #return JsonResponse({'status': 'error','message':'There is d'})



def zip_directory(directory_path,zip_path):
    with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as zip_file:
        for root,dirs,files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root,file)
                arcOfName = os.path.relpath(file_path,directory_path)
                zip_file.write(file_path,arcOfName)

              
    

               



