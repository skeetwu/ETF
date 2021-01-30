# 爬取天天基金网上的ETF基金的详情

## Intro

给朋友帮忙，需要根据天天基金--场内交易基金净值折价率一览表把每个基金的前十名的股票持仓信息。


列表： http://fund.eastmoney.com/cnjy_jzzzl.html

## Start

```bash
# pip3 install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
# python etf_app.py
```
访问页面 http://127.0.0.1:5000/etf

这个地方没做异步返回，可能会返回很慢，后台会打印处理进度。

全部数据在etf_numbers.data，数据比较多，已经按照ETF板块进行了分类。

有一个小数据文件etf_numbers.small.data, 用于测试，可以修改etf_app.py里的da_file参数配置。

显示出来的网页带一点CSS样式，直接全选拷贝里Excel表格就完活了。

excel/etf.xlsx是一个demo。

excel/result_20210129.xlsx是朋友分析的结果，应该根据这个表就可以在每个版块中选择一支最合适的购买ETF基金了。

## 注意

xpath可以使用Chrome的debug模式，选中值或者dom对象，然后右键copy。

copy出来以后，如果路径里面有tbody一定要删掉，lxml目测是无法解析tbody。

