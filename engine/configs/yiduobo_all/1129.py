CONFIG = dict(
    num=1129, title='颜色交替的最短路径', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='按点+颜色拆状态的 BFS', tags=['灵神题单', '广度优先搜索'],
    code='''
class Solution:
    def shortestAlternatingPaths(self, n, red_edges, blue_edges):

        G_r = {}
        for x, y in red_edges:
            if x not in G_r:
                G_r[x] = set()
            G_r[x].add(y)
        
        G_b = {}
        for x, y in blue_edges:
            if x not in G_b:
                G_b[x] = set()
            G_b[x].add(y)

        q = [[0, None]]
        l = 0
        r = 1
        res = [-1] * n
        step = 0
        used_r = [False] * n
        used_b = [False] * n
        while l < r:
            for now, last_c in q[l : r]:
                if res[now] == -1:
                    res[now] = step

                if last_c != 'r' and now in G_r:
                    for next in G_r[now]:
                        if not used_r[next]:
                            q.append([next, 'r'])
                            used_r[next] = True
                
                if last_c != 'b' and now in G_b:
                    for next in G_b[now]:
                        if not used_b[next]:
                            q.append([next, 'b'])
                            used_b[next] = True
            
            l, r = r, len(q)
            step += 1
        
        return res
''',
    call='Solution().shortestAlternatingPaths(5, [[0,1],[2,3]], [[1,2],[0,2]])',
    expect=[0, 1, 1, 2, -1],
    views=[
        dict(type='text', size=28, fn=lambda S: ('红边 ' + '  '.join(f'{k}→{sorted(v)[0]}' for k, v in S['G_r'].items()) + '　　蓝边 ' + '  '.join(f'{k}→{sorted(v)[0]}' for k, v in S['G_b'].items())) if 'G_b' in S and 'G_r' in S else '', h=60),
        dict(type='array', var=lambda S: [f'{a}{c or "·"}' for a, c in S['q']] if 'q' in S else None, label='队列 q（点 + 到达颜色 r/b）',
             window=('l', 'r - 1'), h=150),
        dict(type='array', var='res', label='res（-1 = 暂未到达）', pointers={'now': 'blue'},
             color=lambda S, i, v: 'green' if v != -1 else None, h=150),
        dict(type='array', var='used_r', label='used_r（经红边到过）', h=150),
        dict(type='array', var='used_b', label='used_b（经蓝边到过）', h=150),
    ],
    watch=['step', 'l', 'r', 'now', 'last_c', 'next'],
    captions={
        'q = [[0': '起点 0 入队，来时的颜色记为 `None`：红蓝边都可以从它出发',
        'if res[now] == -1': '`res[now] == {res[now]}`：BFS 按轮次推进，==点第一次被取出时的轮次 `step` 就是最短路==，之后不再改',
        "last_c != 'r' and now in G_r": '上一条边是 `{last_c}`，这次只能走红边：`last_c != \'r\'` 为 {last_c != "r"}，{now} 有红边出口吗：{now in G_r}',
        "last_c != 'b' and now in G_b": '上一条边是 `{last_c}`，这次只能走蓝边：`last_c != \'b\'` 为 {last_c != "b"}，{now} 有蓝边出口吗：{now in G_b}',
        'if not used_r[next]': '`used_r[{next}]` = {used_r[next]}：同一个点“经红边到达”的状态只需入队一次',
        'if not used_b[next]': '`used_b[{next}]` = {used_b[next]}：同一个点“经蓝边到达”的状态只需入队一次',
        "q.append([next, 'r'])": '状态 (`{next}`, 红) 入队：到 {next} 时最后一条边是红的，下轮只能接蓝边',
        "q.append([next, 'b'])": '状态 (`{next}`, 蓝) 入队：到 {next} 时最后一条边是蓝的，下轮只能接红边',
        'l, r = r, len(q)': '这一轮处理完：下一轮要处理的就是本轮新入队的 `q[{l}:{r}]`',
        'step += 1': '一整轮 = 多走一条边，`step` → {step}',
        'return res': '队列空了。点 4 红蓝交替都走不到，保持 -1：返回 `{res}`',
    },
    skip=['G_r[x].add', 'G_b[x].add', 'for x, y in', 'l = 0', 'r = 1', 'step = 0', 'G_r = {}', 'G_b = {}', 'G_r[x] = set()', 'G_b[x] = set()', 'if x not in G_r', 'if x not in G_b', 'used_r = ', 'used_b = ', 'res = [-1]'],
    max_steps=80,
    cards=dict(
        one_liner='一个点拆成两种状态：经红边到 / 经蓝边到',
        complexity='时间 `O(n + E)`，空间 `O(n + E)`',
        problem=['有向图，边分红蓝两色，求 0 到每个点的最短路',
                 '要求路径上的边==红蓝交替==，到不了就是 `-1`',
                 '示例：`n=5` 红 `0→1, 2→3`，蓝 `1→2, 0→2` → `[0,1,1,2,-1]`'],
        quote='边的颜色交替出现，那么每个点就有两种状态，即通过红色边到达以及通过蓝色边到达，需要分别设置访问标记。',
        quote_src='—— yiduobo 题解',
        idea=['边没有权重，从 0 开始 ==BFS，点第一次被访问时的轮次就是距离==',
              '经红边到达的点，只能再发射蓝边；经蓝边到达的，只能再发射红边',
              '所以访问标记分 `used_r` / `used_b` 两张，互不影响'],
        summary=['时间 `O(n + E)`：每个点最多以两种状态各入队一次',
                 '起点没有来时的颜色，记 `None`，红蓝都能出发',
                 '==`res[now]` 只在第一次为 -1 时赋值==，后到的更长路径不覆盖',
                 '原文为 Python 2 写法，本题无需改动，可直接在 Python 3 运行'],
    ),
)
