import requests
import urllib.parse
import re
from datetime import datetime
import pandas as pd

from .parameters import *

def get_last_hour_posts():
    """
    Get the latest hour post ods
    :return:
    """
    until = int(datetime.timestamp(datetime.now()))
    since = until - 60 * 60

    all_posts_req_string = f'{HOST}/{API}/{DB_PAGE_ID}/posts'
    params = {
        'access_token': DB_LONG_LIVED_TOKEN,
        'fields': 'id',
        'since': since,
        'until': until,
    }
    all_posts_resp = requests.get(all_posts_req_string, params=params)
    resp_data = all_posts_resp.json().get('data')
    ids = [get_post_id(post) for post in resp_data]

    return ids


def get_post_id(data):
    """
    Parse
    :param data:
    :return:
    """
    post_id = data.get('id').split('_')[1]
    return post_id


def get_original_post_link(fb_link):
    parsed_link = urllib.parse.unquote(fb_link)
    pattern = r"(php\?u=)(.+)(&h=)"

    return re.search(pattern, parsed_link).group(2)


def get_post_general_data(post_id):
    # PAGEID_POSTID?fields=created_time,attachments{url,media_type},message,shares,permalink_url <- in API explorer

    post_url_req_string = f'{HOST}/{API}/{DB_PAGE_ID}_{post_id}'
    params = {
        'access_token': DB_LONG_LIVED_TOKEN,
        'fields': 'created_time,attachments{url,media_type},message,shares,permalink_url',
        # refactor into separate file in list shape, then import here and
    }

    post_url_resp = requests.get(post_url_req_string, params=params)

    # yea, we should create more fancy parser
    resp_json = post_url_resp.json()

    if resp_json.get('error'):
        print(resp_json.get('error'))
        return

    created_time = resp_json.get('created_time')
    message = resp_json.get('message')
    post_url = resp_json.get('permalink_url')

    # shares_count = resp_json.get('shares').get('count')

    attachments = resp_json.get('attachments').get('data')[0]
    url_to_parse = attachments.get('url')
    media_type = attachments.get('media_type')

    if media_type == 'link':
        original_url = get_original_post_link(url_to_parse)
    else:
        original_url = url_to_parse

    post_object = {
        'post_id': post_id,
        'created_time': created_time,
        'message': message,
        'media_type': media_type,
        'original_url': original_url,
        'post_url': post_url,
        # 'shares_count': shares_count,
    }
    return post_object


def get_reaction_number(reactions_dict, reaction):
    val = reactions_dict.get(reaction)
    return val if val else 0


def get_post_metrics_data(post_id):
    """
    PAGEID_POSTID/insights?metric=post_impressions,post_impressions_paid,post_clicks_by_type,post_reactions_by_type_total,post_negative_feedback_by_type <- in API explorer
    Shitty as hell, will refactor
    :param post_id:
    :return: dict with metrics or None
    """
    post_metric_req_str = f'{HOST}/{API}/{DB_PAGE_ID}_{post_id}/insights?'
    metrics = [
        'post_impressions',
        'post_impressions_paid',
        'post_clicks_by_type',
        'post_reactions_by_type_total',
        'post_negative_feedback_by_type'
    ]
    params = {
        'access_token': DB_LONG_LIVED_TOKEN,
        'metric': ','.join(metrics)
    }

    post_metrics_resp = requests.get(post_metric_req_str, params=params)
    metrics_data = post_metrics_resp.json().get('data')

    if not metrics_data:
        print(post_metrics_resp)
        return

    post_impressions = metrics_data[0]['values'][0]['value']
    post_impressions_paid = metrics_data[1]['values'][0]['value']

    post_clicks = post_metrics_resp.json()['data'][2]['values'][0]['value']
    post_clicks_other = get_reaction_number(post_clicks, 'other clicks')
    post_clicks_link = get_reaction_number(post_clicks,'link clicks')

    post_reactions = post_metrics_resp.json()['data'][3]['values'][0]['value']
    post_reactions_like = get_reaction_number(post_reactions, 'like')
    post_reactions_love = get_reaction_number(post_reactions, 'love')
    post_reactions_haha = get_reaction_number(post_reactions, 'haha')
    post_reactions_sorry = get_reaction_number(post_reactions, 'sorry')
    post_reactions_wow = get_reaction_number(post_reactions, 'wow')
    post_reactions_anger = get_reaction_number(post_reactions, 'anger')

    post_negative_feedback = post_metrics_resp.json()['data'][4]['values'][0]['value']
    post_neg_fb_hide_all = get_reaction_number(post_negative_feedback, 'hide_all_clicks')
    post_neg_fb_hide_clicks = get_reaction_number(post_negative_feedback, 'hide_clicks')
    post_neg_fb_report_spam_clicks = get_reaction_number(post_negative_feedback, 'report_spam_clicks')
    post_neg_fb_unlike_page_clicks = get_reaction_number(post_negative_feedback, 'unlike_page_clicks')

    post_metrics_object = {
        'post_id': post_id,
        'extracted_time': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+0000'),
        'post_impressions': post_impressions,
        'post_impressions_paid': post_impressions_paid,
        'post_clicks_other': post_clicks_other,
        'post_clicks_link': post_clicks_link,
        'post_reactions_like': post_reactions_like,
        'post_reactions_love': post_reactions_love,
        'post_reactions_haha': post_reactions_haha,
        'post_reactions_sorry': post_reactions_sorry,
        'post_reactions_wow': post_reactions_wow,
        'post_reactions_anger': post_reactions_anger,
        'post_neg_fb_hide_all': post_neg_fb_hide_all,
        'post_neg_fb_hide_clicks': post_neg_fb_hide_clicks,
        'post_neg_fb_report_spam_clicks': post_neg_fb_report_spam_clicks,
        'post_neg_fb_unlike_page_clicks': post_neg_fb_unlike_page_clicks
    }

    return post_metrics_object
