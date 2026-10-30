CONFIG = dict(
    num=2288, title='价格减免', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='分割单词 + 格式化',
    tags=[],
    code='''
class Solution:
    def discountPrices(self, sentence: str, discount: int) -> str:
        d = 1 - discount / 100
        a = sentence.split(' ')
        for i, w in enumerate(a):
            if w[0] == '$' and w[1:].isdigit():
                a[i] = f"${int(w[1:]) * d :.2f}"
        return ' '.join(a)
''',
    call="Solution().discountPrices('buy $4 x5 $10 8$ now', 50)",
    expect='buy $2.00 x5 $5.00 8$ now',
    views=[
        dict(type='array', var='a', label='a（按空格分出的单词）', cell=120, h=230,
             pointers={'i': 'blue'},
             color=lambda S, i, v: ('green' if isinstance(v, str) and v.startswith('$') and '.' in v else None)),
        dict(type='text', h=100, size=30,
             fn=lambda S: (f"`w = {S['w']!r}`：" + ('是价格' if S['w'][0] == '$' and S['w'][1:].isdigit() else '不是价格，保持不变')
                           if 'w' in S and 'i' in S else '')),
    ],
    watch=[('d', 'd', 'orange'), ('i', 'i', 'blue'), ('w', 'w', 'pink')],
    captions={
        'd = 1': '折后系数 `d = 1 - {discount}/100 = {d}`',
        'a = sentence.split': '按空格切成单词列表 `a`，共 {len(a)} 个',
        'for i, w in enumerate(a)': lambda S, B, ret: (f'看第 `{S.i}` 个单词 `{S.w!r}`' if 'i' not in B or S.i != B.i else '单词都处理完了'),
        'if w[0]': lambda S, B, ret: (f"`{S.w!r}` 以 `$` 开头，且后面 `{S.w[1:]!r}` 全是数字 → ==是价格==" if (S.w[0] == '$' and S.w[1:].isdigit())
                                      else f"`{S.w!r}` 不满足“`$` 开头 + 全数字” → 不是价格，跳过"),
        'a[i] =': '`{B.w}` → `{a[i]}`：`{int(w[1:])} × {d}` 保留两位小数',
        'return': '用空格拼回去：`{ret!r}`',
    },
    cards=dict(
        one_liner='切成单词，是价格就乘折扣，再拼回去',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['单词形如 `$` 加数字就是价格，把每个价格打 `discount%` 折',
                 '结果保留两位小数，其余单词不变',
                 '本视频：`"buy $4 x5 $10 8$ now"`，`discount = 50`'],
        quote='遍历 a 中的每个单词，如果单词是以 $ 开头，并且其余字母均为数字，则替换数字。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`split(\' \')` 切单词，原地改写列表 `a`',
              '判断价格：`w[0] == \'$\'` 且 `w[1:].isdigit()`',
              '格式串 `:.2f` 直接保留两位小数'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`8$`、`$`、`$10$` 都不是价格；`w[1:].isdigit()` 对 `$` 单独成词为 False（空串）',
                 '易错：`w[0]` 对非空单词安全；单词不会为空，因为分隔符是单个空格'],
    ),
)
