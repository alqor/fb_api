""""
Contains only selected metrics for usage in sample data collection.
Full list could be find here -
https://developers.facebook.com/docs/graph-api/reference/v12.0/insights
"""

# metrics with by and
# metrics with not real-time mark
# should be treated different

PAGE_METRICS_ENGAGEMENT = [
    'page_engaged_users',
    'page_post_engagements',
    'page_consumptions',
    'page_consumptions_unique',
    # 'page_consumptions_by_consumption_type',
    # 'page_consumptions_by_consumption_type_unique',
    'page_negative_feedback',
    'page_negative_feedback_unique',
    # 'page_negative_feedback_by_type',
    # 'page_negative_feedback_by_type_unique',
    # 'page_positive_feedback_by_type',
    # 'page_positive_feedback_by_type_unique',
    # 'page_fans_online', # not real-time
    # 'page_fans_online_per_day', # not real-time
    # 'page_fan_adds_by_paid_non_paid_unique'
]

PAGE_METRICS_IMPRESSIONS = [
    'page_impressions',
    # 'page_impressions_unique',
    'page_impressions_paid',
    # 'page_impressions_paid_unique',
    # 'page_impressions_organic',
    # 'page_impressions_organic_unique',
    # 'page_impressions_viral',
    # 'page_impressions_by_city_unique', # not real-time
    # 'page_impressions_by_age_gender_unique'  # not real-time
]

PAGE_METRICS_POSTS = [
    'page_posts_impressions',
    # 'page_posts_impressions_unique',
    'page_posts_impressions_paid',
    # 'page_posts_impressions_paid_unique',
    # 'page_posts_impressions_organic',
    # 'page_posts_impressions_organic_unique',
]

PAGE_METRICS_REACTIONS = [
    'page_actions_post_reactions_like_total',
    'page_actions_post_reactions_love_total',
    'page_actions_post_reactions_wow_total',
    'page_actions_post_reactions_haha_total',
    'page_actions_post_reactions_sorry_total',
    'page_actions_post_reactions_anger_total'
]

PAGE_METRICS_DEMOGRAPHICS = [
    'page_fans',
    # 'page_fans_city',
    # 'page_fans_gender_age',
    'page_fan_adds',
    # 'page_fans_by_like_source',
    'page_fan_removes',
    # 'page_fans_by_unlike_source_unique',
]

PAGE_METRICS_VIEWS = [
    'page_views_total',
    # 'page_views_external_referrals',
    # 'page_views_by_site_logged_in_unique',
]

PAGE_METRICS_VIDEO = [
    'page_video_views',
    'page_video_views_paid',
    'page_video_views_click_to_play',
    'page_video_views_unique',
    'page_video_complete_views_30s',
    'page_video_complete_views_30s_paid',
]
# POSTS!!
POST_METRICS_ENGAGEMENT = [
    'post_engaged_users',
    'post_negative_feedback',
    'post_negative_feedback_unique',
    'post_engaged_fan',
    'post_clicks',
    'post_clicks_unique',
]

POST_METRICS_IMPRESSIONS = [
    'post_impressions',
    'post_impressions_unique',
    'post_impressions_paid',
    'post_impressions_paid_unique',
    'post_impressions_fan',
    'post_impressions_fan_unique',
    'post_impressions_fan_paid',
    'post_impressions_fan_paid_unique',
]

POST_METRICS_REACTIONS = [
    'post_reactions_by_type_total',
    # The "like" reaction counts include both "like" and "care" reactions. (care - hugging heart)
]

POST_METRICS_VIDEO = [
    'post_video_avg_time_watched',
    'post_video_length',
    'post_video_views',
    'post_video_views_paid',
]
