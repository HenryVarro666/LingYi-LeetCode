EV = [[1, 2, 4], [3, 4, 3], [2, 3, 1]]


def _fmt(v):
    return '·' if v is None else str(v)


def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or S.get('_line', 0) < 20:
        return None
    if S['_line'] in (21, 22, 23):
        if r == i and c == j:
            return 'yellow'
        s = S.get('s')
        if s is not None and r == s - 1 and c == j - 1:
            return 'green'
    return None


def _ev_txt(S):
    e = S.get('sorted_events')
    if e is None:
        return ''
    p = S.get('p', -1)
    m = S.get('mapping_dict', {})
    return '按结束时间排序（时间已压缩成序号）：' + '  '.join(
        (f'==[{m.get(a, a)},{m.get(b, b)}]:{c}==' if k == p else f'[{m.get(a, a)},{m.get(b, b)}]:{c}') for k, (a, b, c) in enumerate(e))


def _formula(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('s') is None or S['_line'] not in (21, 22, 23):
        return '`f[i][j]` = 到时刻 `i` 为止参加 `j` 个会议的最大价值；`·` 表示不可能'
    s = S['s']
    pv = S['f'][s - 1][j - 1]
    return f'`f[{s - 1}][{j - 1}] + {S["sorted_events"][S["p"]][2]}` = {pv + S["sorted_events"][S["p"]][2]}（接在 `f[s-1]` 后面）'


CONFIG = dict(
    num=1751, title='最多可以参加的会议数目 II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='时间离散化 · 按时刻 DP + 单调指针',
    tags=['灵神题单', '难度分 2041'],
    code='''
class Solution(object):
    def maxValue(self, events, k):

        date_set = set()
        for s, e, v in events:
            date_set.add(s)
            date_set.add(e)
        
        mapping_dict = {}
        for index, date in enumerate(sorted(list(date_set))):
            mapping_dict[date] = index + 1
        
        n = len(mapping_dict) + 1
        f = [[None] * (k + 1) for _ in range(n)]
        f[0][0] = 0
        sorted_events = sorted(events, key=lambda d:d[1])
        p = 0
        for i in range(1, n):
            for j in range(k + 1):
                if f[i - 1][j] is not None:
                    f[i][j] = f[i - 1][j]
            
            while p < len(sorted_events) and mapping_dict[sorted_events[p][1]] == i:
                s = mapping_dict[sorted_events[p][0]]
                for j in range(1, k + 1):
                    if f[s - 1][j - 1] is not None:
                        if f[i][j] is None or f[i][j] < f[s - 1][j - 1] + sorted_events[p][2]:
                            f[i][j] = f[s - 1][j - 1] + sorted_events[p][2]
                
                p += 1
        
        return max(f[-1])
''',
    call=f'Solution().maxValue({EV!r}, 2)',
    expect=7,
    max_steps=90,
    skip=['date_set.add', 'for s, e, v in events', 'for index, date in enumerate', 'mapping_dict[date] =', 'for j in range', 'f[i][j] = f[i - 1][j]'],
    views=[
        dict(type='text', fn=_ev_txt, size=24, h=70),
        dict(type='table', var='f', label='f[i][j]：到时刻 i 为止参加 j 个会议的最大价值（黄 = 更新，绿 = 来源）', h=330, cell=90,
             values=True,
             rows=lambda S: [f't={t}' for t in range(len(S['f']))] if 'f' in S else [],
             cols=lambda S: [f'j={t}' for t in range(len(S['f'][0]))] if 'f' in S else [],
             color=_cell),
        dict(type='text', fn=_formula, size=28, h=80),
    ],
    watch=['i', ('s', 's if _line >= 21 else "-"', 'pink'), ('p', 'p', 'blue'), ('j', 'j if _line >= 20 else "-"')],
    captions={
        'date_set = set()': '先收集所有出现过的开始 / 结束日期',
        'mapping_dict = {}': '把日期压缩成 `1..` 的序号：只关心相对大小，时间点最多 `2n` 个',
        'n = len(mapping_dict)': lambda S, B, r: f'`mapping_dict` = {S.mapping_dict}；`n = {S.n}`：时刻 `0..{S.n - 1}`（0 = 还没开始）',
        'f = [[None]': '`f[i][j]`：到时刻 `i` 为止参加 `j` 个会议的最大价值；`None` = 不可能达到',
        'f[0][0] = 0': '边界：时刻 0 参加 0 个会议，价值 0',
        'sorted_events = sorted': '按结束时间排序：处理时刻 `i` 时，右端点为 `i` 的会议依次排在 `p` 后面',
        'p = 0': '`p` 指向下一个还没处理的会议，只会往后走 → 均摊 O(1)',
        'for i in range': lambda S, B, r: ('所有时刻都算完了' if S.i == B.get('i') else f'算时刻 `{S.i}`'),
        'if f[i - 1][j] is not None': lambda S, B, r: (f'`j={S.j}`：时刻 {S.i - 1} 参加 {S.j} 个是可行的 → 时刻 {S.i} 先==继承==这个值 `{S.f[S.i - 1][S.j]}`（`f[i][j] = f[i-1][j]`）' if S.f[S.i - 1][S.j] is not None
                                                      else f'`j={S.j}`：`f[{S.i - 1}][{S.j}]` 是 None（不可能），不继承'),
        'while p < len': lambda S, B, r: (f'`sorted_events[{S.p}]` 在时刻 {S.i} 结束 → 枚举它' if S.p < len(S.sorted_events) and S.mapping_dict[S.sorted_events[S.p][1]] == S.i
                                          else f'时刻 {S.i} 结束的会议都处理完了'),
        's = mapping_dict': '会议开始于时刻 `s = {s}`：选它就只能接在 `f[{s - 1}]` 后面（开始日不能等于别人的结束日）',
        'if f[s - 1][j - 1] is not None': lambda S, B, r: (f'`j={S.j}`：`f[{S.s - 1}][{S.j - 1}] = {S.f[S.s - 1][S.j - 1]}` 可行，可以再加一个会议' if S.f[S.s - 1][S.j - 1] is not None
                                                           else f'`j={S.j}`：`f[{S.s - 1}][{S.j - 1}]` 不可能，这个会议当第 {S.j} 个不行'),
        'if f[i][j] is None or': lambda S, B, r: f'比较：现有 `f[{S.i}][{S.j}]` = {S.f[S.i][S.j]}，选这个会议 = `{S.f[S.s - 1][S.j - 1]} + {S.sorted_events[S.p][2]}` = {S.f[S.s - 1][S.j - 1] + S.sorted_events[S.p][2]}',
        'f[i][j] = f[s - 1][j - 1] +': '`f[{i}][{j}]` 更新为 =={f[i][j]}==',
        'p += 1': '这个会议用完了，`p` → {p}',
        'return max(f[-1])': '不一定要参加满 `k` 个，所以取最后一行的最大值 `max(f[-1])` = =={ret}==',
    },
    cards=dict(
        one_liner='时间离散化后按时刻 DP；答案取最后一行的最大值',
        complexity='时间 `O(n log n + nk)`，空间 `O(nk)`',
        problem=['`events[i] = [开始, 结束, 价值]`，最多参加 `k` 个会议，同一时间只能参加一个',
                 '不能同时参加开始日等于另一个结束日的两个会议',
                 '示例：`events=[[1,2,4],[3,4,3],[2,3,1]], k=2` → `7`'],
        quote='会议的时刻只需要关心相对的大小关系，而具体的时间节点是无所谓的，因此可以按照顺序从小到大排序，然后建立起时间节点到顺序的映射。',
        quote_src='—— yiduobo 题解原文',
        idea=['时间最大 `10^9`，先压缩成 `1..2n` 的序号，`f[i]` 才开得下',
              '`f[i][j]` 先继承 `f[i-1][j]`（时刻 i 不参加），再枚举结束于 `i` 的会议：`f[s-1][j-1] + value`',
              '会议按结束时间排序，指针 `p` 单调后移，每个会议只处理一次'],
        summary=['时间 `O(n log n + nk)`，空间 `O(nk)`（压缩后时刻最多 `2n`，表格更大）',
                 '易错：用 `s - 1` 而不是 `s`，因为结束日与开始日相同也算冲突',
                 '`None` 表示「恰好参加 j 个」不可能；所以最后是 `max(f[-1])`，不是 `f[-1][-1]`',
                 '原文没有 Python 2 特有写法，代码未改动',
                 '对比灵神：灵神定义「至多 j 个」+ 二分找上一个会议；yiduobo 定义「恰好 j 个」+ 离散化'],
    ),
)
