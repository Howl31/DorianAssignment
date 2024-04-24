from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse
import os, re, datetime
import pandas as pd
from .models import *
from django.contrib import messages

# Create your views here.


# def DataTransformation(request):
#     if request.method == "POST":
#         print(request.FILES)
#         inputFile = request.FILES.get('inputFile')
#         name, extension = os.path.splitext(inputFile.name)
#         firstRow = pd.read_excel(inputFile, sheet_name='Segmentwise Report', nrows=1, header=None)
#         results = re.findall('(?:January|February|March|April|May|June|July|August|September|October|November|December)[\s-]\d{2,4}', firstRow.iloc[0][0])
#         print(results)
#         df = None
#         if extension.lower() == ".xlsx":
#             df = pd.read_excel(inputFile, skiprows=[0,2], sheet_name='Segmentwise Report')
#         elif extension.lower() == ".csv":
#             df = pd.read_csv(inputFile, skiprows=[0,2])
#         df = df.rename(columns={'Unnamed: 0': 'Insurer'})
#         insurerObj = InsurerMaster.objects.all()
#         insurers = insurerObj.values('insurer').order_by('insurer').distinct()
#         for insurer in insurers[4:7]:
#             if (insurer["insurer"] in df.Insurer.values):
#                 tempDf = df[df['Insurer'] == insurer["insurer"]]
#                 tempDf.set_index('Insurer', inplace=True)
#                 for col in tempDf:
#                     clubbed_name = insurerObj.get(insurer=insurer["insurer"]).clubbed_name
#                     category = CategoryMaster.objects.get(clubbed_name=clubbed_name).category
#                     product = None
#                     if 'misc' in col.lower() or LOBMaster.objects.filter(lob__icontains=col.replace('  ', ' ')).exists():
#                         if 'misc' in col.lower():
#                             product = LOBMaster.objects.get(lob__icontains="Misc").lob
#                         else:
#                             product = LOBMaster.objects.get(lob__icontains=col.replace('  ', ' ')).lob
#                     print(product)
#                     print(f'{col.replace("  ", " ")}: {tempDf[col].values[0]}')
#     return render(request, 'uploadCsv.html')


def DataTransformation(request):
    try:
        if request.method == "POST":
            inputFile = request.FILES.get('inputFile')     
            df = pd.read_excel(inputFile,nrows=1, header=None, sheet_name="Segmentwise Report")
            # monthYear = re.findall('(?:January|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|December)[\s-]\d{2,4}', df[0].values[0])[0]
            month, year = re.findall('(?:January|February|March|April|May|June|July|August|September|October|November|December)[\s-]\d{2,4}', df[0].values[0])[0].split(' ')

            df = pd.read_excel(inputFile, skiprows=[0,2], sheet_name="Segmentwise Report")
            upload_data = []
            for i, g in df.groupby(df.index // 2):
                g.rename(columns={'Unnamed: 0': 'LOB'}, inplace=True)
                g.set_index('LOB', inplace=True)
                rawDf = g.T
                rawDf = rawDf.fillna(0)
                rawDf["Product"] = rawDf.index
                columns = rawDf.columns.values
                
                if InsurerMaster.objects.filter(insurer=columns[0]).exists():
                    insurer = InsurerMaster.objects.get(insurer=columns[0])
                    rawDf.rename(columns={columns[0]: 'Insurer'}, inplace=True)
                    rawDf["value"] = round(rawDf[rawDf.columns.values[0]] - rawDf[rawDf.columns.values[1]], 2)
                    rawDf["year"] = year
                    rawDf["month"] = datetime.datetime.strptime(month,'%B').strftime('%b')
                    rawDf["category"] = CategoryMaster.objects.get(clubbed_name=insurer.clubbed_name)
                    rawDf["clubbed_name"] = columns[0]
                    rawDf["product"] = rawDf.index
                    rawDf["product"] = rawDf['product'].apply(lambda x: x.replace("  ", " "))
                    
                    newColumns = ['product', 'value', 'year', 'month', 'category', 'product']
                    newDf = rawDf[newColumns]
                    for index, row in newDf.iterrows():
                        row = row.to_dict()
                        if "misc" in row["product"].lower() or LOBMaster.objects.filter(lob=row["product"]).exists():
                            if "misc" in row["product"].lower():
                                row["product"] = LOBMaster.objects.get(lob__icontains="Misc")
                            else:
                                row["product"] = LOBMaster.objects.get(lob__icontains=row["product"])
                            upload_data.append(InsurerValue(**row))
            InsurerValue.objects.bulk_create(upload_data)
            messages.success(request, "Details successfully saved.")
        # else:
        #     messages.error(request, "Get request is not allowed")
        return render(request, 'uploadCsv.html')
    except Exception as e:
        messages.error(request, f"Exception: {e}")
        return render(request, 'uploadCsv.html')
    

def downloadExcel(request):
    prod_df = pd.DataFrame.from_records(
        data=InsurerValue.objects.all().values('year', 'month', 'category__category', 'category__clubbed_name', 'product__lob', 'value')
        # columns=['Year', 'Month', 'category', 'clubbed_name', 'Product', 'Value']
    )
    prod_df.rename(columns={'year': 'Year', 'month': "Month", 'category__category': "Category", 'category__clubbed_name': "Clubbed Name", 
                            'product__lob': "Product", 'value': "Value"}, inplace=True)
    print(prod_df.head())
    response = HttpResponse(content_type='application/xlsx')
    response['Content-Disposition'] = f'attachment; filename="InsurerValue.xlsx"'
    with pd.ExcelWriter(response) as writer:
        prod_df.to_excel(writer, sheet_name='BC DOWNLOAD', index=False)
    return response


def dashboard(request):
    prod_df = pd.DataFrame.from_records(
        data=InsurerValue.objects.all().values('year', 'month', 'category__category', 'category__clubbed_name', 'product__lob', 'value')
    )
    prod_df.rename(columns={'year': 'Year', 'month': "Month", 'category__category': "Category", 'category__clubbed_name': "Clubbed Name", 
                            'product__lob': "Product", 'value': "Value"}, inplace=True)
    labels = [label[0] for label in prod_df.groupby(["Product", "Year"]).sum(['Value']).index]

    data_dict = prod_df.groupby(["Product", "Year"]).sum(['Value']).to_dict()["Value"]
    data = {"labels": labels, "dataset": [{'label': year, 'data': [round(data_dict[i], 2) for i in data_dict if i[1] == str(year)]} for year in sorted(prod_df['Year'].unique())[:2]]}
    for enum, i in enumerate(data['dataset']):
        print(enum)
        i['stack'] = "Stack " + str(enum)
        i['borderWidth']= 2
        if enum == 0:
            i['borderColor'] = 'rgb(255, 205, 86)'
            i['backgroundColor'] = 'rgba(255, 205, 86, 0.4)'
        else:
            i['borderColor'] = 'rgb(75, 192, 192)'
            i['backgroundColor'] = 'rgba(75, 192, 192, 0.4)'
    return JsonResponse(data)
