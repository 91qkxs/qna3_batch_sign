## Qna3批量签到脚本

- 邀请链接：
  https://qna3.ai/?inviteCode=3EwnfTtN

  https://qna3.ai/?inviteCode=3cxXpKyR

  https://qna3.ai/?inviteCode=kFFwkduE

  https://qna3.ai/?inviteCode=T3jMhz7E

- 项目初始化使用：

  ​			第一步：python环境（本人用的3.9.7）

  ​			第二步：clone项目

  ​			第三步：命令终端输入'pip3 install -r requirements.txt'导包

- 批量创建钱包使用方法

  ​			第一步：找到qna3_batch_create.py文件 

  ~~~python
  if __name__ == '__main__':
      generate_and_save_wallets('generate_wallets.txt', 100)
  ~~~

  ​			第二步：拉到最后找到上面代码，第一个参数generate_wallets.txt是你生成钱包放的文件目录名称，第二个参数100就是一次生成多少个钱包

  ​			第三步：运行qna3_batch_create.py文件即可批量生成钱包，生成钱包格式：addresss,private_key 每行一个

- 批量转账使用方法

  ​			第一步：找到qna3_batch_tranf.py文件

   ~~~python
  # 示例调用
  wallet_file = "from_wallets.txt"
  new_file = "to_wallets.txt"
  t_file = "success_wallets.txt"
  transfer_from_new_to_wallet(wallet_file, new_file, t_file)
   ~~~

  ​			第二步：拉到文件最后，找到上面代码

  ​			第三步：wallet_file：你要转出obnb的钱包地址（有opbnb余额的），建议多个钱包分发，new_file：你要转入的钱包地址，t_file：转账成功的钱包地址

  ​							需要注意这些钱包格式都是：addresss,private_key 每行一个

  ​			第四步：运行qna3_batch_tranf.py文件即可

- 批量邀请签到使用方法

  ​			第一步：wallets.txt里面放入你的地址和私钥信息格式：addresss,private_key 每行一个（建议小号本地运行，放到云服务器丢失不负责）

  ​			第二步：找到qna3_sign文件，替换代码中的邀请码既可以，运行 qna3_sign文件即可批量邀请签到，如果签到的账号是新账号就会自动加入你的圈子，

  ​						 每个账号20个名额，邀请满了第一次440积分左右

  

  

  ​			

  

- 细节注意：

  ​		代理相关：号多的话建议挂代理，把这里的代理相关替换为你的，不会百度一下就好了，几十个号就没必要

  ![QvCQL1](https://raw.githubusercontent.com/91qkxs/tc/file/uPic/QvCQL1.png)

  ​		线程问题：线程休眠根据你需要自己调整即可