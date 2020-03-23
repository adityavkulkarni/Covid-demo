import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
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

def yesterday():
    import datetime 
    yesterday = datetime.date.today() - datetime.timedelta(days = 1)
    return str(yesterday)

def table_to_df(URL):
    html = requests.get(URL)
    soup = BeautifulSoup(html.text)
    tables = soup.find_all("table")
    output = []
    for table in tables:
        output_rows = []
        for table_row in table.findAll('tr'):
            columns = table_row.findAll('td')
            output_row = []
            for column in columns:
                output_row.append(column.text)
            output_rows.append(output_row)
        output.append(output_rows)
    return output

def update_data():
	URL = 'https://www.mohfw.gov.in/'
	df = pd.DataFrame(table_to_df(URL)[1])
	df = df.drop(0,axis=1)
	df = df.drop(0,axis=0)
	df.columns = ['Name of State / UT', 'Total Confirmed cases (Indian National)','Total Confirmed cases ( Foreign National )','Cured/Discharged/Migrated','Deaths'] 
	ind = []
	for i in range(len(df)):
	    ind.append(i)
	df.index = ind
	stats = df.loc[len(df)-1,:]
	total_cnf_ind_cases = stats['Name of State / UT']
	total_cnf_for_cases = stats['Total Confirmed cases (Indian National)']
	total_cnf_for_cases = total_cnf_for_cases.replace('\n','')
	total_cnf_for_cases = total_cnf_for_cases.replace(' *','')
	total_cnf_ind_cases = total_cnf_ind_cases.replace(' *','')
	
	total_cases = int(total_cnf_for_cases)+int(total_cnf_ind_cases)
	total_cured = int(stats['Total Confirmed cases ( Foreign National )'].replace('\n',''))
	total_death = int(stats['Cured/Discharged/Migrated'].replace('\n',''))
	df = df.drop(len(df)-1,axis=0)
	per_day = pd.read_csv('data/perday.csv')
	per_day = per_day.drop('Unnamed: 0',axis = 1)
	per_day_latest = per_day.loc[len(per_day)-1,:]
	date = yesterday()	
	new_cases = per_day_latest['New Cases']
	if per_day_latest['Date']!= date:
	
		new_cases = int(total_cases) - int(per_day_latest['Total Cases'])
		active_cases = int(total_cases) - int(total_cured) - int(total_death)
		days_since_100 = per_day_latest['Days after surpassing 100 cases']+1.0
		new_row = [date,total_cases,new_cases,active_cases,total_cured,total_death,days_since_100]
		col = list(per_day.columns)
		per_day = per_day.append(pd.Series(new_row, index=col), ignore_index=True)
		per_day.to_csv('data/perday.csv')
		df.to_csv('data/covidin.csv')
	return new_cases

	











