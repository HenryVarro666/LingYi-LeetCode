CONFIG = dict(
    num=2288, title='价格减免', difficulty='Medium', category='字符串',
    author='yiduobo', technique='逐词判断 + 格式化',
    tags=[],
    code='''
class Solution(object):
    def discountPrices(self, sentence, discount):

        def check(word):
            if len(word) < 2:
                return False
            if word[0] != '$':
                return False
            
            for char in word[1:]:
                if char < '0' or char > '9':
                    return False
            
            return True

        res = []
        for word in sentence.split(' '):
            if check(word):
                res.append('$%.2f' % (int(word[1:]) * 1.0 * (100 - discount) / 100.0))
            else:
                res.append(word)
        
        return ' '.join(res)
''',
    call="Solution().discountPrices('buy $4 x5 $10 8$ now', 50)",
    expect='buy $2.00 x5 $5.00 8$ now',
    views=[
        dict(type='array', var='res', label='res（已处理的单词）', cell=120, h=200,
             color=lambda S, i, v: ('green' if isinstance(v, str) and v.startswith('$') and '.' in v else None)),
        dict(type='string', var='word', label='当前单词 word', cell=70, h=150,
             color=lambda S, i, v: ('yellow' if S.get('char') == v and S['_line'] in (11, 12, 13) else None)),
        dict(type='text', h=90, size=30, fn=lambda S: (f"当前 `word = {S['word']!r}`" if 'word' in S else '')),
    ],
    watch=[('word', 'word', 'blue'), ('char', 'char', 'pink'), ('discount', 'discount', 'orange')],
    captions={
        'def check': '先定义判断函数 `check(word)`：三个条件都满足才是价格',
        'for word in sentence.split': lambda S, B, ret: (f'取下一个单词 `{S.word!r}`' if len(S.res) < len(S.sentence.split(' ')) else '单词都处理完了'),
        'if check(word)': '调用 `check({word!r})` 判断是不是价格',
        'if len(word) < 2': '长度 `{len(word)}`：{"小于 2，只可能是单独的 $" if len(word) < 2 else "至少 2 位，继续"}',
        "if word[0] != '$'": "首字符 `{word[0]!r}`：{'不是 $ → 不是价格' if word[0] != '$' else '是 $，继续'}",
        "if char < '0'": "`{char!r}` {'不是数字 → 不是价格' if (char < '0' or char > '9') else '是数字，继续'}",
        'return False': '不满足条件，`check` 返回 `False`',
        'return True': '三个条件都满足，`check` 返回 `True`',
        'res.append(\'$%': "打折：`{int(word[1:])} × (100 − {discount}) / 100`，格式化成两位小数 → `{res[-1]}`",
        'res.append(word)': '不是价格，原样放进 `res`',
        'return \' \'.join': '用空格拼起来：`{ret!r}`',
    },
    cards=dict(
        one_liner='三个条件判断价格，再按两位小数打折',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['单词是 `$` 加非负数字才算价格，需要打 `discount%` 折',
                 '结果恰好保留两位小数，其余单词不变',
                 '本视频：`"buy $4 x5 $10 8$ now"`，`discount = 50`'],
        quote='一个单词为价格单词需要满足三个条件：1、单词的长度必须大于等于2 2、单词的首字母为美元符号 3、单词中除首字母外的所有字符都必须为数字',
        quote_src='—— yiduobo 题解原文',
        idea=['空格切成单词，逐个交给 `check` 判断',
              '是价格就算 `数值 × (100 − discount) / 100`，用 `%.2f` 格式化',
              '不是价格原样放进答案数组，最后用空格拼起来'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '先判长度 ≥ 2，避免单独一个 `$` 被当成价格',
                 '`8$`、`$10$` 首字符或末尾不合条件，都不是价格',
                 '原文已是 Python 3 可运行的写法（`/` 作用于浮点，无需修改）'],
    ),
)
