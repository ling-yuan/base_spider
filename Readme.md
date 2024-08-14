# 基于scrapy的多阶段式通用爬虫框架

## 前提环境

[python](https://www.python.org/)

[make (windows)](https://gnuwin32.sourceforge.net/packages/make.htm)

[Chrome](https://www.google.com/chrome/)

## 使用
> [!note]
>
> 环境配置: [环境配置](./doc/环境配置.md)
>
> 配置模板参考: [配置模板](./universal_spider/template/config_template.py)
> 
> 配置字段文档: [配置详解](./doc/配置详解.md)
>
> 测试配置: [测试配置](./doc/test_config.md)
>

# 待办

- [X] 添加测试配置
- [X] 添加 Makefile
- [X] 添加git提交预检查
- [ ] 自动继承上个请求的cookie（假设存在）
- [ ] 中间件添加
  - [X] 请求头
  - [X] 代理
  - [X] 请求间隔
  - [X] 重定向
  - [ ] 统计响应状态
  - [ ] 其他
- [ ] 添加管道
  - [X] mysql
  - [X] mongodb
  - [ ] local csv/json/xlsx
  - [ ] 其他
- [ ] 添加解析字段的额外处理逻辑
  - [ ] 解析前
  - [X] 解析后
- [X] 添加浏览器的抓取方式 （中间件形式）
- [ ] 其他
  - [ ] 添加接口方式提交配置进行抓取
  - [ ] 封装成容器
  - [ ] 根据通用配置生成requests爬虫
