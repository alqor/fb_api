import pandas as pd
from parameters import *
from functions import get_post_metrics_data, get_last_hour_posts, get_post_general_data


def main():
    # get last hour posts and collect their general data

    new_ids = get_last_hour_posts()

    new_posts_gen_data = pd.DataFrame()
    for post_id in new_ids[:4]:
        df = get_post_general_data(post_id)
        new_posts_gen_data = new_posts_gen_data.append(df, ignore_index=True)

    new_posts_gen_data.to_sql(PG_POST_GEN_TAB,
                              con=PG_CONN,
                              schema=PG_SCHEMA,
                              if_exists='append',
                              index=False)

    # get all post_ids that were created less than 100 hours ago
    sql = f"""SELECT post_id 
             FROM {PG_SCHEMA}.{PG_POST_GEN_TAB} 
             WHERE created_time::TIMESTAMP >= CURRENT_TIMESTAMP - INTERVAL '100 hour'"""

    post_metrics_ids = pd.read_sql(sql, PG_CONN)['post_id'].to_list()

    # get metrics data
    metrics_df = pd.DataFrame()

    for id in post_metrics_ids:
        try:
            d = get_post_metrics_data(id)
            # print(d)
            metrics_df = metrics_df.append(d, ignore_index=True)
        except Exception as e:
            print(e)
            continue

    metrics_df.to_sql(PG_POST_METRICS_TAB,
                      con=PG_CONN,
                      schema=PG_SCHEMA,
                      if_exists='append',
                      index=False)

    print("I'm done")


if __name__ == "__main__":
    main()
