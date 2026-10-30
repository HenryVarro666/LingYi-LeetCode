CONFIG = dict(
    num=4037, title='最多有效分割位置 II', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='前后缀 GCD · 至多删一个数 · p/q 计数',
    tags=['灵神题单·数学算法', '难度分 2372'],
    code='''
class Solution:
    def maxValidSplits(self, nums: list[int]) -> int:
        n = len(nums)
        pre_gcd = [0] * n
        g = 0
        for i, x in enumerate(nums):
            g = gcd(g, x)
            pre_gcd[i] = g

        suf_gcd = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            suf_gcd[i] = gcd(suf_gcd[i + 1], nums[i])

        # 不删任何数
        all_gcd = suf_gcd[0]
        p = pre_gcd.index(all_gcd)  # [p,n-1] 都是 all_gcd
        q = bisect_right(suf_gcd, all_gcd, 0, n) - 1  # [0,q] 都是 all_gcd
        ans = max(q - p, 0)  # 满足 i >= p 且 i+1 <= q 的 i 的个数

        for i in range(n):
            if i > 0 and pre_gcd[i] == pre_gcd[i - 1]:
                continue

            # 删除 nums[i]
            pre_g = pre_gcd[i - 1] if i > 0 else 0
            suf_g = suf_gcd[i + 1] if i < n - 1 else 0
            if suf_g > all_gcd and pre_g % suf_g == 0:  # 兼容 pre_g 为 0 的情况
                new_g = suf_g
            elif pre_g > all_gcd and suf_g % pre_g == 0:  # 兼容 suf_g 为 0 的情况
                new_g = pre_g
            else:
                continue

            g = 0
            for j, x in enumerate(nums):
                if j == i:
                    continue
                g = gcd(g, x)
                if g == new_g:
                    p = j
                    break

            g = 0
            for j in range(n - 1, -1, -1):
                if j == i:
                    continue
                g = gcd(g, nums[j])
                if g == new_g:
                    q = j
                    break

            res = q - p
            if p <= i < q:
                res -= 1  # 因为删除了 nums[i]，少一个有效分割
            ans = max(ans, res)
            break

        return ans
''',
    call='Solution().maxValidSplits([10, 30, 15, 10])',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 枚举的 i，红 = 被删的数）', cell=96, h=190,
             pointers={'i': 'blue'},
             color=lambda S, i, v: ('red' if (S.get('new_g') is not None and S['_line'] >= 31 and i == S.get('i')) else None)),
        dict(type='array', var='pre_gcd', label='pre_gcd[i]：前缀 gcd（只会变小）；p = 第一个等于目标 gcd 的位置', cell=96, h=215, pointers={'p': 'pink'}),
        dict(type='array', var='suf_gcd', label='suf_gcd[i]：后缀 gcd；q = 最后一个等于目标 gcd 的位置', cell=96, h=215, pointers={'q': 'orange'}),
        dict(type='text', h=70, size=28, fn=lambda S: (f"`p = {S['p']}`，`q = {S['q']}`：有效分割位置 `i` 满足 `p ≤ i < q`，共 `max(q − p, 0)` 个" if 'q' in S and 'p' in S else '')),
    ],
    watch=[('i', 'i', 'blue'), ('all_gcd', 'all_gcd', 'cyan'), ('new_g', 'new_g', 'yellow'), ('p', 'p', 'pink'), ('q', 'q', 'orange'), ('ans', 'ans', 'green')],
    skip=['n = len(nums)', 'pre_gcd = [0]', 'suf_gcd = [0]'],
    captions={
        7: '前缀 gcd：`g = gcd({B.g}, {x}) = {g}`',
        'pre_gcd[i] = g': '`pre_gcd[{i}] = {g}`：前缀 `nums[0..{i}]` 的 gcd',
        'suf_gcd[i] = gcd': '`suf_gcd[{i}] = {suf_gcd[i]}`：后缀 `nums[{i}..]` 的 gcd',
        'all_gcd = suf_gcd[0]': '整个数组的 gcd = `{all_gcd}`。==性质一：任何有效分割，两侧 gcd 都必须等于它==',
        'p = pre_gcd.index': '`pre_gcd` 递减，第一次等于 `all_gcd` 的位置 `p = {p}`：前缀至少要包含到 `p`，分割点 `i ≥ p`',
        'q = bisect_right': '`suf_gcd` 递增，最后一个等于 `all_gcd` 的位置 `q = {q}`：后缀从 `i+1` 开始，要求 `i+1 ≤ q`',
        'ans = max(q - p': '不删数时有效分割个数 = `max({q} − {p}, 0) = {ans}`',
        'for i in range(n):': '枚举要删除的 `nums[i]`',
        'if i > 0 and pre_gcd[i] == pre_gcd[i - 1]': lambda S, B, r: (f'`pre_gcd[{S.i}] == pre_gcd[{S.i - 1}]`：它不改变前缀 gcd → ==性质二：删它不会让得分更大，跳过==' if S.i > 0 and S.pre_gcd[S.i] == S.pre_gcd[S.i - 1] else '前缀 gcd 在这里变化了（或 `i = 0`）→ 值得考虑删除它'),
        'pre_g = pre_gcd[i - 1]': '删 `nums[{i}]` 后，左边剩余部分的 gcd `pre_g = {pre_g}`（`i=0` 时为 0）',
        'suf_g = suf_gcd[i + 1]': '右边剩余部分的 gcd `suf_g = {suf_g}`（最后一个时为 0）',
        'if suf_g > all_gcd': lambda S, B, r: (f'`suf_g = {S.suf_g} > all_gcd = {S.all_gcd}` 且 `pre_g` 是它的倍数 → ==性质四：L 是 R 的倍数，可能有有效分割==，删后整体 gcd `new_g = {S.suf_g}`' if (S.suf_g > S.all_gcd and S.pre_g % S.suf_g == 0) else '`suf_g` 不大于 `all_gcd`，或者 `pre_g` 不是它的倍数，看另一种情况'),
        'elif pre_g > all_gcd': lambda S, B, r: (f'`pre_g = {S.pre_g} > all_gcd = {S.all_gcd}` 且 `suf_g` 是它的倍数 → 删后 `new_g = {S.pre_g}`' if (S.pre_g > S.all_gcd and S.suf_g % S.pre_g == 0) else '两侧 gcd 不成倍数关系 → ==删它不可能有有效分割=='),
        'new_g = suf_g': '`new_g = {new_g}`：删掉 `nums[{i}]` 后数组的 gcd',
        'new_g = pre_g': '`new_g = {new_g}`：删掉 `nums[{i}]` 后数组的 gcd',
        'continue': lambda S, B, r: ('这个位置不用考虑，看下一个' ),
        34: '重新算删除 `nums[{i}]` 后的前缀 gcd，==提前停在第一次等于 new_g 的位置==',
        'for j, x in enumerate': '从左往右扫，跳过被删的 `nums[{i}]`',
        38: '`g = gcd({B.g}, {x}) = {g}`',
        47: '`g = gcd({B.g}, {nums[j]}) = {g}`（从右往左）',
        'if g == new_g': lambda S, B, r: (f'`g = {S.g} == new_g = {S.new_g}` → ==找到了==' if S.g == S.new_g else f'`g = {S.g} ≠ new_g = {S.new_g}`，继续'),
        'p = j': '删除后前缀 gcd 第一次到 `new_g` 的位置 `p = {p}`（下标按原数组）',
        'q = j': '删除后后缀 gcd 第一次（从右往左）到 `new_g` 的位置 `q = {q}`',
        'res = q - p': '删除后分割点个数 `q − p = {res}`',
        'res -= 1': '`p ≤ i < q`：被删的 `nums[{i}]` 夹在中间，分割位置少一个 → `res = {res}`',
        'ans = max(ans, res)': '`ans = max({B.ans}, {res}) = {ans}`',
        43: '再从右往左算后缀 gcd，同样==提前停在第一次等于 new_g 的位置==',
        41: '这一步找到了，退出扫描',
        50: '这一步找到了，退出扫描',
        56: '==性质三：至多只需考虑一个要删除的数==，直接结束循环',
        'return ans': '最多有效分割位置：`{ans}`',
    },
    cards=dict(
        one_liner='有效分割两侧 gcd 都等于全体 gcd：找到 p、q，数一数就行',
        complexity='时间 `O(n + log U)`，空间 `O(n)`',
        problem=['可以删除至多一个元素，得到数组 `arr`',
                 '分割位置 `i` 有效：`gcd(arr[0..i]) == gcd(arr[i+1..])`，求最多有效分割个数',
                 '示例：`[10,30,15,10]` → `2`（删 15 后 `[10,30,10]`）'],
        quote='对于 a 的任意有效分割 P+Q，都满足 gcd(P) = gcd(Q) = gcd(a)。……至多只需考虑一个要删除的数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['性质一：有效分割两侧 gcd 都等于整个数组的 gcd，所以数 `p ≤ i < q` 的个数就行',
              '性质二～四：删除的位置只考虑「前缀 gcd 变化」的下标，且左右 gcd 要成倍数关系，最多删一个',
              '前缀 gcd 要么不变要么至少减半，所以扫描提前停止'],
        summary=['时间 `O(n + log U)`，空间 `O(n)`；题解还给出了更慢的 `O(log U)` 个删除位置写法',
                 '易错点：删除位置夹在 `p` 和 `q` 之间要 `res -= 1`；`i=0` 或 `i=n-1` 时 `pre_g/suf_g` 用 0 兼容',
                 '`suf_gcd[n] = 0` 只是哨兵，`bisect_right` 只查 `[0, n)`',
                 '本视频选的是题解最后一种写法（性质四），前面几种写法逐步放宽剪枝'],
    ),
)
