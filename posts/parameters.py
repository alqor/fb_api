import os

HOST = 'https://graph.facebook.com'
API = 'v12.0'

DB_PAGE_ID = os.environ['DB_PAGE_ID']
DB_LONG_LIVED_TOKEN = os.environ['DB_LONG_LIVED_TOKEN']

# I use PG here because the database was actually postgres
PG_CONN = os.environ['PG_CONN']

PG_SCHEMA = 'facebook_insights'
PG_DAILY_PAGE_TAB = 'page_daily_data'
PG_POST_GEN_TAB = 'fb_post_data'
PG_POST_METRICS_TAB = 'fb_post_metrics'
