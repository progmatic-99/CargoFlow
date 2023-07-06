from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse

# Create your models here.
from django.utils import timezone


class Company(models.Model):
    slug = AutoSlugField(populate_from="name", unique=True)
    name = models.CharField(max_length=200)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=15, default="NA")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("company-list")


class Shipper(models.Model):
    slug = AutoSlugField(populate_from="email", unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.contact_person} ({self.company.name})"

    def get_absolute_url(self):
        return reverse("shipper-list")


class Consignee(models.Model):
    slug = AutoSlugField(populate_from="contact_person", unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.contact_person} ({self.company.name})"

    def get_absolute_url(self):
        return reverse("consignee-list")


class Vessel(models.Model):
    slug = AutoSlugField(populate_from="imo_number", unique=True)
    name = models.CharField(max_length=200)
    imo_number = models.CharField(max_length=15)
    flag = models.CharField(max_length=50)
    on_port = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("vessel-list")


class ForeignVessel(Vessel):
    purpose_of_call = models.CharField(max_length=500)
    import_no = models.CharField(max_length=15)
    export_no = models.CharField(max_length=15)
    cha_boe = models.TextField(null=True, blank=True)
    agent_importer = models.CharField(max_length=200)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("foreign-vessel-list")


class Container(models.Model):
    slug = AutoSlugField(populate_from="container_number", unique=True)
    container_number = models.CharField(max_length=20)
    container_type = models.CharField(max_length=10)
    tare_weight = models.FloatField()
    on_port = models.BooleanField(default=False)  # Change this line

    def __str__(self):
        return self.container_number

    def get_absolute_url(self):
        return reverse("container-list")


class Cargo(models.Model):
    slug = AutoSlugField(populate_from="weight", unique=True)
    description = models.CharField(max_length=200)
    weight = models.FloatField()
    container = models.ForeignKey(
        Container, on_delete=models.CASCADE, null=True, blank=True
    )
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)
    consignee = models.ForeignKey(Consignee, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description} ({self.container.container_number})"

    def get_absolute_url(self):
        return reverse("cargo-list")


class ContainerStatus(models.Model):
    name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from="name", unique=True)

    def __str__(self):
        return self.name


class looseCargo(models.Model):
    slug = AutoSlugField(populate_from="description", unique=True)
    description = models.CharField(max_length=200)
    weight = models.FloatField()
    color = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.description} ({self.color})"


class Voyage(models.Model):
    slug = AutoSlugField(populate_from="voyage_number", unique=True)
    voyage_number = models.CharField(max_length=50)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    from_port = models.CharField(max_length=200)
    to_port = models.CharField(max_length=200)
    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField()

    def __str__(self):
        return f"({self.voyage_number}) - {self.from_port} -> {self.to_port}"

    def get_absolute_url(self):
        return reverse("voyage-list")


class PortHandling(models.Model):
    slug = AutoSlugField(populate_from="status", unique=True)
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE)
    Container = models.ForeignKey(Container, on_delete=models.CASCADE)
    status = models.ForeignKey(ContainerStatus, on_delete=models.CASCADE, null=True)
    status_start_time = models.DateTimeField(default=timezone.now)
    status_end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.voyage.vessel.name} - ({self.status_start_time} - {self.status_end_time})"

    def status_duration(self):
        if self.status_end_time:
            return self.status_end_time - self.status_start_time
        else:
            return timezone.now() - self.status_start_time


class BillOfLading(models.Model):
    slug = AutoSlugField(populate_from="bill_of_lading_number", unique=True)
    bill_of_lading_number = models.CharField(max_length=50)
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE)
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)
    consignee = models.ForeignKey(Consignee, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, blank=True, null=True)
    loose_cargo = models.ForeignKey(
        looseCargo, on_delete=models.CASCADE, blank=True, null=True
    )
    issued_date = models.DateTimeField()

    def __str__(self):
        return f"{self.bill_of_lading_number} - ({self.voyage.voyage_number})"


class Manifest(models.Model):
    slug = AutoSlugField(populate_from="created_at", unique=True)
    voyage = models.OneToOneField(Voyage, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Manifest for {self.voyage.vessel.name} ({self.voyage.voyage_number})"

    def get_bill_of_lading_records(self):
        return BillOfLading.objects.filter(voyage=self.voyage)


class ServiceType(models.Model):
    slug = AutoSlugField(populate_from="name", unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price_per_tonnage = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("service-type-list")


class ServiceManager(models.Manager):
    def services_for_vessel(self, vessel):
        return self.filter(vessel=vessel)


class Service(models.Model):
    slug = AutoSlugField(populate_from="service_date", unique=True)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    service_type = models.ManyToManyField(ServiceType)
    service_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    objects = ServiceManager()

    class Meta:
        verbose_name_plural = "Services"

    def __str__(self):
        return f"{self.service_type.name} for {self.vessel.name}"

    def get_absolute_url(self):
        return reverse("service-list")

    def calculate_service_revenue(self):
        total_revenue = 0

        for service_type in self.service_type.all():
            total_revenue += service_type.price_per_tonnage

        return round(total_revenue, 2)


class DeliveryOrder(models.Model):
    slug = AutoSlugField(populate_from="order_number", unique=True)
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
        return BillOfLading.objects.select_related(
            "cargo", "loose_cargo", "shipper", "consignee", "voyage"
        ).filter(consignee=self.consignee, voyage=self.voyage)
