def _p(S):
    p = S.get('p')
    if isinstance(p, list):
        return p[:S['m']]
    if 'm' in S:
        return S['nums'][:S['m']]
    return S['nums']


def _txt(S):
    if not isinstance(S.get('p'), list) or 'sl' not in S:
        return '把第 i 个 1 的位置 `pos` 换成 `pos − i`：交换代价变成「到中位数的距离和」'
    i, k, p = S.get('i'), S['k'], S['p']
    if i is None:
        return '三个前缀和 `sl = s[i]`，`sm = s[i+k//2]`，`sr = s[i+k]`，窗口右移时各加一项'
    mid = i + k // 2
    return f'窗口 `p[{i}:{i + k}]` 的中位数是 `p[{mid}] = {p[mid]}`：距离和 = `sl + sr − 2×sm' + (f' − p[{mid}]`' if k % 2 else '`') + f' = ==' + str(S['sl'] + S['sr'] - S['sm'] * 2 - p[mid] * (k % 2)) + '=='


def _win(S, i, v):
    p = S.get('p')
    if isinstance(p, list) and 'i' in S and 'sl' in S:
        if S['i'] <= i < S['i'] + S['k']:
            return 'yellow' if i == S['i'] + S['k'] // 2 else 'blue'
        return None
    return None


CONFIG = dict(
    num=1703, title='得到连续 K 个 1 的最少相邻交换次数', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='减去序号 + 中位数贪心 + 前缀和',
    tags=['前缀和', '中位数贪心', '难度分 2467'],
    code='''
class Solution:
    def minMoves(self, nums: List[int], k: int) -> int:
        m = 0
        for i, p in enumerate(i for i, x in enumerate(nums) if x):
            nums[i] = p - i
            m += 1
        if m == len(nums): return 0  # 全部都是 1
        ans, p = inf, nums
        sl, sm, sr = 0, sum(p[:k // 2]), sum(p[:k])  # s[i] s[i+k//2] s[i+k] 忽略切片开销
        for i in range(m - k + 1):
            ans = min(ans, sl + sr - sm * 2 - p[i + k // 2] * (k % 2))
            sl += p[i]
            sm += p[i + k // 2]
            sr += p[i + k]
        return ans
''',
    call='Solution().minMoves([1,0,0,1,0,1,0,0,1], 3)',
    expect=3,
    views=[
        dict(type='array', var=_p, label='p：每个 1 的位置减去它的序号（存在 nums 前 m 格）', h=230,
             color=_win, pointers={'i': 'pink'}),
        dict(type='text', fn=_txt, h=70),
    ],
    watch=['m', 'i', ('sl', 'sl', 'cyan'), ('sm', 'sm', 'purple'), ('sr', 'sr', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'nums[i] = p - i': '第 `{i}` 个 1 在位置 `{p}`，存 `p - i = {p - i}`：把「相邻交换」变成「到同一点的距离」',
        'm += 1': '已找到 `{m}` 个 1',
        'if m == len(nums)': '1 的个数 `m = {m}`，不是全 1 → 继续',
        'ans, p = inf': '`p` 就是上面存好的数组：`{p[:m]}`（后面的格子不再用）',
        'sl, sm, sr': '三个前缀和对应窗口 `[0,k)`：`sl = 0`，`sm = s[k//2]` = {sm}，`sr = s[k]` = {sr}',
        'for i in range(m - k + 1)': lambda S, B, r: ('所有窗口都枚举完了' if 'i' in B and B.i == S.i
                                                       else f'枚举窗口 `p[{S.i}:{S.i + S.k}]`，共 {S.m - S.k + 1} 个'),
        'ans = min': lambda S, B, r: (f'窗口 `p[{S.i}:{S.i + S.k}]` 以中位数 `p[{S.i + S.k // 2}] = {S.p[S.i + S.k // 2]}` 为目标：'
                                      f'左边 − 右边的差合起来 = =={S.sl + S.sr - S.sm * 2 - S.p[S.i + S.k // 2] * (S.k % 2)}==，'
                                      f'`ans = min({B.ans}, …) = {S.ans}`'),
        'sl += p[i]': '窗口右移：左端 `p[{i}] = {p[i]}` 离开，`sl` → {sl}',
        'sm += p[i + k // 2]': '中位数右移一格，`sm` += `p[{i + k // 2}]` → {sm}',
        'sr += p[i + k]': lambda S, B, r: (f'右端新进 `p[{S.i + S.k}] = {S.p[S.i + S.k]}`，`sr` → {S.sr}' if S.i + S.k < S.m
                                           else f'已是最后一个窗口：这次多读的 `p[{S.i + S.k}]` 在有效范围外，之后不会再用'),
        'return ans': '最少交换次数 `{ans}`',
    },
    cards=dict(
        one_liner='每个 1 减去序号，相邻交换就变成到中位数的距离和',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 只含 0 和 1，每次交换相邻两个数',
                 '求让数组里出现 `k` 个连续 1 的最少交换次数',
                 '示例：`[1,0,0,1,0,1]`，`k=2` → `1`；视频用 `[1,0,0,1,0,1,0,0,1]`，`k=3`'],
        quote='它到 p[0] 和 p[k-1] 的距离和都是一个定值，那么去掉 p[0] 和 p[k-1] 这两个最左最右的数，问题规模缩小。',
        quote_src='—— 灵茶山艾府题解答疑',
        idea=['选 `k` 个相邻的 1（不会跨过别的 1 去换）',
              '第 j 个 1 要挨着排好，目标位置是 `x + j`；减去序号后目标就是同一个数 `x`',
              '`x` 取中位数最优，窗口内距离和用前缀和 `O(1)` 算'],
        summary=['时间 `O(n)`；优化版把 `p` 存回 `nums`，额外空间 `O(1)`',
                 '`s[i]+s[i+k]−2·s[i+k//2]` 再减 `p[mid]×(k%2)`：奇数个时中位数自己多算了一次',
                 '`m == len(nums)` 全是 1，答案 0；易错：别忘了 `p[i] − i`',
                 '灵神也给了不改 `nums`、用 `accumulate` 前缀和数组的写法'],
    ),
)
