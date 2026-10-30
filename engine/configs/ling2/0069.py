X = 20


def _color(S, i, v):
    if 'left' not in S:
        return None
    if i <= S['left']:
        return 'blue'
    if i >= S['right']:
        return 'red'
    return None


def _top(S):
    if 'left' not in S:
        return ''
    l, r = S['left'], S['right']
    if 'm' in S and S['_line'] in (9, 10):
        m = S['m']
        return f"`m = {m}`：`m² = {m * m}` {'≤' if m * m <= X else '>'} `x = {X}`"
    if l + 1 < r:
        return f'开区间 `({l}, {r})` 里的 `{r - l - 1}` 个数还==不知道颜色=='
    return f'`left + 1 == right`：`{l}² = {l * l} ≤ {X} < {r * r} = {r}²`'


def _while(S, B, ret):
    l, r = B.left, B.right
    if l + 1 < r:
        return f'开区间 `({l}, {r})` 不为空 → 继续二分'
    return f'`left + 1 == right = {r}`：开区间为空，==所有数都染好色了=='


def _if(S, B, ret):
    m = S.m
    if m * m <= S.x:
        return f'`{m}² = {m * m} ≤ {S.x}` 成立 → 答案 ==大于等于 m==，m 和它左边都染蓝'
    return f'`{m}² = {m * m} > {S.x}` → 答案 ==小于 m==，m 和它右边都染红'


CONFIG = dict(
    num=69, title='x 的平方根', difficulty='Easy', category='二分查找',
    author='灵茶山艾府', technique='开区间二分 · 红蓝染色',
    tags=['字节30天', '热题173', '面试经典150'],
    code='''
SQRT_MAX = 46340  # isqrt(2 ** 31 - 1)
class Solution:
    def mySqrt(self, x: int) -> int:
        # 开区间 (left, right)
        left, right = 0, min(x, SQRT_MAX) + 1
        while left + 1 < right:  # 开区间不为空
            # 循环不变量：left^2 <= x
            # 循环不变量：right^2 > x
            m = (left + right) // 2
            if m * m <= x:
                left = m
            else:
                right = m
        # 循环结束时 left+1 == right
        # 此时 left^2 <= x 且 right^2 > x
        # 所以 left 最大的满足 m^2 <= x 的数
        return left
''',
    call=f'Solution().mySqrt({X})',
    expect=4,
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='array', var=lambda S: list(range(X + 2)), label='候选答案 0..x+1（蓝 = m² ≤ x，红 = m² > x，灰 = 未知）',
             cell=44, color=_color, pointers={'left': 'blue', 'm': 'yellow', 'right': 'red'}, h=230),
        dict(type='array', var=lambda S: [i * i for i in range(X + 2)], label='对应的 m²（和 x = 20 比较）',
             cell=44, color=_color, index=False, h=150),
        dict(type='text', fn=lambda S: '循环不变量：==left² ≤ x==（蓝区最右），==right² > x==（红区最左）' if 'left' in S else '', size=26),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'red'), ('m', 'm', 'yellow'), ('m * m', 'm * m'), ('x', 'x')],
    captions={
        'left, right = 0': '开区间 `(0, {right})`：`0² ≤ x` 一定成立（蓝），`{right}² > x` 一定成立（红）',
        'while left + 1 < right': _while,
        'm = (left + right)': '取中点 `m = ({left} + {right}) // 2 = {m}`',
        'if m * m <= x': _if,
        'left = m': '`left = {left}`：循环不变量 ==left² ≤ x== 仍然成立',
        'right = m': '`right = {right}`：循环不变量 ==right² > x== 仍然成立',
        'return left': '`left = {left}` 就是==最大的==满足 `m² ≤ x` 的数 → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='m 越大越不满足 m² ≤ x，有单调性 → 二分答案',
        complexity='时间 `O(log min(x, U))`，空间 `O(1)`',
        problem=['给你非负整数 `x`，返回它的==算术平方根==，只保留整数部分',
                 '即：最大的非负整数 `m`，满足 `m² ≤ x`；不能用 `pow`、`x ** 0.5`',
                 '示例：`x = 8` → `2`（`2.828…` 舍去小数）；本视频 `x = 20` → `4`'],
        quote='由于 m 越小越满足 m²≤x，m 越大越不满足 m²≤x，有单调性，可以二分答案。本文用开区间二分。',
        quote_src='—— 灵茶山艾府题解',
        idea=['开区间 `(left, right)`：`left` 始终满足 `left² ≤ x`（蓝），`right` 始终满足 `right² > x`（红）',
              '`m² ≤ x` 就更新 `left = m`，否则更新 `right = m`',
              '「求最大」：`check(mid)` 为真时更新谁，最后就返回谁 → 返回 `left`'],
        summary=['时间 `O(log min(x, U))`，`U = 46340`；空间 `O(1)`',
                 '右边界 `min(x, 46340) + 1`：`46341² > 2³¹ − 1`，所以 m² 不会溢出 int',
                 '求最大返回 `left`，求最小返回 `right`：开区间写法不用想加一减一',
                 '其他二分写法（闭区间、左闭右开）也可以'],
    ),
)
