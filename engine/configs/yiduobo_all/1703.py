def _inwin(S, i, v):
    p = S.get('p')
    if p is None or 'l' not in S or 'r' not in S or not v:
        return None
    ones = [j for j in range(i + 1) if S['nums'][j]]
    idx = len(ones) - 1
    if S['l'] <= idx <= S['r']:
        return 'yellow' if idx == S.get('m') and S.get('_line', 0) >= 28 else 'blue'
    return None


def _txt(S):
    if 'now' not in S:
        return '先把所有 1 的位置收进 `p`：答案一定来自 `p` 中连续的 `k` 个'
    ln = S.get('_line', 0)
    if ln < 17:
        return f'窗口 `p[{S["l"]}..{S["r"]}]` 两端配对相减：`now` = ==各对 (p[r] − p[l]) 之和== = =={S["now"]}=='
    if 'm' not in S or 'res' not in S:
        return f'第一个窗口聚到中心的代价 `now` = =={S["now"]}=='
    return f'窗口 `[{S["l"]}, {S["r"]}]`，中心 `m = {S["m"]}`，聚到中心的代价 `now` = =={S["now"]}==，当前最小 `res` = =={S["res"]}=='


CONFIG = dict(
    num=1703, title='得到连续 K 个 1 的最少相邻交换次数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='滑动窗口 + 中位数 + 增量',
    tags=['前缀和', '中位数贪心', '难度分 2467'],
    code='''
class Solution(object):
    def minMoves(self, nums, k):

        p = []
        for index, num in enumerate(nums):
            if num == 1:
                p.append(index)
        
        l = 0
        r = k - 1
        now = 0
        while l < r:
            now += p[r] - p[l]
            l += 1
            r -= 1
        
        res = now
        
        
        m = l
        l = 0
        r = k - 1
        res = now
        n = len(p)

        while r < n - 1:
            if k & 1:
                now += p[r + 1] - p[m + 1]
                now += p[l] - p[m]
            else:
                now += p[r + 1] - p[m]
                now += p[l] - p[m]
            res = min(res, now)
            l += 1
            r += 1
            m += 1
        
        res -= (1 + (k - 1) // 2) * ((k - 1) // 2)
        if k % 2 == 0:
            res -= k // 2
        
        return res
''',
    call='Solution().minMoves([1,0,0,1,0,1,0,0,1], 3)',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 窗口内的 1，黄 = 中心）', h=170,
             color=_inwin),
        dict(type='array', var='p', label='p：每个 1 的位置', h=190, window=('l', 'r'),
             pointers={'m': 'pink'}),
        dict(type='text', fn=_txt, h=70),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'cyan'), ('m', 'm', 'pink'), ('now', 'now', 'orange'), ('res', 'res', 'green')],
    captions={
        'p.append(index)': '位置 `{index}` 是 1，记入 `p = {p}`',
        'while l < r': lambda S, B, r: (f'`l={S.l} < r={S.r}`：还有一对没配' if S.l < S.r else f'`l={S.l} ≥ r={S.r}`：配完了，剩下中间那个（奇数）或没有（偶数）'),
        'now += p[r] - p[l]': '一对点 `p[{r}] − p[{l}]`：不管中心选哪，这两点到中心的距离和就是它们的间距，`now` → {now}',
        'res = now': '`res = now = {now}`：把第一个窗口的代价作为最小值的初始值',
        'm = l': '中心 `m = {m}`：配完后 `l` 停在中间，偶数个时取靠后的那个',
        'r = k - 1': '窗口回到最左：`[{l}, {r}]`',
        'n = len(p)': '一共 `n = {n}` 个 1',
        'while r < n - 1': lambda S, B, r: (f'`r = {S.r} < {S.n - 1}`：窗口还能右移' if S.r < S.n - 1 else f'`r = {S.r}` 已到最右，窗口滑完'),
        'now += p[r + 1] - p[m + 1]': '窗口右移（k 奇）：新进 `p[{r + 1}]`，距离 + `p[{r + 1}] − p[{m + 1}]`，`now` → {now}',
        'now += p[l] - p[m]': '左端 `p[{l}]` 离开，距离 + `p[{l}] − p[{m}]`，`now` → {now}',
        'res = min(res, now)': '`res = min({B.res}, {now}) = {res}`',
        'l += 1': '窗口右移：`l` → {l}',
        'r += 1': '`r` → {r}',
        'm += 1': '中心跟着右移：`m` → {m}',
        'res -= (1': '聚到中心的代价多算了「从中心排开」的部分：减去 `(1+(k−1)//2)×((k−1)//2)` = {(1 + (k - 1) // 2) * ((k - 1) // 2)} → `res` = =={res}==',
        'res -= k // 2': 'k 为偶数，多出落单的 `k//2`，再减去',
        'return res': '最少交换次数 `{res}`',
    },
    cards=dict(
        one_liner='先把 k 个点聚到中心，再减去排开所需的固定代价',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nums` 只含 0 和 1，每次交换相邻两个数',
                 '求让数组里出现 `k` 个连续 1 的最少交换次数',
                 '示例：`[1,0,0,1,0,1]`，`k=2` → `1`；视频用 `[1,0,0,1,0,1,0,0,1]`，`k=3`'],
        quote='最终答案必然是从p中连续的k个值得来的……首先计算所有点聚集到中心点所需的代价，然后计算将这些点从中心点分配到实际的目的地所需的代价，然后使用前者减去后者就是最终答案了。',
        quote_src='—— yiduobo 题解原文',
        idea=['交换操作不能模拟，只统计每个 1 的位置 `p`，答案来自连续的 `k` 个',
              '先算 k 个点==聚到中心点==的代价，再减去「中心排开」的固定代价',
              '窗口右移时 `now` 可以 `O(1)` 增量更新，不必重算'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`k` 奇偶不同：偶数时中心取靠后的那个，增量项也不同',
                 '最后要减去固定代价：奇数 `(1+(k−1)/2)×((k−1)/2)`，偶数再减 `k/2`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '对比灵神：灵神先把 `p[i]` 换成 `p[i]−i`，一步到位；yiduobo 最后补减固定代价'],
    ),
)
