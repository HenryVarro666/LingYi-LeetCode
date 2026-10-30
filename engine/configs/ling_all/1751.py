EV = [[1, 2, 4], [3, 4, 3], [2, 3, 1], [4, 5, 2]]


def _ev_txt(S):
    e = S.get('events')
    if e is None:
        return ''
    i = S.get('i', -1) if S['_line'] >= 13 else -1
    return '按结束时间排序：' + '  '.join((f'==[{a},{b}]:{c}==' if k == i else f'[{a},{b}]:{c}') for k, (a, b, c) in enumerate(e))


def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if S.get('_line', 0) < 15 or i is None:
        return None
    if r == i + 1 and c == j and S['_line'] == 17:
        return 'yellow'
    if r == i and c == j and S['_line'] == 17:
        return 'blue'
    if r == S.get('p') and c == j - 1 and S['_line'] == 17:
        return 'green'
    return None


def _formula(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S['_line'] != 17:
        return '`f[i+1][j]` = 在前 `i+1` 个会议里至多参加 `j` 个的最大价值和'
    e = S['events']
    p = S['p']
    return (f'不选：`f[{i}][{j}]` = {S["f"][i][j]}　选：`f[{p}][{j - 1}] + {S["value"]}` = {S["f"][p][j - 1] + S["value"]}')


CONFIG = dict(
    num=1751, title='最多可以参加的会议数目 II', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='按结束时间排序 · 二分 + 二维 DP',
    tags=['灵神题单', '难度分 2041'],
    code='''
# 手写 max 更快
fmax = lambda a, b: b if b > a else a

class Solution:
    def maxValue(self, events: List[List[int]], k: int) -> int:
        # 特判 k=1 的情况可以更快
        if k == 1:
            return max(e[2] for e in events)

        events.sort(key=lambda e: e[1])  # 按照结束时间排序
        n = len(events)
        f = [[0] * (k + 1) for _ in range(n + 1)]
        for i, (start_day, _, value) in enumerate(events):
            p = bisect_left(events, start_day, hi=i, key=lambda e: e[1])  # hi=i 表示二分上界为 i（默认为 n）
            for j in range(1, k + 1):
                # 为什么是 p 不是 p+1：上面算的是 >= start_day，-1 后得到 < start_day，但由于还要 +1，抵消了
                f[i + 1][j] = fmax(f[i][j], f[p][j - 1] + value)
        return f[n][k]
''',
    call=f'Solution().maxValue({EV!r}, 2)',
    expect=7,
    skip=['for j in range', '# 为什么是'],
    views=[
        dict(type='text', fn=_ev_txt, size=26, h=70),
        dict(type='table', var='f', label='f[i+1][j]：前 i+1 个会议至多参加 j 个（黄 = 算，蓝 = 不选，绿 = 选）', h=330, cell=90,
             rows=lambda S: ['空'] + [f'{a}~{b}' for a, b, c in S.get('events', [])],
             cols=lambda S: [f'j={t}' for t in range(len(S['f'][0]))] if 'f' in S else [],
             color=_cell),
        dict(type='text', fn=_formula, size=28, h=80),
    ],
    watch=['i', 'start_day', 'value', 'p', 'j'],
    captions={
        'k == 1': '`k = {k}`：不等于 1，走 DP（若 `k = 1` 只能参会一次，直接取最大价值更快）',
        'events.sort': '按结束时间排序，这样「前面能接上的会议」一定是一个前缀',
        'n = len(events)': '`n = {n}` 个会议',
        'f = [[0]': '`f[i+1][j]` = 在 `events[0..i]` 中至多参加 `j` 个会议的最大价值和；第 0 行 = 没有会议 = 0',
        'for i, (start_day': lambda S, B, r: ('所有会议都考虑完了' if S.get('i') == B.get('i') and 'i' in B else f'考虑会议 `[{S.start_day}, {S.events[S.i][1]}]`，价值 {S.value}'),
        'p = bisect_left': '二分：结束时间 `< {start_day}` 的会议有 `{p}` 个（本题 ==相邻端点也不能相同==）→ 能接在前 `{p}` 个后面',
        'f[i + 1][j] = fmax': lambda S, B, r: f'`j={S.j}`：不参加 `f[{S.i}][{S.j}]` = {S.f[S.i][S.j]}；参加 `f[{S.p}][{S.j - 1}] + {S.value}` = {S.f[S.p][S.j - 1] + S.value} → `f[{S.i + 1}][{S.j}]` = =={S.f[S.i + 1][S.j]}==',
        'return f[n][k]': '答案 `f[{n}][{k}]` = =={ret}==',
    },
    cards=dict(
        one_liner='1235 的基础上多一维 j：至多参加 j 个会议',
        complexity='时间 `O(nk + n log n)`，空间 `O(nk)`',
        problem=['`events[i] = [开始, 结束, 价值]`，最多参加 `k` 个会议，同一时间只能参加一个',
                 '结束日也算占用：不能参加开始日 = 另一个的结束日的两个会议',
                 '示例：`events=[[1,2,4],[3,4,3],[2,3,1]], k=2` → `7`'],
        quote='和 1235 一样，按照结束时间排序。定义 f[i+1][j] 表示参加 events[0] 到 events[i] 中的至多 j 个会议，能得到的最大价值和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['不参加 `events[i]`：`f[i][j]`',
              '参加：二分找到最大的 `endDay < startDay_i` 的下标 `p`，转移 `f[p+1][j-1] + value`',
              '二分用 `bisect_left` 求 `>= start_day` 的位置，减 1 再加 1 刚好抵消，所以直接用 `p`'],
        summary=['时间 `O(nk + n log n)`，空间 `O(nk)`',
                 '易错：本题相邻端点不能相同，所以是 `endDay < startDay`，对应 `bisect_left`',
                 '`hi=i`：只在前 `i` 个会议里二分；`k=1` 直接特判',
                 '也可交换两维并滚动数组，空间降到 `O(n)`（题解留作练习）',
                 '前置：1235 规划兼职工作；同类：2054、2830'],
    ),
)
