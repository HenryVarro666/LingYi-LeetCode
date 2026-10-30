class _Named:
    def __init__(self, fn, label):
        self.fn, self.label = fn, label

    def __call__(self, S):
        return self.fn(S)

    def __str__(self):
        return self.label

    __repr__ = __str__


def _iv(S):
    return [(u - x, v - x) for x, (u, v) in zip(S['original'], S['bounds'])]


def _out(S):
    mn, mx = S.get('mn'), S.get('mx')
    if mn is None or mx is None or abs(mn) == float('inf') or abs(mx) == float('inf'):
        return []
    return [(int(mn), int(mx))]


def _cur(S):
    if 'x' not in S or 'u' not in S:
        return None
    for i, (x, b) in enumerate(zip(S['original'], S['bounds'])):
        if x == S['x'] and b[0] == S['u'] and b[1] == S['v']:
            return i
    return None


def _ended(S):
    i = _cur(S)
    if i is None or 'mn' not in S:
        return False
    iv = _iv(S)[:i]
    return (S['mn'], S['mx']) != (max([a for a, b in iv], default=-float('inf')), min([b for a, b in iv], default=float('inf')))


def _text(S):
    mn, mx = S.get('mn'), S.get('mx')
    if mn is None:
        return '每个 `bounds[i]` 平移 `-original[i]`，得到 `copy[0]` 的取值区间；它们的==交集==就是答案'
    if abs(mn) == float('inf') or abs(mx) == float('inf'):
        return '交集初始为 `(-inf, inf)`：什么限制都还没有'
    return f'当前交集 `[{int(mn)}, {int(mx)}]`：左端点取最大，右端点取最小，共 `{max(int(mx) - int(mn) + 1, 0)}` 个整数'


CONFIG = dict(
    num=3468, title='可行数组的数目', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='区间求交 · 平移 copy[0]',
    tags=['灵神题单', '难度分 1545'],
    code='''
class Solution:
    def countArrays(self, original: List[int], bounds: List[List[int]]) -> int:
        mn, mx = -inf, inf
        for x, (u, v) in zip(original, bounds):
            mn = max(mn, u - x)  # 计算区间交集
            mx = min(mx, v - x)
        return max(mx - mn + 1, 0)  # 注意交集可能是空的
''',
    call='Solution().countArrays([1,3,2,4], [[1,6],[3,8],[1,4],[2,5]])',
    expect=2,
    views=[
        dict(type='text', fn=_text, h=80, lines=2),
        dict(type='array', var='original', label='original', h=150),
        dict(type='intervals', var=_Named(_iv, '平移后的区间 [u-x, v-x]'), out=_Named(_out, '交集 [mn, mx]'), pointer=_cur, label='蓝：[u-x, v-x]（黄 = 当前）；绿：当前交集', h=360),
    ],
    watch=[('mn', 'mn', 'blue'), ('mx', 'mx', 'pink'), ('x', 'x', 'orange')],
    captions={
        'mn, mx = -inf': '交集从 `(-inf, +inf)` 开始，每来一个区间就收窄一次',
        'for x': lambda S, B, r: ('遍历结束，每个区间都收窄过了' if _ended(S) else f'第 {_cur(S)} 个：`x = {S.x}`，`[u, v] = [{S.u}, {S.v}]`，区间平移后是 `[{S.u - S.x}, {S.v - S.x}]`' if _cur(S) is not None else '遍历结束，交集算完了'),
        'mn = max': lambda S, B, r: f'`copy[0]` 至少是 `u - x = {S.u - S.x}`，左端点取最大：' + (f'`mn` 从 `{B.mn}` 变成 =={S.mn}==' if S.mn != B.mn else f'`mn` 仍是 =={S.mn}==（没有更大）'),
        'mx = min': lambda S, B, r: f'`copy[0]` 至多是 `v - x = {S.v - S.x}`，右端点取最小：' + (f'`mx` 从 `{B.mx}` 变成 =={S.mx}==' if S.mx != B.mx else f'`mx` 仍是 =={S.mx}==（没有更小）'),
        'return max': '交集 `[{mn}, {mx}]` 里有 `{mx} - {mn} + 1` = =={ret}== 个整数；若 `mx < mn` 则交集为空，取 0',
    },
    cards=dict(
        one_liner='确定了 copy[0]，整个数组就确定了：数交集里有几个整数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`copy` 的相邻差必须等于 `original` 的相邻差，且 `u_i ≤ copy[i] ≤ v_i`',
                 '求满足条件的 `copy` 数组个数',
                 '本视频：`original=[1,3,2,4]`，`bounds=[[1,6],[3,8],[1,4],[2,5]]` → `2`'],
        quote='确定了 copy[0]，那么整个数组也就确定了。所以 copy[0] 的取值范围（整数集合）的大小就是答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['逐项累加差分，得 `copy[i] = copy[0] + original[i] - original[0]`',
              '代入 `u ≤ copy[i] ≤ v`：`copy[0]` 落在 `[u - d, v - d]`',
              '优化：只减 `original[i]`，所有区间同时平移 `original[0]`，交集大小不变'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：交集可能为空，要 `max(mx - mn + 1, 0)`',
                 '主视频是「只减 `x`」的优化写法；首个写法先算 `d = x - original[0]`',
                 '写法二：用两个生成器分别求 `max` 和 `min`'],
    ),
)
