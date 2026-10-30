CONFIG = dict(
    num=3164, title='优质数对的总数 II', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='枚举因子 · 哈希表统计',
    tags=['灵神题单', '数论', '难度分 1777'],
    setup='from math import isqrt',
    code='''
class Solution:
    def numberOfPairs(self, nums1: List[int], nums2: List[int], k: int) -> int:
        cnt = defaultdict(int)
        for x in nums1:
            if x % k:
                continue
            x //= k
            for d in range(1, isqrt(x) + 1):  # 枚举因子
                if x % d:
                    continue
                cnt[d] += 1  # 统计因子
                if d * d < x:
                    cnt[x // d] += 1  # 因子总是成对出现
        return sum(cnt[x] for x in nums2)
''',
    call='Solution().numberOfPairs([3,6,12,5,12], [1,2,4], 3)',
    expect=9,
    views=[
        dict(type='array', var='nums1', label='nums1（红 = 不是 k 的倍数，直接淘汰）', h=130, cell=70,
             color=lambda S, i, v: 'red' if v % S['k'] else None),
        dict(type='array', var='nums2', label='nums2', h=140, cell=70),
        dict(type='map', var='cnt', label='cnt[d]：有多少个 nums1[i]/k 含因子 d', h=170),
        dict(type='text', h=80, fn=lambda S: (f"`x = nums1[i] / k = {S['x']}`，因子对：`d = {S['d']}` 和 `{S['x'] // S['d']}`" if 'd' in S and 'x' in S and S['d'] and S['x'] % S['d'] == 0 else '')),
    ],
    watch=['k', 'x', 'd'],
    captions={
        'cnt = defaultdict': '`cnt[d]` 要统计：nums1 里有多少个 ==x / k== 以 d 为因子',
        'for x in nums1': '看 `nums1` 的 `{x}`',
        'if x % k': lambda S, B, r: (f'`{S.x} % {S.k} != 0`：不是 k 的倍数，凑不出 b*k → ==跳过==' if S.x % S.k else f'`{S.x} % {S.k} == 0`：是 k 的倍数，继续'),
        'continue': '不满足，看下一个',
        'x //= k': '`x` 变成 `x / k` = =={x}==：问题变成"b[j] 是不是 x 的因子"',
        'for d in range': '枚举到 `sqrt(x)`：`d = {d}`',
        'if x % d': lambda S, B, r: (f'`{S.x} % {S.d} != 0`：d 不是因子' if S.x % S.d else f'`{S.x} % {S.d} == 0`：==因子 {S.d}==  是 x 的因子'),
        'cnt[d] += 1': '因子 `{d}` 计数 +1 → `cnt[{d}] = {cnt[d]}`',
        'if d * d < x': lambda S, B, r: (f'`{S.d}×{S.d} < {S.x}`：x 还有另一个因子 `{S.x // S.d}`' if S.d * S.d < S.x else f'`{S.d}×{S.d} = {S.x}`：两个因子相同，不重复统计'),
        'cnt[x // d] += 1': '因子成对出现：`cnt[{x // d}] += 1` → {cnt[x // d]}',
        'return sum': lambda S, B, r: f'每个 `nums2[j]` 直接查 `cnt`，相加得 =={r}==',
    },
    cards=dict(
        one_liner='把 nums1 除以 k，数每个因子被多少个数含有',
        complexity='时间 `O(n√(U/k) + m)`，空间 `O(U/k)`',
        problem=['`nums1[i]` 能被 `nums2[j] × k` 整除，则 `(i, j)` 是优质数对',
                 '求优质数对的个数，长度可达 10^5，数值可达 10^6',
                 '示例：`[1,2,4,12]`，`[2,4]`，`k=3` → `2`'],
        quote='a[i] 能被 b[j]·k 整除，等价于 a[i] 是 k 的倍数且 a[i]/k 能被 b[j] 整除。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先过滤：不是 k 的倍数的 `a[i]` 不可能配对，其余除以 k',
              '`x = a[i]/k` 的所有因子 d 记入哈希表 `cnt`，因子成对出现（d 与 x/d）',
              '遍历 `nums2`，`cnt[b[j]]` 就是以 b[j] 为伙伴的个数'],
        summary=['枚举到 `isqrt(x)`，`d*d < x` 时加上配对因子，避免平方数重复',
                 '第二种写法：枚举 b[j] 的倍数 + 调和级数，时间 `O((U/k) log m)`',
                 '`cnt` 用 `defaultdict`，最后 `cnt[x]` 取不到时自动为 0',
                 '演示小输入：`nums1=[3,6,12,5,12]`，`nums2=[1,2,4]`，`k=3`'],
    ),
)
