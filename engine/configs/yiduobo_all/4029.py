def _fv(S):
    return [[('' if v is None else v) for v in row] for row in S['f']] if 'f' in S else [['']]


def _gv(S):
    return [[('' if v is None else v) for v in row] for row in S['g']] if 'g' in S else [['']]


def _rtxt(S):
    r = S.get('r')
    if not r:
        return '`requests = ' + str(S['requests']) + '`  （[到达时间, 楼层]），电梯起点 `' + str(S['start']) + '`'
    return '按楼层排序：' + '  '.join(f'`#{i}` 楼层 =={x}== 最晚 {t} 秒' for i, (x, t) in enumerate(r))


CONFIG = dict(
    num=4029, title='电梯请求 IV', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='区间 DP · 折线越折越往内', tags=[],
    code='''
class Solution(object):
    def elevatorRequests(self, n, start, requests):
        
        last = {}
        for t, x in requests:
            last[x] = max(t, last.get(x, 0))
        
        if start in last and last[start] == 0:
            last.pop(start)
        
        if not last:
            return 0

        r = sorted(last.items())
        m = len(r)

        f = [[None] * m for _ in range(m)]
        g = [[None] * m for _ in range(m)]
        f[0][m - 1] = max(r[0][1], abs(start - r[0][0]))
        g[0][m - 1] = max(r[-1][1], abs(start - r[-1][0]))

        for length in range(m, 1, -1):
            for start in range(m):
                end = start + length - 1
                if end >= m:
                    break
                
                if f[start][end]:
                    f_from_left = max(r[start + 1][1], f[start][end] + r[start + 1][0] - r[start][0])
                    if f[start + 1][end] is None or f[start + 1][end] > f_from_left:
                        f[start + 1][end] = f_from_left

                    g_from_left = max(r[end][1], f[start][end] + r[end][0] - r[start][0])
                    if g[start + 1][end] is None or g[start + 1][end] > g_from_left:
                        g[start + 1][end] = g_from_left
                
                if g[start][end]:
                    f_from_right = max(r[start][1], g[start][end] + r[end][0] - r[start][0])
                    if f[start][end - 1] is None or f[start][end - 1] > f_from_right:
                        f[start][end - 1] = f_from_right
                
                    g_from_right = max(r[end - 1][1], g[start][end] + r[end][0] - r[end - 1][0])
                    if g[start][end - 1] is None or g[start][end - 1] > g_from_right:
                        g[start][end - 1] = g_from_right

        res = None
        for x in range(m):
            if f[x][x] is not None and (res is None or res > f[x][x]):
                res = f[x][x]
            if g[x][x] is not None and (res is None or res > g[x][x]):
                res = g[x][x]
        return res
''',
    call='Solution().elevatorRequests(10, 4, [[1, 5], [6, 2], [3, 8]])',
    expect=10,
    views=[
        dict(type='text', fn=_rtxt, size=24),
        dict(type='table', var=_fv, label='f[start][end]：折线还要走 start..end，start 的请求已满足', h=230, cell=64,
             cursors=[('start', 'end', 'yellow', '')],
             rows=lambda S: list(range(len(S['f']))) if 'f' in S else [0], cols=lambda S: list(range(len(S['f']))) if 'f' in S else [0]),
        dict(type='table', var=_gv, label='g[start][end]：折线还要走 start..end，end 的请求已满足', h=230, cell=64,
             cursors=[('start', 'end', 'yellow', '')],
             rows=lambda S: list(range(len(S['g']))) if 'g' in S else [0], cols=lambda S: list(range(len(S['g']))) if 'g' in S else [0]),
    ],
    watch=['length', 'start', 'end', ('res', 'res', 'green')],
    skip=['m = len(r)', 'f = [[None]', 'g = [[None]', 'end = start + length - 1', ' is None or ', 'is not None and', 'if end >= m', 'for t, x in requests'],
    max_steps=56,
    captions={
        'last[x] = max': '同一层只留最晚的请求：`last[{x}] = {last[x]}`（晚的一到，早的也一起满足）',
        'if start in last and last[start] == 0': '电梯起点 `{start}` 若有请求且 0 秒就到 → 一开始就完成，不用管它：{"==删掉==" if (start in last and last[start]==0) else "没有这种情况"}',
        'if not last': '没有剩余请求就不用动，返回 0；这里还有 `{len(last)}` 个楼层',
        'r = sorted': '按楼层从小到大排序：`{r}`，每项是 `(楼层, 最晚到达时间)`',
        'f[0][m - 1] = max': '第一步必先走到最低层 `r[0]`：耗时 `max(到达时间 {r[0][1]}, 路程 {abs(start - r[0][0])})` = =={f[0][m-1]}==，记入 `f[0][m-1]`',
        'g[0][m - 1] = max': '或者先走到最高层 `r[-1]`：耗时 `max({r[-1][1]}, {abs(start - r[-1][0])})` = =={g[0][m-1]}==，记入 `g[0][m-1]`',
        'for length in range': '折线管的范围长度 `length = {length}`：越折越往内，范围只会变短',
        'for start in range': '枚举范围左端点 `start = {start}`',
        'if end >= m': lambda S, B, r: f'`end = {S.end}`' + (' 超出 `m-1`，这个长度的范围已枚举完 → 退出内层循环' if S.end >= len(S.r) else ' 在范围内，继续'),
        'if f[start][end]:': lambda S, B, ret: f'`f[{S.start}][{S.end}] = {S.f[S.start][S.end]}`：' + ('有值 → 现在在最低端 `start`，可以往右折' if S.f[S.start][S.end] else '还没有这个状态，跳过'),
        'f_from_left =': '从 start 走到 start+1：`max(请求到达 {r[start+1][1]}, {f[start][end]} + 路程 {r[start+1][0]-r[start][0]})` = =={f_from_left}==（更小才更新）',
        'f[start + 1][end] = f_from_left': '`f[{start+1}][{end}]` 取更小的 → =={f[start+1][end]}==',
        'g_from_left =': '或者直接冲到 end：`max(请求到达 {r[end][1]}, {f[start][end]} + 路程 {r[end][0]-r[start][0]})` = =={g_from_left}==（更小才更新）',
        'g[start + 1][end] = g_from_left': '`g[{start+1}][{end}]` 取更小的 → =={g[start+1][end]}==',
        'if g[start][end]:': lambda S, B, ret: f'`g[{S.start}][{S.end}] = {S.g[S.start][S.end]}`：' + ('有值 → 现在在最高端 `end`，可以往左折' if S.g[S.start][S.end] else '还没有这个状态，跳过'),
        'f_from_right =': '直接冲到 start：`max(请求到达 {r[start][1]}, {g[start][end]} + 路程 {r[end][0]-r[start][0]})` = =={f_from_right}==（更小才更新）',
        'f[start][end - 1] = f_from_right': '`f[{start}][{end-1}]` 取更小的 → =={f[start][end-1]}==',
        'g_from_right =': '从 end 走到 end-1：`max(请求到达 {r[end-1][1]}, {g[start][end]} + 路程 {r[end][0]-r[end-1][0]})` = =={g_from_right}==（更小才更新）',
        'g[start][end - 1] = g_from_right': '`g[{start}][{end-1}]` 取更小的 → =={g[start][end-1]}==',
        'res = None': '折线最后收缩成单个楼层：枚举 `f[x][x]` 和 `g[x][x]` 取最小',
        'res = f[x][x]': '`res` 更新为 `f[{x}][{x}] = {res}`',
        'res = g[x][x]': '`res` 更新为 `g[{x}][{x}] = {res}`',
        'return res': '处理完所有请求最短 `{res}` 秒',
    },
    cards=dict(
        one_liner='电梯的路线是越折越往内的折线，用区间 DP 一层层缩',
        complexity='时间 `O(m^2)`，空间 `O(m^2)`，m 为不同楼层的请求数',
        problem=['`n` 层楼，电梯从 `start` 出发，每秒上、下一层或不动',
                 '请求 `[到达时间, 楼层]`：到达后电梯只要到过该层就算完成',
                 '求完成所有请求的最短时间；本视频：`n=10, start=4`，3 个请求，答案 `10`'],
        quote='电梯必然是来回来回地走折线，除了首次移动之外，其他的折线必然被包含在上一轮的折线之内。',
        quote_src='—— yiduobo 题解原文',
        idea=['同一楼层只留最晚的请求，按楼层排序，第一步一定先到最低或最高层',
              '`f[s][e]`：还要走 s..e，且 s 的请求已满足；`g[s][e]`：end 的请求已满足',
              '从 s 往右一步缩到 s+1，或直接冲到 e 折返；耗时取 `max(请求到达, 到达路程)`'],
        summary=['时间 `O(m^2)`，空间 `O(m^2)`',
                 '关键结论：折线只会向内收缩，所以区间 `[start, end]` 只会变短',
                 '等待用 `max(请求到达时间, 走到的时间)` 表示：早到就等',
                 '原文用 `if f[start][end]:` 判断状态是否存在，耗时为 0 时不会成立',
                 '代码里 `start` 先是起点楼层，后来被循环变量覆盖；原文如此'],
    ),
)
