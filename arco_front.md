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

####  各个文件解释 

1. `config/vite.config.base.ts`文件


2. `package.json`

```
{

/* package.json 和 package-lock.json 都是 Node.js 项目中的重要文件，它们共同管理项目的依赖，但它们有不同的作用和用途。下面是这两个文件的详细区别：
  1. package.json
/* package.json 是 Node.js 项目的配置文件，存储了项目的元数据和依赖信息。
/* 主要内容：
/* 项目元数据：如项目名称、版本、作者、许可证等信息。
/* 依赖管理：
/* dependencies：生产环境依赖。
/* devDependencies：开发环境依赖。
/* 项目脚本：如构建、测试、启动等命令。
/* 主要作用：
/* 定义项目的依赖和配置：当你添加新的依赖时，它们会记录在 dependencies 或 devDependencies 中。
/* 指定运行脚本：如 start、build、test 等命令，可以通过 npm run <script> 运行。
*/

  "name": "arco-design-pro-vue", /* 项目的名称 在 npm 包发布时会使用这个名称。*/
  "description": "Arco Design Pro for Vue", /* 项目的简短描述*/
  "version": "1.0.0",   /* 项目的版本号 通常遵循 SemVer 语义化版本控制规范。*/
  "private": true, /* 如果是 true，表示该项目是私有的，不能发布到 npm 仓库 .一般用于私有项目，避免错误发布。*/
  "author": "ArcoDesign Team", /* 项目的作者*/
  "license": "MIT", /* 项目的许可证类型，通常使用开源协议 MIT, 这里使用的是 MIT 许可证，意味着其他人可以自由使用、修改、分发这个项目。*/
  "scripts": {
     /* 运行 Vite 开发服务器，使用 config/vite.config.dev.ts 作为 Vite 配置文件。--open：启动后自动打开浏览器。*/
    "server": "vite --config ./config/vite.config.dev.ts --open",
    /* vue-tsc --noEmit：运行 TypeScript 类型检查，不生成 .js 文件（--noEmit）。*/
    /* vite build --config ./config/vite.config.prod.ts：用 config/vite.config.prod.ts 进行 Vite 生产环境打包。*/
    "build": "vue-tsc --noEmit && vite build --config ./config/vite.config.prod.ts",
    /*  生成打包分析报告 */
    /* cross-env REPORT=true：设置 REPORT 环境变量为 true（兼容 Windows 和 macOS）。*/
    /* npm run build：执行打包，并生成报告（可能 vite.config.prod.ts 里有 if (process.env.REPORT) {} 相关逻辑）。*/
    "report": "cross-env REPORT=true npm run build",
    "preview": "npm run build && vite preview --host",
    /* TypeScript 类型检查 */
    /* vue-tsc --noEmit：运行 TypeScript 类型检查，不生成 .js 文件。*/
    /* --skipLibCheck：跳过对 node_modules 里的 .d.ts 进行检查，提高速度。*/
    "type:check": "vue-tsc --noEmit --skipLibCheck",
    "lint-staged": "npx lint-staged",
    "prepare": "husky install"
  },
  /* dependencies 主要用来存储项目在 生产环境 下运行时需要的依赖包。这些依赖包通常是应用的核心功能所需的库或工具。*/
  /* 举例：
  /* React / Vue / Angular：前端框架
  /* Axios：用于发送 HTTP 请求
  /* Lodash：工具库
  /* 当你执行 npm install 时，dependencies 中的所有依赖都会被安装，确保生产环境能正常运行应用。
  /* 安装命令：
  /* 生产环境安装： npm install（会安装 dependencies 和 devDependencies）
  /* 只安装生产依赖： npm install --production
  */
  "dependencies": {
  },
  /* devDependencies 存储的是项目在 开发环境 中需要的依赖。这些依赖是为了 开发和构建 过程中使用的工具，通常不涉及到实际运行在生产环境中的代码。
  /* 举例：
  /* Webpack / Vite：模块打包工具
  /* Babel：代码转换工具
  /* ESLint：代码检查工具
  /* TypeScript：类型检查工具
  /* devDependencies 中的包仅用于开发和构建，生产环境中并不需要这些依赖
  /*   安装命令：
  /* 开发环境安装： npm install --save-dev 或者 npm install（默认会安装 devDependencies 和 dependencies）
  /* 只安装开发依赖： npm install --only=dev
  /*   ###### 总结 #########
  /* dependencies：生产环境下需要的包
  /* devDependencies：开发环境下需要的包（如构建工具、测试框架等）
  /* 通常情况下：
  /* 生产环境依赖：用户访问时必需的工具（Vue、React、Axios 等）
  /* 开发环境依赖：开发和构建时必需的工具（Webpack、Babel、ESLint 等）
  */
  "devDependencies": {
  },
  "engines": {
  },
  "resolutions": {
  }
}
```

2. `package-lock.json`

```
/*   package-lock.json 是由 npm 自动生成的，记录了项目所有依赖的具体版本和树形结构。

/* 主要内容：
/* 锁定依赖的具体版本：它会锁定每个依赖（包括直接依赖和间接依赖）的版本号，确保项目在不同的机器或环境中安装相同版本的依赖。
/* 依赖树结构：描述了所有依赖包的具体版本，以及它们的子依赖，保证依赖树的一致性。
/* 主要作用：
/* 确保一致性：package-lock.json 确保在不同的机器或团队成员之间，安装的依赖版本完全一致，从而避免了由于依赖版本差异导致的问题。
/* 提高安装速度：package-lock.json 中的版本信息让 npm install 更高效，能够快速解析并安装依赖。
/* 记录非直接依赖：package-lock.json 记录了 node_modules 中所有安装的包，无论是直接依赖还是间接依赖。
*/
```

3. `tsconfig.json`文件

 tsconfig.json 文件是 TypeScript 的配置文件，用于配置 TypeScript 编译器的行为。以下是对每一行的详细解释：

```
{
  "compilerOptions": { 
    "target": "ES2020",   // 指定 TypeScript 编译后 的 JavaScript 版本，这里是 ES2020。
                          影响：比如 optional chaining (?.)、nullish coalescing (??) 等新特性可以直接使用。
    "module": "ES2020",  // 指定使用 ES2020 的模块化方案（ESM），即 import/export 语法。
                          影响：确保编译后的代码仍然使用 import/export，而不是 require/module.exports（CommonJS）。
    "moduleResolution": "node", // 指定 模块解析方式，这里使用 node 解析模式（类似于 Node.js 的 require）。
                        影响：1 可以直接 import npm 包 2 可以解析 package.json 里的 "main" 字段; 3默认支持 .ts, .tsx, .js, .jsx 后缀
    "strict": true, // 开启 严格模式，包括：1 noImplicitAny（必须声明类型）2 strictNullChecks（必须处理 null 和 undefined）3 strictFunctionTypes（参数类型严格检查）
                     影响：代码更安全，但写代码时可能要多声明类型。
    "jsx": "preserve", // 用于 Vue 或 React 项目，让 tsx 文件保持 JSX 语法，不转换 JSX。
                     影响：在 Vue 项目中，setup() 里可以使用 JSX。在 React 项目中，JSX 语法不会转换，交给 babel 处理。
    "sourceMap": true, // 生成 .map 文件，方便 调试 TypeScript 代码。
                        影响：浏览器 断点调试 时，可以看到 TypeScript 源码，而不是编译后的 JavaScript。
    "resolveJsonModule": true, // 允许 import JSON 文件。 import config from "./config.json"; // ✅ 正常导入 JSON
    "esModuleInterop": true, // 允许 CommonJS (require) 和 ES6 (import/export) 互操作。
                           影响：允许 import fs from 'fs' 这样的方式，而不需要 import * as fs from 'fs'。
    "baseUrl": ".", // 指定 TypeScript 项目的根目录，这里是 当前目录（.`）。
                    影响：配合 paths，可以使用 @/ 进行路径别名。
    "paths": {  
      "@/*": ["src/*"] // 配置 路径别名，让 @/ 代表 src/ 目录。 
                       // import MyComponent from "@/components/MyComponent.vue"; // ✅ 相当于 src/components/MyComponent.vue
    },
    "lib": ["es2020", "dom"], // 指定 TypeScript 需要的 库，这里包含："es2020"：支持 ES2020 新特性（如 BigInt, Promise.allSettled） "dom"：支持 浏览器 DOM API（如 document.querySelector）。
    "skipLibCheck": true // 跳过第三方库的类型检查，提升 编译速度。 影响：TypeScript 不会检查 node_modules 里的 .d.ts 文件。
  },
  "include": ["src/**/*", "src/**/*.vue"], // （要编译的文件）指定 哪些文件 需要 TypeScript 进行编译。src/**/*：所有 TS 代码 src/**/*.vue：Vue 组件（.vue）中的 <script lang="ts">
  "exclude": ["node_modules"] // 不编译的文件
}

```


## 项目拆解 

### 一 登录  `arco_front/src/views/login/index.vue`

1. 登录区域使用组件 `<LoginForm />` 位置 `src/views/login/components/login-form.vue`
2. `<LoginForm />`组件中调用`useStore`登录接口`login`方法 ，遇到请求拦截器
   2.1 点击提交调用`handleSubmit`，校验表单是否有误。
   2.1 表单无误，调用登录接口`userStore.login`
      - 调用接口前`被请求拦截器`拦截,位置`src/api/interceptor.ts` 方法：`axios.interceptors.request.use((config: AxiosRequestConfig)=>{}`
   2.2 当你发起一个请求时，Axios 会创建一个 AxiosRequestConfig 对象来存储这个请求的所有配置信息。然后，拦截器会接收到这个对象，允许你在请求真正发送之前进行修改。
       - 响应拦截 1 正确 直接返回响应内容 2 有错 判断属于什么错误，返回错误内容
   2.4 `useStore.login`方法, 将`token` 存入`localStorage`
   2.5 拦截请求响应`axios.interceptors.response.use`，处理接口的响应，弹出对应错误
        
3. 登录成功后，需要跳转路由，遇到`路由导航守卫`,位置`src/router/guard/index.ts` eg: 如果登录地址是这样的 `http://localhost:6888/login?redirect=users_manage`, 代表登录后要跳转到`系统管理-用户管理`
   
   3.1 守卫一 `setupPageGuard(router)` 中调用 `setRouteEmitter(to)`函数，将当前路由信息 to 传递给事件监听器，以触发路由变化的事件。
   3.2 守卫二 如果已登录，没有角色，请求用户信息`userStore.info()`
   3.4 守卫三 未登录，调用登出接口`userStore.logout()`，重定向到登录页面。
   
### 一 登录后 初始页面怎么加载出来的 eg:`http://localhost:6888/dashboard/workplace`
1. `src/views/login/components/login-form.vue` 在登陆后，如果链接后面没有跟重定向页面，就设定`Workplace`
2. 命中 路由`Workplace`，就会将`该组件内容`以及`父组件`加载出来
3. 该组件路由 `src/router/routes/modules/dashboard.ts`，包含父组件`DEFAULT_LAYOUT`
4. `DEFAULT_LAYOUT` 组件在 `src/router/routes/base.ts`导出。
5. `html`页面自上而下加载，`import`的模块会优先执行，哪怕它写在`console`后面。这是`ES Modules` 的标准机制！
   这样做的好处是：
      保证模块依赖是 可预测且静态的（静态分析才能实现 Tree-shaking、预加载等优化）
      保证执行顺序符合模块依赖关系 
      允许工具像 Vite / Webpack 更高效地编译/

### 页面组件嵌套, 布局组件（导航栏，侧边栏，页面结构（页面内容，就是自己的匹配到的路由））
```html
DEFAULT_LAYOUT(<NavBar />，<Menu/>，PageLayout(</router-view>))
```



### 页面展示 什么样的菜单树？

#### 原理

1. 前端配置了所有路由 
2. 后端返回能看到哪些菜单树 
3. 前端去遍历后端返回的菜单树，后端返回的 name companent 具体啥时候能用上？
4. 即使访问一个存在的路由，路由导航守卫也会去看他在不在服务端的菜单中，在的话，才可以看。

#### 代码实现

1. 页面渲染 `/src/components/menu/index.vue` , 通过执行该函数`renderSubMenu()`渲染出菜单。

2. 该函数 `renderSubMenu()` 利用到了 `menuTree` 该变量来自 `/src/components/menu/use-menu-tree.ts` 中的 `useMenuTree()`

3. 该函数`useMenuTree()` 又读取了 `appRoute`, 该变量就是关键。

   - 菜单来自于前端静态写的 `appClientMenus` 由`保护登录页`，`404` ，`登录页` `模块页` 整合后的一个列表
   - 菜单来自于后端获取 `appStore.appAsyncMenus` 只有 `模块页`


   ```html
   const appClientMenus = mixinRoutes.map((el) => {
     const { name, path, meta, redirect, children } = el;
     return {
       name, // 路由名称
       path, // 路由路径 
       meta, // 路由元数据 （如是否需要认证，是否在菜单栏中显示等）
       redirect, // 路由重定向路径
       children, // 子路由
     };
   });
   ```
   
   ```html
     const appRoute = computed(() => { //  是一个计算属性，根据 appStore.menuFromServer 的值返回从服务端或者本地 获取菜单数据
       if (appStore.menuFromServer) {
         console.log(filePath,'从后端获取菜单树-->',appStore.appAsyncMenus)
         // console.log(filePath,'后端菜单 追加 前端菜单')
         return appStore.appAsyncMenus;
       }
       console.log(filePath, '从前端获取菜单树-->',appClientMenus)
       return appClientMenus;
     });
   ```
