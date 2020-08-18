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
  curl -X GET http://{host}:{port}/chat?msg=hello
```

## 接下来的工作
    1.将模型放到工程里
    2.模型代码实现输入输出接口
    3.客户端服务端接口联调  