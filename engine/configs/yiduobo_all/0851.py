def _hl(S, i, v):
    if i == S.get('now'):
        return 'blue'
    n = S.get('next')
    if isinstance(n, int) and i == n:
        return 'pink'
    return None


CONFIG = dict(
    num=851, title='喧闹和富有', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='拓扑排序 · 动态规划',
    tags=['拓扑排序'],
    code='''
class Solution(object):
    def loudAndRich(self, richer, quiet):

        n = len(quiet)
        f = list(range(n))
        ind = [0] * n
        g = {x : set() for x in range(n)}
        for x, y in richer:
            g[x].add(y)
            ind[y] += 1
        
        q = []
        for index in range(n):
            if ind[index] == 0:
                q.append(index)
        
        l = 0
        r = len(q)
        while l < r:
            now = q[l]
            l += 1
            for next in g[now]:
                if quiet[f[next]] > quiet[f[now]]:
                    f[next] = f[now]
                ind[next] -= 1
                if ind[next] == 0:
                    q.append(next)
                    r += 1
        
        return f
''',
    call='Solution().loudAndRich([[1,0],[2,1],[3,1],[3,5],[4,3]], [3,2,5,4,1,0])',
    expect=[4, 4, 2, 4, 4, 5],
    skip=['g[x].add(y)', 'n = len(quiet)', 'ind = [0] * n', 'g = {x', 'q = []', 'l = 0', 'r = len(q)', 'l += 1', 'r += 1', 'for index in range(n)', 'q.append(index)', 'ind[next] -= 1', 'q.append(next)', 'for x, y in richer'],
    max_steps=80,
    views=[
        dict(type='array', var='quiet', label='quiet 安静值', color=_hl, h=200),
        dict(type='array', var='f', label='f：最安静的人', color=lambda S, i, v: _hl(S, i, v) or ('green' if i != v else None), h=200),
        dict(type='array', var='ind', label='ind：入度', color=_hl, h=200),
        dict(type='array', var='q', label='q：队列', pointers={'l': 'cyan', 'r': 'orange'}, h=200),
        dict(type='map', var='g', label='g：x → 比 x 穷的人', fmt=lambda k, v: f'{k}→{sorted(v)}', h=200),
    ],
    watch=[('now', 'now', 'blue'), ('next', "S.get('next') if not callable(S.get('next')) else '-'", 'pink'), ('l', 'l', 'cyan'), ('r', 'r', 'orange')],
    captions={
        'f = list(range(n))': '`f[y]` 先设成 y 自己：最安静的人至少可以是自己',
        'ind[y] += 1': '`x` 比 `y` 有钱：建边 `{x} → {y}`，`ind[{y}]` = {ind[y]}',
        'if ind[index] == 0': '`ind[{index}] = {ind[index]}`：{"没有更富有的人，作为起点入队" if ind[index]==0 else "还有人比他富有，先不入队"}',
        'now = q[l]': '取出队头 `now = {now}`：比它更富有的人都已处理完，`f[{now}]` 已定型',
        'for next in g[now]': '`next = {next}` 比 `now = {now}` 穷，`now` 的答案也可能是 `next` 的答案',
        'if quiet[f[next]] > quiet[f[now]]': '比安静值：`quiet[f[next]]` = {quiet[f[next]]} 对 `quiet[f[now]]` = {quiet[f[now]]} → {"now 的答案更安静，要更新" if quiet[f[next]] > quiet[f[now]] else "next 已有更安静的，不变"}',
        'f[next] = f[now]': '`f[{next}]` 改成 `{f[next]}`（`f[y] = min(f[x], f[y])` 按安静值取小）',
        'ind[next] -= 1': '`now` 对 `next` 的影响已考虑：`ind[{next}]` → {ind[next]}',
        'if ind[next] == 0': '`ind[{next}]` 减 1 → {ind[next]}：{"入度为 0：更富有的人全部考虑完，`next` 入队" if ind[next]==0 else "还有更富有的人没处理，先等着"}',
        'return f': '返回 `f` = {f}',
    },
    cards=dict(
        one_liner='谁更富有就把“最安静的人”沿富有关系传给更穷的人',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['`richer[i] = [a, b]` 表示 a 比 b 更有钱，`quiet[i]` 是第 i 个人的安静值',
                 '对每个人 x，找出==所有不比 x 穷的人里最安静的那个==，返回其编号',
                 '示例：`quiet = [3,2,5,4,6,1,7,0]` → `[5,5,2,5,4,5,6,7]`',
                 '本视频：`quiet = [3,2,5,4,1,0]`，`richer = [[1,0],[2,1],[3,1],[3,5],[4,3]]`'],
        quote='对于每个人而言，其最终的answer只会受到其自身以及明确比此人更富有的人的影响，因此可以使用动态规划来解决。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[y] = min(f[x], f[y])`：x 是明确比 y 更富有的人，按安静值取小',
              '先算更富有的人，所以按 `x → y` 建图做==拓扑排序==',
              '入度为 0 的人没人比他富，先入队；`y` 入度减到 0 再入队'],
        summary=['时间 `O(n + m)`，空间 `O(n + m)`',
                 '`f[y]` 存的是人的编号，比较要用 `quiet[f[..]]`，不是 `f` 本身',
                 '没有 `richer` 的人，答案就是他自己',
                 '原文为 Python 2 写法，`f = range(n)` 已改为 `f = list(range(n))`（Python 3 的 range 不可修改）'],
    ),
)
