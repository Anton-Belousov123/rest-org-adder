import psycopg2

from syncer.utils import timer


@timer
def get_link_by_offer_id(offer_id):
    conn = psycopg2.connect(
        host='188.225.42.200',
        database='default_db',
        user='gen_user',
        password='Lola2011',
    )
    cur = conn.cursor()

    cur.execute(f"SELECT (s_url) FROM {'oleg'} WHERE s_article=%s", (offer_id,))
    record = cur.fetchone()
    conn.close()
    if not record:
        return None
    return record[0]


@timer
def get_all_links():
    conn = psycopg2.connect(
        host='188.225.42.200',
        database='default_db',
        user='gen_user',
        password='Lola2011',
    )
    cur = conn.cursor()

    cur.execute(f"SELECT (s_article, s_url) FROM {'oleg'};")
    record = cur.fetchall()
    conn.close()
    records = {}
    for r in record:
        items = r[0].replace('(', '').replace(')', '').split(',')
        records[items[0]] = items[1]
    return records

