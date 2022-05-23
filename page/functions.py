import requests
import datetime

import pandas as pd

from parameters import HOST, API, DB_PAGE_ID, DB_LONG_LIVED_TOKEN, PG_CONN, PG_SCHEMA


def get_page_metric_data(metric, date_preset=None, period=None, since=None, until=None):
    """
    To obtain metric from page with specified parameters.

    :param
        # PAGE_ID - (int), the ID of Facebook Page
        # TOKEN - (str), the access token for the page
        metric - (str), the metric(s) names could be find in metrics.py
            in case of multiple metrics it should be single string with comma separated metrics
        date_preset - (str, optional) - names could be found in parameters.py
        period - (str, optional) - day, week, days_28 or lifetime (depends on metric, see official documentation)
        since, until - (int) - epoch seconds of datetime

    :return: (dict) with metric(s) data
    """
    get_string = f'{HOST}/{API}/{PAGE_ID}/insights'

    data_dict = {}
    extract_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+0000')

    request_params = {
        'access_token': TOKEN,
        'metric': metric,
        'date_preset': date_preset,
        'period': period,
        'since': since,
        'until': until,
    }

    try:
        resp = requests.get(get_string,
                            params=request_params)

        data_dict = resp.json()
        data_dict['extract_time'] = extract_time

        data_dict.pop('id', None)
        data_dict.pop('paging', None)
    except Exception as e:
        data_dict['data'] = e
        # TODO: log!
    return data_dict


def parse_main(data):
    """
    To parse metrics data from json (dict)
    :param data: dict
    :return: pandas DataFrame
    """
    i = 1
    try:
        for item in data['data']:
            name = item['name']
            period = item['period']
            value = item['values'][0]['value'] if item['values'][0]['value'] else -1
            end_time = pd.to_datetime(
                item['values'][0]['end_time']) if item['values'][0]['end_time'] else pd.NaT
            extract_time = pd.to_datetime(data['extract_time'])
            data_object = {
                'name': [name],
                'value': [value],
                'end_time': [end_time],
                'extract_time': [extract_time],
                'period': [period]
            }
            metric_df = pd.DataFrame.from_dict(data_object)
            if i == 1:
                res = metric_df
            else:
                res = res.append(metric_df)
            i += 1

        return res
    except Exception as e:
        print(e)
        # TODO: log!


def parse_description(data):
    """
    To parse metrics description from json (dict)
    :param data: dict
    :return: pandas DataFrame
    """
    i = 1
    try:
        for item in data['data']:
            name = item['name']
            title = item['title']
            description = item['description']

            description_object = {
                'name': [name],
                'title': [title],
                'description': [description]
            }
            desc_df = pd.DataFrame.from_dict(description_object)
            if i == 1:
                desc_res = desc_df
            else:
                desc_res = desc_res.append(desc_df)
            i += 1
        return desc_res
    except Exception as e:
        print(e)
        # TODO: log!


def to_pg(df, table_name):
    """ 
    Write dataframe to facebook_insights schema in PG DB
    """
    df.to_sql(name=table_name, con=PG_CONN,
              schema=PG_SCHEMA, index=False, if_exists='append')
