"""Hello Analytics Reporting API V4."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd, pprint


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = '<REPLACE_WITH_JSON_FILE>'
VIEW_ID = '<REPLACE_WITH_VIEW_ID>'
"""Initializes an Analytics Reporting API V4 service object."""
credentials = ServiceAccountCredentials.from_json_keyfile_name(
		KEY_FILE_LOCATION, SCOPES)
# Build the service object.
analytics = build('analyticsreporting', 'v4', credentials=credentials)

def get_report(dimension, metric, filter_, start, end, pageToken):
	makeList = lambda item, name: [{name: i} for i in item] if isinstance(item, list) else [{name: item}]
	return analytics.reports().batchGet(body={'reportRequests': [{
		'viewId': VIEW_ID,
		'dateRanges': [{'startDate': start, 'endDate': end}],
		'dimensions': makeList(dimension, 'name'), 
		'metrics': makeList(metric, 'expression'),
		'dimensionFilterClauses': [{'filters': [filter_]}],
		'orderBys': makeList(dimension, 'fieldName'),
		'pageToken': pageToken,
		'pageSize': '10000'
	}]}).execute()

def print_response2(response):
	output = []
	report = response.get('reports', [])[0]
	for row in report.get('data', {}).get('rows', []):
		dimension = row.get('dimensions', [])
		metric = row.get('metrics', [])[0].get('values', [])
		output.append(dimension+[float(m) for m in metric])
	columnHeader = report.get('columnHeader', {})
	dimensionHeader = columnHeader.get('dimensions', [])
	metricHeader = [c.get('name') for c in columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])]
	df = pd.DataFrame(output, columns = dimensionHeader+metricHeader)
	return df, report.get('nextPageToken', None)
	
def main(dimension, metric, filter_, start, end):
	pageToken = '0'
	tables = []
	while pageToken:
		response = get_report(dimension, metric, filter_, start, end, pageToken)
		df, pageToken = print_response2(response)
		tables.append(df)
		size = pageToken if pageToken else len(df)
		print(size, dimension, metric, start, end)
	return pd.concat(tables)
