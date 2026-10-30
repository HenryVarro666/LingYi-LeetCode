CONFIG = dict(
    num=1819, title='序列中不同最大公约数的数目', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='枚举 gcd 的倍数 · 调和级数',
    tags=['灵神题单·数学算法', '难度分 2540'],
    code='''
class Solution:
    def countDifferentSubsequenceGCDs(self, nums: List[int]) -> int:
        ans = 0
        mx = max(nums)
        has = [False] * (mx + 1)
        for x in nums:
            if not has[x]:
                has[x] = True
                ans += 1  # 单独一个数也算

        for i in range(1, mx // 3 + 1):  # 优化循环上界
            if has[i]:
                continue
            g = 0  # 0 和任何数 x 的最大公约数都是 x
            for j in range(i * 2, mx + 1, i):  # 枚举 i 的倍数 j
                if has[j]:  # 如果 j 在 nums 中
                    g = gcd(g, j)  # 更新最大公约数
                    if g == i:  # 找到一个答案（g 无法继续减小）
                        ans += 1
                        break  # 提前退出循环
        return ans
''',
    call='Solution().countDifferentSubsequenceGCDs([6, 10, 3])',
    expect=5,
    views=[
        dict(type='text', h=70, size=30, fn=lambda S: (f"枚举 `i = {S['i']}`：它的倍数里，在 nums 中的数的 gcd 目前是 `g = {S['g']}`" if 'i' in S and 'g' in S and S['_line'] >= 14 else '')),
        dict(type='array', var='[int(b) for b in has]', label='has[v]：v 是否在 nums 中（1 = 在）', cell=72, h=260,
             pointers={'i': 'blue', 'j': 'pink'},
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('g', 'g', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 统计不同 gcd 的个数',
        'mx = max': '值域上界 `mx = {mx}`：从==值域==而不是子序列的角度来数',
        'has = [False]': '`has[v]` 记录 `v` 是否在 `nums` 中，比哈希表更快',
        'if not has[x]': lambda S, B, ret: (f'`{S.x}` 第一次出现' if not B.has[S.x] else f'`{S.x}` 已经算过，跳过'),
        'has[x] = True': '标记 `has[{x}]`',
        'ans += 1  # 单独': '长度为 1 的子序列，gcd 就是它自己 → ==不同的数各算一个==：`ans = {ans}`',
        'for i in range': '枚举可能的 gcd `i`；至少要有 `2i`、`3i` 两个数才能 gcd 为 `i`，所以只需到 `mx // 3 = {mx // 3}`',
        'if has[i]': lambda S, B, ret: (f'`{S.i}` 本身就在 nums 里，已经在单个数里算过 → 跳过，避免重复' if B.has[S.i] else f'`{S.i}` 不在 nums 里，看它能不能由几个倍数凑出来'),
        'g = 0': '`g` 是 `i` 的倍数们的 gcd，从 0 开始（`gcd(0, x) = x`）',
        'for j in range': '枚举 `i = {i}` 的倍数 `j`（从 `2i` 起）',
        'if has[j]': lambda S, B, ret: (f'`{S.j}` 在 nums 中 → 加入子序列' if B.has[S.j] else f'`{S.j}` 不在 nums 中 → 跳过'),
        'g = gcd(g, j)': '`g = gcd({B.g}, {j}) = {g}`：gcd 只会越来越小',
        'if g == i': lambda S, B, ret: (f'`g = {S.g} == i = {S.i}` → ==找到一个子序列的 gcd 恰好是 {S.i}==' if S.g == S.i else f'`g = {S.g} > i = {S.i}`，还不够小，继续找倍数'),
        'ans += 1': '`{i}` 是一个可行的 gcd：`ans = {ans}`',
        'break': '`g` 不会再变小，==提前退出==这一轮',
        'return ans': '不同 gcd 一共 `{ans}` 个',
    },
    cards=dict(
        one_liner='别数子序列，换到值域上：枚举 gcd，再看它的倍数',
        complexity='时间 `O(n + U log U)`，空间 `O(U)`',
        problem=['求 `nums` 所有非空子序列的 gcd 中，==不同值==有多少个',
                 '示例：`[6,10,3]` → `5`（6、10、3、2、1）',
                 '子序列有 `2^n - 1` 个，不能直接枚举'],
        quote='多个数的最大公约数等于 g，也反过来说明这些数都是 g 的倍数。……那么就枚举 i 及其倍数，当作子序列中的数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['换视角：枚举值域里的 `i`，看 nums 里 `i` 的倍数',
              '倍数的 gcd 能降到 `i`，说明存在子序列 gcd 恰好是 `i`',
              '枚举量是调和级数 `U/1 + U/2 + ...`，只有 `O(U log U)`'],
        summary=['时间 `O(n + U log U)`；`g` 每次要么不变要么至少减半，算 gcd 总共也是 `O(U log U)`',
                 '优化：长度 1 的子序列单独算（不同元素个数）；长度 ≥ 2 时 `i` 不在 nums 里，且至少要有 `2i`、`3i`，所以 `i ≤ U/3`',
                 '易错点：内层从 `2i` 开始枚举，因为 `i` 不在 nums 里；`g` 要从 0 开始',
                 '优化前的写法（枚举到 `U`，从 `i` 开始）逻辑相同，只是常数更大'],
    ),
)
