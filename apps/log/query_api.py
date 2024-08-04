# -*-coding:utf-8-*-
from pymysql import Connection
import pymysql
from datetime import datetime, timedelta
from django.conf import settings
import logging

logger = logging.getLogger('acro')


def get_chunk_data(start_date, end_date):
    """
        日志管理 - 浏览日志 - 四小块指标
    """
    yest_start_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=-1)
    yest_end_date = yest_start_date + timedelta(days=(datetime.strptime(start_date, '%Y-%m-%d') - datetime.strptime(end_date, '%Y-%m-%d')).days)

    sql = f"""
        SELECT *
        FROM 
            (SELECT
                COUNT(if(`action`='V', id , NULL)) as view_pv, 
                COUNT(DISTINCT if(`action`='V', actor_id , NULL)) as view_uv,
                COUNT(if(`action`='D', id , NULL)) as download_pv,
                COUNT(DISTINCT if(`action`='D', actor_id , NULL)) as download_uv
            FROM log_viewlog 
            WHERE 
--                 DATE_FORMAT(CONVERT_TZ(action_time,'+00:00','+08:00'), '%Y-%m-%d')  BETWEEN '{start_date}' AND '{end_date}' 
                DATE_FORMAT(action_time, '%Y-%m-%d') BETWEEN '{start_date}' AND '{end_date}') AS tmp1
        join
            (SELECT 
                COUNT(if(`action`='V', id , NULL)) as yest_view_pv, 
                COUNT(DISTINCT if(`action`='V', actor_id , NULL)) as yest_view_uv,
                COUNT(if(`action`='D', id , NULL)) as yest_download_pv,
                COUNT(DISTINCT if(`action`='D', actor_id , NULL)) as yest_download_uv
            FROM log_viewlog
            WHERE 
--                 DATE_FORMAT(CONVERT_TZ(action_time,'+00:00','+08:00'), '%Y-%m-%d') BETWEEN '{yest_start_date.date()}' AND '{yest_end_date.date()}' 
                DATE_FORMAT(action_time, '%Y-%m-%d') BETWEEN '{yest_start_date.date()}' AND '{yest_end_date.date()}' ) AS tmp2
    """

    with Connection(**settings.MYSQL_INFO) as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute(sql)
            result = cur.fetchone()
            return result


def get_line_data(start_date, end_date, metric):
    """
        日志管理 - 浏览日志 - 趋势图
    """
    format_mode = "%Y-%m-%d" if start_date != end_date else '%H'

    if metric == 'pv_line':
        if_condition = "COUNT(if(`action`='V', id , NULL)) as PV"
    elif metric == 'uv_line':
        if_condition = "COUNT(DISTINCT if(`action`='V', actor_id , NULL)) as UV"
    elif metric == 'dl_pv_line':
        if_condition = "COUNT(if(`action`='D', id , NULL)) as Download_PV"
    elif metric == 'dl_uv_line':
        if_condition = "COUNT(DISTINCT if(`action`='D', actor_id , NULL)) as Download_UV"

    sql = f"""
        SELECT 
--             DATE_FORMAT(CONVERT_TZ(action_time,'+00:00','+08:00'), '{format_mode}') as h,  
            DATE_FORMAT(action_time, '{format_mode}') as h,  
            {if_condition}
        FROM log_viewlog lv 
--         WHERE DATE_FORMAT(CONVERT_TZ(action_time,'+00:00','+08:00'), '%Y-%m-%d') BETWEEN '{start_date}' AND '{end_date}'
        WHERE DATE_FORMAT(action_time, '%Y-%m-%d') BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY h
        order BY h;
    """

    with Connection(**settings.MYSQL_INFO) as conn:
        with conn.cursor() as cur:
            logger.info(f'趋势图查询 ---> {sql}')
            cur.execute(sql)
            result = cur.fetchall()
            if start_date == end_date:
                a = map(lambda a: '0' + a if len(a) < 2 else a, [str(i) for i in range(0, 24)])
                meta_data = dict(zip(a, [i - i for i in range(0, 24)]))
                meta_data.update(dict(result))
                x_axios = [i for i in meta_data.keys()]
                y_axios = [i for i in meta_data.values()]
            else:
                x_axios = [i[0] for i in result]
                y_axios = [i[1] for i in result]
            return {"x_axios": x_axios, "y_axios": y_axios}


def get_page_top10(start_date, end_date, keyword):
    condition = []
    keyword and condition.append(f"(page_desc LIKE '%{keyword}%' OR page_url LIKE '%{keyword}%')")
    _c = f"AND {' AND '.join(condition)}" if condition else ''

    sql = f"""
        SELECT  
            page_desc, 
            page_url, 
            COUNT(*) as pv, 
            COUNT(DISTINCT actor_id) as uv
        FROM log_viewlog 
        WHERE 
--             DATE_FORMAT(CONVERT_TZ(action_time,'+00:00','+08:00'), '%Y-%m-%d') BETWEEN '{start_date}' AND '{end_date}' 
            DATE_FORMAT(action_time, '%Y-%m-%d') BETWEEN '{start_date}' AND '{end_date}' 
            AND `action` = 'V' {_c}
        GROUP BY page_desc,page_url
        order BY pv desc
    """

    with Connection(**settings.MYSQL_INFO) as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute(sql)
            result = cur.fetchall()
            return {'data': result}


def get_person_top10(start_date, end_date, keyword):
    condition = []
    keyword and condition.append(
            f"(u.name LIKE '%{keyword}%' OR l.page_desc LIKE '%{keyword}%' OR l.page_url LIKE '%{keyword}%')")
    _c = f"AND {' AND '.join(condition)}" if condition else ''

    sql = f"""
        select  
            name,
            sum(c) as pv,
            SUBSTRING_INDEX(group_concat(page_desc order by c desc),',',1)  as page_desc
        from 
            (select 
                u.id as id,
                u.name as name,
                l.page_desc as page_desc,
                count(1) as c
            from users_user u left join log_viewlog l 
            on u.id =l.actor_id 
            where  
--                 DATE_FORMAT(CONVERT_TZ(l.action_time,'+00:00','+08:00'), '%Y-%m-%d') BETWEEN '{start_date}' AND '{end_date}'
                DATE_FORMAT(l.action_time, '%Y-%m-%d') BETWEEN '{start_date}' AND '{end_date}'
                AND l.`action` = 'V'
                AND l.page_desc != "" {_c}
            group by u.id,u.name,l.page_desc
            order by count(1) desc ) tmp
        group by name 
        order by pv desc
    """

    with Connection(**settings.MYSQL_INFO) as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute(sql)
            result = cur.fetchall()
            return {'data': result}


def get_all(start_date, end_date, keyword, action, page, page_size):
    condition = []
    if action == '浏览': condition.append("`action` = 'V'")
    elif action == '导出': condition.append("`action` = 'D'")

    keyword and condition.append(f"(name like '%{keyword}%' OR page_desc LIKE '%{keyword}%' OR "
                                 f"page_url LIKE '%{keyword}%')")

    _c = f"AND {' AND '.join(condition)}" if condition else ''

    sql = f"""
        SELECT 
--             DATE_FORMAT(CONVERT_TZ(action_time,'+00:00','+08:00'), '%Y-%m-%d %H:%i') as action_time, 
            DATE_FORMAT(action_time, '%Y-%m-%d %H:%i') as action_time, 
            name, 
            CASE `action` WHEN 'V' THEN '浏览' WHEN 'D' THEN '导出' END `action` ,
            page_desc , 
            page_url , 
            client_ip 
        FROM log_viewlog left join users_user on log_viewlog.actor_id = users_user.id 
        WHERE 
--             DATE_FORMAT(CONVERT_TZ(action_time,'+00:00','+08:00'), '%Y-%m-%d') BETWEEN '{start_date}' AND '{end_date}' 
            DATE_FORMAT(action_time, '%Y-%m-%d') BETWEEN '{start_date}' AND '{end_date}' 
            {_c}
        order by action_time desc
    """

    offset = (int(page) - 1) * int(page_size)
    limit = page_size

    count_sql = f""" SELECT COUNT(*) as num  FROM ({sql}) as ps"""
    context_sql = f""" {sql} limit {limit} offset {offset} """

    with Connection(**settings.MYSQL_INFO) as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute(count_sql)
            total = cur.fetchone().get('num', 0)
            cur.execute(context_sql)
            result = cur.fetchall()
            return {'total': total, 'data': result}
