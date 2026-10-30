STR = [3, 4]
K = 1


def _sub(S):
    """锁 × 位置 的费用矩阵（取自 cost 的左下块）"""
    if 'cost' not in S or 'n' not in S:
        return None
    n = S['n']
    return [[S['cost'][i][j] for j in range(n, 2 * n)] for i in range(n)]


def _used(S, i, j, v):
    """锁 i 已经（暂定）放在位置 j：反向边有流量"""
    n = S['n']
    return 'green' if S['c'][n + j][i] > 0 else None


def _nodes(S):
    n = S['n']
    return [f'锁{i}' for i in range(n)] + [f'位{j + 1}' for j in range(n)] + ['s', 't']


def _flowtxt(S):
    if 'res' not in S:
        return ''
    n = S['n']
    pairs = [f'锁{i}→位{j + 1}' for i in range(n) for j in range(n) if S['c'][n + j][i] > 0]
    return f'当前分配：{"  ".join(pairs) if pairs else "（空）"}　累计费用 =={S["res"]}=='


def _dis_fmt(S, B, ret):
    return ''


CONFIG = dict(
    num=3385, title='破解锁的最少时间 II', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='最小费用最大流（锁与位置的最优匹配）',
    tags=['灵神题单·图论算法', '难度分 3376'],
    code='''
class Solution(object):
    def findMinimumTime(self, strength, K):
        
        n = len(strength)
        s = n + n
        t = n + n + 1

        c = [[0] * (t + 1) for _ in range(t + 1)]
        cost = [[0] * (t + 1) for _ in range(t + 1)]

        for i in range(n):
            c[s][i] = 1
        
        for j in range(n, n + n):
            c[j][t] = 1
        
        for i in range(n):
            for j in range(n, n + n):
                c[i][j] = 1
                cost[i][j] = (strength[i] - 1) // (1 + K * (j - n)) + 1
                cost[j][i] = -cost[i][j]
        
        res = 0
        while True:
            dis = [None] * (t + 1)
            prev = [None] * (t + 1)
            used = set([s])
            dis[s] = 0
            now = s
            while t not in used:
                min_dis = None
                nxt = None
                for index in range(t + 1):
                    if c[now][index] > 0 and (dis[index] is None or dis[index] > dis[now] + cost[now][index]):
                        dis[index] = dis[now] + cost[now][index]
                        prev[index] = now
                        if index in used:
                            used.remove(index)
                    if index not in used and dis[index] is not None and (min_dis is None or min_dis > dis[index]):
                        nxt = index
                        min_dis = dis[index]

                if min_dis is None:
                    return res
                
                used.add(nxt)
                now = nxt

            res += dis[t]
            now = t
            while now != s:
                c[prev[now]][now] -= 1
                c[now][prev[now]] += 1
                now = prev[now]
''',
    call=f'Solution().findMinimumTime({STR}, {K})',
    expect=5,
    skip=['n = len', 's = n + n', 't = n + n + 1', 'c = [[0]', 'cost = [[0]', 'c[s][i] = 1', 'c[j][t] = 1',
          'c[i][j] = 1', 'cost[j][i] = -', 'min_dis = None', 'nxt = None', 'for index in range',
          'prev[index] = now', 'if index in used:', 'used.remove', 'min_dis = dis[index]', 'nxt = index',
          'for i in range(n)', 'for j in range(n, n + n)', 'c[prev[now]][now] -= 1', 'now = prev[now]',
          'dis = [None]', 'prev = [None]', 'used = set', 'dis[s] = 0', 'now = s', 'now = t',
          'if c[now][index] > 0', 'now = nxt', 'while t not in used', 'if min_dis is None', 'while now != s', 'if index not in used and dis'],
    max_steps=110,
    views=[
        dict(type='grid', var=_sub, label='cost[锁][位置] = 等待分钟（绿 = 暂定分配）；strength = [3,4]', cell=84, h=300,
             rows=lambda S: [f'锁{i}' for i in range(S['n'])] if 'n' in S else None,
             cols=lambda S: [f'位{j + 1}' for j in range(S['n'])] if 'n' in S else None,
             color=_used),
        dict(type='array', var='dis', label='dis[点]（0,1 = 锁；2,3 = 位置；4 = s；5 = t；蓝 = now，绿 = 已确定）', cell=84, h=190,
             color=lambda S, i, v: 'blue' if i == S.get('now') else ('green' if i in S.get('used', ()) else None)),
        dict(type='array', var='prev', label='prev[点]：最短路上的前驱', cell=84, h=170),
        dict(type='text', fn=_flowtxt, h=60),
    ],
    watch=[('res', 'res', 'green'), ('now', 'now', 'blue'), 'used'],
    captions={
        'dis[index] = dis[now]': lambda S, B, r: (f'从点 `{S.now}` 经边 `{S.now}→{S.index}`（费用 `{S.cost[S.now][S.index]}`）松弛：`dis[{S.index}] = {S.dis[S.index]}`，前驱 `{S.now}`'
                                                   + ('（==负费用边：撤销之前的分配==）' if S.cost[S.now][S.index] < 0 else '')),
        'while t not in used': lambda S, B, r: ('汇点 `t` 还没定下最短路，继续取 `dis` 最小的点' if S.t not in S.used
                                                 else '`t` 的最短距离确定，这条增广路就是最便宜的'),
        'used.add(nxt)': '选 `dis` 最小的未确定点 `{nxt}`（`dis = {dis[nxt]}`）标为已确定，下一步从它出发松弛',
        'if min_dis is None': lambda S, B, r: (f'`min_dis = {S.min_dis}`：还有待确定的点 → 继续' if S.min_dis is not None
                                                else f'没有任何点可扩展 → 流已经最大，返回总费用 `{S.res}`'),
        'cost[i][j] = (': '锁 `{i}`（`strength = {strength[i]}`）放在位置 `{j - n + 1}`：`({strength[i]}-1)//(1+{K}*{j - n}) + 1` = ==`{cost[i][j]}`==，反向边取负',
        'return res': '每把锁都分到位置，最小总时间 ==`{res}`==',
        'res += dis[t]': '沿最便宜的增广路送 1 单位流，费用 `{dis[t]}`：`res = {res}`',
        'c[now][prev[now]] += 1': '回溯路径：边 `{prev[now]}→{now}` 容量 −1，反向边 `{now}→{prev[now]}` +1（==反向边以后可以“退回”这次分配==）',
        'res = 0': '`res` 累计总等待时间',
        'while True': '开始新一轮：找一条费用最小的增广路',
    },
    cards=dict(
        one_liner='把“第几个开哪把锁”当作分配问题，用费用流求最小总时间',
        complexity='时间约 `O(n^2)` 条边 × `n` 次增广，空间 `O(n^2)`',
        problem=['`strength[i]` 是开第 `i` 把锁所需的能量，要把 `n` 把锁都打开',
                 '剑的能量每分钟增加 `X`，`X` 初始为 1；开一把锁后能量归零，`X` 增加 `K`',
                 '求打开所有锁的最少分钟数（本题 `K` 固定为 1）',
                 '本视频：`strength = [3,4]`，`K = 1` → `5`'],
        quote='如果以全排列中的位置来看待第几个开的锁的话，本题就可以视为有n把锁和n个位置，需要将这些锁分配到这些位置上',
        quote_src='—— yiduobo 题解原文',
        idea=['第 `j` 个开的锁，`X = (j-1)·K + 1`，开第 `i` 把锁要 `(strength[i]-1)//X + 1` 分钟',
              '锁和位置各 `n` 个，边的费用就是上面的等待时间 → 二分图最优匹配',
              '建图：源点→锁（容量 1），锁→位置（容量 1，费用=等待时间），位置→汇点；跑最小费用最大流'],
        summary=['状压 DP 的 `2^n` 对 `n=80` 不可行，最优匹配把它变成多项式',
                 '本写法每轮用类 Dijkstra 找最短增广路（费用有负边，所以允许点被“撤销已确定”）',
                 '负费用的反向边是关键：它允许后来的锁把先前的分配“换走”',
                 '原文已是 Python 3 写法（用 `//`、变量名 `nxt`），代码未改动'],
    ),
)
