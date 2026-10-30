_COLS = ['blue', 'pink', 'green', 'purple', 'cyan', 'orange']


def _root(fa, x):
    while fa[x] != x:
        x = fa[x]
    return x


def _comp(S, i, v):
    fa = S.get('fa')
    if not isinstance(fa, list):
        return None
    r = _root(fa, i)
    if sum(1 for j in range(len(fa)) if _root(fa, j) == r) < 2:
        return None
    return _COLS[r % len(_COLS)]


def _color_nums(S, i, v):
    ln = S.get('_line', 0)
    if ln >= 19 and 'x' in S and v == S['x']:
        return 'yellow'
    if ln >= 25 and 'y' in S and v == S['y']:
        return 'orange'
    return _comp(S, i, v)


def _txt(S):
    if 'g' not in S:
        return ''
    g, t = S['g'], S.get('threshold')
    if 'x' in S and 'y' in S and S.get('_line', 0) >= 25:
        x, y = S['x'], S['y']
        return f"枚举 `g = {g}`：`x = {x}`，`y = {y}`，`x·y/g = {x * y // g}` ≤ `{t}` → ==连起来=="
    if 'x' in S and S.get('_line', 0) >= 21:
        return f"`g = {g}`：最小的倍数 `x = {S['x']}`，`y` 只需枚举到 `g·t/x = {g * t // S['x']}`"
    return f"枚举公因数 `g = {g}`（`t = {t}`）"


CONFIG = dict(
    num=3378, title='统计最小公倍数图中的连通块数目', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='枚举 GCD + 最小倍数 + 并查集',
    tags=['常用数据结构', '难度分 2532'],
    code='''
class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        n = len(nums)
        fa = list(range(n))
        # 非递归并查集
        def find(x: int) -> int:
            rt = x
            while fa[rt] != rt:
                rt = fa[rt]
            while fa[x] != rt:
                fa[x], x = rt, fa[x]
            return rt

        # 记录每个数的下标
        idx = {x: i for i, x in enumerate(nums)}

        for g in range(1, threshold + 1):
            fi = -1
            for x in range(g, threshold + 1, g):
                if x in idx:
                    fi = find(idx[x])
                    break
            if fi < 0:
                continue
            for y in range(x + g, g * threshold // x + 1, g):
                if y in idx:
                    fj = find(idx[y])
                    if fj != fi:
                        fa[fj] = fi  # 合并 idx[x] 和 idx[y]
                        n -= 1  # 连通块个数减一
        return n
''',
    call='Solution().countComponents([2,4,3,6,9], 6)',
    expect=2,
    views=[
        dict(type='text', fn=_txt, size=28),
        dict(type='array', var='nums', label='nums（黄 = x，橙 = y，同色 = 已连通）', h=170, cell=80, color=_color_nums),
        dict(type='array', var='fa', label='fa（并查集，下标与 nums 对应）', h=170, cell=80,
             color=lambda S, i, v: _comp(S, i, v)),
        dict(type='map', var='idx', label='idx：值 → 下标（用哈希表查“某个数在不在 nums 里”）', h=130, font=24,
             fmt=lambda k, v: f'{k} → {v}'),
    ],
    watch=[('g', 'g', 'yellow'), ('x', 'x', 'blue'), ('y', 'y', 'orange'), ('fi', 'fi', 'cyan'), ('连通块 n', 'n', 'green')],
    captions={
        'n = len(nums)': '先假设每个数各自一块：`n = {n}`',
        'fa = list': '并查集初始化：`fa = {fa}`',
        'idx = {x': '记录每个数的下标：`idx = {idx}`',
        'for g in range': '枚举公因数 `g = {g}`：只考虑 `g` 的倍数，`fi = -1` 表示最小倍数还没找到',
        'fi = -1': '`fi` 记录最小倍数所在块的根，`-1` 表示还没找到',
        'for x in range': '依次看 `g` 的倍数 `x = {x}`，找 nums 里==最小==的那个',
        'if x in idx': lambda S, B, r: (f'`{S.x}` 在 nums 里 → 它就是最小的 `g` 的倍数' if S.x in S.idx else f'`{S.x}` 不在 nums 里，看下一个倍数'),
        'fi = find': '选最小的 `x`：`x·y ≤ g·t` 时 `y` 能取得最多，所以先找到它所在块的根',
        'if fi < 0': lambda S, B, r: ('`g` 的倍数里一个也不在 nums → 这轮不用处理' if S.fi < 0 else f'找到了 `x = {S.x}`，根为 `{S.fi}`'),
        'for y in range': lambda S, B, r: (f'`y` 取 `x` 之后的倍数，上界 `g·t/x = {S.g * S.threshold // S.x}`：再大 `x·y/g` 就超过 `{S.threshold}`' if S.y <= S.g * S.threshold // S.x else f'`y` 的范围 `{S.x + S.g}..{S.g * S.threshold // S.x}` 是空的：没有能和 `x` 连的'),
        'if y in idx': lambda S, B, r: (f'`y = {S.y}` 在 nums 里，`x·y/g = {S.x * S.y // S.g}` ≤ `{S.threshold}`，可以和 `x` 连' if S.y in S.idx else f'`y = {S.y}` 不在 nums 里，跳过'),
        'fj = find': '找 `y` 所在块的根 `fj`',
        'if fj != fi': lambda S, B, r: (f'`y` 所在块的根 `{S.fj}` ≠ `x` 的根 `{S.fi}`：原来不在同一块，要合并' if S.fj != S.fi else f'两个根都是 `{S.fi}`：已经连通，不用合并'),
        'fa[fj] = fi': '合并：`fa[{fj}] = {fi}`，`fa = {fa}`',
        'n -= 1': '少了一个连通块：`n = {n}`',
        'return n': '枚举完所有 `g`，剩下 `{ret}` 个连通块',
    },
    skip=['rt = x', 'while fa[rt]', 'rt = fa[rt]', 'while fa[x]', 'fa[x], x', 'return rt', 'break', 'fi = -1', 'fj = find', 'continue'],
    max_steps=110,
    cards=dict(
        one_liner='枚举 GCD，只拿最小的倍数当中介去连别的数',
        complexity='时间 `O(n + α·t·log t)`，空间 `O(n)`',
        problem=['给无重复数组 `nums` 和阈值 `threshold`（记作 `t`）',
                 '`lcm(nums[i], nums[j]) ≤ t` 的两个数之间连一条边',
                 '返回图中连通块的个数',
                 '示例：`[2,4,3,6,9], t=6` → `2`（`9` 单独一块）'],
        quote='枚举 g=1,2,3,…,t，以及 g 的倍数 x 和 y，对于满足 x·y ≤ g·t 的 x 和 y，把它们的下标用并查集连起来。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`lcm(x,y) ≤ t` 等价于 `x·y/gcd ≤ t`；枚举 `g` 当公因数',
              '`g` 的倍数很多，两两枚举会超时 → ==只取 nums 里最小的倍数 x==',
              '`x` 最小，满足 `x·y ≤ g·t` 的 `y` 就最多；其它 `y` 都被这个 `x` 带进同一块',
              '每合并一次，连通块数减一'],
        summary=['时间 `O(n + α·t·log t)`（调和级数），空间 `O(n)`',
                 '易错点：`y` 的范围是 `x+g` 到 `g·t/x`，用整除 `//`',
                 '`g` 不一定是 `gcd(x,y)`（如 `g=2,x=4,y=8`），但 `x·y/g ≤ t` 成立时真 lcm 更小，不影响正确性',
                 '大于 `t` 的数永远连不上别人，天然不会出现在 `g` 的倍数里',
                 '题解另有“数组”写法：用长 `t+1` 的数组 `idx` 代替哈希表，其余相同'],
    ),
)
