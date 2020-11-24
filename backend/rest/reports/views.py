from rest_framework.views import View
from django.http import HttpResponse
from invoiceDetails.models import InvoiceDetail
from invoices.models import Invoice
from products.models import Product
from products.serializers import ProductSerializer
from invoices.serializers import InvoiceSerializer
import json

# View for Report 1:
class MostSelledProducts(View):
    def get(self, request):

        # Product sales count:
        products = ProductSerializer(Product.objects.all(), many = True).data
        dictionary = []
        for i in range(len(products)):
            product = products[i]['codeProduct']

            invoiceDetails = InvoiceDetail.objects.filter(productInvoiceDetail = product)
            sales = 0
            for j in invoiceDetails:
                sales = sales + j.quantityInvoiceDetail

            data = {
                'product': products[i],
                'sales': sales                     
            }
            dictionary.append(data)

        # Most selled products:
        response = {
            'report': sorted(dictionary, key = lambda x: x['sales'], reverse = True)[:5]
        }

        return HttpResponse(json.dumps(response))

# View for Report 2:
class HoursWithMoreSales(View):
    def get(self, request):

        # Hour sales count:
        times = Invoice.objects.all().values('dateTimeInvoice')
        hours = []
        for i in times:
            hour = i['dateTimeInvoice'].strftime('%H')
            if (hour not in hours):
                hours.append(hour)

        dictionary = []
        for i in hours:
            sales = 0
            for j in times:
                if (i == j['dateTimeInvoice'].strftime('%H')):
                    sales = sales + 1

            data = {
                'time': i,
                'sales': sales                     
            }
            dictionary.append(data)

        # Most selled products:
        response = {
            'report': sorted(dictionary, key = lambda x: x['sales'], reverse = True)[:5]
        }

        return HttpResponse(json.dumps(response))


