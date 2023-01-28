# 信息检索系统

### 分词技术

分词技术就是搜索引擎针对用户提交查询的关键词串进行的查询处理后根据用户的关键词串用各种匹配方法进行分词的一种技术。相比于英文分词技术，中文分词技术更加复杂和困难，这是由于中文在基本文法上有其特殊性，具体表现在：与英文为代表的拉丁语系语言相比，英文以空格作为天然的分隔符，而中文由于继承自古代汉语的传统，词语之间没有分隔；同时，在中文里，“词”和“词组”边界模糊。

目前的中文分词工具有**jieba**、**SnowNLP**、**THULAC**、**NLPIR**等，本文使用Python jieba进行分词处理。

### 倒排索引机制

为了保证信息检索系统的速度和效率，通常要对文档库中的文档建立索引。**倒排索引**（inversed index）是目前大多数信息检索系统所使用的索引机制。倒排索引的数据结构从逻辑上可分为两部分：一部分是索引，其中列出了文档库中所有的索引项。另一部分由多个位置表组成，每个位置表和索引中的某个索引项对应，其中记录了所有出现过该索引项的文档以及出现位置。

<img src="C:\Users\12944\AppData\Roaming\Typora\typora-user-images\image-20220613155105936.png" alt="image-20220613155105936" style="zoom:50%;" />

<center style = 'font-weight:bolder'>Fig 1 倒排索引机制</center>

### 向量空间检索匹配算法

向量空间模型（VSM：Vector Space Model）由Salton等人于20世纪70年代提出，并成功地应用于文本检索系统。VSM概念简单，把对文本内容的处理简化为向量空间中的向量运算，并且它以空间上的相似度表达语义的相似度，直观易懂。当文档被表示为文档空间的向量，就可以通过计算向量之间的相似性来度量文档间的相似性。文本处理中最常用的相似性度量方式是余弦距离。

向量空间对于相关性度量的算法由如下几个步骤描述：

1. 计算权重(Term weight)的过程

   影响一个词(Term)在一篇文档中的重要性主要有两个因素：

   Term Frequency ($TF$)：即此Term在此文档中出现了多少次。$TF$越大说明越重要。

   Document Frequency ($DF$)：即有多少文档包含Term。$DF$ 越大说明越不重要。

   我们有：
   $$
   W_{t,doc} = {TF}_{t,doc}*\log{(\frac{n}{DF_{t}})}
   $$
   其中n为总文档的数量。

2. 2.判断Term之间的关系从而得到文档相关性的过程，也即向量空间模型的算法(VSM)。

   我们把文档看作一系列词(Term)，每一个词(Term)都有一个权重(Term weight)，不同的词(Term)根据自己在文档中的权重来影响文档相关性的打分计算。
   于是我们把所有此文档中词(term)的权重(term weight) 看作一个向量。

   $Document = {t_1, t_2, …… ,t_N}$

   $Document_Vector = {W_{1,d}, W_{2,d}, …… ,W_{N,d}}$

   同样我们把查询语句看作一个简单的文档，也用向量来表示。

   $Document = {t_1, t_2, …… ,t_N}$

   $Document_Vector = {W_{1,q}, W_{2,q}, …… ,W_{N,q}}$

   则有：
   $$
   score(q,d) = cos(\theta) = \frac{\sum_{i=1}^{n} W_{i,q}W{i,d}}{\sqrt{\sum_{i=1}^{n} W_{i,q}^2}\cdot \sqrt{\sum_{i=1}^{n} W_{i,d}^2}}
   $$

<img src="C:\Users\12944\AppData\Roaming\Typora\typora-user-images\image-20220613155419358.png" alt="image-20220613155419358" style="zoom:50%;" />

<center style = 'font-weight:bolder'>Fig 2 文档和查询语句的向量表示</center>

## 实验内容与实验设计

### 文件树

文件树显示本项目的**核心文件**

```
Information retrieval - : 总文件夹 
	data - ： 数据文件夹
		data_content : 文本数据文件夹
		data_url : 文本数据链接
	InvertedIndex : 分词与倒排索引构建文件夹
		inverted.py: 分词与倒排索引构建文件
	WebSpide ：网络爬虫文件夹
		spider.py：网络爬虫文件
	WebGUI : 图形化界面文件夹
		web_client: 网页GUI
		log: 查询日志文件夹
		search.py: 查询处理文件
		server.py: 网页服务器后端
```

### 网络爬虫与数据存储模块

#### 技术框架

- **Requests**

  **Requests库是一个Python的第三方库，可以通过调用来帮助我们实现自动爬取HTML网页页面以及模拟人类访问服务器自动提交网络请求。**Requests可以实现对目标url进行各种方式的网络请求

- **Selenium**

  **Selenium是一个用于测试网站的自动化测试工具**，支持各种浏览器包括Chrome、Firefox、Safari等主流界面浏览器，同时也支持phantomJS无界面浏览器。Selenium通过模拟浏览器真实操作进行自动化测试，可以访问动态加载的网页数据，并能实现包括点击、拖动、停留、数据录入等事件，协助数据爬取工作完成。

  <img src="C:\Users\12944\AppData\Roaming\Typora\typora-user-images\image-20220614002237955.png" alt="image-20220614002237955" style="zoom:50%;" />

<center style = 'font-weight:bolder'>Fig 3 Requests</center>

#### 模块设计与核心代码

- spider.py

  ```python
  def get_data():def get_data():
      if os.path.exists('./news_url.txt'):
          news_file = open('./news_url.txt', 'r')
          news_list_str = news_file.read()
          news_list = ast.literal_eval(news_list_str)
          news_file.close()
      else:
          origin_url = 'https://new.qq.com'
          browser = webdriver.Chrome(service=Service('./chromedriver.exe'))
          browser.get(origin_url)
          for i in range(10):
              browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
              time.sleep(3)
          page_text = browser.page_source
          tree = etree.HTML(page_text)
          web_news_list = tree.xpath("//ul[@class = 'list']//div[@class = 'detail']//h3/a/@href")
          news_list = []
          news_list.extend(web_news_list)
          news_file = open('news_url.txt', 'w')
          news_file.write(str(news_list))
          news_file.close()
          print(len(news_list))
          time.sleep(5)
          browser.quit()
  
      if not os.path.exists('../data/data_content'):
          os.makedirs('../data/data_content')
      if not os.path.exists('../data/data_url'):
          os.makedirs('../data/data_url')
      page = 1
      for index, url in enumerate(news_list):
          res = requests.get(url)
          page_tree = etree.HTML(res.text)
          try:
              title = page_tree.xpath('//h1/text()')[0]
          except:
              continue
          ret = page_tree.xpath("//div[@class = 'content-article']")[0].xpath(".//p/text()")
          if not ret:
              continue
          print(page)
          for i in range(len(ret)):
              ret[i] = ret[i].strip()
          raw_content = ''.join(ret)
          content = raw_content.strip()
          fnews = open(os.path.join('../data/data_content', str(page) + '.txt'), 'w', encoding='utf-8')
          time.sleep(0.3)
          fnews.write(title + '\n' + content + '\n')
          fnews.close()
          fnewsurl = open(os.path.join('../data/data_url', str(page) + '.txt'), 'w', encoding='utf-8')
          fnewsurl.write(url)
          page += 1
          fnewsurl.close()
  ```

  通过 Python Requests 和 Selenium模拟浏览器操作，爬取（>100 条有效数据）腾讯新闻并存储在data数据文件夹中。

### 分词与倒排索引建立模块

#### 技术框架

- **jieba分词**

  **jieba分词是一款基于 Python 设计的中文分词组件。**其支持四种分词模式：精确模式、全模式、搜索引擎模式和paddle模式。本设计使用搜索引擎模式，通过调用`jieba.cut_for_search` 方法进行。该方法接受两个参数：需要分词的字符串；是否使用 HMM 模型。搜索引擎模式适合用于设计信息检索系统，用于构建倒排索引的分词，粒度比较细。

- **使用混合索引的方式优化查询**

#### 模块设计与核心代码

- Inverted.py

  核心部分代码如下：

  ```python
  def word_segmention():
      fstopwords = open('./cn_stopwords.txt', 'r', encoding='utf-8')
      stopwords = fstopwords.read()
      fstopwords.close()
      news_set = glob.glob('../data/data_content/*.txt')
      for index in range(len(news_set)):
          fnews = open(os.path.join('../data/data_content', str(index + 1) + '.txt'), 'r', encoding='utf-8')
          news = fnews.read()
          fnews.close()
          pre_news_words = jieba.lcut_for_search(news)
          news_words = []
          for words in pre_news_words:
              if words not in stopwords:
                  news_words.append(words)
          words_dict = dict(Counter(news_words))
          for word, value in words_dict.items():
              if word in words_freq:
                  words_freq[word] += 1
                  words_index[word].append(index)
              else:
                  words_freq[word] = 1
                  words_index[word] = [index]
          fnewsurl = open(os.path.join('../data/data_url', str(index + 1) + '.txt'), 'r', encoding='utf-8')
          now_url = fnewsurl.read()
          fnewsurl.close()
          global_news.append({
              'title': news[0:news.find('\n')],
              'url': now_url,
              'words': words_dict
          })
      fdata = open("../data/global_data.txt", 'w', encoding='utf-8')
      fdata.write(str(words_freq) + '\n' + str(words_index) + '\n' + str(global_news) + '\n')
  ```

  处理爬虫模块获取的数据，进行中文分词、停用词处理、建立倒排索引、控制数据的持久化。

### 文本查询模块

#### 技术框架

基于倒排索引机制和向量空间检索匹配算法进行查询，并生成日志文件。具体算法原理已在前文中进行介绍。

<img src="C:\Users\12944\AppData\Roaming\Typora\typora-user-images\image-20220614002402200.png" alt="image-20220614002402200" style="zoom:50%;" />

<center style = 'font-weight:bolder'>Fig 4 倒排索引</center>

#### 模块设计与核心代码

- search.py

  ```python
  def search(text):
      if not global_news:
          load()
      raw_words = jieba.lcut_for_search(text)
      words = []
      for word in raw_words:
          if word not in stopwords:
              words.append(word)
      words_dict = dict(Counter(words))
      news_set = set()
      for word in words:
          news_set = news_set | set(words_index[word])
      news_list = list(news_set)
      res_list = []
      for index in news_list:
          col_top = 0.0
          col_bot1 = 0.0
          col_bot2 = 0.0
          for word, value in words_dict.items():
              now_weight = get_weight(value, words_freq[word])
              if word in global_news[index]['words']:
                  col_top += now_weight * get_weight(global_news[index]['words'][word], words_freq[word])
              col_bot1 += now_weight * now_weight
          for word, value in global_news[index]['words'].items():
              now_weight = get_weight(value, words_freq[word])
              col_bot2 += now_weight * now_weight
          col_bot1 = math.sqrt(col_bot1)
          col_bot2 = math.sqrt(col_bot2)
          if col_bot1 * col_bot2 == 0:
              break
          correlation = col_top / (col_bot1 * col_bot2)
          res_list.append({
              'correlation': correlation,
              'title': global_news[index]['title'],
              'url': global_news[index]['url']
          })
      res_list = sorted(res_list, key=lambda x: x['correlation'], reverse=True)
  
      existed_logs = glob.glob('./log/*.txt')
      logs_num = len(existed_logs)
      flog = open(os.path.join('./log', str(logs_num + 1) + '.txt'), 'w', encoding='utf-8')
      flog.write(str(res_list))
      flog.close()
  
      res_list = res_list[0:min(len(res_list), 5)]
      return res_list
  ```

  

### 网页GUI模块

#### 技术框架

项目采用最新的前后端框架和设计模式进行开发。

- **Vue3 + Vite2 + Typescript + Naive UI**

  **Vue是一套用于构建用户界面的渐进式框架**。与其它大型框架不同的是，Vue 被设计为可以自底向上逐层应用。Vue 的核心库只关注视图层，不仅易于上手，还便于与第三方库或既有项目整合。另一方面，当与现代化的工具链以及各种支持类库结合使用时，Vue 也完全能够为复杂的单页应用提供驱动。

  **Vite是下一代前端开发与构建工具。**Vite意在提供开箱即用的配置，同时它的插件API和 JS/TS API 带来了高度的可扩展性，并有完整的类型支持。Vite基于原生ES模块，提供了丰富的内建功能，并支持快速的模块热更新。

  **TypeScript是微软开发的一个开源的编程语言，通过在 JavaScript 的基础上添加静态类型定义构建而成。**TypeScript通过TypeScript编译器或Babel转译为JavaScript代码，可运行在任何浏览器，任何操作系统。TypeScript添加了很多尚未正式发布的ECMAScript新特性。目前的最新版本为V4.7.2.

  **Naive UI 是一个 Vue3 的组件库。**Naive UI有超过 80 个组件，主题可调，全量使用 TypeScript 编写，使用 MIT license 许可证书。

  <img src="C:\Users\12944\AppData\Roaming\Typora\typora-user-images\image-20220614002519537.png" alt="image-20220614002519537" style="zoom: 33%;" />

  <center style = 'font-weight:bolder'>Fig 5 VUE3.0</center>

- **Flask**

  **Flask是一个使用 Python 编写的轻量级 Web 应用框架。**其 WSGI 工具箱采用 Werkzeug ，模板引擎则使用 Jinja2 。Flask使用 BSD 授权。

- **Axios**

  **前后端交互使用Axios进行通信。Axios是一个基于promise 的网络请求库**，作用于node.js和浏览器中。其在服务端使用原生node.js http模块, 而在客户端 (浏览端) 则使用 XMLHttpRequest。

#### 模块设计与核心代码

模块文件见WebGUI文件夹下的web_client中。遵守Vue@cli脚手架项目设计规范，具体可查阅 Vue@cli use Vue-ts 项目标准资料。

<img src="C:\Users\12944\AppData\Roaming\Typora\typora-user-images\image-20220614002125736.png" alt="image-20220614002125736" style="zoom: 67%;" />

<center style = 'font-weight:bolder'>Fig 6 web-client文件结构</center>

### 模块算法优化

本项目从三个方面对传统算法模式进行了优化。除去爬虫模块需考虑对应网站的访问压力进行间隔爬取之外，在算法效率的提升方面实现了即时响应。

- “SQL式查询”。在数据查询过程中，对于可局部化的索引，优先抽离局部数据，后进行综合索引。

- 使用混合索引进一步丰富查询结果，提高查询效率。

  在建立倒排索引的基础上，使用混合索引的方式加速相关数据访问和计算（如相关程度等）。

- 高频数据持久化。对于访问频度较高的数据，在尽可能合并压缩其空间开销的基础上，采用本地存储等方式实现数据持久化。

### 项目运行方式

#### 模块测试

各模块可进行单独测试，运行单个Python文件，设置观察数据即可。

#### 总项目运行方式

1. 运行spider.py文件进行数据采集

2. 运行inverted.py文件，进行检索系统的建立

3. windows下执行cd命令进入WebGUI文件夹。

4. 进入web_client文件夹，执行命令

   ```
   npm install
   ```

   为前端项目安装node_modules依赖

5. 运行server.py文件，部署用于信息检索的本地服务器，默认端口号：http://127.0.0.1:5000

6. 进入web_client文件夹，执行命令

   ```
   npm run dev
   ```

   部署前端测试服务器，为页面提供支持。默认端口号：http://127.0.0.1:3000

7. 使用浏览器打开前端测试服务器的端口号地址，等待前端页面加载，进行信息检索。

8. 若想投入生产部署，在web_client下运行

   ```
   npm run build
   ```

   生成静态页面。连接可提供对应url接口支持的后端服务器即可。

## 运行结果

### 查询1

**输入信息进行检索：**唐山打人事件

<img src="C:\Users\12944\AppData\Roaming\Typora\typora-user-images\image-20220614004035501.png" alt="image-20220614004035501" style="zoom: 25%;" />

<center style = 'font-weight:bolder'>Fig 7 前端未检索窗口1</center>

**结果：**（输出相关度最高的前5条信息）

<img src="C:\Users\12944\AppData\Roaming\Typora\typora-user-images\image-20220614004124836.png" alt="image-20220614004124836" style="zoom:25%;" />

<center style = 'font-weight:bolder'>Fig 8 前端检索窗口1</center>

### 查询2

**输入信息进行检索：**乌克兰

**结果：**

<img src="C:\Users\12944\AppData\Roaming\Typora\typora-user-images\image-20220614004237181.png" alt="image-20220614004237181" style="zoom:25%;" />

<center style = 'font-weight:bolder'>Fig 9 前端检索窗口2</center>

### 准确率计算

系统整体检索准确率可以进行多次随机检索取平均值，此处以检索“唐山打人事件”为例。选取文本的理由如下：

- 符合搜索引擎的一般使用情景。这一信息不显得匮乏，而又避免了信息过于丰富的可能性。
- 由于新闻的时效性，这一事件有所特指，可以进一步判断检索系统的准确程度。
- 在文档规模较小的情况下，选取符合数据采集规律的检索项，增加数据的有效性。

准确率计算公式：
$$
Precision = \frac{t_p}{t_p+f_p}
$$
其中，$t_p$ 为检索结果中的正例，$f_p$ 为检索结果中的伪例，$f_n$ 为未检出的正例，$f_n$ 为未检出的伪例。

本实验中的检出结果如下：

|        | 相关 | 不相关 |
| :----: | :--: | :----: |
|  检出  |  23  |   12   |
| 未检出 |  0   |   83   |

计算得到准确率 $Precision \approx 65.7$



