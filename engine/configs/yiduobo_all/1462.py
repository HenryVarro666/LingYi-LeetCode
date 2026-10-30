def _f_map(S):
    f = S.get('f')
    if f is None:
        return {}
    return {i: '{' + ','.join(str(x) for x in sorted(v)) + '}' for i, v in enumerate(f)}


def _ind_map(S):
    return {i: v for i, v in enumerate(S.get('ind', []))}


CONFIG = dict(
    num=1462, title='课程表 IV', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='拓扑排序 · 传递前置课程集合',
    tags=['灵神题单·图论算法'],
    code='''
class Solution(object):
    def checkIfPrerequisite(self, numCourses, prerequisites, queries):

        g = {}
        ind = [0] * numCourses
        for x, y in prerequisites:
            if x not in g:
                g[x] = set()
            g[x].add(y)
            ind[y] += 1
        
        q = []
        f = [set() for _ in range(numCourses)]
        for index in range(numCourses):
            if ind[index] == 0:
                q.append(index)
        
        l = 0
        r = len(q)
        while l < r:
            now = q[l]
            l += 1
            for next in g.get(now, set()):
                ind[next] -= 1
                f[next] |= f[now]
                f[next].add(now)
                if ind[next] == 0:
                    q.append(next)
                    r += 1
        
        return [x in f[y] for x, y in queries]
''',
    call='Solution().checkIfPrerequisite(5, [[0,1],[1,2],[3,2],[2,4]], [[0,4],[3,1],[4,0]])',
    expect=[True, False, False],
    views=[
        dict(type='array', var='ind', label='ind（入度，0 才能出队）', pointers={'now': 'blue'}, h=260, cell=90),
        dict(type='array', var='q', label='q（拓扑序队列）：l 指向待处理，r 是队尾后一位', pointers={'l': 'cyan'}, h=260, cell=90),
        dict(type='map', var=_f_map, label='f[x]：x 的所有前置课程（直接 + 间接）', fmt=lambda k, v: f'{k}: {v}', h=190, font=32),
        dict(type='map', var='g', label='g：x → 直接后置课程', fmt=lambda k, v: f'{k} → {sorted(v)}', h=150, font=28),
    ],
    watch=[('l', 'l', 'cyan'), ('r', 'r', 'orange'), ('now', 'now', 'pink')],
    skip=['g[x] = set()', 'if x not in g', 'l = 0', 'r = len(q)'],
    captions={
        'g[x].add(y)': '建图：课程 `{x}` 的后置课程加入 `{y}`',
        'ind[y] += 1': '`{y}` 多了一门前置课，入度 `ind[{y}]` = {ind[y]}',
        'f = [set()': '`f[x]` 记录 x 的全部前置课程，一开始都是空集',
        'if ind[index] == 0': lambda S, B, r: (f'课程 `{S.index}` 入度为 0，没有前置课 → ==可以先学==' if S.ind[S.index] == 0 else f'课程 `{S.index}` 入度 {S.ind[S.index]}，还有前置课没学，先不入队'),
        'q.append(index)': '`{index}` 入队，作为拓扑排序的起点：`q = {q}`',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}`，队里还有课程 → 继续' if S.l < S.r else f'`l = {S.l} = r`，队列空了 → 拓扑排序结束，f 已完整'),
        'now = q[l]': '取出队头课程 `now = {now}`，它的前置课程集合 `f[{now}]` 已经完整',
        'ind[next] -= 1': '`{now}` 已处理完 → `ind[{next}]` 减 1 变成 {ind[next]}',
        'f[next] |= f[now]': '==继承==：`{now}` 的前置课程 {f[now]} 也都是 `{next}` 的前置课 → `f[{next}]` = {f[next]}',
        'f[next].add(now)': '`{now}` 本身也是 `{next}` 的前置课 → `f[{next}]` = {f[next]}',
        'if ind[next] == 0': lambda S, B, r: (f'`ind[{S.next}] = 0`：前置课都处理完，`f[{S.next}]` 完整 → 入队' if S.ind[S.next] == 0 else f'`ind[{S.next}] = {S.ind[S.next]}`：还有前置课没处理，先不入队'),
        'r += 1': '队尾 `r` → {r}',
        'return [x in f[y]': lambda S, B, r: f'每个查询 `[x, y]` 只需判断 `x in f[y]`：结果 =={r}==',
    },
    cards=dict(
        one_liner='拓扑排序时，把前置课程集合一路传给后置课程',
        complexity='时间 `O(n·(n+m))`（集合合并），空间 `O(n²)`',
        problem=['共 `numCourses` 门课，`[a, b]` 表示学 b 之前必须先学 a（前置关系可传递）',
                 '每个查询 `[x, y]`：问 x 是否是 y 的前置课程',
                 '本视频：5 门课，`[[0,1],[1,2],[3,2],[2,4]]`，查询 `[[0,4],[3,1],[4,0]]` → `[True, False, False]`'],
        quote='最标准的拓扑排序问题，使用f[x]表示课程x的所有前置课程，接下来执行拓扑排序。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[x]` = 课程 x 的所有前置课程；入度为 0 的课先出队',
              '处理课程 `now` 时，它的每个后置课 `next`：入度减 1，==`f[next] |= f[now]`== 再加上 `now` 本身',
              '拓扑序保证：`now` 出队时 `f[now]` 已完整；查询只需 `x in f[y]`'],
        summary=['先建图并统计入度，入度为 0 的课程入队，再按队列顺序处理',
                 '易错：别忘了把 `now` 自己也加进 `f[next]`，只合并 `f[now]` 会漏掉直接前置课',
                 '这里用列表 `q` 加 `l / r` 指针模拟队列，不弹出元素',
                 '查询是 O(1) 的集合查找；也可以用 Floyd 求传递闭包',
                 '原文就是 Python 3 可运行的写法，没有改动'],
    ),
)
