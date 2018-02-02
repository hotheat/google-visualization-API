import csv
import gviz_api

def get_gviz_data():
    afile = "./data/median-dpi-countries.csv"
    datarows = []
    with open(afile, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            datarows.append(row)
    description = {
        "country": ("string", "Country"),
        "dpi": ("number", "EUR")
    }

    data = []
    for each in datarows:
        data.append({
            'country': each[0],
            'dpi': (float(each[1]), each[1])
        })

    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)
    json = data_table.ToJSon(columns_order=("country", "dpi"),
                             order_by='country')
    return json
