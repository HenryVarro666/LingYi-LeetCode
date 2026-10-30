CONFIG = dict(
    num=1712, title='将数组分成三个子数组的方案数', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='前缀和 + 枚举 r 二分 l（Go 原文转写）',
    tags=['滑动窗口与双指针', '常用数据结构', '难度分 2079'],
    code='''
class Solution:
    def waysToSplit(self, a: List[int]) -> int:
        n = len(a)
        sum = [0] * (n + 1)
        for i, v in enumerate(a):
            sum[i + 1] = sum[i] + v
        ans = 0
        r = 2
        while r < n and 3 * sum[r] <= 2 * sum[n]:
            l1 = bisect_left(sum[1:r], 2 * sum[r] - sum[n]) + 1
            ans += bisect_left(sum[l1:r], sum[r] // 2 + 1)
            r += 1
        return ans % (10 ** 9 + 7)
''',
    call='Solution().waysToSplit([1, 2, 2, 2, 5, 0])',
    expect=3,
    views=[
        dict(type='array', var='a', label='a', h=150, cell=80),
        dict(type='array', var=lambda S: S['sum'] if isinstance(S.get('sum'), list) else None, label='前缀和 sum（l 是第一刀，r 是第二刀；黄 = 合法的 l 范围）', h=230, cell=80,
             pointers={'r': 'pink', 'l1': 'blue'},
             color=lambda S, i, x: 'yellow' if 'l1' in S and 'r' in S and S['l1'] <= i < S['r'] and x <= S['sum'][S['r']] // 2 and S['_line'] in (10, 11) else None),
        dict(type='text', h=80, size=24,
             fn=lambda S: (f"`sum[l] ≥ 2·sum[r] − sum[n]` = `{2*S['sum'][S['r']]-S['sum'][-1]}` 且 `2·sum[l] ≤ sum[r]` → `sum[l] ≤ {S['sum'][S['r']]//2}`" if 'r' in S and S['r'] < len(S['a']) and S['_line'] in (10, 11) else '')),
    ],
    watch=[('r', 'r', 'pink'), ('l1', 'l1', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'sum = [0] * (n + 1)': '`sum[i]` = 前 `i` 个数之和，`sum[0] = 0`',
        'sum[i + 1] = sum[i] + v': '前缀和 `sum[{i+1}] = {sum[i+1]}`',
        'r = 2': '枚举第二刀 `r`：右段 `a[r:]`，中段 `a[l:r]`，`l ≥ 1`，`r ≥ 2`',
        'while r < n and': lambda S, B, r_: (f'`3·sum[{S.r}] = {3*S.sum[S.r]} ≤ 2·sum[n] = {2*S.sum[-1]}`：右段还够大，继续枚举 `r = {S.r}`' if S.r < len(S.a) and 3 * S.sum[S.r] <= 2 * S.sum[-1]
                                             else '`r` 再往右，右段就小于中段了（`3·sum[r] > 2·sum[n]`）→ 结束'),
        'l1 = bisect_left': '右段 ≥ 中段：`sum[l] ≥ 2·sum[r] − sum[n]` → 二分得到最小的 `l = {l1}`',
        'ans += bisect_left': '中段 ≥ 左段：`2·sum[l] ≤ sum[r]` → `l` 在 `[{l1}, {l1 + (ans - B.ans)})` 内，这个 `r` 有 =={ans - B.ans}== 种，`ans` = {ans}',
        'r += 1': '`r` 右移到 {r}',
        'return ans': '累计 `{ans}` 种，对 `10^9+7` 取模 = =={ret}==',
    },
    cards=dict(
        one_liner='枚举第二刀 r，用前缀和不等式二分出第一刀的范围',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['把数组分成 3 段非空连续子数组 `left, mid, right`',
                 '要求 `sum(left) ≤ sum(mid) ≤ sum(right)`，求方案数（对 `10^9+7` 取模）',
                 '示例：`[1,2,2,2,5,0]` → `3`'],
        quote='记两个分割位置为 l 和 r，利用前缀和可以得到不等式 S_l ≤ S_r − S_l ≤ S_n − S_r。枚举 r，通过二分可以得到使不等式成立的 l 的范围，累加这个范围的长度即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['变形：`S_l ≥ 2S_r − S_n` 与 `2S_l ≤ S_r`，前缀和单调不减，所以 `l` 的范围是一段区间',
              '枚举 `r`，两次二分得到区间的左右端点，区间长度累加进答案',
              '`r` 的范围：`2 ≤ r < n` 且 `3S_r ≤ 2S_n`，超过就可以停'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python：`sort.SearchInts` 对应 `bisect_left`（在切片上二分）',
                 '时间 `O(n log n)`，空间 `O(n)`；元素非负，所以前缀和单调不减才能二分',
                 '易错：`l ∈ [1, r)`，所以第一次二分在 `sum[1:r]` 上并加回 1 的偏移',
                 '最后别忘了对 `10^9+7` 取模'],
    ),
)
