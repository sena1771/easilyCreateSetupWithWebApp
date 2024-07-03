from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import subprocess
import os
from mainApp import setup
import zipfile

def home(request):
    return render(request,'mainApp/home.html')


@csrf_exempt
def run_python_script(request):
    if request.method == "POST" :
        
        #form = UploadForm(request.POST,request.FILES)
        print("Request files:",request.FILES)
    
        if 'ippToolArchive'not in request.FILES:
              return JsonResponse({'status': 'error','message':'There is no archive file found'})
        
        zip_file=request.FILES['ippToolArchive'] 
        update_info =request.POST.get('updateInfo')
       

        
        #download_dir = request.FILES.getlist('downloadDir')[0].name
        version = request.POST.get('version')      
        zip_path =os.path.join(settings.MEDIA_ROOT,'IPP_Tool.zip')
        with open(zip_path,'wb') as f:
            for chunk in zip_file.chunks():
                f.write(chunk)


        #setup_download_folder = os.path.join(settings.MEDIA_ROOT,'setupDownload')
        #if not os.path.exists(setup_download_folder):
            #os.makedirs(setup_download_folder)


        info_file_path = os.path.join(settings.MEDIA_ROOT,'info.txt')
        with open(info_file_path,'w') as info_file:
            
            info_file.write(f"version = {version}\n") 
            info_file.write(f"update_info={update_info}\n")   
                  
        script_path = os.path.join(settings.BASE_DIR,'setup.py')
    
        print("basedir->" + str(settings.BASE_DIR))
        download_dir = ""

        # C:\Users\sena.engin\Desktop\setupCreatorWebApp\setupCreator



        try:
            #result=subprocess.run(['python',script_path,zip_path,download_dir,version,update_info],capture_output=True,text=True) #download_dir was there
            print("create setup oncesi")
            result = setup.createSetupExeFile()
            print("setup sonrasi.")
            #subprocess.Popen(['python',script_path])
            return JsonResponse({'status': 'success','message':'Python script started successfully','output': "ok"})
        except Exception as e:
            return JsonResponse({'status': 'error','message':str(e)})

@csrf_exempt
def download_zip(request):
    #setup.zip_directory(project_directory_download_folder,zip_pathOfDownload)            
    #zip_pathOfDownload = os.path.join(settings.MEDIA_ROOT,'setupDownload.zip')
    path_directory = os.path.dirname(os.path.abspath(__file__))
    project_directory_download_folder = os.path.join(path_directory,'setupDownload')
    zip_pathOfDownload = os.path.join(path_directory,'setupDownload.zip')
    setup.zip_directory(project_directory_download_folder,zip_pathOfDownload)

    if os.path.exists(zip_pathOfDownload):
        with open(zip_pathOfDownload,'rb') as f:
            response = HttpResponse (f.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="setupDownload.zip"'
            return response  
    else:
        return JsonResponse({'status': 'error','message':'File not found'})     
        
   