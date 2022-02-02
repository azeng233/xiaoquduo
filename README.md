## 说明

本项目是在阿里云`函数计算FC`中进行部署的，代码是根据[While True: learn()](https://battlehawk233.cn/post/64.html)修改而来的。

基本功能：

- [x] 自动打卡
- [x] 邮件发送

## 配置函数调用

首先登陆`阿里云`，找到`控制台`-`函数计算FC`-`创建服务`，进入之后选择创建函数：

![image-20220202161050787](https://cdn.zengchen233.cn/img/202202021610898.png)

然后配置基本设置：

![image-20220202161319990](https://cdn.zengchen233.cn/img/202202021613075.png)

## 上传代码

代码在上方，需要的自己`clone`，这里有几点详细说明：

 详细说明：

- 打卡点 checkPlace 格式：XX省-XX市-XX区
- 联系方式 contactMethod 格式：电话号码
- 居住地 livingPlace 格式：XX省-XX市-XX区
- 详细住址 livingPlaceDetail
- 打卡省份 checkPlaceProvince
- 打卡城市 checkPlaceCity
- 打卡县市区 checkPlaceArea

以上这些是必须要填写的，另外还有一个不能忽视：

```json
"other": {
        "openid": ""
    }
```

这里是一定不能忘记的，要不然就会一直报错，这里需要用到抓包工具，我推荐一个抓包工具：[Fiddler](https://www.telerik.com/fiddler/fiddler-everywhere)。

## 获取openid

首先需要在电脑上登陆微信，找到校趣多的小程序：

![image-20220202181253494](https://cdn.zengchen233.cn/img/202202021812542.png)

用电脑打卡一次，去找到路径：

![image-20220202181541444](https://cdn.zengchen233.cn/img/202202021815541.png)

获取到自己openid以后就填写到代码当中去，这里最好先手动生成一下`config.json`,因为阿里云FC那个里面不知道是怎么回事，无法通过代码自动生成`config.json`。

## 结果截图

![image-20220202182901321](https://cdn.zengchen233.cn/img/202202021829414.png)

------

![image-20220202182916790](https://cdn.zengchen233.cn/img/202202021829832.png)

------

