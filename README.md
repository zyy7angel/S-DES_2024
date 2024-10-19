# S-DES_2024
Implementation and exploration of S-DES encryption algorithm
## 关卡测试
***
### 第一关：基本测试
  * 输入明文：“11111111”；输入密钥：“1111111111”；加密结果：“00001111”
![](images/encrypt.jpg)
  * 输入密文：“00001111”；输入密钥：“1111111111”；解密结果：“11111111”
![](images/decrypt.jpg)
  * 错误输入提示报错
![](images/error.jpg)
***
### 第二关：交叉测试
1. 加密  
    明文：11111111  
    密钥：1111111111
* 我们组加密情况：
 ![](images/encrypt.jpg)
* 史亚涛组加密情况：
  ![](https://github.com/Yhaokaf/S-DES/blob/master/README.assets/image-20241007172406648.png)
2. 解密  
    密文：11111110  
    密钥：1111111111  
* 我们组解密情况：
  ![](images/decrypt_with_syt.png)  
* 史亚涛组解密情况：
  ![](https://github.com/Yhaokaf/S-DES/blob/master/README.assets/image-20241007172543059.png)
***
### 第三关：扩展功能
考虑到向实用性扩展，加密算法的数据输入可以是ASII编码字符串(分组为1 Byte)，对应地输出也可以是ACII字符串(很可能是乱码)。
1. 字符串加密  
   明文：abandon    
   密钥：1111111111  
   加密结果：CCSãS  
   ![](images/acsii_encrypt.jpg)
2. 字符串解密  
   密文：CCSãS  
   密钥：1111111111  
   解密结果：abandon
   ![](images/ascii_decrypt.jpg)
***
### 第四关：暴力破解
假设你找到了使用相同密钥的明、密文对(一个或多个)，请尝试使用暴力破解的方法找到正确的密钥Key。在编写程序时，你也可以考虑使用多线程的方式提升破解的效率。请设定时间戳，用视频或动图展示你在多长时间内完成了暴力破解。

   
   
  
