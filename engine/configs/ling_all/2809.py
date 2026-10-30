def _formula(S, B):
    ln = S.get('_line', 0)
    inner = S.get('_inner', {})
    if 'j' in inner and 'a' in inner and 'f' in S and ln in (6, 7, 8, 9):
        a, b, j, f = inner['a'], inner['b'], inner['j'], B.get('f', S['f'])
        if j >= 1:
            return f'选它做第 `{j}` 次操作：`f[{j-1}] + {a} + {b}×{j}` = =={f[j-1] + a + b * j}==，不选：`f[{j}] = {f[j]}`'
    if 't' in inner and 's1' in S:
        t, v = inner['t'], inner['v']
        tot = S['s1'] + S['s2'] * t - v
        return f'第 `{t}` 秒最小和：`{S["s1"]} + {S["s2"]}×{t} − {v}` = =={tot}==（x = {S["x"]}）'
    return '`f[j]` = 在前 i 个（按 nums2 排序）里操作 j 次，最多减少多少'


def _fcolor(S, i, v):
    j = S.get('_inner', {}).get('j')
    t = S.get('_inner', {}).get('t')
    if S.get('_line', 0) <= 9 and j is not None and i == j:
        return 'yellow'
    if t is not None and S.get('_line', 0) >= 11 and i == t:
        return 'yellow'
    return None


CONFIG = dict(
    num=2809, title='使数组和小于等于 x 的最少时间', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='排序 + 0-1 背包',
    tags=['其他线性 DP', '难度分 2979'],
    code='''
class Solution:
    def minimumTime(self, nums1: List[int], nums2: List[int], x: int) -> int:
        pairs = sorted(zip(nums1, nums2), key=lambda p: p[1])
        n = len(pairs)
        f = [0] * (n + 1)
        for i, (a, b) in enumerate(pairs):
            for j in range(i + 1, 0, -1):
                f[j] = max(f[j], f[j - 1] + a + b * j)

        s1 = sum(nums1)
        s2 = sum(nums2)
        for t, v in enumerate(f):
            if s1 + s2 * t - v <= x:
                return t
        return -1
''',
    call='Solution().minimumTime([1,2,3], [1,2,3], 4)',
    expect=3,
    skip=['for j in range'],
    views=[
        dict(type='text', fn=lambda S: ('排序后 `(nums1, nums2)`：' + '  '.join(f'==({a},{b})==' for a, b in S['pairs'])) if 'pairs' in S else '先把 `nums1`、`nums2` 绑在一起，按 `nums2` 从小到大排序', size=26, h=60),
        dict(type='array', var='nums1', label='nums1', h=130, cell=90),
        dict(type='array', var='nums2', label='nums2', h=130, cell=90),
        dict(type='array', var='f', label='f[j]：操作 j 次，最多减少多少', h=190, cell=90,
             pointers={'j': 'blue', 't': 'pink'}, color=_fcolor),
        dict(type='text', fn=_formula, size=26, h=70),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'orange'), ('a', 'a'), ('b', 'b'), ('s1', 's1'), ('s2', 's2'), ('t', 't', 'pink')],
    captions={
        'pairs = sorted': '把 `(nums1[i], nums2[i])` 绑在一起，按 `nums2` ==从小到大==排序：`{pairs}`。操作顺序就是这个顺序（排序不等式）',
        'n = len(pairs)': '最多操作 `n = {n}` 次：同一个下标操作多次，只有最后一次有用',
        'f = [0] * (n + 1)': '`f[j]` 初始为 0：还没有数可选，选 `j` 个的减少量先记 0',
        'for i, (a, b)': lambda S, B, r: (f'考虑第 `{S.i}` 个数 `(a, b) = ({S.a}, {S.b})`：选 or 不选' if 'i' not in B or S.i != B.i
                                            else '所有数都考虑完了'),
        'f[j] = max': '`f[{j}] = max(f[{j}], f[{j-1}] + {a} + {b}×{j})` = =={f[j]}==：把它放在第 {j} 次操作，减少量 `a + b×j`；==j 倒序==防止重复选',
        's1 = sum': '`s1 = sum(nums1) = {s1}`：什么都不做时第 0 秒的和',
        's2 = sum': '`s2 = sum(nums2) = {s2}`：每过一秒，和增加 `s2`',
        'for t, v': lambda S, B, r: (f'枚举答案 `t = {S.t}`，最多能减少 `v = f[{S.t}] = {S.v}`' if 't' in S else '枚举结束，没有满足条件的 t'),
        'if s1 + s2': '第 `{t}` 秒最小和 = `{s1} + {s2}×{t} − {v}` = =={s1 + s2*t - v}==，{"<= x，满足" if s1 + s2*t - v <= x else "> x，还不够"}（x = {x}）',
        'return t': '`t = {t}` 是第一个满足的，也就是最少时间 =={ret}==',
        'return -1': '所有 t 都不行，返回 `-1`',
    },
    max_steps=70,
    cards=dict(
        one_liner='操作系数恰好是 1,2,...,t，排序后做 0-1 背包',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['每秒 `nums1[i]` 增加 `nums2[i]`，之后可选一个下标清零',
                 '求让 `nums1` 之和 `<= x` 的最少秒数，不可能则 `-1`',
                 '示例：`[1,2,3]`、`[1,2,3]`、`x = 4` → `3`'],
        quote='下标为 i 的数如果不操作，它在第 t 秒的值等于 nums1[i] + nums2[i] * t。如果在第 k 秒把它变成 0，……让数组元素和减少了 ==nums1[i] + nums2[i] * k==。',
        quote_src='—— 灵茶山艾府题解（提示 3）',
        idea=['同一下标至多操作一次，所以答案 `t <= n`，枚举 `t`',
              '第 `k` 秒清零 `i`，减少量 `nums1[i] + nums2[i]×k`，系数刚好是操作时间',
              '按 `nums2` 排序后（排序不等式），选出的第 `j` 个数系数就是 `j` → 0-1 背包'],
        summary=['`f[j] = max(f[j], f[j-1] + a + b*j)`，一维数组要 ==j 倒序==',
                 '答案是第一个满足 `s1 + s2*t - f[t] <= x` 的 `t`，没有就 `-1`',
                 '易错：必须先按 `nums2` 排序，否则系数 `j` 的含义不成立',
                 '时间 `O(n^2)`，空间 `O(n)`'],
    ),
)
