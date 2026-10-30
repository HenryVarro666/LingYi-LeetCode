def _text(S):
    if 'index' not in S:
        return '先求 `F(0)` 和总和 `s`'
    A = S['A']
    if S.get('_line', 0) >= 10:
        return f"`f[{S['index']}] − f[{S['index'] - 1}] = sum(A) − {len(A)} × A[{len(A) - S['index']}] = {S['s']} − {len(A) * A[len(A) - S['index']]}`"
    return f"累加：`now += {S['index']} × {A[S['index']]}`，`s += {A[S['index']]}`"


def _color(S, k, v):
    if 'index' in S and S.get('_line', 0) >= 10 and k == len(S['A']) - S['index']:
        return 'pink'
    if 'index' in S and S.get('_line', 0) < 10 and k == S['index']:
        return 'blue'
    return None


CONFIG = dict(
    num=396, title='旋转函数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='找规律 · 递推差值',
    tags=[],
    code='''
class Solution(object):
    def maxRotateFunction(self, A):

        now = 0
        s = 0
        for index, num in enumerate(A):
            now += index * num
            s += num

        res = now
        for index in range(1, len(A)):
            now += s - len(A) * A[len(A) - index]
            res = max(now, res)

        return res
''',
    call='Solution().maxRotateFunction([4, 3, 2, 6])',
    expect=26,
    views=[
        dict(type='text', fn=_text, h=80),
        dict(type='array', var='A', label='A（蓝 = 累加 F(0) 时的当前项，粉 = 第 index 次旋转后系数变为 0 的那一项）', cell=110,
             color=_color, h=230),
        dict(type='text', fn=lambda S: (f"now = F({S['index'] if S.get('_line', 0) >= 10 else 0}) = =={S['now']}==，res = =={S['res']}==" if 'res' in S else (f"`now` = =={S['now']}==" if 'now' in S else '')), h=70),
    ],
    watch=[('index', 'index', 'pink'), ('now', 'now', 'blue'), ('s', 's', 'cyan'), ('res', 'res', 'green')],
    skip=['now = 0', 's = 0'],
    captions={
        'for index, num': lambda S, B, r: (f"第一个循环：`F(0)` 和总和 `s` 一起累加，取 `A[{S['index']}] = {S['num']}`" if B.get('index') != S['index'] or 'index' not in B
                                           else '第一个循环结束'),
        'now += index': '`now += {index} × {num}` → =={now}==',
        's += num': '`s += {num}` → {s}',
        'res = now': '`F(0) = {now}`，先当作最大值 `res`',
        'for index in range': lambda S, B, r: (f"`index = {S['index']}`：算 `F({S['index']})`，相比 `F({S['index'] - 1})` 变化的是 A 的总和减掉最后那一项" if S['index'] != B.get('index')
                                               else '所有 F 都算过了'),
        'now += s': '`F({index}) = F({index - 1}) + sum(A) − len(A) × A[len(A) − {index}]` = {B.now} + {s} − {len(A)}×{A[len(A) - index]} = =={now}==',
        'res = max': '`res = max({now}, {B.res})` = =={res}==',
        'return res': '最大值 `{ret}`',
    },
    cards=dict(
        one_liner='f[index] − f[index−1] = sum(A) − len(A)·A[len(A)−index]',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`arr_k` 是 `A` 顺时针旋转 `k` 位后的数组',
                 '`F(k) = 0·arr_k[0] + 1·arr_k[1] + … + (n−1)·arr_k[n−1]`',
                 '求 `F(0)…F(n−1)` 的最大值，示例：`[4,3,2,6]` → `26`'],
        quote='f[index] - f[index - 1] = sum(A) - len(A) * A[len(A) - index]，到了这里，我们就可以在O(n)的时间内逐个递推出所有的f，其中的最大值即为答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['把 `f[1]` 按 `A` 的顺序重排：`1·A0 + 2·A1 + 3·A2 + 0·A3`，和 `f[0]` 逐项相减',
              '前面每项系数差 1，最后一项差 `0−3`，拆成 `(4−3)·A3 − 4·A3`',
              '合起来就是 `sum(A) − 4·A3`：每次递推只用 `O(1)`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：第 index 次旋转，被甩到最前面的是 `A[len(A) − index]`',
                 '`res` 要从 `F(0)` 开始，再逐个比较',
                 '原文本身是 Python 2/3 通用写法，代码一字未改',
                 '对比灵神：灵神倒着遍历 `i`，同一个递推式；yiduobo 用逐项相减的推导'],
    ),
)
