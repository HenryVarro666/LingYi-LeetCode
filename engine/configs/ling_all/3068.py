K = 3


def _f(v):
    return '−∞' if v == float('-inf') else str(int(v))


def _idx(S):
    x = S.get('x')
    if x is None or x not in S['nums']:
        return None
    return S['nums'].index(x)


def _state(S):
    return [S.get('f0', 0), S.get('f1', float('-inf'))]


def _txt(S):
    if 'f0' not in S:
        return '`f0` = 偶数个数异或 `k` 的最大和；`f1` = 奇数个'
    x = S.get('x')
    base = f"`f0 = {_f(S['f0'])}`（偶数个异或）   `f1 = {_f(S['f1'])}`（奇数个异或）"
    if x is None:
        return base
    return f"`x = {x}`，`x ^ k = {x ^ K}`   " + base


CONFIG = dict(
    num=3068, title='最大节点价值之和', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='状态机 DP · 偶数个元素异或 k',
    tags=['灵神题单', '动态规划', '难度分 2268'],
    code='''
class Solution:
    def maximumValueSum(self, nums: List[int], k: int, _: List[List[int]]) -> int:
        f0, f1 = 0, -inf
        for x in nums:
            f0, f1 = max(f0 + x, f1 + (x ^ k)), max(f1 + x, f0 + (x ^ k))
        return f0
''',
    call='Solution().maximumValueSum([1, 2, 5, 4], 3, [[0, 1], [0, 2], [0, 3]])',
    expect=16,
    views=[
        dict(type='array', var='nums', label='nums（蓝框 = 正在处理的 x；edges 用不上）', h=210, cell=110,
             color=lambda S, i, v: 'blue' if i == _idx(S) else None),
        dict(type='array', var=_state, label='[ f0（偶数个异或 k），f1（奇数个异或 k） ]', h=200, cell=150, index=False,
             fmt=lambda S, i, v: _f(v), color=lambda S, i, v: ('green', 'orange')[i]),
        dict(type='text', fn=_txt, size=28, h=90),
    ],
    watch=[('f0', 'f0', 'green'), ('f1', 'f1', 'orange'), 'x'],
    captions={
        'f0, f1 = 0, -inf': '`f0 = 0`：什么都没选，偶数个（0 个）；`f1 = -inf`：没有数，不可能选出奇数个',
        'for x in nums': lambda S, B, r: ('所有数都处理完了' if B.get('x') == S.x else
                                          f'`x = {S.x}`：选它异或 `k` 得 `{S.x ^ K}`，不选还是 `{S.x}`'),
        'f0, f1 = max': lambda S, B, r: (
            f"新 `f0 = max({_f(B.f0)} + {S.x}, {_f(B.f1)} + {S.x ^ K}) = {_f(S.f0)}`（不选 or 选它：奇数变偶数）；"
            f"新 `f1 = max({_f(B.f1)} + {S.x}, {_f(B.f0)} + {S.x ^ K}) = {_f(S.f1)}`"),
        'return f0': '必须选出==偶数个==元素异或 `k`，答案 `f0` = =={ret}==',
    },
    cards=dict(
        one_liner='边是多余的：任意两个数都能同时异或 k，所以只看“偶数个”',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['树上每次选一条边，把两端点的值都异或 `k`，操作任意次',
                 '求操作后所有节点价值之和的最大值',
                 '示例：`nums=[1,2,5,4]`, `k=3` → `16`'],
        quote='所以题目中的操作可以作用在任意两个数上。我们不需要建树，edges 是多余的！',
        quote_src='—— 灵茶山艾府题解',
        idea=['性质一：路径上的中间点被异或两次相当于没动 → 能==任选两个数==异或',
              '性质二：被异或的元素个数永远是==偶数==',
              '状态机 DP：`f0`/`f1` 记录已选偶数/奇数个，选或不选 `x` 就是两种转移'],
        summary=['时间 `O(n)`，空间 `O(1)`，`edges` 参数不用',
                 '`f1` 初始为 `-inf`：0 个数不可能选出奇数个，保证 `max` 不会取到它',
                 '两个变量要用元组同时赋值，否则 `f1` 会用到更新后的 `f0`',
                 '答案是 `f0`（偶数个），不是 `max(f0, f1)`'],
    ),
)
