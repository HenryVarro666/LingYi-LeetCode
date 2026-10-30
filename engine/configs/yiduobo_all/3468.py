class _Named:
    def __init__(self, fn, label):
        self.fn, self.label = fn, label

    def __call__(self, S):
        return self.fn(S)

    def __str__(self):
        return self.label

    __repr__ = __str__


def _iv(S):
    return [(u - o, v - o) for o, (u, v) in zip(S['original'], S['bounds'])]


def _out(S):
    x, y = S.get('x'), S.get('y')
    if x is None or y is None:
        return []
    return [(x, y)]


def _cur(S):
    if 'o' not in S or 'u' not in S:
        return None
    for i, (o, b) in enumerate(zip(S['original'], S['bounds'])):
        if o == S['o'] and b[0] == S['u'] and b[1] == S['v']:
            return i
    return None


def _ended(S):
    i = _cur(S)
    if i is None:
        return False
    iv = _iv(S)[:i]
    return (S.get('x'), S.get('y')) != (max([a for a, b in iv], default=None), min([b for a, b in iv], default=None))


def _text(S):
    x, y = S.get('x'), S.get('y')
    if x is None:
        return '`copy` 就是 `original` 整体加上同一个偏移 `offset`，数一数有几个 `offset` 可行'
    if y is None:
        return f'下界 `x = {x}`（`u - o` 的最大值）'
    return f'`{x} ≤ offset ≤ {y}`' + (f'：有 `{y - x + 1}` 个整数' if x <= y else '：下界超过上界，无解')


CONFIG = dict(
    num=3468, title='可行数组的数目', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='统一偏移量 offset',
    tags=['灵神题单', '难度分 1545'],
    code='''
class Solution(object):
    def countArrays(self, original, bounds):
        
        x, y = None, None
        for o, (u, v) in zip(original, bounds):
            new_x, new_y = u - o, v - o
            if x is None or x < new_x:
                x = new_x
            if y is None or y > new_y:
                y = new_y
        
        if x <= y:
            return y - x + 1
        else:
            return 0
''',
    call='Solution().countArrays([2,4,3,5], [[1,6],[4,9],[1,5],[4,6]])',
    expect=2,
    views=[
        dict(type='text', fn=_text, h=80, lines=2),
        dict(type='array', var='original', label='original', h=150),
        dict(type='intervals', var=_Named(_iv, 'offset 的范围 [u-o, v-o]'), out=_Named(_out, '当前 [x, y]'), pointer=_cur, label='蓝：offset 的范围 [u-o, v-o]（黄 = 当前）；绿：当前 [x, y]', h=360),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('o', 'o', 'orange')],
    captions={
        'x, y = None': '`x` 记下界、`y` 记上界，先都设为 `None`（还没有任何限制）',
        'for o': lambda S, B, r: ('所有项都处理完了' if _ended(S) else f'第 {_cur(S)} 项：`o = {S.o}`，`[u, v] = [{S.u}, {S.v}]`' if _cur(S) is not None else '所有项都处理完了'),
        'new_x, new_y': '`u[i] ≤ o + offset ≤ v[i]` → `offset` 在 `[{u} - {o}, {v} - {o}]` = `[{new_x}, {new_y}]`',
        'x is None or x < new_x': lambda S, B, r: (f'`x` 还是 None → 直接取 `{S.new_x}`' if B.x is None else
                                                    (f'`{B.x} < {S.new_x}`：新下界更大 → 要更新' if B.x < S.new_x else f'`{B.x} ≥ {S.new_x}`：下界不变')),
        'y is None or y > new_y': lambda S, B, r: (f'`y` 还是 None → 直接取 `{S.new_y}`' if B.y is None else
                                                    (f'`{B.y} > {S.new_y}`：新上界更小 → 要更新' if B.y > S.new_y else f'`{B.y} ≤ {S.new_y}`：上界不变')),
        'x = new_x': '`x` → =={x}==',
        'y = new_y': '`y` → =={y}==',
        'if x <= y': lambda S, B, r: f'`x = {S.x}`，`y = {S.y}`：' + ('下界不超过上界，offset 有解' if S.x <= S.y else '下界大于上界，无解'),
        'return y - x': '`offset` 取 `x` 到 `y` 共 `{y} - {x} + 1` = =={ret}== 种',
        'return 0': '没有可行的 offset → 答案 0',
    },
    cards=dict(
        one_liner='copy = original + 同一个偏移量，数有几个偏移量可行',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`copy` 相邻项之差与 `original` 相同，且每项落在 `[u, v]` 内',
                 '求满足条件的 `copy` 个数',
                 '本视频：`original=[2,4,3,5]`，`bounds=[[1,6],[4,9],[1,5],[4,6]]` → `2`'],
        quote='copy就相当于对original中的每一项都加上了同一个偏移量offset，而本题就转化成了计算有多少种可行的offset可以使得copy满足条件2。',
        quote_src='—— yiduobo 题解原文',
        idea=['把条件 1 移项：`copy[i] - original[i]` 对所有 `i` 都相等',
              '每一项给出 `u - o ≤ offset ≤ v - o`，一共 `n` 个不等式',
              '取 `x = max(u - o)`，`y = min(v - o)`，答案 `y - x + 1`（`x ≤ y` 时）'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文为 Python 2 写法，本题代码无需改动，Python 3 直接可运行',
                 '用 `None` 表示还没有限制，所以要写 `x is None or ...`',
                 '最后一定要判断 `x <= y`，否则答案会是负数',
                 '对比灵神：灵神用 `-inf/inf` 做初值，并先减 `d`；这里直接用偏移量 `offset` 的说法'],
    ),
)
