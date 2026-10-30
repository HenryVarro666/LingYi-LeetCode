_POS = {0: (0.14, 0.5), 1: (0.45, 0.0), 3: (0.45, 1.0), 2: (0.82, 0.0)}
_EDGES = [(0, 1, 10), (1, 2, 15), (0, 3, 10)]
_VALUES = [0, 32, 10, 43]


def _graph(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 2), '绿 = 价值已算入（在 used 中）　蓝圈 = 当前点　边上 = 耗时', 22, T['muted'], bold=True)
    W, Hh = x1 - x0 - 120, y1 - y0 - 200
    pt = {k: (x0 + 60 + p[0] * W, y0 + 75 + p[1] * Hh) for k, p in _POS.items()}
    inn = S.get('_inner', {})
    cur = inn.get('now')
    used = inn.get('used')
    if used is None:
        used = S.get('used')
    nxt = inn.get('next')
    for a, b, t in _EDGES:
        (ax, ay), (bx, by) = pt[a], pt[b]
        hot = cur in (a, b) and nxt in (a, b) and nxt != cur
        cv.line([(ax, ay), (bx, by)], T['yellow'] if hot else T['dim'], 5 if hot else 3)
        mx, my = (ax + bx) / 2, (ay + by) / 2
        cv.rect((mx - 24, my - 16, mx + 24, my + 16), fill=T['panel'], r=8)
        cv.text((mx, my), t, 24, T['text'], anchor='mm', bold=True)
    for k, (px, py) in pt.items():
        on = used is not None and k in used
        cv.d.ellipse((px - 34, py - 34, px + 34, py + 34), fill=T['green'] if on else T['panel2'],
                     outline=T['blue'] if k == cur else (T['green'] if on else T['border']), width=6 if k == cur else 3)
        cv.text((px, py), k, 34, T['bg'] if on else T['text'], anchor='mm', bold=True)
        cv.text((px, py + 52), f'价值 {_VALUES[k]}', 22, T['muted'], anchor='mm')


def _info(S):
    inn = S.get('_inner', {})
    if 't' in inn and 'now' in inn:
        return (f"当前点 `{inn['now']}`，已用时间 ==`{inn['t']}`== / {S['maxTime']}，"
                f"路径价值 ==`{inn['v']}`==，最佳 `{S.get('self.res')}`")
    return '度 ≤ 4、最多 10 条边：直接 dfs，访问过的点不再加价值'


CONFIG = dict(
    num=2065, title='最大化一张图中的路径价值', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='dfs 暴搜（used 集合去重价值）',
    tags=['灵神题单·图论算法', '难度分 2178'],
    code='''
class Solution(object):
    def maximalPathQuality(self, values, edges, maxTime):

        g = {}

        for x, y, time in edges:
            if x not in g:
                g[x] = {}
            g[x][y] = time

            if y not in g:
                g[y] = {}
            g[y][x] = time

        self.res = 0
        used = set([0])

        def dfs(now, used, v, t):
            if now == 0:
                self.res = max(self.res, v)
            
            for next, time in g.get(now, {}).items():
                if time + t <= maxTime:
                    if next in used:
                        dfs(next, used, v, t + time)
                    else:
                        used.add(next)
                        dfs(next, used, v + values[next], t + time)
                        used.remove(next)

        dfs(0, used, values[0], 0)
        return self.res
''',
    call='Solution().maximalPathQuality([0, 32, 10, 43], [[0, 1, 10], [1, 2, 15], [0, 3, 10]], 40)',
    expect=75,
    views=[
        dict(type='custom', draw=_graph, h=460),
        dict(type='text', fn=_info, size=24, h=60),
        dict(type='calls', h=170),
    ],
    watch=[('res', lambda S: S.get('self.res'), 'green'), ('now', lambda S: S['_inner'].get('now'), 'blue'),
           ('used', lambda S: S['_inner'].get('used', S.get('used')), 'cyan')],
    skip=['g = {}', 'if x not in g', 'if y not in g', 'g[x] = {}', 'g[y] = {}', 'g[x][y] = time', 'g[y][x] = time',
          'for x, y, time in edges', 'for next, time in g.get', 'self.res = 0'],
    captions={
        'used = set': '`used` 记录价值已经算过的点，一开始只有起点 `0`',
        'dfs(0, used, values[0], 0)': '从 0 出发：价值 `{values[0]}`，时间 `0`',
        'if now == 0': lambda S, B, r: (f'回到 0，路径合法：用价值 `{S.v}` 更新 `res`' if S.now == 0
                                        else f'在 `{S.now}`，还没回到 0，不结算'),
        'self.res = max': '`res = max({B.self.res}, {v}) = {self.res}`；回到 0 后还能继续走',
        'if time + t <= maxTime': lambda S, B, r: (
            f'走到 `{S.next}`：`{S.t}+{S.time}` = {S.t + S.time}'
            + (f' <= {S.maxTime}，走得动' if S.time + S.t <= S.maxTime else f' > {S.maxTime}，超时，换一条边')),
        'if next in used': lambda S, B, r: (f'`{S.next}` 在 `used` 中：价值已算过' if S.next in S.used
                                            else f'`{S.next}` 第一次到：价值要加'),
        'dfs(next, used, v, t + time)': '再次经过：价值 `v` 不变，只加时间 `+{time}`',
        'used.add': '`used.add({next})`：标记它的价值已算入',
        'dfs(next, used, v + values[next]': '第一次经过：价值 `+{values[next]}`，时间 `+{time}`，递归',
        'used.remove': '回溯：把 `{next}` 移出 `used`，别的路线再来时仍算第一次',
        'return self.res': '全部搜完，最大价值 =={ret}==',
    },
    max_steps=64,
    cards=dict(
        one_liner='边最多 10 条、度最多 4，状态不过 4^10，直接 dfs',
        complexity='时间 `O(4^k)`，`k = maxTime / min(time) ≤ 10`',
        problem=['无向图每点有价值；从 `0` 出发回到 `0`，总时间不超过 `maxTime`',
                 '价值 = 经过的不同点的价值和，点可以重复走',
                 '示例（改小）：`values=[0,32,10,43]`，`maxTime=40` → `75`'],
        quote='题目中给出了一个条件，就是10 <= time[j], maxTime <= 100，也就是说从0出发走一圈再回到0，经过的边的条数最多为10条。',
        quote_src='—— yiduobo 题解',
        idea=['一开始担心要用桥、连通分量缩点，很复杂',
              '注意到边数 ≤ 10、度 ≤ 4 → 状态最多 4^10，约一百万，扛得住',
              '做法就是常规 dfs：访问过的点可再访问，但价值不能再加'],
        result='最大价值 75（走 0→1→0→3→0）',
        summary=['时间 `O(4^k)`，空间 `O(n+m+k)`',
                 '`now == 0` 时更新 `res`，但==不要停==，回到 0 还能继续走',
                 '`used.add` 与 `used.remove` 要成对，否则别的路线会少算价值',
                 '原文已是 Python 3 可运行写法，未作修改'],
    ),
)
