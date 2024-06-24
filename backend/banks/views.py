from io import StringIO
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from .models import Bank
import pandas as pd
import requests



@require_GET
def get_data(request):
    url = "https://stat.fsc.gov.tw/FSC_OAS3_RESTORE/api/CSV_EXPORT?TableID=B14&OUTPUT_FILE=Y"
    response = requests.get(url)
    
    if response.status_code == 200:
        csv_data = response.content.decode('utf-8')
        dataFrame = pd.read_csv(StringIO(csv_data))
        dataFrame = dataFrame.where(pd.notnull(dataFrame),None)
        data = dataFrame.to_dict(orient='records')

        for row in data:
            name = row['機構名稱']
            address = row['地址'] if row['地址'] else 'null'
            tel = row['電話'] if row['電話'] else ''
            headOfficeCode = row['總機構代號']
            branchOfficeCode = row['機構代號']

            bank = Bank(
                name = name, 
                address = address, 
                tel = tel, 
                headOfficeCode = headOfficeCode, branchOfficeCode = branchOfficeCode
            )
            bank.save()
            
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"error": "Failed to retrieve data"}, status=response.status_code)
    
@require_GET
def get_head_offices(request):
    data = list(Bank.objects.values("headOfficeCode","headOffice").order_by("headOfficeCode").distinct())
    return JsonResponse(data, safe=False)

@require_GET
def get_branches(request):
    head_office = request.GET.get('head_office')
    branches = Bank.objects.filter(headOffice=head_office).exclude(branchOffice="").values('id', 'branchOffice')
    return JsonResponse(list(branches), safe=False)