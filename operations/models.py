from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Shipper(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.contact_person} ({self.company.name})"

class Consignee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.contact_person} ({self.company.name})"

class Vessel(models.Model):
    name = models.CharField(max_length=200)
    imo_number = models.CharField(max_length=15)
    flag = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Container(models.Model):
    container_number = models.CharField(max_length=20)
    container_type = models.CharField(max_length=10)
    tare_weight = models.FloatField()
    on_port = models.BooleanField(default=False)  # Change this line

    def __str__(self):
        return self.container_number

class Cargo(models.Model):
    description = models.CharField(max_length=200)
    weight = models.FloatField()
    container = models.ForeignKey(Container, on_delete=models.CASCADE, null=True, blank=True)
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)
    consignee = models.ForeignKey(Consignee, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description} ({self.container.container_number})"



class ContainerStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class PortHandling(models.Model):
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    arrival_date = models.DateTimeField()
    departure_date = models.DateTimeField()
    port = models.CharField(max_length=200)
    status = models.ForeignKey(ContainerStatus, on_delete=models.CASCADE, null=True)
    status_start_time = models.DateTimeField(default=timezone.now)
    status_end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.vessel.name} - {self.port} ({self.arrival_date.strftime('%Y-%m-%d')} - {self.departure_date.strftime('%Y-%m-%d')})"

    def status_duration(self):
        if self.status_end_time:
            return self.status_end_time - self.status_start_time
        else:
            return timezone.now() - self.status_start_time

class looseCargo(models.Model):
    description = models.CharField(max_length=200)
    weight = models.FloatField()
    color = models.CharField(max_length=50, blank=True, null=True)
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)
    consignee = models.ForeignKey(Consignee, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description} ({self.color})"


class Voyage(models.Model):
    voyage_number = models.CharField(max_length=50)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    from_port = models.CharField(max_length=200)
    to_port = models.CharField(max_length=200)
    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField()

    def __str__(self):
        return f"{self.vessel.name} ({self.voyage_number}) - {self.from_port} -> {self.to_port}"

class BillOfLading(models.Model):
    bill_of_lading_number = models.CharField(max_length=50)
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE)
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)
    consignee = models.ForeignKey(Consignee, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, blank=True, null=True)
    loose_cargo = models.ForeignKey(looseCargo, on_delete=models.CASCADE, blank=True, null=True)
    issued_date = models.DateTimeField()

    def __str__(self):
        return f"{self.bill_of_lading_number} - ({self.voyage.voyage_number})"


class Manifest(models.Model):
    voyage = models.OneToOneField(Voyage, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Manifest for {self.voyage.vessel.name} ({self.voyage.voyage_number})"

    def get_bill_of_lading_records(self):
        return BillOfLading.objects.filter(voyage=self.voyage)


class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price_per_tonnage = models.FloatField(default=0)

    def __str__(self):
        return self.name

class ServiceManager(models.Manager):
    def services_for_vessel(self, vessel):
        return self.filter(vessel=vessel)

class Service(models.Model):
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    service_type = models.ManyToManyField(ServiceType)
    service_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    objects = ServiceManager()

    class Meta:
        verbose_name_plural = "Services"

    def __str__(self):
        return f"{self.service_type.name} for {self.vessel.name}"
    


class DeliveryOrder(models.Model):
    order_number = models.CharField(max_length=50)
    issued_date = models.DateTimeField()
    consignee = models.ForeignKey(Consignee, on_delete=models.CASCADE)
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Delivery Orders"

    def __str__(self):
        return f"Delivery Order for {self.consignee} - {self.voyage}"

    def get_bill_of_lading_records(self):
        return BillOfLading.objects.filter(consignee=self.consignee, voyage=self.voyage)
