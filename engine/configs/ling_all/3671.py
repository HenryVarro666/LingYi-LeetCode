def _tree(S):
    t = S.get('t')
    if t is not None and hasattr(t, 'tree'):
        return t.tree
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'groups[d] = nums 中 d 的倍数（保持原顺序）；右边是 f[d]：GCD 是 d 的倍数的严格递增子序列数', 22, T['muted'], bold=True)
    g = S.get('groups')
    if g is None:
        return
    m = len(g) - 1
    f = S.get('f')
    cur = (S['g'] if 'b' in S else S.get('i')) if 'f' in S else S.get('d')
    inn = S.get('_inner', {})
    cur_x = None
    row_h = min(60, (y1 - y0 - 60) / max(1, m))
    for d in range(1, m + 1):
        y = y0 + 52 + (d - 1) * row_h
        hot = d == cur
        if hot:
            cv.rect((x0 + 14, y - 2, x1 - 14, y + row_h - 8), fill=T['panel2'], outline=T['yellow'], width=2, r=8)
        cv.text((x0 + 30, y + row_h / 2 - 4), f'd={d}', 24, T['yellow'] if hot else T['muted'], anchor='lm', bold=True)
        cx = x0 + 130
        for v in g[d]:
            on = hot and cur_x is not None and v == cur_x * d
            cv.rect((cx, y + 4, cx + 60, y + row_h - 12), fill=T['yellow'] if on else T['panel2'], outline=T['border'], r=6)
            cv.text((cx + 30, y + row_h / 2 - 4), v, 22, T['bg'] if on else T['text'], anchor='mm', bold=True)
            cx += 68
        if f is not None and d < len(f):
            done = f[d] != 0 or (cur is not None and d > cur)
            cv.text((x1 - 30, y + row_h / 2 - 4), f'f[{d}] = {f[d]}', 24, T['green'] if done else T['dim'], anchor='rm', bold=True)


def _formula(S):
    inn = S.get('_inner', {})
    if 'f' not in S:
        return '先给每个 d 找出 nums 里它的所有倍数，分到 `groups[d]` 里'
    i = S['g'] if 'b' in S else S['i']
    if 'g' in S and 'b' in S:
        return f'`d = {i}`：在 `groups[{i}] = {S["groups"][i]}` 里数严格递增子序列（元素先除以 {i}）'
    js = list(range(i * 2, len(S['f']), i))
    if js:
        return f'`d = {i}`：恰好 = 倍数个数 − ' + ' − '.join(f'f[{j}]' for j in js)
    return f'`d = {i}`：没有更大的倍数，恰好 = 倍数个数'


CONFIG = dict(
    num=3671, title='子序列美丽值求和', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='倍数容斥 + 值域树状数组数严格递增子序列',
    tags=['灵神题单·动态规划', '灵神题单·常用数据结构'],
    code='''
MOD = 1_000_000_007

# 预处理每个数的因子
MX = 70_001
divisors = [[] for _ in range(MX)]
for i in range(1, MX):
    for j in range(i, MX, i):  # 枚举 i 的倍数 j
        divisors[j].append(i)  # i 是 j 的因子

# 完整模板见 https://leetcode.cn/circle/discuss/mOr1u6/
class FenwickTree:
    def __init__(self, n: int):
        self.tree = [0] * (n + 1)  # 使用下标 1 到 n

    # a[i] 增加 val
    # 1 <= i <= n
    # 时间复杂度 O(log n)
    def update(self, i: int, val: int) -> None:
        t = self.tree
        while i < len(t):
            t[i] += val
            i += i & -i

    # 计算前缀和 a[1] + ... + a[i]
    # 1 <= i <= n
    # 时间复杂度 O(log n)
    def pre(self, i: int) -> int:
        t = self.tree
        res = 0
        while i > 0:
            res += t[i]
            i &= i - 1
        return res % MOD

class Solution:
    def totalBeauty(self, nums: List[int]) -> int:
        m = max(nums)

        # 计算 b 的严格递增子序列的个数
        def count_increasing_subsequence(b: List[int], g: int) -> int:
            t = FenwickTree(m // g)
            res = 0
            for x in b:
                x //= g
                # cnt 表示以 x 结尾的严格递增子序列的个数
                cnt = t.pre(x - 1) + 1  # +1 是因为 x 可以一个数组成一个子序列
                res += cnt
                t.update(x, cnt)  # 更新以 x 结尾的严格递增子序列的个数
            return res

        groups = [[] for _ in range(m + 1)]
        for x in nums:
            for d in divisors[x]:
                groups[d].append(x)

        f = [0] * (m + 1)
        ans = 0
        for i in range(m, 0, -1):
            f[i] = count_increasing_subsequence(groups[i], i)
            # 倍数容斥
            for j in range(i * 2, m + 1, i):
                f[i] -= f[j]
            ans += f[i] * i
        return ans % MOD
''',
    call='Solution().totalBeauty([1,2,3])',
    expect=10,
    skip=['m = max(nums)', 'self.tree = [0]', 't = self.tree', 'res = 0', 'f = [0] * (m + 1)', 'ans = 0', 'groups = [[]',
          'while i < len(t)', 'for x in nums:', 'for d in divisors[x]', 'for x in b:', 'for j in range', 't[i] += val', 'i += i & -i', 'while i > 0', 'res += t[i]', 'i &= i - 1', 'return res % MOD'],
    views=[
        dict(type='text', fn=_formula, size=24, h=56),
        dict(type='custom', draw=_draw, h=250),
        dict(type='array', var=_tree, label='当前树状数组 t.tree（下标 1..m//g，每个位置 = 以该值结尾的子序列数的前缀累加）', h=165, cell=80),
        dict(type='array', var='f', label='f[d]（容斥后变成「GCD 恰好是 d」）', h=165, cell=80, pointers={'g if "b" in locals() else i': 'blue'}, pointer_labels={'g if "b" in locals() else i': 'd'}),
    ],
    watch=[('g', 'g if "b" in locals() else (i if "f" in locals() else None)', 'blue'), ('cnt', 'cnt', 'cyan'), ('ans', 'ans', 'yellow')],
    captions={
        'groups[d].append(x)': '`{x}` 的因子有 `{divisors[x]}`，`{d}` 是其一 → `{x}` 放进 `groups[{d}]`',
        'f[i] = count_increasing_subsequence': '倒着枚举 `g = {i}`（大的先算好才能容斥）：数 `groups[{i}]` 里严格递增子序列个数 = GCD 是 `{i}` 的 ==倍数== 的子序列数',
        't = FenwickTree': '建树状数组，大小只要 `m // g = {m // g}`（元素先除以 g）',
        'x //= g': '除以 `g = {g}`：`x = {x}`（值域缩小，树状数组就小了）',
        'cnt = t.pre': '`t.pre({x} - 1)` = 比 `{x}` 小的数结尾的子序列数；`+1` 是 `{x}` 自己单独一个',
        'res += cnt': '以 `{x}` 结尾的严格递增子序列有 `cnt = {cnt}` 个 → `res = {res}`',
        't.update(x, cnt)': '把 `cnt = {cnt}` 记在位置 `{x}`，后面更大的数可以接在它后面',
        'return res': lambda S, B, r: f'`groups[{S.g}]` 共有 =={r}== 个严格递增子序列',
        'f[i] -= f[j]': '`{j}` 是 `{i}` 的倍数：GCD 是 `{j}` 的子序列被多算了 → `f[{i}] -= f[{j}] = {f[j]}` → =={f[i]}==',
        'ans += f[i] * i': '恰好 GCD 为 `{i}` 的有 `{f[i]}` 个，美丽值 `{i} × {f[i]} = {f[i] * i}` → `ans = {ans}`',
        'return ans': '所有 `g` 的美丽值之和 `{ans}`，取模后 =={ret}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='先数「GCD 是 g 的倍数」，再倍数容斥扣成「恰好 g」',
        complexity='时间 `O(D·n·log U + U·log U)`，空间 `O(D·n + U)`',
        problem=['数组 `nums`，对每个 `g`，求 GCD ==恰好等于 g== 的严格递增子序列个数，乘以 `g` 后全部相加','答案对 `10^9+7` 取模','示例：`[1,2,3]` → `10`（`1×5 + 2×1 + 3×1`）'],
        quote='我们可以先求出有多少个严格递增子序列的 GCD 是 g 的倍数，再利用倍数容斥，转化成「恰好」。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`groups[d]` = `nums` 里 `d` 的倍数；这些数的任意子序列，GCD 都是 `d` 的倍数','数严格递增子序列：`f[x]` = 以 `x` 结尾的个数 = `1 + 比 x 小的 f 之和` → ==值域树状数组==','`g` 从大到小：`f[g] -= f[2g] + f[3g] + …`，剩下就是恰好为 `g` 的个数'],
        summary=['时间 `O(D·n·log U + U·log U)`，`D ≤ 120` 是单个数的最大因子数','把每个元素除以 `g`，树状数组只要 `m // g` 大小，避免每次 `O(U)` 初始化','灵神还给了写法二：用时间戳懒初始化，只建一棵树，适合更一般的场景','树状数组 `pre` 里要取模；容斥的减法会出现负数，最后 `% MOD` 保证非负','视频里把树状数组内部循环折叠了，只看每次更新后的树状数组']
    ),
)
