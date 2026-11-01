CONFIG = dict(
    num=2293, title='极大极小游戏', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='直接模拟，每轮折半（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def minMaxGame(self, a: List[int]) -> int:
        while len(a) > 1:
            b = [0] * (len(a) // 2)
            for i in range(len(b)):
                if i % 2 == 0:
                    b[i] = min(a[i * 2], a[i * 2 + 1])
                else:
                    b[i] = max(a[i * 2], a[i * 2 + 1])
            a = b
        return a[0]
''',
    call='Solution().minMaxGame([1,3,5,2,4,8,2,2])',
    expect=1,
    views=[
        dict(type='array', var='a', pointers={'i': 'blue'}, label='a（当前轮的数组）', h=200,
             color=lambda S, i, v: 'blue' if 'i' in S and i in (S['i'] * 2, S['i'] * 2 + 1) and S['_line'] in (6, 7, 8, 9) else None),
        dict(type='array', var='b', pointers={'i': 'pink'}, label='b（下一轮的数组）', h=200),
        dict(type='text', fn=lambda S: (f"第 `{S['i']}` 个位置是{'偶数' if S['i'] % 2 == 0 else '奇数'}下标 → 取 =={'min' if S['i'] % 2 == 0 else 'max'}==" if 'i' in S and 'b' in S and S['_line'] in (6, 7, 8, 9) else ''), h=70),
    ],
    watch=['i', ('len(a)', 'len(a)', 'cyan')],
    captions={
        'while len(a) > 1': '`len(a) = {len(a)}`：{"还没缩成一个数，再来一轮" if len(a) > 1 else "只剩一个数了，结束"}',
        'b = [0]': '新开数组 `b`，长度是 `a` 的一半：`{len(b)}`',
        'for i in range': '依次填 `b` 的每个位置 `i`（0 到 {len(b) - 1}）',
        'if i % 2': '`i = {i}`：{"偶数" if i % 2 == 0 else "奇数"}下标 → 取{"较小" if i % 2 == 0 else "较大"}值',
        'min(': '`b[{i}] = min(a[{i*2}], a[{i*2+1}])` = min({a[i*2]}, {a[i*2+1]}) = =={b[i]}==',
        'max(': '`b[{i}] = max(a[{i*2}], a[{i*2+1}])` = max({a[i*2]}, {a[i*2+1]}) = =={b[i]}==',
        'a = b': '这一轮填完，`a` 换成 `b`：长度折半成 `{len(a)}`',
        'return a[0]': '只剩一个数，答案就是 =={a[0]}==',
    },
    cards=dict(
        one_liner='每轮把相邻两数按奇偶下标取小/取大，数组折半',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组长度是 2 的幂。每轮：新数组第 `i` 位 = 原数组 `2i`、`2i+1` 两数',
                 '`i` 为偶数取 `min`，为奇数取 `max`，重复到只剩一个数',
                 '示例：`[1,3,5,2,4,8,2,2]` → `1`'],
        quote='按题意模拟：每轮新建数组 b，长度为 len(a)/2，偶数下标取 min，奇数下标取 max，然后 a = b。',
        quote_src='—— 灵茶山艾府题解（Go 代码）',
        idea=['每轮长度折半，总共 `n + n/2 + … ≈ 2n` 次操作',
              '`i % 2` 决定取 min 还是 max，别把它写成两数下标的奇偶'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 'Go 里自己写的 `min`/`max` 辅助函数，在 Python 中直接用内置 `min`/`max`',
                 '时间 `O(n)`，空间 `O(n)`（可原地写回 `a` 做到 `O(1)`）',
                 '易错：奇偶看的是新数组下标 `i`，不是 `a` 的下标'],
    ),
)
