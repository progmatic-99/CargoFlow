from django.db import models

# Create your models here.
from django.db import models

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
    on_port = models.BooleanField(default=False)

    def __str__(self):
        return self.container_number

class Cargo(models.Model):
    description = models.CharField(max_length=200)
    weight = models.FloatField()
    color = models.CharField(max_length=50, null=True, blank=True)
    container = models.ForeignKey(Container, on_delete=models.CASCADE, null=True, blank=True)
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)
    consignee = models.ForeignKey(Consignee, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description} ({self.container.container_number})"

class looseCargo(models.Model):
    description = models.CharField(max_length=200)
    weight = models.FloatField()
    color = models.CharField(max_length=50, blank=True, null=True)
    #container = models.ForeignKey(Container, on_delete=models.CASCADE, null=True, blank=True)
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)
    consignee = models.ForeignKey(Consignee, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description} ({self.container.container_number})"


class PortHandling(models.Model):
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    arrival_date = models.DateTimeField()
    departure_date = models.DateTimeField()
    port = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.vessel.name} - {self.port} ({self.arrival_date.strftime('%Y-%m-%d')} - {self.departure_date.strftime('%Y-%m-%d')})"


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
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    issued_date = models.DateTimeField()

    def __str__(self):
        return f"{self.bill_of_lading_number} - {self.voyage.vessel.name} ({self.voyage.voyage_number})"
