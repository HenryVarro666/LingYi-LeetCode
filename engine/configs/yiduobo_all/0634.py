def _f(upto):
    f = [0, 0, 1]
    for k in range(3, upto + 1):
        f.append((k - 1) * (f[k - 1] + f[k - 2]))
    return f[1:upto + 1]


def _seq(S):
    idx = S.get('index')
    if idx is None:
        return [0, 1]
    # a, b 已更新后 b = f[idx]，否则 b = f[idx-1]
    return _f(idx) if S['b'] == _f(idx)[-1] and S['a'] == _f(idx)[-2] else _f(idx - 1)


def _text(S):
    idx = S.get('index')
    if idx is None or 'a' not in S:
        return '`f[1] = 0`，`f[2] = 1`；`n ≥ 3` 时 `f[n] = (n−1) × (f[n−1] + f[n−2])`'
    f = _f(idx)
    if S['b'] == f[-1] and S['a'] == f[-2]:
        return f'`f[{idx}] = ({idx}−1) × ({f[-2]} + {f[-3]})` = =={f[-1]}==（b 现在就是 f[{idx}]）'
    return f'下一项 `f[{idx}] = ({idx}−1) × (b + a)`，a、b 是 f[{idx - 2}]、f[{idx - 1}]'


CONFIG = dict(
    num=634, title='寻找数组的错位排列', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='错排递推 · 两个变量滚动',
    tags=[],
    code='''
class Solution(object):
    def findDerangement(self, n):

        if n == 1:
            return 0
        
        if n == 2:
            return 1
        
        a, b = 0, 1
        mod = 10 ** 9 + 7
        for index in range(3, n + 1):
            a, b = b, (index - 1) * (b + a) % mod
        
        return b
''',
    call='Solution().findDerangement(6)',
    expect=265,
    views=[
        dict(type='text', fn=_text, size=26, h=70),
        dict(type='array', var=_seq, label='f[1], f[2], … 依次排列（错排数）', index=False, cell=100, h=190),
    ],
    watch=['n', ('index', 'index', 'blue'), ('a', 'a', 'cyan'), ('b', 'b', 'green')],
    skip=['mod = '],
    captions={
        'if n == 1': '`n = {n} ≠ 1`：`n = 1` 时唯一的数只能放回原位，`f[1] = 0`；这里继续',
        'if n == 2': '`n = {n} ≠ 2`：`n = 2` 时 `[2,1]` 是唯一错排，`f[2] = 1`；这里继续',
        'return 0': '`f[1] = 0`',
        'return 1': '`f[2] = 1`',
        'a, b = 0, 1': '用两个变量滚动：`a = f[1] = 0`，`b = f[2] = 1`，不用整张数组',
        'for index in range': lambda S, B, r: (f'`index = {S.index}`：要算 `f[{S.index}]`' if B.get('index') != S.index or 'index' not in B
                                               else f'`index` 已经走完 `3..{S.n}` → 退出循环'),
        'a, b = b': '`a, b = b, (index−1) × (b + a)`：`a` 变成 {a}，`b` = f[{index}] = =={b}==（再取模）',
        'return b': '循环结束，`b` 就是 `f[{n}]` = =={ret}==',
    },
    cards=dict(
        one_liner='看 n 放在哪：放在 k 位置，再分「k 回 n」与否两种情况',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`1..n` 的排列里，==没有任何数在原位置==的叫错位排列',
                 '求这样的排列个数，结果对 `10^9 + 7` 取模',
                 '示例：`n = 3` → `2`（`[2,3,1]`、`[3,1,2]`）；本视频取 `n = 6`'],
        quote='n只能在1到n - 1中选一个位置来放置，不妨设放置在了位置k上。',
        quote_src='—— yiduobo 题解原文',
        idea=['n 有 `n−1` 种位置可选，设放在 k；k 要么放回位置 n（剩 `f[n−2]`），要么把 n 当作 k 的「正确位置」（`f[n−1]`）',
              '合起来 `f[n] = (n−1) × (f[n−1] + f[n−2])`',
              '只依赖前两项，用 `a, b` 滚动即可'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先单独处理 `n = 1`（0）和 `n = 2`（1），循环从 3 开始',
                 '每步都要取模；递推里有变量 `n−1`，不适合用矩阵快速幂加速',
                 '前几项：`0, 1, 2, 9, 44, 265`'],
    ),
)
