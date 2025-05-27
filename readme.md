



#### Arco


### 目录结构

```
├──arco                                项目根
├──apps                                
│    ├──system_manage                     系统管理                      
│    ├──arco_demo                         arco_demo                      
│    ├──log                               日志                                        
│    ├──users                             用户信息相关                      
│    ├──download_center                   下载中心                      
├──deploy                              部署文档                             
     ├──dev                               测试环境                             
     ├──prod                              生产环境                           
├──docs                                项目相关文档                             
     ├──deploy.md                         部署文档                             
     ├──api.md                            api接口文档                             
├──settings                            环境区分       
     ├──base.py                           基础环境        
     ├──local.py                          开发环境        
     ├──dev.py                            测试环境        
     ├──prod.py                           生产环境        
├──utils                               工具 
│    ├── common.py                        共用的（eg:常量）            
│    ├── middleware.py                    中间件           
├──libs                                第三方封装 
│    ├── mysql_wrapper                    mysql封装
│    ├── impala_wrapper                   impala封装    
│    ├── exceptions                        全局异常捕获       
├──logs                                日志目录
      ├──log.log                           程序日志
      ├──middleware.log                    中间件日志
├──readme.md                           
├──manage.py                           启动文件
├──requirements.txt                    配置文件

```



