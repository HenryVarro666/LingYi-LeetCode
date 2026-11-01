A = [1, 2, 3, 1, 2, 4]
K = 3


def _cnt(S):
    c = S.get('cnt')
    return [r[:8] for r in c] if c else None


def _dp(S):
    c = S.get('dp')
    return [r[:8] for r in c] if c else None


def _txt(S):
    ln = S.get('_line', 0)
    if 'dp' not in S:
        if 'ans' in S and ln >= 12:
            return f"情况 1：某一组全改，其余各留最多的一个 → 保留 `ans = {S['ans']}`（累加各组最大次数，再减去最小的那组）"
        return '先数每一组（下标模 k 相同）里每个数出现几次：`cnt[组][值]`'
    if 22 <= ln <= 31 and 'p' in S:
        return f"`f({S.get('p')}, {S.get('xor')})`：前 {S.get('p', 0) + 1} 组保留的数异或为 `{S.get('xor')}` 时，最多保留几个"
    return f"情况 2：每组都留一个数，异或为 0；情况 1 的保留数 `ans = {S.get('ans')}`"


def _acol(S, idx, v):
    ln = S.get('_line', 0)
    cur = S.get('j') if ln in (9, 10, 11) else (S.get('i') if ln in (27, 28) else None)
    return 'blue' if cur == idx else None


CONFIG = dict(
    num=1787, title='使所有区间的异或结果为零', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='按下标模 k 分组 + 异或 DP（Go 原文转写）',
    tags=['灵神题单·动态规划', '难度分 2640'],
    code='''
class Solution:
    def minChanges(self, a: List[int], k: int) -> int:
        cnt = [[0] * 1024 for _ in range(k)]
        n = len(a)
        minCnt = n
        ans = 0
        for i in range(k):
            maxCnt = 0
            for j in range(i, n, k):
                cnt[i][a[j]] += 1
                maxCnt = max(maxCnt, cnt[i][a[j]])
            ans += maxCnt
            minCnt = min(minCnt, maxCnt)
        ans -= minCnt

        dp = [[0] * 1024 for _ in range(k)]
        for i in range(len(dp)):
            for j in range(1024):
                dp[i][j] = -1

        def f(p: int, xor: int) -> int:
            if p == 0:
                return cnt[0][xor]
            if dp[p][xor] >= 0:
                return dp[p][xor]
            res = 0
            for i in range(p, n, k):
                res = max(res, cnt[p][a[i]] + f(p - 1, xor ^ a[i]))
            dp[p][xor] = res
            return res

        return n - max(ans, f(k - 1, 0))
''',
    call=f'Solution().minChanges({A}, {K})',
    expect=1,
    max_events=12000,
    skip=['minCnt = min', 'res = 0', 'n = len(a)', 'minCnt = n', 'ans = 0', 'maxCnt = 0', 'for j in range(1024)', 'dp[i][j] = -1', 'for i in range(len(dp))',
          'dp = [[0]', 'def f('],
    views=[
        dict(type='array', var='a', label='a（蓝 = 当前读的元素；第 g 组 = 下标模 k 为 g）', cell=70, h=130,
             color=_acol),
        dict(type='table', var=_cnt, label='cnt[组][值]：每组里各值出现次数（只画值 0..7）', cell=70, h=190,
             rows=lambda S: [f'组{g}' for g in range(K)], cols=lambda S: list(range(8)),
             color=lambda S, r, c, v: 'yellow' if S.get('_line') in (10, 11) and S.get('i') == r and S.get('j') is not None and S['a'][S['j']] == c else None),
        dict(type='table', var=_dp, label='dp[p][xor]：记忆化（-1 = 还没算；只画 xor 0..7）', cell=70, h=190,
             rows=lambda S: [f'p={g}' for g in range(K)], cols=lambda S: list(range(8)),
             color=lambda S, r, c, v: 'yellow' if S.get('p') == r and S.get('xor') == c and S.get('_line', 0) >= 22 else None),
        dict(type='calls', h=110, hide=()),
        dict(type='text', fn=_txt, size=22, h=60),
    ],
    watch=[('ans', 'ans', 'green'), ('minCnt', 'minCnt', 'pink'), ('p', 'p', 'blue'), ('xor', 'xor', 'purple'), ('res', 'res', 'yellow')],
    captions={
        'cnt = [[0] * 1024': '`cnt[i][v]`：第 `i` 组里数 `v` 出现的次数（值 < 1024，只画前 8 列）',
        'n = len(a)': '`n = {n}`',
        'for i in range(k)': lambda S, B, r: (f'第 `{S.i}` 组：下标 ≡ {S.i} (mod {S.k}) 的元素' if B.get('i') != S.get('i') else '各组统计完毕'),
        'for j in range(i, n, k)': '遍历第 `{i}` 组的元素：`j` 从 `{i}` 起每次加 `k = {k}`；遍历完这组就往下走',
        'cnt[i][a[j]] += 1': '第 {i} 组里 `{a[j]}` 出现了 `{cnt[i][a[j]]}` 次',
        'maxCnt = max': '这一组出现最多的次数 `maxCnt` = =={maxCnt}==',
        'ans += maxCnt': '情况 1 的贪心：每组留出现最多的那个数，累加 → `ans = {ans}`',
        'minCnt = min': '记下最小的组最大次数 `minCnt = {minCnt}`（它就是被“全改掉”的那一组）',
        'ans -= minCnt': '==有一组全改==：扣掉最大次数最小的那组（`minCnt = {minCnt}`），情况 1 最多保留 `ans` = =={ans}== 个',
        'return cnt[0][xor]': '第 0 组：只能选值 `{xor}`，保留 `cnt[0][{xor}]` = =={ret}== 个',
        'if p == 0': lambda S, B, r: (f'`p = 0`：递归边界，直接查第 0 组' if S.p == 0 else f'`p = {S.p}`：还要继续往前枚举'),
        'if dp[p][xor] >= 0': lambda S, B, r: (f'`dp[{S.p}][{S.xor}] = {S.dp[S.p][S.xor]}` 已算过 → ==直接返回==' if S.dp[S.p][S.xor] >= 0
                                               else f'`dp[{S.p}][{S.xor}]` 还没算过（-1），要枚举'),
        'res = 0': '`res` 记录第 `{p}` 组的最优选择',
        'res = max(res': '选 `a[{B.i}] = {B.a[B.i]}`：本组该数出现 `cnt[{B.p}][{B.a[B.i]}] = {B.cnt[B.p][B.a[B.i]]}` 次，再加上 `f({B.p - 1}, {B.xor ^ B.a[B.i]})`（前面各组异或为这个值的最优）',
        'dp[p][xor] = res': '记忆化：`dp[{p}][{xor}] = {res}`，下次直接用',
        'return n - max': lambda S, B, r: ('先算情况 2：调用 `f(k-1, 0)`，求每组各留一个、异或为 0 时的最大保留数' if r is None
                                           else f'两种情况取最大保留数，答案 = `n` − 最大保留数 = =={r}=='),
        'for i in range(p, n, k)': '枚举第 `{p}` 组里选哪个数 `a[i]`（`i` 每次加 `k`）；枚举完就记忆化并返回',
    },
    cards=dict(
        one_liner='数组必须以 k 为周期，按模 k 分组，求最多能保留几个数',
        complexity='时间 `O(n·2^L)`，空间 `O(k·2^L)`',
        problem=['给整数数组 `nums` 和整数 `k`，每个长度为 `k` 的区间异或和都要为 0',
                 '问至少要改动几个元素',
                 '示例：`nums = [1,2,3,1,2,4]`，`k = 3` → `1`（把 `4` 改成 `3`）'],
        quote='通过计算最多能保留多少个数不变，来计算最少需要更改的个数。要使区间异或和为 0，数组中的数必须是以 k 为周期的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['按下标模 `k` 分成 `k` 组，每组最终全相同',
              '情况 1：有一组全改 → 其余组各留出现最多的数',
              '情况 2：每组留一个、异或为 0 → `f(p, xor)` 记忆化',
              '答案 = `n` − 两种情况的最大保留数'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（原文自带的 `min`/`max` 函数改用 Python 内置；`defer` 写回改为返回前写入 `dp`）',
                 '为了演示用了小数据，但 `1024` 的数组大小是题目值域上限，原样保留',
                 '时间 `O(n·2^L)`：状态 `k·2^L`，每个状态枚举 `n/k` 个数',
                 '易错：必须分“某组全改”和“每组都留一个”两种情况；`dp` 初值用 `-1`，因为保留数可能为 0'],
    ),
)
