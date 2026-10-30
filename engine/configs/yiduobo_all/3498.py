def _formula(S):
    if 'char' not in S or 'index' not in S:
        return '`res` 累计「位置 × 反转值」，反转值 = `123 − ord(char)`'
    c, i = S['char'], S['index']
    return f"`'{c}'`：反转值 `123 − {ord(c)} = {123 - ord(c)}`，位置 `{i} + 1 = {i + 1}`，乘积 =={(i + 1) * (123 - ord(c))}=="


CONFIG = dict(
    num=3498, title='字符串的反转度', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟遍历 · ASCII 码推导',
    tags=[],
    code='''
class Solution(object):
    def reverseDegree(self, s):
        res = 0
        for index, char in enumerate(s):
            res += (index + 1) * (123 - ord(char))
        return res
''',
    call='Solution().reverseDegree("zaza")',
    expect=160,
    views=[
        dict(type='text', fn=_formula, size=28, h=70),
        dict(type='string', var='s', label='s（蓝 = 当前字符）', cell=110, h=200, pointers={'index': 'blue'},
             color=lambda S, k, v: 'blue' if k == S.get('index') else ('green' if k < S.get('index', 0) else None)),
    ],
    watch=[('index', 'index', 'blue'), ('char', 'char'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计反转度，初始为 0',
        'for index, char': lambda S, B, ret: (f"取第 `{S.index + 1}` 个字符 `'{S.char}'`（下标 `index = {S.index}`，题目位置从 1 开始）"
                                              if S.get('index') is not None and ('index' not in B or S.index != B.get('index') or S.char != B.get('char')) else '遍历完了'),
        'res += ': '`res` += `({index} + 1) × (123 − {ord(char)})` = `{index + 1} × {123 - ord(char)}`，现在 `res` = =={res}==',
        'return res': '所有字符的乘积加完，反转度 = =={ret}==',
    },
    cards=dict(
        one_liner='反转值 = 123 − ord(字符)，再乘 index + 1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符在==反转字母表==中的位置：`a = 26, ..., z = 1`',
                 '反转度 = 每个字符「反转位置 × 字符串下标（从 1 开始）」之和',
                 '示例：`"abc"` → `148`；本视频 `"zaza"` → `160`'],
        quote='ord(reverse) - ord(\'a\') = ord(\'z\') - ord(char)',
        quote_src='—— yiduobo 题解原文（移项后的结果）',
        idea=['`char` 到 `a` 的距离，等于它的反转字符到 `z` 的距离',
              '反转字符的位置 = `ord("z") − ord(char) + 1`，而 `ord("z") + 1 = 123`',
              '所以一趟遍历：`res += (index + 1) * (123 - ord(char))`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`123` 就是 `ord("z") + 1`，推导时别漏掉这个 +1',
                 '`enumerate` 的 `index` 从 0 开始，要用 `index + 1`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神写成 `ord("{") - ord(c)` 配合 `enumerate(s, 1)` 一行完成'],
    ),
)
