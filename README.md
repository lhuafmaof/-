# 代码分析助手（python脚本）
利用openai api来分析项目，快速的了解整体项目的情况。提高代码阅读的效率，菜鸡专用。

# 为什么做这么一个东西？
最近gpt的出现，只要是个人就能写点代码。对，就是我这种菜鸡。然后会遇到两个问题：
1、ai没学过的代码，就tm乱写，然后就要找github 的项目来看。
2、看得时候就是盲人摸象，英文不好+基本没有代码基础。各种好项目根本看不懂，如同看见刘亦菲不知道她的美在哪里？让人十分不能接受。
所有就有了用轮子造轮子拆解轮子的想法。

# 本项目实现的功能：
## 1、整体分析
+ First item  让人快速知道这个项目是干什么
+ Second item  用什么语言写的
+ Third item   使用了哪些框架
+ Fourth item  有哪些文件，都是干什么的，哪些是代码，哪些是配置文件等等。

## 2、具体文件分析
+ First item   当前文件路径（方便找文件）
+ Second item  当前代码主要结构
+ Third item   当前代码主要逻辑

# 本项目依赖
也可以查看requeirement文件。
annotated-types==0.7.0
anyio==4.4.0
certifi==2024.6.2
colorama==0.4.6
distro==1.9.0
gitdb==4.0.11
GitPython==3.1.43
h11==0.14.0
httpcore==1.0.5
httpx==0.27.0
idna==3.7
openai==1.33.0
pydantic==2.7.3
pydantic_core==2.18.4
smmap==5.0.1
sniffio==1.3.1
tqdm==4.66.4
typing_extensions==4.12.2

# 使用教程 （开发1年以上的麻烦跳过，免得侮辱你）
