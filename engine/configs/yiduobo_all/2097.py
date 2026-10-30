CONFIG = dict(
    num=2097, title='合法重新排列数对', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='一笔画 · Hierholzer 算法',
    tags=['灵神题单', '难度分 2651'],
    code='''
class Solution(object):
    def validArrangement(self, pairs):

        ind = {}
        oud = {}
        g = {}
        for x, y in pairs:
            if x not in g:
                g[x] = []
            g[x].append(y)
            ind[y] = ind.get(y, 0) + 1
            oud[x] = oud.get(x, 0) + 1
        
        start = pairs[0][0]
        for x in oud:
            if oud[x] - ind.get(x, 0) == 1:
                start = x
                break

        def dfs(now):
            while g.get(now, []):
                next = g[now][-1]
                g[now].pop()
                dfs(next)
                res.append([now, next])

        res = []
        dfs(start)
        res.reverse()
        return res
''',
    call='Solution().validArrangement([[1,2],[1,3],[2,1]])',
    expect=[[1, 2], [2, 1], [1, 3]],
    views=[
        dict(type='map', var='g', label='g（出边表：数值 = 点，列表 = 还没走的出边）', h=150,
             fmt=lambda k, v: f'{k} → {v}'),
        dict(type='map', var='oud', label='oud（出度）', h=110, fmt=lambda k, v: f'{k}: {v}'),
        dict(type='map', var='ind', label='ind（入度）', h=110, fmt=lambda k, v: f'{k}: {v}'),
        dict(type='calls', h=200),
        dict(type='stack', var='res', label='res（回溯时才追加，所以是倒序的）', h=130,
             fmt=lambda x: f'{x[0]}→{x[1]}'),
    ],
    watch=[('start', 'start', 'green'), ('now', lambda S: S['_inner'].get('now'), 'blue'), ('next', lambda S: S['_inner'].get('next'), 'pink')],
    skip=['ind = {}', 'oud = {}', 'g = {}', 'if x not in g', 'g[x] = []', 'break'],
    captions={
        'g[x].append(y)': '数对 `[{x},{y}]` 看作有向边 `{x} → {y}`：加入 `g[{x}]` = `{g[x]}`',
        'ind[y] = ': '`ind[{y}] = {ind[y]}`：点 {y} 的==入度==加一',
        'oud[x] = ': '`oud[{x}] = {oud[x]}`：点 {x} 的==出度==加一',
        'start = pairs[0][0]': '默认起点：第一个数对的起点 `{start}`（入度都等于出度时任选一个点即可）',
        'for x in oud': '枚举有出边的点，找一笔画的起点',
        'if oud[x] - ind.get': lambda S, B, r: (
            f'点 `{S.x}`：出度 {S.oud[S.x]} − 入度 {S.ind.get(S.x, 0)} = {S.oud[S.x] - S.ind.get(S.x, 0)}'
            + ('，==出度多 1 → 它就是起点==' if S.oud[S.x] - S.ind.get(S.x, 0) == 1 else '，不是起点')),
        'start = x': '起点定为 `{start}`',
        'while g.get(now, [])': lambda S, B, r: (
            f'点 `{S.now}` 还有出边 `{S.g.get(S.now)}` → 继续走' if S.g.get(S.now)
            else f'点 `{S.now}` 没有出边了 → ==回溯=='),
        'next = g[now][-1]': '取点 `{now}` 的一条出边，走向 `next = {next}`',
        'g[now].pop()': '这条边只能走一次：从 `g[{now}]` 删掉 → `{g[now]}`',
        'dfs(next)': '递归：站到点 `{next}` 继续一笔画',
        'res.append([now, next])': '从 `{next}` 回溯回来，把边 `{now}→{next}` 追加到 `res`：==先走完的子路径先入答案，所以是倒序==',
        'res = []': '`res` 保存边，按「回溯完成」的顺序追加',
        'dfs(start)': '从起点 `{start}` 开始 Hierholzer',
        'res.reverse()': '`res` 是倒序：翻转后才是行走顺序 → `{res}`',
        'return res': '合法排列：`{res}`，前一条的终点 == 后一条的起点',
    },
    max_steps=80,
    cards=dict(
        one_liner='数对 = 有向边，找一笔画：Hierholzer 回溯后倒序',
        complexity='时间 `O(n)`，空间 `O(n)`（n 为数对个数）',
        problem=['`pairs[i] = [start, end]`，重排使得前一对的 `end` == 后一对的 `start`',
                 '返回任意一个合法重排，保证有解',
                 '本视频：`[[1,2],[1,3],[2,1]]` → `[[1,2],[2,1],[1,3]]`'],
        quote='如果将数对里面的数值视为图中的点，数对视为图中的有向边，那么最终的问题就是能否找出一个点，从这个点开始在图中走，保证图中每条边经过且仅经过一次，这就是经典的一笔画问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['先数每个点的入度、出度：出度比入度多 1 的点是==起点==，没有就任选',
              '从起点走：有出边就删掉这条边、走过去；走到头再回溯，回溯时记录边',
              '桥可能被先走过去，子图只能回溯时才补上 → 记录顺序是倒的，最后 `reverse`'],
        summary=['时间 `O(n)`，空间 `O(n)`；每条边只走一次',
                 '==必须倒序==：本例先走到死路 `1→3`，它先入 res，实际应排在最后',
                 '起点：出度 − 入度 = 1 的点；找不到（欧拉回路）就用任意点',
                 '原文是 Python 2 风格，代码无需修改，直接运行',
                 '同类题：332 重新安排行程（有向图欧拉路径）'],
    ),
)
