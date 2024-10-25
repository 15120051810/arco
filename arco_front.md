```
├── App.vue
├── api
│ ├── dashboard.ts
│ ├── permission.ts
│ └── user.ts
├── assets
│ ├── images
│ ├── logo.svg
│ ├── style
│ └── world.json
├── components
│ ├── breadcrumb
│ ├── chart
│ ├── footer
│ ├── global-setting
│ ├── index.ts
│ ├── menu
│ ├── message-box
│ ├── navbar
│ └── tab-bar
├── config
│ └── settings.json
├── directive
│ ├── index.ts
│ └── permission
├── env.d.ts
├── hooks
│ ├── permission.ts
│ └── visible.ts
├── layout
│ ├── default-layout.vue
│ └── page-layout.vue
├── locale
│ └── zh-CN.ts
├── main.ts
├── mock
│ ├── index.ts
│ ├── message-box.ts
│ └── user.ts
├── router
│ ├── app-menus
│ ├── constants.ts
│ ├── guard  路由导航守卫
│ ├── index.ts 
│ ├── routes
│ └── typings.d.ts
├── store
│ ├── index.ts
│ └── modules
├── types
│ ├── echarts.ts
│ ├── global.ts
│ └── mock.ts
├── utils
│ ├── auth.ts
│ ├── date-handle.ts
│ ├── env.ts
│ ├── event.ts
│ ├── index.ts
│ ├── is.ts
│ ├── monitor.ts
│ ├── route-listener.ts
│ └── setup-mock.ts
└── views
    ├── dashboard
```

步骤

1. main.ts 文件
    - 实例化App
    - `app.use(router)` 注册路由，

2. `router/guard` 路由上集成了各个导航守卫
    - setupPageGuard(router); 设置页面守卫
    - setupUserLoginInfoGuard(router); 用户登录信息守卫
    - setupPermissionGuard(router); 权限守卫
        - 获取用户菜单 `/api/user/menu`
    刷新页面的时候，会走导航守卫，重新获取用户菜单，和用户信息。获取用户信息的时候，会更新`$state`

3. 请求拦截器 `api/interceptor.ts` 

3. 登录页面点击登录按钮后，
4. 返回用户信息，用户所属角色，用户能够看到的路由菜单信息

####     