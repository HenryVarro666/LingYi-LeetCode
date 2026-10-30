def _mat(S):
    if 'x' not in S:
        return [[0]]
    x = S['x']
    y = S.get('y') or ((S['k'] - 1) // x + 1)
    return [[0] * x for _ in range(y)]


def _col(S, i, j, v):
    if 'x' not in S:
        return None
    return 'green' if i * S['x'] + j < S['k'] else 'dim'


def _text(S):
    k = S['k']
    if 'x' not in S:
        return f'`k = {k}`：找两个尽量接近的数 `x, y`，使 `x × y ≥ {k}`，答案 `x + y - 2`'
    x = S['x']
    if 'y' in S:
        return f'`x = {x}`，`y = {S["y"]}`：`{x} × {S["y"]} = {x * S["y"]} ≥ {k}`，操作数 `{x} + {S["y"]} - 2`'
    return f'`x = {x}`，`x × x = {x * x}`' + (f' < {k}，还不够' if x * x < k else f' ≥ {k}')


CONFIG = dict(
    num=3091, title='执行操作使数据元素之和大于等于 K', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='x × y ≥ k · 取尽量接近的两数',
    tags=['灵神题单', '难度分 1522'],
    code='''
class Solution(object):
    def minOperations(self, k):

        x = int(k ** 0.5)
        if x * x < k:
            x += 1
        
        y = (k - 1) // x + 1
        return x + y - 2
''',
    call='Solution().minOperations(17)',
    expect=7,
    views=[
        dict(type='text', fn=_text, h=90, lines=2),
        dict(type='grid', var=_mat, values=False, color=_col, label='x 列 × y 行：绿格 = 前 k 个数，共 x × y 个', h=380),
    ],
    watch=[('k', 'k', 'blue'), ('x', 'x', 'pink'), ('y', 'y', 'orange')],
    captions={
        'x = int': '`x = int(√{k})` = =={x}==：先对 k 开根号取整',
        'if x * x < k': lambda S, B, r: (f'`{S.x}×{S.x} = {S.x * S.x}` < `{S.k}`：不够' if S.x * S.x < S.k else f'`{S.x}×{S.x} = {S.x * S.x}` ≥ `{S.k}`：够了，x 不用再加'),
        'x += 1': '开根号向上取整：`x` → =={x}==',
        'y = (k - 1)': '`y = ceil(k / x)`，用 `(k-1)//x + 1` 写：`({k}-1)//{x} + 1` = =={y}==',
        'return x + y': '一共 `x + y - 2 = {x} + {y} - 2` = ==`{ret}`==（加一 `x-1` 次，复制 `y-1` 次）',
    },
    cards=dict(
        one_liner='x×y ≥ k，让 x、y 尽量接近，答案 x+y−2',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`nums = [1]`，操作：某元素加一 / 复制某元素到末尾',
                 '求让数组之和 `≥ k` 的最少操作次数',
                 '本视频：`k = 17` → `7`'],
        quote='可以发现，当t固定时，让a尽可能接近t / 2是最优的选择。',
        quote_src='—— yiduobo 题解原文',
        idea=['加一都在复制之前：先复制再加一，等于浪费了一',
              '共 `t` 次操作，加一 `a` 次 → 数组里有 `t-a+1` 个 `a+1`，和 `(a+1)(t-a+1)`',
              '令 `x = a+1`，`y = t-a+1`：要 `xy ≥ k` 且 `x+y` 最小 → 越接近越好'],
        after=[dict(heading='为什么越接近越好', lines=['周长固定时正方形面积最大，同理 `x + y` 固定时 `x·y` 最大', '所以 `x = ceil(√k)`，再让 `y = ceil(k / x)`', '`k = 17`：`5 × 4 = 20 ≥ 17`，操作数 `5 + 4 - 2 = 7`']),],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '原文为 Python 2 写法，本题代码无需改动，Python 3 直接可运行',
                 '`k ** 0.5` 是浮点数，`int` 向下取整后再判断是否要进位',
                 '对比灵神：灵神枚举/只试 `rt` 和 `rt+1` 两个 m，这里直接开根号取整并向上凑'],
    ),
)
