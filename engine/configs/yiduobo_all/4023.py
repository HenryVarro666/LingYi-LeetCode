def _tbl(S, i, j, v):
    s, e = S.get('start'), S.get('end')
    if s is None or e is None or S.get('length') is None:
        return 'green' if v == 0 else None
    if (i, j) == (s, e):
        return 'yellow'
    if (i, j) in ((s + 1, e), (s, e - 1)):
        return 'blue'
    if (i, j) == (S.get('index'), S.get('index')):
        return 'green'
    return None


def _formula(S):
    if S.get('length') is None or 'end' not in S:
        return '`f[s][e]` / `g[s][e]`：处理完 `requests[s..e]`，电梯停在左端 / 右端的最小总惩罚'
    n, L = S['n'], S['length']
    return f'区间长 `{L}`，未处理 {n - L} 个；本次 `move_cost × {n - L + 1}`'


CONFIG = dict(
    num=4023, title='电梯请求 II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='区间 DP · 两个表 f / g',
    tags=['区间 DP'],
    code='''
class Solution(object):
    def elevatorRequests(self, n, start, requests):
        
        if start not in requests:
            requests.append(start)
        requests.sort()
        index = requests.index(start)

        n = len(requests)
        f = [[None] * n for _ in range(n)]
        g = [[None] * n for _ in range(n)]
        f[index][index] = 0
        g[index][index] = 0

        for length in range(2, n + 1):
            for start in range(n):
                end = start + length - 1
                if end >= n:
                    break
                
                if f[start + 1][end] is not None:
                    cost = f[start + 1][end] + (requests[start + 1] - requests[start]) * (n - length + 1)
                    if f[start][end] is None or f[start][end] > cost:
                        f[start][end] = cost
                if g[start + 1][end] is not None:
                    cost = g[start + 1][end] + (requests[end] - requests[start]) * (n - length + 1)
                    if f[start][end] is None or f[start][end] > cost:
                        f[start][end] = cost
                
                if f[start][end - 1] is not None:
                    cost = f[start][end - 1] + (requests[end] - requests[start]) * (n - length + 1)
                    if g[start][end] is None or g[start][end] > cost:
                        g[start][end] = cost
                if g[start][end - 1] is not None:
                    cost = g[start][end - 1] + (requests[end] - requests[end - 1]) * (n - length + 1)
                    if g[start][end] is None or g[start][end] > cost:
                        g[start][end] = cost

        res = None
        if f[0][-1] is not None and (res is None or res > f[0][-1]):
            res = f[0][-1]
        if g[0][-1] is not None and (res is None or res > g[0][-1]):
            res = g[0][-1]
        return res
''',
    call='Solution().elevatorRequests(10, 5, [0, 2, 9])',
    expect=22,
    skip=['for _ in range', 'if f[start][end] is None or', 'if g[start][end] is None or', 'is not None:', 'if end >= n', 'break', 'res is None or res >'],
    max_steps=110,
    views=[
        dict(type='array', var='requests', label='requests（排序后，含 start）', h=215, cell=80,
             pointers={'start': 'blue', 'end': 'pink', 'index': 'green'}),
        dict(type='text', fn=_formula, size=24, h=50),
        dict(type='table', var='f', label='f[s][e]：电梯停在左端 requests[s]', h=215, cell=60, color=_tbl,
             rows=lambda S: list(range(len(S['f']))), cols=lambda S: list(range(len(S['f'])))),
        dict(type='table', var='g', label='g[s][e]：电梯停在右端 requests[e]', h=215, cell=60, color=_tbl,
             rows=lambda S: list(range(len(S['g']))), cols=lambda S: list(range(len(S['g'])))),
    ],
    watch=[('length', 'length', 'yellow'), ('start', 'start', 'blue'), ('end', 'end', 'pink'), ('cost', 'cost', 'green')],
    captions={
        'if start not in requests': '起点 `start = {start}` 不在请求里：==先加进去==，它是区间 DP 的起点',
        'requests.sort()': '排序：`requests = {requests}`。电梯走过的楼层必是一段连续区间',
        'index = ': '起点在排序后的下标 `index = {index}`',
        'n = len(requests)': '`n` 被重新赋值为请求个数 `{n}`（楼层数 n 用不上了）',
        'f = [[None]': '`f[s][e]`：处理完 `s..e`，停在左端的最小惩罚；`None` = 到不了',
        'g = [[None]': '`g[s][e]`：同样的区间，停在右端',
        'f[index][index] = 0': '起点自己：区间长 1，惩罚 0（只剩起点已被处理）',
        'g[index][index] = 0': '`g[{index}][{index}] = 0`',
        'for length in range': lambda S, B, r: (f'==区间长度 `{S.length}`== 从小到大：先把小区间算好' if S.get('length') != B.get('length') else '区间长度枚举完毕'),
        'end = start + length - 1': lambda S, B, r: (f'区间 `[{S.start}, {S.end}]`，右端 `end = {S.end}` ≥ {S.n} 出界 → ==换下一个长度==' if S.end >= S.n else f'区间 `[{S.start}, {S.end}]`：长 {S.length}，右端 `end = {S.end}`'),
        'if end >= n': lambda S, B, r: (f'`end = {S.end} >= {S.n}`：区间出界，换下一个长度' if S.end >= S.n else f'`end = {S.end}` 没出界，继续'),
        'if f[start + 1][end] is not None': lambda S, B, r: f'`f[{S.start+1}][{S.end}]` = {S.f[S.start+1][S.end]}：' + ('有值，可以从它走过来' if S.f[S.start+1][S.end] is not None else '到不了，跳过'),
        'cost = f[start + 1][end]': '`cost = f[{start+1}][{end}] + ({requests[start+1]}−{requests[start]}) × ({n}−{length}+1)` = =={cost}==：从 `start+1` 走到 `start`',
        'f[start][end] = cost': '`f[{start}][{end}]` 更新为 =={cost}==',
        'if g[start + 1][end] is not None': lambda S, B, r: f'`g[{S.start+1}][{S.end}]` = {S.g[S.start+1][S.end]}：' + ('有值，从右端 end 走到左端 start' if S.g[S.start+1][S.end] is not None else '到不了，跳过'),
        'cost = g[start + 1][end]': '`cost = g[{start+1}][{end}] + ({requests[end]}−{requests[start]}) × ({n}−{length}+1)` = =={cost}==：从 `end` 走到 `start`',
        'if f[start][end - 1] is not None': lambda S, B, r: f'`f[{S.start}][{S.end-1}]` = {S.f[S.start][S.end-1]}：' + ('有值，从左端 start 走到右端 end' if S.f[S.start][S.end-1] is not None else '到不了，跳过'),
        'cost = f[start][end - 1]': '`cost = f[{start}][{end-1}] + ({requests[end]}−{requests[start]}) × ({n}−{length}+1)` = =={cost}==：从 `start` 走到 `end`',
        'if g[start][end - 1] is not None': lambda S, B, r: f'`g[{S.start}][{S.end-1}]` = {S.g[S.start][S.end-1]}：' + ('有值，从 end-1 走到 end' if S.g[S.start][S.end-1] is not None else '到不了，跳过'),
        'cost = g[start][end - 1]': '`cost = g[{start}][{end-1}] + ({requests[end]}−{requests[end-1]}) × ({n}−{length}+1)` = =={cost}==：从 `end-1` 走到 `end`',
        'g[start][end] = cost': '`g[{start}][{end}]` 更新为 =={cost}==',
        'res = None': '最后看整段区间 `[0, n-1]`：f 和 g 取较小',
        'res = f[0][-1]': '`res = f[0][-1]` = =={res}==',
        'res = g[0][-1]': '`res = g[0][-1]` = =={res}==',
        'return res': '处理完所有请求的最小总惩罚 =={res}==',
    },
    cards=dict(
        one_liner='区间里已处理 k 个，这一步移动让剩下的都多挨 1 秒罚',
        complexity='时间 `O(m^2)`，空间 `O(m^2)`',
        problem=['电梯在 `start`，每秒走一层；请求楼层同时发出，到达即处理，时刻 `t` 处理的请求罚 `t`',
                 '求处理完全部请求的==最小总惩罚==，楼层数 `n` 可达 `10^9`，请求最多 1500 个',
                 '示例：`n=10, start=5, requests=[0,2,9]` → `22`'],
        quote='电梯无论怎样移动，其经过的楼层必然是一个连续的区间，其对应到requests中也必然是连续的区间，因此在这里很自然想到一种动态规划的算法',
        quote_src='—— yiduobo 题解原文',
        idea=['先把 `requests` 排序，`f[s][e]` / `g[s][e]` 表示处理完 `s..e` 且停在左端 / 右端',
              '状态里没有当前时间，改算「这次行动的贡献」：`move_cost × (n − length + 1)`',
              '外层枚举区间长度，向两侧扩展一格'],
        summary=['时间 `O(m^2)`，空间 `O(m^2)`；`m` 是请求个数（含 start）',
                 '`start` 不在请求里要先加入再排序；代码里 `n`、`start` 被重新使用，注意别混',
                 '`None` 表示不可达；区间长度从小到大，保证前置状态已算好',
                 '原文为 Python 2 风格（`class Solution(object)`），无需修改即可在 Python 3 运行',
                 '对比灵神：灵神加哨兵 + 滚动数组，yiduobo 用 f/g 两张二维表按长度推'],
    ),
)
