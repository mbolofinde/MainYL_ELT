import logging


logger = logging.getLogger(__name__)
table = 'yt_api'

def insert_rows(cur, conn, schema, row):

    try:
        if schema == 'staging':
            video_id = 'video_id'

            cur.execute(
                f'''INSERT INTO {schema}.{table}("Video_ID", "Video_Title","Upload_Date","Duration","Video_views","Likes_Count","Comments_Count")
                
            )
