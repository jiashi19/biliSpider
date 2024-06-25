import re

def remove_html_tags(text):
    # This regex pattern will match HTML tags
    tag_re = re.compile(r'<[^>]+>')
    # Substitutes the tags with an empty string
    return tag_re.sub('', text)

# 示例字符串
text1 = '<em class="keyword">apex</em>'
text2 = '【<em class=\"keyword\">Apex</em>/数据分析】第一赛段及线下赛表现回顾——北美赛'

# 去除标签后的字符串
cleaned_text1 = remove_html_tags(text1)
cleaned_text2 = remove_html_tags(text2)

print(cleaned_text1)
print(cleaned_text2)
