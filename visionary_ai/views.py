from django.shortcuts import render
from django.http import JsonResponse
import base64
from io import BytesIO
from pathlib import Path
import json
from google import genai
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from PIL import Image
from decouple import config


# Create your views here.
def home(request):
    if request.method == 'POST':
        try:
            data=json.loads(request.body)
            raw_image=data['image']
            meta_data,orignal_raw_image=raw_image.split(',')
            print(meta_data)
            prompt=data['prompt']
            image_bytes=base64.b64decode(orignal_raw_image)
            byte_io_file=BytesIO(image_bytes)
            byte_io_file.seek(0)
            image=ContentFile(byte_io_file.read())
            image.seek(0)
            fs=FileSystemStorage()
            fs.save('image.jpeg',image)
            path=Path(fs.location)/'image.jpeg'
        except:
            path.unlink()
            return JsonResponse({'result':'Some Exception occured.Try again.'})
        

      
        try:
            if prompt == 'history':
                input=config('HISTORY_PROMPT')
                client=genai.Client(api_key=config('API_KEY'))
                file=client.files.upload(file=path)
                response=client.models.generate_content(model='gemini-3-flash-preview',
                                            contents=[file,input]
                                        
                                            
                                            )
                data={'result':response.text}
                print(data)
                path.unlink()
                return JsonResponse(data)
        except:
            path.unlink()
            return JsonResponse({'result':'Some Exception occured.Try again.'})
        


        try: 
            if prompt == 'future':
                input=config('FUTURE_PROMPT')
                client=genai.Client(api_key=config('API_KEY'))
                file=client.files.upload(file=path)
                response=client.models.generate_content(model='gemini-3-flash-preview',
                                            contents=[file,input]
                                        
                                            
                                            )
                data={'result':response.text}
                print(data)
                path.unlink()
                return JsonResponse(data)
        except Exception as e:
            path.unlink()
            print(e)
            return JsonResponse({'result':'Some Exception occured.Try again.'})
        

        
        try:
            if prompt == 'reality':
                input=config('REALITY_PROMPT')
                client=genai.Client(api_key=config('API_KEY'))
                file=client.files.upload(file=path)
                response=client.models.generate_content(model='gemini-3-flash-preview',
                                            contents=[file,input]                    
                                            
                                            )
                data={'result':response.text}
                print(data)
                path.unlink()
                return JsonResponse(data)
        except Exception as e:
            path.unlink()
            print(e)
            return JsonResponse({'result':'Some Exception occured.Try again.'})
    return render(request,'visionary_ai/index.html')