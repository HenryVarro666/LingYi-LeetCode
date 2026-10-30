M = [[3, 5, 4], [4, 7, 8], [8, 10, 3], [1, 3, 2]]


def _fmt(v):
    return '-inf' if v == float('-inf') else str(v)


def _txt(S):
    if 'pre_max' not in S:
        return '`f[i]`：以第 i 场会议结尾的最大收益；`pre_max` 存 `f[j] - end[j]` 的前缀最大值'
    if 'start' not in S:
        return '`f[i] = revenue + start + max(f[j] - end[j])`，其中 `end[j] <= start`'
    s, e, r = S['start'], S['end'], S['revenue']
    f = S.get('f')
    if 'j' in S and S['_line'] >= 15 and f is not None:
        return f'`f = {r} + {S["pre_max"][S["j"]]} + {s}` = =={f}==（收益 + 左边最优的 f−end + 本场开始）'
    return f'当前会议 `[{s}, {e})`，收益 {r}；答案 `ans` = =={S["ans"]}=='


CONFIG = dict(
    num=4068, title='考虑空闲时间的会议最大收益', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='相邻相关 DP · 前缀最大 + 二分', tags=[],
    code='''
class Solution:
    def maxEarnings(self, meetings: list[list[int]]) -> int:
        # 按结束时间从小到大排序
        meetings.sort(key=lambda m: m[1])
        end0 = meetings[0][1]

        # pre_max[i+1] = [0,i] 中的 f[j] - end[j] 的前缀最大值
        pre_max = [-inf] * (len(meetings) + 1)
        ans = 0
        for i, (start, end, revenue) in enumerate(meetings):
            f = revenue
            if start >= end0:  # 左边有会议
                j = bisect_right(meetings, start, hi=i, key=lambda m: m[1])  # hi=i 表示二分上界为 i（默认为 n）
                # 为什么是 j 不是 j+1：上面算的是 > start，-1 后得到 <= start，但由于还要 +1，抵消了
                f += pre_max[j] + start
            ans = max(ans, f)
            pre_max[i + 1] = max(pre_max[i], f - end)

        return ans
''',
    call=f'Solution().maxEarnings({M!r})',
    expect=15,
    views=[
        dict(type='table', var='meetings', label='meetings（按结束时间排序；黄 = 当前第 i 场）', rows=lambda S: [f'#{k}' for k in range(len(S['meetings']))],
             cols=['开始', '结束', '收益'], h=250, cell=110,
             color=lambda S, i, j, v: 'yellow' if i == S.get('i') else None),
        dict(type='array', var='pre_max', label='pre_max[k] = 前 k 场里 f − end 的最大值', fmt=_fmt, pointers={'j': 'pink'}, h=200, cell=110),
        dict(type='text', h=100, size=27, fn=_txt),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('f', 'f', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'meetings.sort': '按==结束时间==排序：这样 `[0, i)` 里满足「结束 <= 当前开始」的会议恰好是一段前缀，可以二分',
        'end0 = ': '最早结束的会议结束于 `end0 = {end0}`：开始早于它的会议，左边不可能再有会议',
        'pre_max = ': '`pre_max[k]` 存前 k 场的 `f − end` 最大值，初始 `-inf`（还没有会议）',
        'ans = 0': '`ans` 是所有 `f` 的最大值',
        'for i, (start': lambda S, B, r: ('会议都枚举完了，`ans` 就是答案' if 'i' in B and B['i'] == S['i'] else f'第 `{S.i}` 场：`[{S.start}, {S.end})`，收益 {S.revenue}。`f` 表示它==一定要选==且为最后一场时的最大收益'),
        'f = revenue': '没有前一场时 `f = revenue = {f}`',
        'if start >= end0': lambda S, B, r: (
            f'`start = {S.start} >= end0 = {S.end0}`：左边可能有会议 → 要去找倒数第二场' if S.start >= S.end0
            else f'`start = {S.start} < end0 = {S.end0}`：左边放不下任何会议，`f` 就是收益'),
        'j = bisect_right': '二分：前 `i = {i}` 场里，结束时间 <= `{start}` 的有 `j = {j}` 场，它们都能当倒数第二场',
        'f += pre_max': '`f = revenue + pre_max[{j}] + start = {revenue} + {pre_max[j]} + {start}` = =={f}==：`start − end[j]` 就是空闲时间收益',
        'ans = max': '`ans = max({B.ans}, {f}) = {ans}`',
        'pre_max[i + 1] =': '`f − end = {f} − {end} = {f - end}`，并入前缀最大 → `pre_max[{i + 1}]` = =={pre_max[i + 1]}==',
        'return ans': '最大总收益 =={ans}==',
    },
    cards=dict(
        one_liner='把 `f[j] − end[j]` 做前缀最大，空闲时间收益就拆成了 start − end[j]',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['选一些互不重叠的会议，得到收益之和；相邻两场之间每单位空闲时间再加 1',
                 '首场之前、末场之后的空闲不算；只选一场没有空闲收益',
                 '本视频：`[[3,5,4],[4,7,8],[8,10,3],[1,3,2]]` → `15`'],
        quote='本题需要知道倒数第二场会议的位置，从而计算空闲时间的收益。所以本题是相邻相关 DP，故定义成 meetings[i] 一定要选，从而方便转移。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i] = max(f[j] + start_i − end_j) + revenue_i`，枚举倒数第二场 `j`（`end_j <= start_i`）',
              '提出与 j 无关的项：`start_i + revenue_i + max(f[j] − end_j)`',
              '按结束时间排序后，`f[j] − end[j]` 做前缀最大，用二分找到 j 的范围'],
        summary=['时间 `O(n log n)`，空间 `O(n)`；是 1235 题（规划兼职工作）的变形',
                 '易错：`f` 要求第 i 场一定选，答案是 `max(f)`，不是 `f` 的最后一项',
                 '`bisect_right(..., hi=i)` 返回的下标刚好抵消了 `pre_max` 的 +1 偏移，所以用 `pre_max[j]`',
                 '没有左邻会议时 `f = revenue`，不能加 `start`（首场前的空闲不算）'],
    ),
)
