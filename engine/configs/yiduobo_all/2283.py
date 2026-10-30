def _txt(S):
    if 'index' in S and S['_line'] >= 9:
        i = S['index']
        d = S['num'][i]
        return f"下标 `{i}`：数字 `{i}` 应出现 `{d}` 次，实际出现 `{S['cnt_dict'].get(i, 0)}` 次"
    return '先统计每种数字出现几次，再逐位核对：数位 `i` 出现的次数是否等于 `num[i]`'


CONFIG = dict(
    num=2283, title='判断一个数的数字计数是否等于数位的值', difficulty='Easy', category='字符串',
    author='yiduobo', technique='哈希表计数 · 两趟遍历',
    tags=[],
    code='''
class Solution(object):
    def digitCount(self, num):

        cnt_dict = {}
        for char in num:
            cnt_dict[int(char)] = cnt_dict.get(int(char), 0) + 1
        
        for index, char in enumerate(num):
            if cnt_dict.get(index, 0) != int(char):
                return False
        
        return True
''',
    call='Solution().digitCount("1210")',
    expect=True,
    views=[
        dict(type='string', var='num', label='num（蓝 = 当前字符）', cell=96, h=210,
             pointers={'index': 'pink'},
             color=lambda S, i, v: 'blue' if 'index' in S and S['_line'] >= 9 and i == S['index'] else None),
        dict(type='map', var='cnt_dict', label='cnt_dict（数字 → 出现次数）', fmt=lambda k, v: f'{k}: {v}', h=190, font=34),
        dict(type='text', h=110, size=28, fn=_txt),
    ],
    watch=[('index', 'index', 'pink'), ('char', 'char', 'blue')],
    captions={
        'cnt_dict = {}': '`cnt_dict` 记录每种数字出现的次数',
        'for char in num:': lambda S, B, r: f'第一趟：取字符 `{S.char!r}`',
        'cnt_dict[int(char)] =': '数字 `{int(char)}` 出现次数 +1 → `cnt_dict = {cnt_dict}`',
        'for index, char in enumerate': lambda S, B, r: f'第二趟：核对下标 `{S.index}`，`num[{S.index}] = {S.char!r}`，即数字 `{S.index}` 应该出现 `{int(S.char)}` 次',
        'if cnt_dict.get(index, 0) !=': lambda S, B, r: (
            f'数字 `{S.index}` 实际出现 `{S.cnt_dict.get(S.index, 0)}` 次，应为 `{int(S.char)}` 次 → ==不相等，违反条件==' if S.cnt_dict.get(S.index, 0) != int(S.char)
            else f'数字 `{S.index}` 实际出现 `{S.cnt_dict.get(S.index, 0)}` 次 == `{int(S.char)}` → 符合（没出现用 `get(…, 0)` 当 0 次）'),
        'return False': '有一位对不上，直接返回 `False`',
        'return True': '每一位都符合，返回 `True`',
    },
    cards=dict(
        one_liner='先数一遍每种数字，再逐位核对下标对应的次数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['字符串 `num` 长度为 `n`，若对每个下标 `i`，数字 `i` 在 `num` 中恰好出现 `num[i]` 次，返回 `true`',
                 '示例：`"1210"` → `true`；`"030"` → `false`'],
        quote='由于题目给出的数的长度很短，因此可以直接一趟遍历，统计每种数字出现的次数，然后再一趟遍历，判断每一位下标对应的数字出现的次数是否恰好等于这位下标对应的数。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟：用哈希表 `cnt_dict` 统计每种数字出现次数',
              '第二趟：下标 `index` 对应的数字出现次数要等于 `int(char)`',
              '没出现过的数字次数是 0，用 `get(index, 0)`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`num` 里是字符，要 `int(char)` 转成数字再比较',
                 '下标超出出现过的数字范围时，要用 `get(index, 0)` 取 0',
                 '原文为 Python 2 风格，无需改动即可在 Python 3 运行'],
    ),
)
