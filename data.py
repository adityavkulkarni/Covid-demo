def get_data_from_kaggle():
	import kaggle
	kaggle.api.authenticate()
	kaggle.api.dataset_download_files('parulpandey/coronavirus-cases-in-india', path='/home/aditya/dash/data', unzip=True)

def highlight_max(s):
    is_max = s == s.max()
    return ['background-color: pink' if v else '' for v in is_max]
