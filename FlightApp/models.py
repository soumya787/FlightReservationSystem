from django.db import models

# Create your models here.
class Flight(models.Model):
    FlightName = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.FlightName}"
class DestinationCity(models.Model):
    Destination_City = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.Destination_City}"
class ArrivalCity(models.Model):
    Arrival_City = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.Arrival_City}"
class FlightDetails(models.Model):
    FlightNumber=  models.CharField(max_length=50)
    FlightName = models.ForeignKey(Flight,on_delete=models.CASCADE)
    ArrivalCity = models.ForeignKey(ArrivalCity,on_delete=models.CASCADE)
    DestinationCity = models.ForeignKey(DestinationCity,on_delete=models.CASCADE)
    Date = models.DateField()
    ArrivalTime = models.TimeField()
    Cost = models.IntegerField()

    def __str__(self):
        return f"{self.FlightName} -- {self.FlightNumber} -- {self.ArrivalTime} -- {self.Date} -- {self.Cost}"

class Customer(models.Model):
    cust_name =  models.CharField(max_length=50)
    cust_phno = models.BigIntegerField()
    cust_email = models.CharField(max_length=50)
    cust_pswd = models.CharField(max_length=50)
    
class ReservationDetials(models.Model):
    fight_data = models.ForeignKey(FlightDetails,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phno = models.BigIntegerField()
    age = models.IntegerField()
    booking_status = models.BooleanField()
    cust_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
