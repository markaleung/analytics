# analytics
Link Google Analytics' API to Pandas Dataframes

This module allows you to read from Google Analytics' API as a Pandas DataFrame. Before using this module, please read the Google Quickstart: https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py

The module has one method: 

main(dimensions, metrics, filter_, start, end)
- dimensions is a list of dimensions. 
- metric is a list of metrics. 
- filter_ is a DimensionFilters dictionary such as {"dimensionName": "ga:browser", "operator": "EXACT", "expressions": ["Chrome"]}. 
- start is a date string. 
- end is a date string. 

The method returns a Pandas DataFrame with one column for each dimension and metric. It returns all data for multipage results. 

For more information about dimensions, and metrics, see https://developers.google.com/analytics/devguides/reporting/core/dimsmets. 

For more information about everything else, see https://developers.google.com/analytics/devguides/reporting/core/v4/basics. 
