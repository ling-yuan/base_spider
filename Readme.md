# 基于scrapy的多阶段式通用爬虫框架

## 前提环境

[python 官网](https://www.python.org/)

[make (windows)](https://gnuwin32.sourceforge.net/packages/make.htm)

## 安装

```bash
make
```

```bash
make install
```

在main.py中修改配置信息即可运行

> [!note]
>
> 配置文件信息模板参考: `universal_spider\template\config_template.py`
> 
> 栗子: `test_config.md`
>

# 待办

- [X] 添加测试配置
- [X] 添加 Makefile
- [X] 添加git提交预检查
- [ ] 中间件添加
  - [X] 请求头
  - [X] 代理
  - [ ] 请求重试
  - [ ] 其他
- [ ] 添加管道
  - [X] mysql
  - [X] mongodb
  - [ ] 其他
- [ ] 添加浏览器的抓取方式
- [ ] 其他
  - [ ] 添加接口方式提交配置进行抓取
  - [ ] 封装成容器
  - [ ] 根据通用配置生成requests爬虫
