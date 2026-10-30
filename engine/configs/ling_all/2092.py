CONFIG = dict(
    num=2092, title='找出知晓秘密的所有专家', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='按时间分组 · 建图 · DFS 传播',
    tags=['并查集', '图论算法', '难度分 2004'],
    code='''
class Solution:
    def findAllPeople(self, _, meetings: List[List[int]], firstPerson: int) -> List[int]:
        # 按照 time 从小到大排序
        meetings.sort(key=lambda m: m[2])

        # 一开始 0 和 firstPerson 都知道秘密
        have_secret = {0, firstPerson}

        # 分组循环
        m = len(meetings)
        i = 0
        while i < m:
            # 在同一时间发生的会议，建图
            g = defaultdict(list)
            time = meetings[i][2]
            while i < m and meetings[i][2] == time:
                x, y, _ = meetings[i]
                g[x].append(y)
                g[y].append(x)
                i += 1

            # 每个连通块只要有一个人知道秘密，那么整个连通块的人都知道秘密
            vis = set()  # 避免重复访问节点

            def dfs(x: int) -> None:
                vis.add(x)
                have_secret.add(x)
                for y in g[x]:
                    if y not in vis:
                        dfs(y)

            # 遍历在 time 时间点参加会议的专家
            for x in g:
                # 从知道秘密的专家出发，DFS 标记其余专家
                if x in have_secret and x not in vis:
                    dfs(x)

        # 可以按任何顺序返回答案
        return list(have_secret)
''',
    call='Solution().findAllPeople(5, [[3,4,2],[1,2,1],[2,3,1]], 1)',
    expect=[0, 1, 2, 3, 4],
    result_fn=sorted,
    views=[
        dict(type='text', h=70, fn=lambda S: ('会议（已按时间排序）：' + '  '.join(f'`{a}-{b}@{t}`' for a, b, t in S['meetings'])) if 'meetings' in S else ''),
        dict(type='text', h=70, fn=lambda S: (f"当前时间点 `{S['time']}`：同一时间的会议并成一张图" if 'time' in S and S.get('_inner', {}).get('g') is not None else '')),
        dict(type='set', var='have_secret', fmt=lambda x: str(x), label='have_secret（知道秘密）', h=170),
        dict(type='map', var='g', fmt=lambda k, v: f'{k} → {v}', label='g（本时间点的图）', h=260),
        dict(type='calls', h=200),
    ],
    watch=[('i', 'i'), ('time', 'time', 'cyan'), ('x', 'x', 'blue'), ('vis', 'sorted(vis)', 'purple')],
    captions={
        'meetings.sort': '先按时间排序：==必须按开会先后顺序传播==，否则会让还不知道秘密的人“提前传播”',
        'have_secret = {0': '一开始 `0` 和 `firstPerson={firstPerson}` 都知道秘密：`{sorted(have_secret)}`',
        'g = defaultdict': '新的一组：为同一时间的会议重新建一张空图',
        'time = meetings': '这组的时间 `time = {time}`',
        'while i < m and': lambda S, B, r: (f'`meetings[{S.i}][2] == {S.time}`？同一时间 → ==继续把这场会议加入这一组==' if S.i < S.m and S.meetings[S.i][2] == S.time else '这一组（同一时间）收集完了，去传播秘密'),
        'x, y, _ =': '取出这场会议的两个专家 `{x}`、`{y}`',
        'g[x].append(y)': '会议 `{x}-{y}`：在图里连一条无向边 `{x}`—`{y}`',
        'g[y].append(x)': '无向边：`{y}` 也连回 `{x}`',
        'i += 1': '`i` → {i}，看下一场会议是否同一时间',
        'vis = set()': '`vis`：本组内已访问的节点，避免 DFS 重复走',
        'vis.add(x)': '访问 `{x}`',
        'have_secret.add(x)': '==`{x}` 获得秘密==：同一连通块里只要有人知道，所有人都知道（同一时间可连续传播）',
        'for y in g[x]': '遍历 `{x}` 的邻居 `{g[x]}`',
        'if y not in vis': '邻居 `{y}` 还没访问吗？{"是 → 递归 DFS" if y not in vis else "已访问，跳过"}',
        'dfs(y)': '递归进入 `{y}`',
        'for x in g': '遍历这个时间点参会的专家',
        'if x in have_secret and x not in vis': lambda S, B, r: (f'`{S.x}` 知道秘密且没访问过 → ==从它出发 DFS 整个连通块==' if S.x in S.have_secret and S.x not in S.vis else f'`{S.x}` ' + ('已被本组 DFS 访问过' if S.x in S.vis else '还不知道秘密，不能作为起点')),
        'dfs(x)': '从知道秘密的 `{x}` 出发 DFS',
        'return list': '所有会议结束，知道秘密的专家：`{sorted(have_secret)}`',
    },
    skip=['def dfs', 'g[y].append(x)', 'vis = set()'],
    max_steps=110,
    cards=dict(
        one_liner='同一时间的会议建成一张图，有人知道秘密的连通块整块知道',
        complexity='时间 `O(m log m)`，空间 `O(m)`',
        problem=['`n` 个专家，`meetings[i] = [x, y, time]` 表示 `x`、`y` 在 `time` 时开会',
                 '专家 `0` 在时间 0 把秘密告诉 `firstPerson`；知道秘密的人开会时会传给对方，且==同一时间可连续传播==',
                 '示例：`n=5, [[3,4,2],[1,2,1],[2,3,1]], firstPerson=1` → `[0,1,2,3,4]`'],
        quote='在同一时间发生的所有会议，可以视作一个无向图。专家是图中的节点，meetings[i] 是图的边。对于一个连通块，如果其中有知道秘密的专家，那么这个专家会把秘密分享给这个连通块中的其他专家。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先按时间排序，==按开会先后顺序==模拟传播',
              '用「分组循环」：内层循环收集同一时间的会议并建图，外层负责建图前后的工作',
              '每组里从知道秘密的专家出发 DFS，把整个连通块标记为知道秘密'],
        after=[dict(heading='另一种写法：并查集', lines=[
            '题解方法二：把 `x`、`y` 合并，`firstPerson` 与 `0` 先合并',
            '每组会议处理完后，==不和 0 同集合的人要撤销合并==（重置 `fa[x] = x`）',
            '最后和 `0` 在同一集合的人都知道秘密'])],
        summary=['时间 `O(m log m)`（排序是瓶颈），空间 `O(m)`',
                 '==必须按时间分组==：同一时间的会议才能一起建图传播，不同时间不能混',
                 '分组循环不需要特判最后一组，是最不容易出 bug 的写法',
                 '`for x in g` 起点必须是已知秘密者；未知秘密者即使在同一连通块里也要等被 DFS 到',
                 '另有并查集写法（撤销合并），见题解方法二'],
    ),
)
