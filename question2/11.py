import re
from datetime import datetime

def reg_search(text, regex_list):
    results = []
    for regex_dict in regex_list:
        result_dict = {}
        for key, pattern in regex_dict.items():
            if key == '标的证券':
                pattern = r'股票代码：(\d{6}\.SH)'
                match = re.search(pattern, text)
                if match:
                    result_dict[key] = match.group(1)
            elif key == '换股期限':
                pattern = r'(\d{4} 年 \d{1,2} 月 \d{1,2} 日)'
                matches = re.findall(pattern, text)
                if matches:
                    # 转换日期格式为 YYYY-MM-DD
                    formatted_dates = [datetime.strptime(m.replace(' ', ''), '%Y年%m月%d日').strftime('%Y-%m-%d') for m in matches]
                    result_dict[key] = formatted_dates
        if result_dict:
            results.append(result_dict)
    return results

# 示例使用
text = '''
标的证券：本期发行的证券为可交换为发行人所持中国长江电力股份
有限公司股票（股票代码：600900.SH，股票简称：长江电力）的可交换公司债券。
换股期限：本期可交换公司债券换股期限自可交换公司债券发行结束
之日满 12 个月后的第一个交易日起至可交换债券到期日止，即 2023 年 6 月 2
日至 2027 年 6 月 1 日止。
'''

regex_list = [{
    '标的证券': '*自定义*',
    '换股期限': '*自定义*'
}]

results = reg_search(text, regex_list)
print(results)
