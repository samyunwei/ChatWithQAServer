# 二级工程实践聊天问答系统服务端

## 安装
```shell script
   pip install -r requirement
   cd ./script 
   ./genprotos.sh
```


## 启动服务端
### REST
```shell script
    python3 app.py
```
### gRPC
```shell script
    python3 gRPCServer.py 
```


## 测试
```shell script
  curl -X GET http://{host}:{port}/chat?msg=hello #获取聊天对话
  curl -X GET http://{host}:{port}/dict?{method}?key=xxx&value=xxx #字典API
```

## 接下来的工作
    1. 两个模型切换的阈值判断
    2. 文档筹备