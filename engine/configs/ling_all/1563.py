def _sum_txt(S):
    if 'k' not in S or 'j' not in S or 'i' not in S or 'pre_max' not in S:
        return '`f[j]`：当前行 `i` 固定时，子数组 `[i,j)` 的最大得分'
    s, i, j, k = S['s'], S['i'], S['j'], S['k']
    if k > j:
        return ''
    return f"左段 `[{i},{k})` 和 = =={s[k] - s[i]}==，右段 `[{k},{j})` 和 = =={s[j] - s[k]}=="


CONFIG = dict(
    num=1563, title='石子游戏 V', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='区间 DP · 前后缀最大值 + 双指针',
    tags=['数学算法', '难度分 2087'],
    code='''
class Solution:
    def stoneGameV(self, stoneValue: List[int]) -> int:
        n = len(stoneValue)
        s = list(accumulate(stoneValue, initial=0))  # stoneValue 的前缀和
        f = [0] * (n + 1)
        suf_max = [[-inf] * (n + 1) for _ in range(n + 1)]

        for i in range(n - 1, -1, -1):
            suf_max[i][i + 1] = -s[i]  # f[i][i+1] - s[i] = 0 - s[i] = -s[i]
            pre_max = -inf  # 本题元素都是正数，也可以初始化成 0
            k = i + 1
            for j in range(i + 2, n + 1):
                while s[k] - s[i] <= s[j] - s[k]:
                    pre_max = max(pre_max, f[k] + s[k])
                    k += 1
                # 循环结束后 s[k] - s[i] > s[j] - s[k]
                q = k if s[k - 1] - s[i] != s[j] - s[k - 1] else k - 1
                f[j] = max(pre_max - s[i], suf_max[q][j] + s[j])
                suf_max[i][j] = max(suf_max[i + 1][j], f[j] - s[i])

        return f[n]
''',
    call='Solution().stoneGameV([1,2,3,1])',
    expect=4,
    views=[
        dict(type='text', fn=_sum_txt),
        dict(type='array', var='s', label='前缀和 s',
             pointers={'i': 'blue', 'j': 'pink', 'k': 'orange'}, h=250),
        dict(type='array', var='f', label='f[j]：区间 [i, j) 的最大得分', pointers={'j': 'pink'}, h=230),
        dict(type='grid', var='suf_max', label='suf_max[q][j]：右段更小一侧的最大值', h=330,
             cursors=[('i', 'j', 'blue', '(i,j)')]),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('k', 'k', 'orange'), 'q', 'pre_max'],
    captions={
        'suf_max[i][i + 1] = -s[i]': '区间 `[{i},{i+1})` 只剩一块石子，得分 0 → `suf_max[{i}][{i+1}] = 0 − s[{i}] = {-s[i]}`',
        'k = i + 1': '`k` 从 `i+1` 开始：切点左边至少留一块石子',
        'for j in': lambda S, B, r: ('`j` 枚举完了，换下一个 `i`' if B.get('j') == S.j and B.get('i') == S.i else f'枚举区间右端点 `j = {S.j}`：现在求 `f[{S.j}]` = 区间 `[{S.i},{S.j})` 的最大得分'),
        'for i in': lambda S, B, r: ('`i` 从右往左枚举完了，`f[n]` 就是答案' if B.get('i') == S.get('i') else f'`i = {S.i}`：区间左端点从右往左枚举，右边的子问题已经算好'),
        'while s[k]': lambda S, B, r: (f"左段和 `{S.s[S.k] - S.s[S.i]}` <= 右段和 `{S.s[S.j] - S.s[S.k]}`：Bob 丢右段，Alice 留左段 → ==这个切点算进 pre_max=="
                                       if S.s[S.k] - S.s[S.i] <= S.s[S.j] - S.s[S.k] else
                                       f"左段和 `{S.s[S.k] - S.s[S.i]}` > 右段和 `{S.s[S.j] - S.s[S.k]}`：再往右切左段只会更大 → `k` 停下（`j` 变大时 `k` 只会右移）"),
        'pre_max = max': '`pre_max` = 左段更小的所有切点里 `f[k] + s[k]` 的最大值 = =={pre_max}==',
        'k += 1': '`k` 右移到 {k}',
        'q = k if': lambda S, B, r: (f'左右段和恰好相等：`k-1` 这个切点两边都能留，所以 `q = k - 1 = {S.q}`'
                                     if S.q == S.k - 1 else f'`q = k = {S.q}`：右段更小的切点从 `{S.q}` 开始'),
        'f[j] = max': '`f[{j}] = max(pre_max − s[i], suf_max[q][j] + s[j])` = max({pre_max - s[i]}, {suf_max[q][j] + s[j]}) = =={f[j]}==：左段更小 / 右段更小两边取最大',
        'suf_max[i][j] = max': '更新后缀最大值：`suf_max[{i}][{j}] = max(suf_max[{i+1}][{j}], f[{j}] − s[{i}])` = {suf_max[i][j]}',
        'return f[n]': '`f[n]` 就是整行石子的最大得分 = =={f[n]}==',
    },
    skip=['n = len(stoneValue)', 'f = [0] * (n + 1)', 'pre_max = -inf', 'suf_max = [[', 'k = i + 1', 'suf_max[i][i + 1]'],
    max_steps=110,
    cards=dict(
        one_liner='区间 DP 的 O(n³) 转移，用双指针 + 前后缀最大值压成 O(n²)',
        complexity='时间 `O(n²)`，空间 `O(n²)`',
        problem=['一排石子，Alice 每轮切成左右两段，Bob 丢掉和更大的一段，Alice 得到留下那段的和',
                 '相等时 Alice 自己选丢哪边，游戏到只剩一块石子结束，求 Alice 最大总分',
                 '示例：`[6,2,3,4,5,5]` → `18`；本视频：`[1,2,3,1]` → `4`'],
        quote='设 p 是最大的满足 s[k]-s[i] <= s[j]-s[k] 的下标 k……有了前后缀最大值，就能 O(1) 时间计算 f[i][j]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先想到记忆化搜索 `dfs(i,j)`，枚举切点 `k`，翻译成递推是 `O(n³)`',
              '左段和 `<=` 右段和的切点是一个前缀，其余是一个后缀：==两段都是区间最大值==',
              '`j` 变大，满足条件的最大 `k` 不会变小：同向双指针维护 `pre_max`，`suf_max` 记录后缀最大值'],
        summary=['时间 `O(n²)`：`k` 对每个 `i` 总共只右移 `O(n)` 次',
                 '`q` 是右段和更小那一侧的起点；两段恰好相等时 `q = k - 1`，两边都能取',
                 '`f` 的第一维可以压掉，但 `suf_max` 仍要二维',
                 '题解还有：记忆化搜索 `@cache`（`O(n³)`）、1:1 递推、带最优性剪枝的递推，本视频讲最后的优化写法'],
    ),
)
