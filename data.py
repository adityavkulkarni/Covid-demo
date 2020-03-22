def get_data_from_kaggle():
	import kaggle
	kaggle.api.authenticate()
	kaggle.api.dataset_download_files('parulpandey/coronavirus-cases-in-india', path='/home/aditya/dash/data', unzip=True)

def highlight_max(s):
    is_max = s == s.max()
    return ['background-color: pink' if v else '' for v in is_max]

def create_table(df):
    table=df.to_html(classes='w3-table w3-striped w3-bordered w3-border w3-hoverable w3-white')
    table = table.replace('\n','')
    table = table.replace('dataframe','')
    table = table.replace('border="1"','')
    table = table.replace('style="text-align: right;"','')
    table = table.replace('<th></th>','<th>States</th>')
    table = table.replace(' <tr>      <th>Name of State / UT</th>      <th>States</th>    </tr>','')
    return table
