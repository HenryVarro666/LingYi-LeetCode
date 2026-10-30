_COLS = ['blue', 'pink', 'green', 'purple', 'cyan', 'orange']


def _root(fa, x):
    while fa[x] != x:
        x = fa[x]
    return x


def _color(S, i, v):
    fa = S.get('fa')
    t = S.get('threshold')
    if not isinstance(fa, dict) or v not in fa:
        return None
    r = _root(fa, v)
    if sum(1 for k in fa if _root(fa, k) == r) < 2:
        return None
    return _COLS[r % len(_COLS)]


def _div(S):
    d = S.get('divisor')
    if not isinstance(d, list):
        return None
    return {i: d[i] for i in range(len(d)) if d[i]}


def _txt(S):
    if 'divisor' not in S:
        return ''
    ln = S.get('_line', 0)
    if ln >= 22 and 'v' in S:
        d = S['divisor'][S['v']] if S['v'] < len(S['divisor']) else []
        if len(d) < 2:
            return f"公倍数 `v = {S['v']}`：约数列表 `divisor[{S['v']}] = {d}`，不到两个，没有可连的对"
        return f"公倍数 `v = {S['v']}`：约数列表 `divisor[{S['v']}] = {d}`，它们两两的 lcm ≤ `{S['v']}` ≤ `{S['threshold']}` → 全部连通"
    if 'v' in S:
        return f"把 `{S['v']}` 记为 `{S['v']}, {2*S['v']}, {3*S['v']}, …` 这些数的约数"
    return ''


CONFIG = dict(
    num=3378, title='统计最小公倍数图中的连通块数目', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='约数表 + 并查集（类筛法）',
    tags=['常用数据结构', '难度分 2532'],
    code='''
class Solution(object):
    def countComponents(self, nums, threshold):
        
        divisor = [[] for _ in range(threshold + 1)]
        fa = {}

        res = len(nums)
        nums.sort()
        for v in nums:
            if v > threshold:
                break
            fa[v] = v
            for x in range(v, threshold + 1, v):
                divisor[x].append(v)

        def find(fa, x):
            if fa[x] != x:
                fa[x] = find(fa, fa[x])
            return fa[x]

        for v in range(1, threshold + 1):
            if len(divisor[v]) < 2:
                continue
            x = divisor[v][0]
            fa_x = find(fa, x)
            for y in divisor[v][1:]:
                fa_y = find(fa, y)
                if fa_x != fa_y:
                    fa[fa_y] = fa_x
                    res -= 1

        return res
''',
    call='Solution().countComponents([6,2,3,9,4], 6)',
    expect=2,
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='array', var='nums', label='nums（排序后；> threshold 的数直接是单独一块）', h=150, cell=80,
             color=_color, dim=lambda S, i, v: 'threshold' in S and v > S['threshold']),
        dict(type='map', var=_div, label='divisor[v]：v 的约数里（在 nums 中的）有哪些', h=260, font=24,
             fmt=lambda k, v: f'{k}: {v}'),
        dict(type='map', var='fa', label='fa：数 → 父亲（同色 = 已连通）', h=130, font=24,
             fmt=lambda k, v: f'{k} → {v}'),
    ],
    watch=[('v', 'v', 'yellow'), ('x', 'x if _line >= 24 else None', 'blue'), ('y', 'y if _line >= 26 else None', 'orange'), ('res', 'res', 'green')],
    captions={
        'divisor = [[]': '`divisor[x]` 要装 nums 里 `x` 的所有约数，`x` 最大到 `threshold`',
        'res = len': '先假设每个数各自一块：`res = {res}`',
        'nums.sort': '排序：小的约数在前；大于 `threshold` 的会排在最后',
        'for v in nums': '取 nums 里的数 `v = {v}`',
        'if v > threshold': lambda S, B, r: (f'`{S.v}` > `{S.threshold}`：lcm 一定 ≥ 它自己，永远连不上别人 → 单独一块，后面的更大，直接 break' if S.v > S.threshold else f'`{S.v}` ≤ `{S.threshold}`，有可能连边'),
        'fa[v] = v': '`{v}` 先自成一棵树：`fa[{v}] = {v}`',
        'for x in range(v': '`v = {v}` 是 `{v}, {2*v}, {3*v}, …` 的约数，把它登记进这些位置',
        'divisor[x].append': '`{v}` 是 `{x}` 的约数：`divisor[{x}] = {divisor[x]}`',
        'for v in range(1': '枚举公倍数 `v = {v}`',
        'if len(divisor[v]) < 2': lambda S, B, r: (f'`divisor[{S.v}] = {S.divisor[S.v]}` 不到两个数，没有可连的对 → 跳过' if len(S.divisor[S.v]) < 2 else f'`divisor[{S.v}] = {S.divisor[S.v]}`：它们两两的 lcm 都 ≤ `{S.v}` ≤ `{S.threshold}`，要全部连起来'),
        'x = divisor[v][0]': '以最小的约数 `{x}` 为中心，去连其余的',
        'fa_x = find': '`{x}` 所在块的根',
        'for y in divisor[v][1:]': '依次取其余约数 `y = {y}`',
        'fa_y = find': '`y` 所在块的根',
        'if fa_x != fa_y': lambda S, B, r: (f'根 `{S.fa_y}` ≠ `{S.fa_x}`：原来不连通，要合并' if S.fa_x != S.fa_y else f'两个根都是 `{S.fa_x}`：早就连通了'),
        'fa[fa_y] = fa_x': '合并：`fa[{fa_y}] = {fa_x}`',
        'res -= 1': '少了一个连通块：`res = {res}`',
        'return res': '最终剩下 `{ret}` 个连通块',
        'if fa[x] != x': lambda S, B, r: (f'`{S.x}` 不是根（父亲 `{S.fa[S.x]}`），继续往上找' if S.fa[S.x] != S.x else f'`{S.x}` 的父亲是自己：它就是根'),
        'fa[x] = find': '路径压缩：`fa[{x}]` 直接指向根',
    },
    skip=['continue', 'return fa[x]', 'break'],
    max_steps=120,
    cards=dict(
        one_liner='把每个数登记到它的倍数上：同一个公倍数下的约数全部连通',
        complexity='时间 `O(n + t log t · α)`，空间 `O(t)`',
        problem=['`nums` 各不相同，`lcm(nums[i], nums[j]) ≤ threshold` 的两点连一条无向边',
                 '求图的连通块数量',
                 '本视频：`nums=[6,2,3,9,4], threshold=6` → `2`（`9` 单独一块）'],
        quote='若某个数nums[i]大于threshold，那么其与任意其他数的lcm也必然大于threshold，也就是说nums[i]在图中必然不会与其他节点相连。',
        quote_src='—— yiduobo 题解原文',
        idea=['两两枚举太慢，只能从数值入手：大于 `threshold` 的数一定是孤点',
              '类似筛法：每个 `v` 从自己开始以 `v` 为步长，把自己加进 `divisor[x]`',
              '对每个公倍数 `v`：`divisor[v]` 里任意两数的 lcm 都 ≤ `v` ≤ `threshold`，全部相连',
              '用并查集合并，每合并一次连通块减一'],
        summary=['时间 `O(n + t log t · α)`，空间 `O(t)`',
                 '易错点：大于 `threshold` 的数不进并查集，但要计入初始连通块数 `len(nums)`',
                 '`divisor[v]` 里的数是 `v` 的约数，所以两两 lcm ≤ `v`，不用真的算 lcm',
                 '作者的递归 `find` 带路径压缩；原文为 Python 2 风格，本题语法无需改动即可在 Python 3 运行'],
    ),
)
