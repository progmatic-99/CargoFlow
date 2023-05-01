from django.core.management.base import BaseCommand
from operations.models import (
    Company, Shipper, Consignee, Vessel, Container, Cargo, PortHandling, Voyage,
    BillOfLading, Manifest, ServiceType, Service, looseCargo
)
import random
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Populate demo data for all models'

    def handle(self, *args, **options):
        self.stdout.write("Creating demo data...")

        # Create companies
        for _ in range(3):
            Company.objects.create(
                name=fake.company(),
                address=fake.address(),
                email=fake.company_email(),
                phone=fake.phone_number()
            )

        # Create shippers and consignees
        for company in Company.objects.all():
            for _ in range(2):
                Shipper.objects.create(
                    company=company,
                    contact_person=fake.name(),
                    email=fake.email(),
                    phone=fake.phone_number()
                )
                Consignee.objects.create(
                    company=company,
                    contact_person=fake.name(),
                    email=fake.email(),
                    phone=fake.phone_number()
                )

        # Create vessels
        for _ in range(3):
            Vessel.objects.create(
                name=fake.catch_phrase(),
                imo_number=fake.unique.random_number(digits=7),
                flag=fake.country()
            )

        # Create containers
        container_types = ['20GP', '40GP', '40HC', '45HC']
        for _ in range(10):
            Container.objects.create(
                container_number=fake.unique.random_number(digits=11),
                container_type=random.choice(container_types),
                tare_weight=random.uniform(2000, 5000),
                on_port=random.choice([True, False])
            )

        # Create cargos and loose cargos
        for shipper in Shipper.objects.all():
            for consignee in Consignee.objects.all():
                for _ in range(2):
                    Cargo.objects.create(
                        description=fake.bs(),
                        weight=random.uniform(1000, 20000),
                        container=random.choice(Container.objects.all()),
                        shipper=shipper,
                        consignee=consignee
                    )

                    looseCargo.objects.create(
                        description=fake.bs(),
                        weight=random.uniform(100, 1000),
                        color=fake.safe_color_name(),
                        shipper=shipper,
                        consignee=consignee
                    )

        # Create voyages
        for vessel in Vessel.objects.all():
            Voyage.objects.create(
                voyage_number=fake.unique.random_number(digits=4),
                vessel=vessel,
                from_port=fake.city(),
                to_port=fake.city(),
                departure_date=fake.date_between(start_date='-1y', end_date='today'),
                arrival_date=fake.date_between(start_date='today', end_date='+1y')
            )

        # Create bill of ladings
        for voyage in Voyage.objects.all():
            for shipper in Shipper.objects.all():
                for consignee in Consignee.objects.all():
                    BillOfLading.objects.create(
                                                bill_of_lading_number=fake.unique.random_number(digits=6),
                        voyage=voyage,
                        shipper=shipper,
                        consignee=consignee,
                        cargo=random.choice(Cargo.objects.all()),
                        loose_cargo=random.choice(looseCargo.objects.all()),
                        issued_date=fake.date_between(start_date='-1y', end_date='today')
                    )

        # Create manifests
        for voyage in Voyage.objects.all():
            Manifest.objects.create(
                voyage=voyage,
                created_at=fake.date_between(start_date='-1y', end_date='today')
            )

        # Create service types
        for _ in range(5):
            ServiceType.objects.create(
                name=fake.catch_phrase(),
                description=fake.sentence(),
                price_per_tonnage=random.uniform(50, 500)
            )

        # Create services
        for vessel in Vessel.objects.all():
            for _ in range(3):
                service = Service.objects.create(
                    vessel=vessel,
                    service_date=fake.date_between(start_date='-1y', end_date='today'),
                    description=fake.sentence()
                )
                service.service_type.set(ServiceType.objects.order_by('?')[:random.randint(1, 3)])
                service.save()

        self.stdout.write(self.style.SUCCESS("Demo data created successfully!"))

