# -*-coding:utf-8-*-
import os
import sys
import django
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.local')
django.setup()

from django_redis import get_redis_connection
from system_manage.org_manage_serializers import OrgTreeSerializer, OrgFlattenSerializer
from loguru import logger
from users.models import Org
import datetime
from impala.dbapi import connect
from django.db import connections
redis_cli = get_redis_connection('default')

IMPALA = {
    'host': '172.16.99.3',
    'port': 27009,
    'user': '*******',
    'password': '********',
}

log_path = os.path.abspath(os.path.join(__file__, '../logs/synchronization_orginfo.log'))
logger.add(sink=log_path, level='INFO', retention='10 days', rotation="00:00", enqueue=True)


def synchronization_org_info():
    connection = connections['default']
    # 取消外键约束
    with connection.cursor() as cursor:
        cursor.execute('SET FOREIGN_KEY_CHECKS=0;')

    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    sql = f"""
        SELECT
            orgname as org_name,
            -- orgType as org_type,
            orgcode as org_code,
            sortno as order_index,
            case when id = '19b68aac3f7d11ef96edba6936edc966' THEN '3f615c8f0dce11e99d340242ac110003' 
            else parentid 
            end as parent_id,
            id as org_id,
            `state`
        FROM ods.ods_erp_ms_supplychain_tb_sys_organization_df
        WHERE dt="{yesterday}" and entid = "0481f3a70dce11e980f00242ac110002"
    """

    try:
        with connect(**IMPALA, timeout=60) as db:
            with db.cursor(user=IMPALA['user'], dictify=True) as cursor:
                cursor.execute('refresh ods.ods_erp_ms_supplychain_tb_sys_organization_df')
                cursor.execute(sql)
                org_info = cursor.fetchall()

                for org in org_info:
                    logger.info(f"开始更新 --- {org}")
                    Org.objects.update_or_create(defaults=org, org_id=org['org_id'])
                    logger.info(f"更新成功 --- {org}")

                qs = Org.objects.all().order_by('order_index')
                resp = OrgFlattenSerializer(qs, many=True)
                resp_tree = OrgTreeSerializer(qs.filter(org_type__isnull=True, org_name="圆心科技"), many=True)
                orgs_list = json.dumps(resp.data)
                orgs_tree = json.dumps(resp_tree.data)
                # redis_cli.set("orgs_list", orgs_list)
                # redis_cli.set("orgs_tree", orgs_tree)

    except Exception as e:
        logger.error(f"出现错误：{e}")

    finally:
        # 启用外键约束
        with connection.cursor() as cursor:
            cursor.execute('SET FOREIGN_KEY_CHECKS=1;')

if __name__ == '__main__':
    synchronization_org_info()
