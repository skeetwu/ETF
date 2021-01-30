# !/usr/bin/env python
# vi: set ft=python sts=4 ts=4 sw=4 et:
# -*- coding: utf-8 -*-

import urllib.request

from flask import render_template, Blueprint
from lxml import etree

from etf_app import da_file, base_url

index = Blueprint('pages', __name__ + 'pages', url_prefix='')


@index.route('/etf')
def etf():
    return render_template('etf.html', etf_all_list=get_etf_detail())




def get_etf_detail():
    etf_all_list = []
    with open(da_file, 'r') as f:
        for line in f.readlines():
            if line.strip():

                etf = {}
                # time.sleep(1)
                _url = '%s/%s.html' % (base_url, line.strip())
                print(line.strip())
                etf['etf_code'] = line.strip()
                response = urllib.request.urlopen(_url).read()
                selector = etree.HTML(response)
                div_num = 11
                sub_div_num = 3
                # 基金名称
                etf_name = selector.xpath('//*[@id="body"]/div[%s]/div/div/div[1]/div[1]/div/text()' % div_num)
                if not etf_name:
                    div_num = 12
                    etf_name = selector.xpath('//*[@id="body"]/div[%s]/div/div/div[1]/div[1]/div/text()' % div_num)
                etf['etf_name'] = etf_name[0]
                # 基金规模
                etf_guimo = selector.xpath(
                    '//*[@id="body"]/div[%s]/div/div/div[%s]/div[1]/div[2]/table/tr[1]/td[2]/text()' % (
                        div_num, sub_div_num))
                if not etf_guimo:
                    sub_div_num = 2
                    etf_guimo = selector.xpath(
                        '//*[@id="body"]/div[%s]/div/div/div[%s]/div[1]/div[2]/table/tr[1]/td[2]/text()' % (
                            div_num, sub_div_num))
                etf['etf_guimo'] = etf_guimo[0][1:]

                # 基金成立日期
                etf_chengliriqi = selector.xpath(
                    '//*[@id="body"]/div[%s]/div/div/div[%s]/div[1]/div[2]/table/tr[2]/td[1]/text()' % (
                        div_num, sub_div_num))
                etf['etf_chengliriqi'] = etf_chengliriqi[0][1:]

                # 基金跟踪标的
                etf_genzongbiaodi = selector.xpath(
                    '//*[@id="body"]/div[%s]/div/div/div[%s]/div[1]/div[2]/table/tr[3]/td/text()[1]' % (
                        div_num, sub_div_num))
                etf['etf_genzongbiaodi'] = etf_genzongbiaodi[0][:-3]

                # 重仓前十股票及其URL
                for i in range(2, 12):
                    etf_top = selector.xpath('//*[@id="position_shares"]/div[1]/table/tr[%s]/td[1]/a/text()' % i)
                    if not etf_top:
                        etf_top = ['-']
                    etf['etf_top%s' % (i - 1)] = etf_top[0]
                    etf_top_url = selector.xpath('//*[@id="position_shares"]/div[1]/table/tr[%s]/td[1]/a/@href' % i)
                    if not etf_top_url:
                        etf_top_url = ['-']
                    etf['etf_top%s_url' % (i - 1)] = etf_top_url[0]

                # 前十总占比
                etf_qianshizongzhanbi = selector.xpath('//*[@id="position_shares"]/div[1]/p/span[2]/text()')
                if not etf_qianshizongzhanbi:
                    etf_qianshizongzhanbi = ['-']
                etf['etf_qianshizongzhanbi'] = etf_qianshizongzhanbi[0]

                # print(etf)
                etf_all_list.append(etf)

    return etf_all_list
