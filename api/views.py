from django.shortcuts import render, get_object_or_404
import requests
from django.views import View
from django.http import HttpResponse  , JsonResponse
import json
import subprocess
import datetime
import datetime
from . import models
from random import randint



class ServerStatus(View) : 
    def get(self , request) : 
        data = models.WorkerModel.objects.all()
        if len(data) == 0 : 
            models.WorkerModel.objects.create(license_date =datetime.datetime.now()  ,status = 'off', fruitpass = str(randint(1 , 999)))
            models.WorkerModel.objects.create(license_date =datetime.datetime.now(),status = 'off' , fruitpass = str(randint(1 , 999)))
        worker1 = models.WorkerModel.objects.first()
        worker2 = models.WorkerModel.objects.last()
        return JsonResponse({
            'status' : 'on' ,

            f'worker1' : {
            f'status' : worker1.status , 
            f'pid' : worker1.pid , 
            f'chat_id' : worker1.chat_id ,
            f'license_date' : worker1.license_date , 
            f'fruitpass' : worker1.fruitpass , 
            f'second' : worker1.second
            
                        } , 
            f'worker2' : {
            
            f'status' : worker2.status , 
            f'pid' : worker2.pid , 
            f'chat_id' : worker2.chat_id  ,
            f'license_date' : worker2.license_date , 
            f'fruitpass' : worker2.fruitpass , 
            f'second' : worker2.second
              }

                             })
    

class UserInfo(View) : 
    def get(self, request , fruitpass) :
        NameOP= {'User-Agent' : "Dalvik/2.1.0 (Linux; U; Android 13; SM-A326B Build/TP1A.220624.014)" ,'Connection':'close','Content-Type':"application/x-www-form-urlencoded" ,'Cookie':"FRUITPASSPORT="f"{fruitpass}"}
        data = requests.get('http://iran.fruitcraft.ir/cards/collectgold' , headers = NameOP)
        content = data.content
        if len(content) < 500 : 
            redata = json.loads(data.content)
            return JsonResponse(redata)
        else : 
            print(content)
            return JsonResponse({'status' : 'error'})


class Sender(View) : 
    def get(self , reqeust , fruitpass , date , chat_id , second) : 
        data = models.WorkerModel.objects.filter(status ='off')
       
        if len(data) == 0 : 
            return JsonResponse({'status' : 'False'})
        
        elif len(data) != 0 : 
            check = models.WorkerModel.objects.all()
            duolicate = False

            for i in check : 
                if i.fruitpass == fruitpass : 
                    duolicate = True
                    break
            
            if duolicate == False : 
                start_worker = subprocess.Popen(['python' , 'sender.py' , str(fruitpass)] , start_new_session=True)
                worker = models.WorkerModel.objects.get(id = data[0].id)
                worker.status = 'on'
                worker.pid = start_worker.pid
                worker.chat_id = chat_id
                worker.license_date = datetime.datetime.now() + datetime.timedelta(days=date)
                worker.fruitpass = fruitpass
                worker.second = second
                worker.save()
                return JsonResponse({'status' : 'bot running' ,'pid' : f'{str(start_worker.pid)}' , 'chat_id' : f'{str(chat_id)}' , 'fruitpass' : f'{str(fruitpass)}' , 'second' : f'{{str(second)}}' })
            else : 
                return JsonResponse({'status' : 'duplicate'})
            

class Killer(View) : 
    def get(self , request, pid) : 
        worker = models.WorkerModel.objects.filter(pid = pid).first()
        if worker : 
            if pid == 0 : 
                return JsonResponse({'status' : 'ورکر خاموش است .'})
            else : 
                worker.status = 'off'
                worker.fruitpass = str(randint(1 , 899999))
                worker.save()
                subprocess.Popen(['kill' , '-9' , f'{str(worker.pid)}'])
                return JsonResponse({'status' : 'killed'})

        else : 
            return JsonResponse({'status' : 'pid not found'})