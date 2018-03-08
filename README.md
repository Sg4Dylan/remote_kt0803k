
## 简易的 KT0803K 远程控制 API 服务 
---

介绍：
就是一个远程控制 KT0803K 的 Python 脚本，稍微加点料可以与常用物联网服务或聊天工具配合使用。
~~没有X用的东西~~

需要的准备：
 - 树莓派一块
 - 已安装连接好的 kt0803k (自行确认可以使用)
 - 编译好并已放到环境变量目录的驱动程序 [rpi-kt0803k](https://github.com/inguardians/rpi-kt0803k) (自行确认 `--query` 命令能读取到芯片信息)
 - Python 3.6+ (修改下拼字符串的方法就能兼容 3.x 了)
 - [sh](https://github.com/amoffat/sh)
 - aiohttp

使用方法：
 - API 接口
 `http://监听地址:监听端口/api` (自行修改代码硬编码的参数)
 - 查询芯片状态，对接口 POST 以下 JSON
 ```
    {
        "mode":"query",
        "appkey":"程序内硬编码的APPKEY"
    }
 ```
 - 设置芯片属性，对接口 POST 以下 JSON
 ```
    {
        "mode":"query",
        "appkey":"程序内硬编码的APPKEY",
        "setting":{
            "channel": 77000, # 只包含当前需要修改的属性
            "mute": false
        }
    }
 ```

支持设置的属性：
具体解释详见项目 [rpi-kt0803k](https://github.com/inguardians/rpi-kt0803k)，简略的详见代码 #L17
