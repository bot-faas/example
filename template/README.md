## 函数模板

支持语言如下：

* go 1.16
* node 16
* python 3.9
* php 7.4



### 本地调试

#### 环境变量配置

运行时会读取环境变量中的值，用于调用sdk等操作，可以在运行前先执行如下命令：

**Windows**

```powershell
set APP_ID=xxxx
set APP_TOKEN=xxxx
set SANDBOX_BOT=true
set HOME_URL=https://bot.icodef.com
```

**Linux**

```bash
export APP_ID=xxxx
export APP_TOKEN=xxxx
export SANDBOX_BOT=true
export HOME_URL=https://bot.icodef.com
```

建议写成脚本放在模板目录下



如果是使用IDE，可以在IDE中进行配置，以Goland举例：

点击`Edit Configurations...`进入配置

![image-20220318180458089](./README.assets/image-20220318180458089.png)

点击环境变量的编辑按钮

![image-20220318180651190](./README.assets/image-20220318180651190.png)

输入环境变量

![14640D19200AC99A996899175787F90E](./README.assets/14640D19200AC99A996899175787F90E.jpg)



#### 启动调试

首先需要启动机器人等消息转发程序，请注意该机器人需要在平台上添加且运行

```
./bot-faas-debug forward --appid xxx --apptoken xxx --sandbox --addr localhost:8080
```

其中addr是本地调试函数执行的http地址，模板中默认使用8080端口接收消息，默认只会转发AtMessage消息事件，更多详情可使用`--help`查看详情



### 开发

使用本地调试模板时，请以`function`目录为开发目录，`handler/Handle`方法为入口方法（具体内容请参考语言的模板文件），在平台提交单文件模式的代码也为`handler/Handle`的代码。如果是完整的项目请将整个`function`文件夹压缩为zip进行上传，同时也需要存在语言的包声明文件：php(composer.json)、python(requirements.txt)、node(package.json)，建议使用国内镜像源进行安装。



本地调试，请使用函数模板下的`index`文件启动函数，其中`demo`文件夹是一些函数的示例，`pkg`文件夹是平台内置的一些函数，用于获取数据库、sdk等操作。


### 数据库

如果需要使用数据库请自行在本地配置，默认的函数模板使用数据库需要配置两个环境变量分别是：

* BOT_FAAS_MONGODB_URI # MongoDB的链接URI
* BOT_FAAS_MONGODB_DBNAME # MongoDB的链接数据库名字

配置方法请参考[本地调试](#本地调试)
