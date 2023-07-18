from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache

from FlightApp.models import Customer, DestinationCity, ArrivalCity, Flight, FlightDetails, ReservationDetials


# Create your views here.
def reg_fun(request):
    if request.method == 'POST':
        c1 = Customer()
        c1.cust_name = request.POST["txtName"]
        c1.cust_phno = request.POST["txtPhno"]
        c1.cust_email = request.POST["txtEmail"]
        c1.cust_pswd = request.POST["txtPswd"]
        if Customer.objects.filter(
                Q(cust_name=request.POST["txtName"])
                & Q(cust_pswd =  request.POST["txtPswd"])).exists():
            return render(request,'register.html',{'msg':'Username and password is already present'})
        else:
            c1.save()
            return redirect('log')
    else:
        return render(request,'register.html',{'msg':''})


def log_fun(request):
    if request.method=='POST':
        name = request.POST["txtName"]
        password = request.POST["txtPswd"]
        user = authenticate(username=name,password=password)
        if user is not None:
            if user.is_superuser:
                login(request,user)
                request.session['USER'] = name
                return redirect('adminhome')
        elif Customer.objects.filter(
                Q(cust_name=request.POST["txtName"]) & Q(cust_pswd=request.POST["txtPswd"])).exists():
            request.session['Customer'] = name
            return render(request,'userpage/userhome.html',{'data':request.session['Customer']})
        else:
            return render(request, 'login.html',{'msg':'enter proper credentials'})
    else:
        return render(request,'login.html',{'msg':''})

#--------------------------------------------------------------------------------------
# admin page url function
@login_required
@never_cache
def adminhome_fun(request):
    return render(request,'adminpage/adminhome.html',{'data':request.session['USER']})

from datetime import datetime

@login_required
@never_cache
def addflights_fun(request):
    if request.method == 'POST':
        f1 = FlightDetails()
        f1.FlightNumber = request.POST['txtFlightNum']
        f1.FlightName = Flight.objects.get(FlightName=request.POST['ddlFlightName'])
        f1.ArrivalCity = ArrivalCity.objects.get(Arrival_City=request.POST['ddlArrivalCity'])
        f1.DestinationCity = DestinationCity.objects.get(Destination_City=request.POST['ddlDestCity'])
        f1.Date = request.POST['txtdate']

        datetime_string = request.POST['txtTime']
        datetime_value = datetime_string.split('T')   # taking only time from the textbox

        f1.ArrivalTime = datetime_value[-1]

        f1.Cost = request.POST['txtCOST']
        f1.save()
        return redirect('addflights')
    else:
        dest_city = DestinationCity.objects.all()
        arriva_city = ArrivalCity.objects.all()
        flight = Flight.objects.all()
        return render(request,'adminpage/addflights.html',{'msg':'',
                                                           'dest_city':dest_city,
                                                           'arrival_city':arriva_city,
                                                           'flight':flight
                                                           })

@login_required
@never_cache
def displayflight_fun(request):
    f1 = FlightDetails.objects.all()
    return render(request,'adminpage/displayflights.html',{'data':f1})

@login_required
@never_cache
def reservation_fun(request):
    r1 = ReservationDetials.objects.all()
    return render(request, 'adminpage/display_reserv.html', {'data': r1})

@login_required
@never_cache
def status_fun(request,id):
    r1 = ReservationDetials.objects.get(id=id)
    if request.method == 'POST':
        r1.booking_status = request.POST['txtStatus']
        r1.save()
        return redirect('reservation')
    else:
        return render(request,'adminpage/status.html',{'data':r1})

def logoutadmin_fun(request):
    logout(request)
    return redirect('log')

#-------------------------------------------------------------------------------
# User Page Url functions

@never_cache
def findflights_fun(request):
    dest_city = DestinationCity.objects.all()
    arriva_city = ArrivalCity.objects.all()
    if request.method=='POST':
        arrival_city = request.POST['ddlArrivalCity']
        destination_city = request.POST['ddlDestinationCity']
        date = request.POST['txtDate']
        data = FlightDetails.objects.filter(ArrivalCity=ArrivalCity.objects.get(Arrival_City=arrival_city)
                                            , DestinationCity=DestinationCity.objects.get(Destination_City=destination_city),Date=date)
        print(data)
        if data.count() != 0:
            return render(request,'userpage/findflights.html',{
                                                            'data':data,'value':True,
                                                            'dest_city': dest_city,
                                                            'arrival_city': arriva_city,
                                                            })
        else:
            return render(request, 'userpage/findflights.html', {
                'data': '','value':False,
                'dest_city': dest_city,
                'arrival_city': arriva_city,
            })
    else:
        return render(request,'userpage/findflights.html',{
                                                            'dest_city':dest_city,
                                                            'arrival_city':arriva_city,
                                                            'data':'','value':''
                                                            })

@never_cache
def bookflight_fun(request,id):
    flights = FlightDetails.objects.get(id=id)
    if request.method =='POST':
        r1 = ReservationDetials()
        r1.first_name = request.POST['txtFname']
        r1.last_name = request.POST['txtLname']
        r1.age = request.POST['txtAge']
        r1.phno = request.POST['txtPhno']
        r1.fight_data = flights
        r1.booking_status = False
        r1.cust_id = Customer.objects.get(cust_name=request.session['Customer'])
        r1.save()
        return redirect('displayreservation')
    else:
        return render(request,'userpage/reservationpage.html',{'data':flights})

@never_cache
def displayreservation_fun(request):
    r1= ReservationDetials.objects.filter(cust_id=Customer.objects.get(cust_name=request.session['Customer']))
    return render(request,'userpage/displayreserv.html',{'data':r1})


def userlogout_fun(request):
    del request.session['Customer']
    return redirect('log')