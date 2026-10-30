CONFIG = dict(
    num=332, title='重新安排行程', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='欧拉路径 · DFS 后序倒着收集',
    tags=['欧拉路径'],
    code='''
class Solution(object):
    def findItinerary(self, tickets):

        g = {}
        for x, y in tickets:
            if x not in g:
                g[x] = {}
            if y not in g:
                g[y] = {}
            g[x][y] = g[x].get(y, 0) + 1

        res = []
        self.dfs('JFK', g, res)
        res.reverse()
        return res

    def dfs(self, x, g, res):
        for y in sorted(g[x].keys()):
            if g[x].get(y, 0) > 0:
                g[x][y] -= 1
                self.dfs(y, g, res)
        res.append(x)
''',
    call="Solution().findItinerary([['JFK','SFO'],['JFK','ATL'],['SFO','ATL'],['ATL','JFK'],['ATL','SFO']])",
    expect=['JFK', 'ATL', 'JFK', 'SFO', 'ATL', 'SFO'],
    views=[
        dict(type='map', var='g', label='g（出边表：起点 → {终点: 剩余张数}）', fmt=lambda k, v: f"{k}: " + ', '.join(f"{a}×{b}" for a, b in sorted(v.items())) if isinstance(v, dict) else str(v), h=150, font=28),
        dict(type='calls', h=300, hide=('g', 'res')),
        dict(type='array', var='res', label='res（后序收集：先收集的是终点，最后要反转）', cell=100, h=170),
    ],
    watch=[('x', lambda S: S['_inner'].get('x', '-'), 'blue'), ('y', lambda S: S['_inner'].get('y', '-'), 'pink')],
    skip=['g[x] = {}', 'g[y] = {}', 'if x not in g', 'if y not in g', 'g[x][y] = g[x].get'],
    max_steps=90,
    captions={
        'g = {}': '先建图：`g[x][y]` = 从 `x` 到 `y` 的机票张数（同一路线可能有多张）',
        'for x, y in tickets': '逐张机票加进图里',
        'res = []': '`res` 用来收集后序遍历的结果',
        "self.dfs('JFK'": '从 `JFK` 出发做 DFS：==每走一条边就删掉一张票==，走不下去的点就是当前路径的终点',
        'res.reverse()': '`res` 里是终点在前的顺序 → 反转就是正确行程：`{res}`',
        'return res': '行程：`{res}`',
        'for y in sorted': lambda S, B, r: ((f"`{S._inner['x']}` 的目的地先按字典序排好：`{sorted(S.g[S._inner['x']].keys())}`，先试 `{S._inner['y']}`（保证字典序最小）"
                                              if 'y' not in B._inner else
                                              (f"`{S._inner['x']}` 的目的地都试过了 → 退出循环" if S._inner['y'] == B._inner['y']
                                               else f"回溯回来，`{S._inner['x']}` 的下一个目的地：`{S._inner['y']}`"))),
        'if g[x].get(y, 0) > 0': lambda S, B, r: (f"`{S._inner['x']} → {S._inner['y']}` 还剩 `{S.g[S._inner['x']][S._inner['y']]}` 张票 → 能走"
                                                    if S.g[S._inner['x']].get(S._inner['y'], 0) > 0 else f"`{S._inner['x']} → {S._inner['y']}` 票已用完 → 跳过"),
        'g[x][y] -= 1': '用掉一张 `{x} → {y}` 的票，剩 `{g[x][y]}` 张，再从 `{y}` 继续往下走',
        'self.dfs(y, g, res)': '递归进入 `{y}`',
        'res.append(x)': '`{x}` 的出边全部走完（无路可走）→ 它是当前路径的终点，==后序加入 res==：`{res}`',
    },
    cards=dict(
        one_liner='DFS 走到无路可走的点最先收集，最后整体反转',
        complexity='时间 `O(E log E)`，空间 `O(E)`',
        problem=['给定若干机票 `[from, to]`，必须从 `JFK` 出发，用完所有机票各一次',
                 '多个答案时，返回字典序最小的行程',
                 '本视频：5 张机票 → `JFK ATL JFK SFO ATL SFO`'],
        quote='第一个开始回溯的点必然是路径的终点。……由于题目要求字典序最小，因此在dfs时需要先对边进行排序。',
        quote_src='—— yiduobo 题解原文',
        idea=['这是欧拉路径问题：每张票（边）恰好用一次',
              'DFS 时每走一条边就删一张票；==第一个走投无路的点必是终点==，后序把它放进 `res`',
              '回溯时接着收集前面的点，直到起点；整个 `res` 反转就是行程',
              '边按字典序先后尝试，保证字典序最小'],
        summary=['时间 `O(E log E)`（每个点排序），空间 `O(E)`',
                 '关键：==后序== `res.append(x)`，最后 `reverse`',
                 '`g[x][y]` 记录同一路线的票数，用完才不会再走',
                 '题目保证有解，所以不会出现用不完票的情况'],
    ),
)
