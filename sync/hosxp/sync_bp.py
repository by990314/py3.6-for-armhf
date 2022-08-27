import requests
import time
from datetime import datetime
from con_db import con

api_host = 'http://localhost:3000'
end_point_get_visit = "patient/get_today_visit_by_cid"
end_point_post_data = "bp/post_data_bp"


def get_today_visit_number(cid):
    r = requests.get(f"{api_host}/{end_point_get_visit}/{cid}")
    resp = r.json()
    if resp:
        return resp['visit_number'], resp['visit_date'], resp['visit_time']
    else:
        return None, None, None


def post_data(vn, row):
    data = {
        'vn': vn,
        'data': {
            'tp': row['tp'],
            'bps': row['bps'],
            'bpd': row['bpd'],
            'pulse': row['pulse'],
        }
    }
    r = requests.post(f"{api_host}/{end_point_post_data}", json=data)
    return r.json()


def do():
    print('BP==========', str(datetime.now())[:-7], '==========')
    sql = "select * from smart_gate_bp where vn is null or trim(vn) = ''"
    with con.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
        if not rows:
            print('None Rows has null Vn.')
        for row in rows:
            _id = row['id']
            cid = row['cid']
            vn, _date, _time = get_today_visit_number(cid)
            if vn:
                resp = post_data(vn, row)
                print(cid, resp)
                if resp['vn']:
                    sql = f"update smart_gate_bp set vn = '{vn}',d_sync = now() where id = {_id} "
                    cursor.execute(sql)

            else:
                print(cid, 'VN is none.')

    con.commit()
    print()


def run():
    while 1:
        do()
        time.sleep(5)


run()