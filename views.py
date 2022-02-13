from django.shortcuts import render,redirect
from .models import bModel,tModel
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from datetime import datetime
import urllib
import json

# Create your views here.

def login(request):
	if request.method == "POST":
		n=request.POST.get('un')
		p=request.POST.get('pw')
		usr = authenticate(username=n, password=p)
		if usr is None:
			return render(request, 'login.html',{'msg': 'Invalid Credentials'})
		else:
			auth_login(request, usr)
			return redirect('about')
	else:
		return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')

def about(request):
	return render(request,'about.html')

def add_customer(request):
	if request.method == "POST":
		n=request.POST.get('user')
		p=request.POST.get('pn')
		e=request.POST.get('em')
		b=request.POST.get('bal')
		data=bModel.objects.filter(email=e)
		if data:
			return render(request,'add_customer.html',{'msg':'User Present with same email id'})
		else:
			s=bModel(name=n,phone=p,email=e,balance=b)
			s.save()
			return render(request,'add_customer.html',{'msg':'Account Created'})
	else:
		return render(request,'add_customer.html')

def view_customer(request):
	data=bModel.objects.all()
	return render(request,'view_customer.html',{'data':data})


def transfer_money(request):
	if request.method == "POST":
		data=bModel.objects.all()
		sender_email=request.POST.get('account_sender')
		receiver_email=request.POST.get('account_reciever')
		transfer_amount = (float)(request.POST.get('transfer'))
		transfer_type = request.POST.get('transfer_type')
		print(transfer_type)
		

		if(sender_email == None or receiver_email == None):
			return render(request,'transfer_money.html',{'data':data,'msg':'Please Select Customer'})
		elif(sender_email == receiver_email):
			return render(request,'transfer_money.html',{'data':data,'msg':'Please select Different Accounts'})
		elif(transfer_amount > (bModel.objects.filter(email = sender_email).values('balance'))[0]['balance']):
				return render(request, 'transfer_money.html', {'data' : data, 'msg' : 'Insufficient Funds'})
		elif(transfer_amount < 1.0):
				return render(request, 'transfer_money.html', {'data' : data, 'msg' : 'Please enter correct Amount'})

		else:	
				sender_bal = bModel.objects.filter(email = sender_email).values('balance')
				print(sender_bal)
				sender_bal = sender_bal[0]['balance']
				

				receiver_bal = bModel.objects.filter(email = receiver_email).values('balance')
				receiver_bal = receiver_bal[0]['balance']

				updated_sender = round((sender_bal - transfer_amount), 3)
				sub = bModel.objects.filter(email = sender_email).update(balance = updated_sender)
				updated_receiver = round((receiver_bal + transfer_amount), 3)
				rub = bModel.objects.filter(email = receiver_email).update(balance = updated_receiver)
	
				sender_name = bModel.objects.filter(email = sender_email).values('name')
				sender_name = sender_name[0]['name']
				print(sender_name)	

				receiver_name = bModel.objects.filter(email = receiver_email).values('name')
				receiver_name = receiver_name[0]['name']
				print(receiver_name)
				
				now = datetime.now()
				dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
				print("date and time =", dt_string)
	
				d = tModel(send = sender_name, receive = receiver_name, amount = transfer_amount,transtype=transfer_type,dt = dt_string)	
				d.save()

				
				return render(request, 'transfer_money.html', {'data' : data, 'msg' : 'Transfer Completed'})
	

	else:
		data=bModel.objects.all()
		return render(request,'transfer_money.html',{'data':data})

	
def transfer_history(request):
	if request.method == "POST":
		data = bModel.objects.all()
		email = request.POST.get('history')
		print(email)
		if (email == None):
			return render(request, 'transfer_history.html', {'msg' : 'Please select customer', 'data' : data})
		else:
			dum = bModel.objects.filter(email = email).values('name')
			dum = dum[0]['name']
			print(dum)
			dumm = tModel.objects.filter(send = dum)
			print(dumm)

			rdumm = tModel.objects.filter(receive = dum)	
			print(rdumm)
			return render(request, 'transfer_history.html', {'data' : data, 'dumm' : dumm, 'rdumm' : rdumm})
	else:
		data = bModel.objects.all()
		return render(request, 'transfer_history.html', {'data' : data})
		

		