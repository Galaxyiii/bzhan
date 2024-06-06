### 项目运行所需环境：
python>=3.8，aiohttp>=3.8.3，pymongo>=3.9.0，uvicorn>= 0.18.3，fastapi>=0.85.1，torch>=1.13，transformers>=4.24，tqdm，jieba>=0.42.1

集群环境：Hadoop(2.10.2)`+`Spark(3.1.3)

### 项目运行步骤：
**运行爬虫程序。**
**运行数据处理程序。**
**涉及到spark处理的程序放到集群上运行。**
**运行后端的main函数下载预训练模型到本地。**

**打开mongodb：**
进入bin目录，打开cmd
输入：mongod -f ../conf/mongod.conf

**Pycharm 运行后端的命令：**
G:bigdataproject> uvicorn main:app --reload --host 0.0.0.0 --port 8000

**Pycharm 运行前端的命令：**
运行conda的虚拟环境：
(MyPytorchTensorflow) G:\bigdataproject\Visualization\bigdata-project>npm run dev

**访问：**http://localhost:4000/
