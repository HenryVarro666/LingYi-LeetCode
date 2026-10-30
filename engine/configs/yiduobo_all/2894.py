CONFIG = dict(
    num=2894, title='分类求和并作差', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='一趟遍历 · 倍数减、其余加', tags=[],
    code='''
class Solution(object):
    def differenceOfSums(self, n, m):

        res = 0
        for v in range(1, n + 1):
            if v % m == 0:
                res -= v
            else:
                res += v
        
        return res
''',
    call='Solution().differenceOfSums(10, 3)',
    expect=19,
    views=[
        dict(type='array', var='range(1, n + 1)', h=200, pointers={'v - 1': 'blue'},
             color=lambda S, i, v: ('pink' if v % S['m'] == 0 else 'green') if 'res' in S and v <= S.get('v', 0) else None),
        dict(type='text', size=34, fn=lambda S: f"`res` = =={S['res']}==（绿色加、粉色减）" if 'res' in S else ''),
    ],
    watch=['n', 'm', ('v', 'v', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 直接存 `num1 - num2`，初始为 0',
        'if v % m == 0': '`{v} % {m} = {v % m}` → {"是 m 的倍数，要减" if v % m == 0 else "不是倍数，要加"}',
        'res -= v': '倍数属于 num2：`res -= {v}` → =={res}==',
        'res += v': '非倍数属于 num1：`res += {v}` → =={res}==',
        'return res': '遍历完，答案 =={res}==',
    },
    cards=dict(
        one_liner='遍历 1~n：是 m 的倍数就减，否则就加',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`[1, n]` 中不能被 `m` 整除的数之和为 `num1`，能整除的为 `num2`',
                 '返回 `num1 - num2`',
                 '示例：`n=10, m=3` → `19`'],
        quote='按照题目要求一趟遍历，就其中m的倍数从答案中减去，同时将其他数累加到答案中即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['不用分别算 num1、num2，一个变量 `res` 就够',
              '碰到 `m` 的倍数就 `res -= v`，其余 `res += v`',
              '`n ≤ 1000`，`O(n)` 遍历完全够快'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '用 `v % m == 0` 判断倍数，别把加减写反',
                 '`range(1, n + 1)` 要包含 n',
                 '对比公式解法 `O(1)`：数据小时直接模拟更不易错'],
    ),
)
