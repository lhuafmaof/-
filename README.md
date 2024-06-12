# 代码分析助手（python脚本）
利用openai api来分析项目，快速的了解整体项目的情况。提高代码阅读的效率，菜鸡专用。

# 为什么做这么一个东西？
最近gpt的出现，只要是个人就能写点代码。对，就是我这种菜鸡。然后会遇到两个问题：

1.ai没学过的代码，就tm乱写，然后就要找github 的项目来看。
2.看得时候就是盲人摸象，英文不好+基本没有代码基础。各种好项目根本看不懂，如同看见刘亦菲不知道她的美在哪里？让人十分不能接受。

所有就有了用轮子造轮子拆解轮子的想法。

# 本项目实现的功能：
## 1、整体分析
+ 让人快速知道这个项目是干什么
+ 用什么语言写的
+ 使用了哪些框架
+ 有哪些文件，都是干什么的，哪些是代码，哪些是配置文件等等。
![image](https://github.com/lhuafmaof/code-analysis/assets/33141484/2e9cf350-f796-4412-a20f-0851bae61c36)


## 2、具体文件分析
+ 当前文件路径（方便找文件）
+ 当前代码主要结构（主要是包、类、方法的使用情况）
+ 当前代码主要逻辑（主要是由几个函数，大致是什么关系）
![image](https://github.com/lhuafmaof/code-analysis/assets/33141484/fd37f1cd-4366-42e2-97d9-789a951c0243)


# 本项目依赖
也可以查看requeirement文件。
+ annotated-types==0.7.0
+ anyio==4.4.0
+ certifi==2024.6.2
+ colorama==0.4.6
+ distro==1.9.0
+ gitdb==4.0.11
+ GitPython==3.1.43
+ h11==0.14.0
+ httpcore==1.0.5
+ httpx==0.27.0
+ idna==3.7
+ openai==1.33.0
+ pydantic==2.7.3
+ pydantic_core==2.18.4
+ smmap==5.0.1
+ sniffio==1.3.1
+ tqdm==4.66.4
+ typing_extensions==4.12.2

# 使用教程 （开发1年以上的麻烦跳过，怕侮辱你）
## 1、下载脚本到本地解压
![image](https://github.com/lhuafmaof/code-analysis/assets/33141484/394a3d85-d500-4ee9-907c-c125b525bb92)

### 本地创建项目，把文件放到项目下。
![image](https://github.com/lhuafmaof/code-analysis/assets/33141484/1f81be01-7b3a-4354-bc41-9c3776c7839a)

项目类型选择python。

## 2、安装相关依赖
可以命令行运行下面命令一键安装
pip install -r requirements.txt
![image](https://github.com/lhuafmaof/code-analysis/assets/33141484/14c00c3b-2f6a-4679-a2ec-45d8624ac712)

这个一定要提前做，不要直接跑脚本，不然会一直报缺这个、少那个。和炒菜前先把调料、配菜先准备好一个道理。

## 3、配置openai api
！！！ 不要改代码，图简单直接把key放代码里，不安全。容易被其他人白嫖你在openai充的钱。
### 方法1、本地电脑配置环境变量（推荐）
+ 右键点击“此电脑”或“我的电脑”，选择“属性”。
+ 选择“高级系统设置”。
+ 点击“环境变量”按钮。
+ 在“系统变量”或“用户变量”部分，点击“新建”或“编辑”按钮来添加或修改环境变量。

### 方法2、本地虚拟环境配置
![image](https://github.com/lhuafmaof/code-analysis/assets/33141484/eb7209c8-8202-4806-94b4-be2c223a018a)
![image](https://github.com/lhuafmaof/code-analysis/assets/33141484/077889df-28f1-471d-b70f-9a0ebd02171f)

