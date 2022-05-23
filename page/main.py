from functions import get_page_metric_data, parse_main, to_pg
from itertools import chain

from metrics import PAGE_METRICS_ENGAGEMENT, PAGE_METRICS_IMPRESSIONS, \
    PAGE_METRICS_POSTS, PAGE_METRICS_REACTIONS, PAGE_METRICS_DEMOGRAPHICS, \
    PAGE_METRICS_VIEWS, PAGE_METRICS_VIDEO

from parameters import PG_DAILY_PAGE_TAB


def main():
    metrics_list = list(chain(PAGE_METRICS_ENGAGEMENT, PAGE_METRICS_IMPRESSIONS,
                              PAGE_METRICS_POSTS, PAGE_METRICS_REACTIONS, PAGE_METRICS_DEMOGRAPHICS,
                              PAGE_METRICS_VIEWS, PAGE_METRICS_VIDEO))

    metrics = ','.join(metrics_list)

    data_today = get_page_metric_data(metric=metrics,
                                      period='day',
                                      date_preset='today')

    metrics_df = parse_main(data_today)
    to_pg(metrics_df.loc[:, ['name', 'value', 'end_time', 'extract_time']], PG_DAILY_PAGE_TAB)


if __name__ == "__main__":
    main()
