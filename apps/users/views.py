import itertools

from django.db.models import Q
from django.shortcuts import render

# Create your views here.

import logging
import requests, json
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from users.serializers import UserSerializer
from users.models import User, Role, Org, Api, Router
from utils.common import tree_to_list
from system_manage.serializers import OrgTreeSerializer, OrgTwoTreeSerializer, DepartmentalProjectTreeSerializer, \
    MedicalWorkerDPTreeSerializer
from utils.common import USER_DEFAULT_PASSWORD, BASE_KEYWORD
from utils.get_jwt_token import get_token
from rest_framework.permissions import IsAuthenticated
from utils.common import get_user_org, get_appoint_parent, paginate, give_org_return_shop
from utils.permissions import APIPermission

logger = logging.getLogger("arco")


class CheckBaseTokenView(APIView):
    """
    Base后台跳转带过来的token，解析并获取用户信息。
    """

    def post(self, request):
        base_token = request.data.get("base_token")
        logger.info(f"base_token ---> {base_token}")

        response = requests.post(url=settings.BASE_CHECKTOKEN_URL,
                                 data={"token": base_token, "keyword": BASE_KEYWORD}, timeout=30)

        # logger.info(f"response.content ---> {response.content}")
        res_content = json.loads(response.content)
        # logger.info(f"res_content ---> {res_content}")

        username, real_name, email, staff_code, phone = list(
            map(res_content["data"]["user"].get, ["username", "realname", "email", "staff_code", "phone"]))
        logger.debug(
            f"username, real_name, email, staff_code, phone ---> {username, real_name, email, staff_code, phone}")
        app_list = res_content["data"].get("app_list")
        logger.info(f"app_list ---> {app_list}")

        user_obj = User.objects.filter(username=username).first()

        if not user_obj:
            user_obj = User.objects.create_user(username=username, name=real_name, email=email,
                                                password=USER_DEFAULT_PASSWORD, mobile=phone, staff_code=staff_code)

            role_obj = Role.objects.filter(name="普通用户").first()
            user_obj.roles.add(role_obj.id)
            user_obj.save()
        else:
            user_obj.staff_code = staff_code
            user_obj.mobile = phone
            user_obj.save()

        my_token = get_token(user_obj)
        router_o = {}
        if user_obj.home_page_id:
            router_obj = Router.objects.filter(id=user_obj.home_page_id, roles__role_users=user_obj).first()
            if router_obj: router_o = {'name': router_obj.name, 'title': router_obj.title}
        return Response({"token": my_token, "app_list": app_list, 'router_obj': router_o})


class DestroyBaseTokenView(APIView):
    """销毁BaseToken"""

    def post(self, request):
        base_token = request.data.get("base_token")
        logger.info(f"base_token ---> {base_token}")

        response = requests.post(url=settings.BASE_CHECKLOGOUT_URL, data={"token": base_token, "keyword": BASE_KEYWORD},
                                 timeout=30)
        res_content = json.loads(response.content)
        logger.info(f"销毁结果 ---> {res_content}")

        return Response(res_content)


class UserViewSet(ListModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["GET"])
    def info(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=200, data=serializer.data)


class GetUserRegionProvinceTreeAPIView(APIView):
    """
        获取 用户所属 大区 / 省区树形结构
    """
    permission_classes = [IsAuthenticated, APIPermission]

    def get(self, request):
        user_org_list = request.user.orgs.filter(Q(org_type__in=[1, 2]) | Q(org_name='圆心科技'))
        org_ser = OrgTwoTreeSerializer(user_org_list, many=True)

        tmp = list(map(lambda x: tree_to_list(x, ['key', 'title', 'org_type']), org_ser.data))
        org_list = list(itertools.chain(*tmp))

        result = {
            "org_tree": org_ser.data,
            "org_list": org_list
        }
        return Response(result)


class GetUserDepartmentalProjectTreeView(APIView):
    """
        获取 用户所属 部门 / 项目树形结构
    """
    permission_classes = [IsAuthenticated, APIPermission]

    def get(self, request):
        dp_ser = DepartmentalProjectTreeSerializer(
            request.user.departmental_project.filter(state=1).order_by('order_index'), many=True)

        tmp = list(map(lambda x: tree_to_list(x, ['departmental_project_id', 'name', 'type']), dp_ser.data))
        dp_list = list(itertools.chain(*tmp))

        result = {
            "dp_tree": dp_ser.data,
            "dp_list": dp_list
        }
        return Response(result)


class GetUserMedicalWorkerDPTreeView(APIView):
    """
        获取 用户所属 部门 / 项目树形结构
    """
    permission_classes = [IsAuthenticated, APIPermission]

    def get(self, request):
        dp_ser = MedicalWorkerDPTreeSerializer(
            request.user.medical_worker_dp.filter(state=1).order_by('order_index'), many=True)

        tmp = list(map(lambda x: tree_to_list(x, ['departmental_project_id', 'name', 'type']), dp_ser.data))
        dp_list = list(itertools.chain(*tmp))

        result = {
            "dp_tree": dp_ser.data,
            "dp_list": dp_list
        }
        return Response(result)


class GetUserOrgsView(APIView):
    """
        获取用户 所属机构 （只是机构）
    """
    permission_classes = [IsAuthenticated, APIPermission]

    def get(self, request):
        result = get_user_org(request)
        logger.info(f'获取机构 {len(result)}')
        orgs = [{"org_id": org['org_id'], "org_name": org["org_name"]} for org in result if org['org_type'] in (6, 9)]
        return Response(orgs)


class GetUserChainCorpView(APIView):
    """
        获取用户 所属连锁总部 （只是连锁总部）
    """
    permission_classes = [IsAuthenticated, APIPermission]

    def get(self, request):
        result = get_user_org(request)
        logger.info(f'获取连锁总部 {len(result)}')
        orgs = [{"org_id": org['org_id'], "org_name": org["org_name"]} for org in result if org['org_type'] == 9]
        logger.info(f'获取连锁总部过滤完毕 {len(orgs)}')
        return Response(orgs)


class GetUserRegionsView(APIView):
    """获取用户所属大区"""

    def get(self, request):
        get_regions = lambda **kwargs: Org.objects.exclude(is_ds=1).filter(org_type=1, **kwargs)
        orgs_provinces = get_regions() if request.user.is_superuser else get_regions(users__id=request.user.id)
        org_list = [{"org_name": org.org_name,"org_id":org.org_id} for org in orgs_provinces]
        logger.info(f"用户所属大区 {org_list}")
        return Response(org_list)


class GetUserProvinceView(APIView):
    """获取用户在机构表里中 省份下拉"""

    def get(self, request):
        user_id = request.user.id
        pass


class AppletLogin(APIView):

    def post(self, request):
        mobile = request.data.get('mobile')
        user_obj = User.objects.filter(mobile=mobile).first()
        if not user_obj: return Response({'code': 40000, 'message': '该用户没权限 或 手机号不匹配'})

        logger.info(f"用户 {user_obj.name} 登录了小程序")
        my_token = get_token(user_obj)
        resp = requests.post(url=f'{settings.DC_DOMAIN}/account/login',
                             json={'username': 'sjcpydd', 'password': 'sjcp123@Ydd'}).json()
        logger.info(f"大数据登录返回结果 ---> {resp}")
        dsj_token = resp['data']['token'] if resp['code'] == 20000 else ''

        routers_all = [i.title for i in Router.objects.filter(type=1, system=1).order_by('order_index')]
        my_routers = [i.title for i in Router.objects.filter(type=1, system=1, roles__role_users=user_obj.id)]
        router_res = [{'title': router, 'is_show': True if router in my_routers else False} for router in routers_all]

        return Response({
            'code': 20000,
            'id': user_obj.id,
            'name': user_obj.name,
            'username': user_obj.username,
            'staffCode': user_obj.staff_code,
            'mobile': user_obj.mobile,
            'email': user_obj.email,
            'token': my_token,
            'bigDataToken': dsj_token,
            'routers': router_res
        })


class AppletGetSuperOrg(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        org_id = request.query_params.get('org_id')
        tier = request.query_params.get('tier')
        req_type = request.query_params.get('req_type')

        if org_id:
            if req_type == 'lower' and tier == '2':  # 获取下级 大区查省区
                one_org_obj = Org.objects.filter(org_id=org_id).first()
                two_org_list = [{"org_id": i.org_id, "org_name": i.org_name} for i in
                                one_org_obj.children.filter(org_type=2)]
                two_org_list and two_org_list.insert(0, {'org_id': '', 'org_name': '全部省区'})

                return Response({
                    'code': 20000,
                    'tier': 2,
                    'one_org': {"org_id": one_org_obj.org_id, "org_name": one_org_obj.org_name},
                    'data': two_org_list
                })

            elif req_type == 'lower' and tier == '3':  # 获取下级 省区查门店
                two_org_obj = Org.objects.filter(org_id=org_id).first()
                two_org_tree = OrgTreeSerializer([two_org_obj], many=True)
                three_org_list = list(map(lambda x: tree_to_list(x, ['org_id', 'org_name']), two_org_tree.data))
                three_org_list = list(itertools.chain(*three_org_list))
                three_org_list = [i for i in three_org_list if i['org_id'] != two_org_obj.org_id]
                three_org_list and three_org_list.insert(0, {'org_id': '', 'org_name': '全部门店'})

                return Response({
                    'code': 20000,
                    'tier': 3,
                    'one_org': {"org_id": two_org_obj.parent.org_id, "org_name": two_org_obj.parent.org_name},
                    'two_org': {"org_id": two_org_obj.org_id, "org_name": two_org_obj.org_name},
                    'data': three_org_list
                })

            elif req_type == 'echo' and tier == '2':  # 获取本级 省回显：大区 + 省区
                one_org_obj = Org.objects.get(org_id=org_id).parent
                one_org_res = {"org_id": one_org_obj.org_id, "org_name": one_org_obj.org_name}
                two_org_list = [{"org_id": i.org_id, "org_name": i.org_name} for i in one_org_obj.children.all()]

                my_two_org_list = [org['org_id'] for org in get_user_org(request) if org['org_type'] == 2]
                my_two_org_list_result = [i for i in two_org_list if i['org_id'] in my_two_org_list]
                my_two_org_list_result and my_two_org_list_result.insert(0, {'org_id': '', 'org_name': '全部省区'})

                return Response({
                    'code': 20000,
                    'tier': 2,
                    'one_org': one_org_res,
                    'data': my_two_org_list_result
                })

            elif req_type == 'echo' and tier == '3':  # 获取本级 门店回显：大区 + 省区 + 门店
                three_org_obj = Org.objects.filter(org_id=org_id).first()
                one_org_obj = get_appoint_parent(three_org_obj, org_type=1)
                one_org_res = {"org_id": one_org_obj.org_id, "org_name": one_org_obj.org_name}
                two_org_obj = get_appoint_parent(three_org_obj, org_type=2)
                two_org_res = {"org_id": two_org_obj.org_id, "org_name": two_org_obj.org_name}

                three_org_tree = OrgTreeSerializer(two_org_obj)
                three_org_list = list(map(lambda x: tree_to_list(x, ['org_id', 'org_name']), [three_org_tree.data]))
                three_org_list = list(itertools.chain(*three_org_list))
                three_org_list = [i for i in three_org_list if i['org_id'] != two_org_obj.org_id]

                my_three_org_list = [org['org_id'] for org in get_user_org(request) if org['org_type'] == 6]
                my_three_org_list_result = [i for i in three_org_list if i['org_id'] in my_three_org_list]
                my_three_org_list_result and my_three_org_list_result.insert(0, {'org_id': '', 'org_name': '全部门店'})

                res = {'code': 20000, 'tier': 3, 'data': my_three_org_list_result, 'one_org': one_org_res,
                       'two_org': two_org_res}
                return Response(res)
        else:
            if req_type == 'echo' and tier == '2':
                user_org_list = request.user.orgs.filter(Q(org_type__in=[1, 2]) | Q(org_name='圆心科技'))
                org_ser = OrgTwoTreeSerializer(user_org_list, many=True)
                tmp = list(map(lambda x: tree_to_list(x, ['key', 'title', 'org_type']), org_ser.data))
                org_list = list(itertools.chain(*tmp))
                two_org_list = [{'org_id': i['key'], 'org_name': i['title']} for i in org_list if i['org_type'] == 2]

                return Response({'code': 20000, 'tier': 2, 'data': two_org_list})

            elif req_type == 'echo' and tier == '3':
                result = get_user_org(request)
                org_list = [{"org_id": org['org_id'], "org_name": org["org_name"]} for org in result if
                            org['org_type'] == 6]
                return Response({'code': 20000, 'tier': 3, 'data': [org_list[0]]})

            else:
                user_obj = request.user.orgs.filter(org_name='圆心科技').first()
                user_org_queryset = Org.objects.filter(org_type=1) if user_obj else request.user.orgs.filter(org_type=1)
                if user_org_queryset:
                    user_org = [{'org_id': i.org_id, "org_name": i.org_name} for i in user_org_queryset]
                    user_obj and user_org.insert(0, {'org_id': '', 'org_name': '全国'})
                    return Response({'code': 20000, 'tier': 1, 'data': user_org})
                user_org_queryset = request.user.orgs.filter(org_type=2)
                if user_org_queryset:
                    user_org = [{'org_id': i.org_id, "org_name": i.org_name} for i in user_org_queryset]
                    return Response({'code': 20000, 'tier': 2, 'data': user_org})
                user_org_queryset = request.user.orgs.filter(org_type=6).order_by('org_name')
                if user_org_queryset:
                    user_org = [{'org_id': i.org_id, "org_name": i.org_name} for i in user_org_queryset]
                    return Response({'code': 20000, 'tier': 3, 'data': user_org})
                return Response({'code': 40000, 'message': '请联系相关人员配置权限'})


class AppletSearchOrg(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        keyword = request.query_params.get('keyword')
        page_size = int(request.query_params.get('page_size', 10))
        page_number = int(request.query_params.get('page_number', 1))

        result = get_user_org(request)
        logger.info(f'获取机构 {len(result)}')
        orgs = [{"org_id": org['org_id'], "org_name": org["org_name"], "name": org["org_name"]} for org in result if
                org['org_type'] == 6]
        orgs = [org for org in orgs if keyword in org['org_name']]

        result = paginate(orgs, page_size, page_number)
        return Response({'code': 20000, 'data': result, 'total': len(orgs)})


class GetOrgReturnShopAPIView(APIView):
    """给一个组织返回该组织下所有的门店"""
    permission_classes = [IsAuthenticated, APIPermission]

    def get(self, request):
        logger.info(f"request {request.query_params}")
        org_id = request.query_params.get('org_id')
        org_list = give_org_return_shop(org_id)
        return Response({'org_list': org_list})
