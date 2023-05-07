from django.contrib.admin import AdminSite




class CustomAdminSite(AdminSite):
    site_header  =  "RMS Master Console"  
    site_title  =  "Shipping Management System"
    index_title  =  "Prototyping Tools"

    def has_permission(self, request):
        """
        Override the default has_permission method to grant access based on user status.
        """
        # Check if the user is active and is a staff member.
        return request.user.is_active and request.user.is_staff

    def get_app_list(self, request):
        app_list = super().get_app_list(request)

        section1_models = [ 'Vessel', 'Voyage', 'Service', 'ServiceType',]
        section2_models = ['BillOfLading','Container', 'Cargo','looseCargo','ContainerStatus']
        section3_models = [ 'Manifest','DeliveryOrder','PortHandling',]
        section4_models = ['Consignee', 'Company', 'Shipper']


        your_app = None
        for app in app_list:
            if app['app_label'] == 'operations':
                your_app = app
                break

        if not your_app:
            return []

        sections = [
            {
                'name': 'Ship',
                'models': [model for model in app_list[0]['models'] if model['object_name'] in section1_models]
            },
            {
                'name': 'Operations',
                'models': [model for model in app_list[0]['models'] if model['object_name'] in section2_models]
            },
                        
                        {
                'name': 'Documents',
                'models': [model for model in app_list[0]['models'] if model['object_name'] in section3_models]
            },

                       {
                'name': 'Contacts',
                'models': [model for model in app_list[0]['models'] if model['object_name'] in section4_models]
            },
        ]

        return sections
