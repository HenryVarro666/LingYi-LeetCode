CONFIG = dict(
    num=2092, title='找出知晓秘密的所有专家', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='按时间建图 · BFS 染色',
    tags=['并查集', '图论算法', '难度分 2004'],
    code='''
class Solution(object):
    def findAllPeople(self, n, meetings, firstPerson):

        res_set = set([0, firstPerson])
        time_dict = {}
        for x, y, t in meetings:
            if t not in time_dict:
                time_dict[t] = []
            time_dict[t].append([x, y])
        
        for t in range(1, 100001):
            if t in time_dict:
                g = {}
                q_set = set()
                for x, y in time_dict[t]:
                    if x in res_set:
                        if y in res_set:
                            continue
                        else:
                            q_set.add(x)
                    elif y in res_set:
                        q_set.add(y)
                    
                    if x not in g:
                        g[x] = set()
                    if y not in g:
                        g[y] = set()

                    g[x].add(y)
                    g[y].add(x)

                q = list(q_set)
                l, r = 0, len(q)
                while l < r:
                    now = q[l]
                    l += 1
                    for next in g.get(now, set()):
                        if next not in res_set:
                            q.append(next)
                            res_set.add(next)
                            r += 1
        
        return list(res_set)
''',
    call='Solution().findAllPeople(5, [[3,4,2],[1,2,1],[2,3,1]], 1)',
    expect=[0, 1, 2, 3, 4],
    result_fn=sorted,
    views=[
        dict(type='text', h=70, fn=lambda S: ('按时间分好的会议：' + '  '.join(f'`@{t}: {v}`' for t, v in sorted(S['time_dict'].items()))) if S.get('time_dict') and S.get('x') is not None and 'g' not in S else (f"当前时间点 `{S['t']}`，只用这一刻的边建图" if 'g' in S else '')),
        dict(type='set', var='res_set', fmt=lambda x: str(x), label='res_set（知道秘密 = 已染色）', h=160),
        dict(type='map', var='g', fmt=lambda k, v: f'{k} ~ {sorted(v)}', label='g（这一刻的图）', h=230),
        dict(type='queue', var='q', fmt=lambda x: str(x), label='q（BFS 队列，起点 + 新染色的人）', h=150),
    ],
    watch=[('t', 't', 'cyan'), ('x', 'x', 'blue'), ('y', 'y', 'pink'), ('l', 'l'), ('r', 'r'), ('now', 'now', 'purple')],
    captions={
        'res_set = set': '一开始 `0` 和 `firstPerson={firstPerson}` 知道秘密：`{sorted(res_set)}`',
        'for x, y, t in meetings': '先把所有会议按时间 `t` 收进哈希表 `time_dict`',
        'time_dict[t].append': '时间 `{t}` 的会议加入 `{x}-{y}`',
        'if t in time_dict': '时间 `{t}` 有会议 → 用这一时刻的边建图',
        'g = {}': '时间 `{t}` 有会议：图每时刻都在变，只为这一刻新建一张图',
        'q_set = set()': '`q_set`：这一刻图里==已经知道秘密==的人，作为 BFS 起点',
        'for x, y in time_dict': '处理会议 `{x}-{y}`',
        'if x in res_set': lambda S, B, r: f'`{S.x}` ' + ('知道秘密' if S.x in S.res_set else '不知道秘密'),
        'if y in res_set': lambda S, B, r: f'`{S.y}` ' + ('也知道秘密' if S.y in S.res_set else '不知道秘密') + ('：两人都知道，==这条边没必要加入图==' if S.y in S.res_set else '：只有 x 知道 → x 是 BFS 起点'),
        'continue': '两个人都已知道，跳过这条边（保证复杂度 O(m)）',
        'q_set.add(x)': '`{x}` 知道秘密、`{y}` 不知道 → `{x}` 加入起点 `{sorted(q_set)}`',
        'q_set.add(y)': '`{y}` 知道秘密、`{x}` 不知道 → `{y}` 加入起点 `{sorted(q_set)}`',
        'elif y in res_set': lambda S, B, r: f'x 不知道；`{S.y}` ' + ('知道秘密 → 作为起点' if S.y in S.res_set else '也不知道，但边仍要建图（可能后面被传到）'),
        'if x not in g': '`g` 里还没有 `{x}`？{"没有 → 建空邻居集合" if x not in B.g else "已有"}',
        'if y not in g': '`g` 里还没有 `{y}`？{"没有 → 建空邻居集合" if y not in B.g else "已有"}',
        'g[x].add(y)': '无向边：`{x}` — `{y}`',
        'g[y].add(x)': '反方向：`{y}` — `{x}`',
        'q = list': '起点入队：`q = {q}`',
        'l, r = 0': '`l` 是队头，`r` 是队列长度',
        'while l < r': lambda S, B, r: (f'`l={S.l} < r={S.r}`：队列还有人，继续传播' if S.l < S.r else f'`l={S.l} == r={S.r}`：队列空，这一刻传播结束'),
        'now = q[l]': '取出队头 `now = {now}`',
        'for next in g.get': '看 `{now}` 在这一刻的邻居 `{sorted(g.get(now, set()))}`',
        'if next not in res_set': lambda S, B, r: f'邻居 `{S.next}` ' + ('还不知道 → ==染色并入队==' if S.next not in S.res_set else '已经知道，跳过'),
        'res_set.add(next)': '`{next}` 获得秘密：`{sorted(res_set)}`',
        'q.append(next)': '`{next}` 入队，继续往外传',
        'return list': '最终知道秘密的专家：`{sorted(res_set)}`',
    },
    skip=['for t in range', 'if x not in g', 'if y not in g', 'if t in time_dict', 'r += 1', 'l += 1'],
    max_steps=130,
    max_events=400000,
    cards=dict(
        one_liner='图每个时刻都不同：按时间建图，从知道秘密的人 BFS 染色',
        complexity='时间 `O(m)`（不含排序），空间 `O(m)`',
        problem=['`n` 个专家，`meetings[i] = [x, y, time]` 表示 `x`、`y` 在 `time` 时开会',
                 '专家 `0` 在时间 0 把秘密告诉 `firstPerson`；知道秘密的人开会时传给对方，同一时间可连续传播',
                 '示例：`n=5, [[3,4,2],[1,2,1],[2,3,1]], firstPerson=1` → `[0,1,2,3,4]`'],
        quote='本题是很典型的染色问题，但是与常规染色问题有所不同的是，本题的图是每时每刻都在变化的，因此可以先将所有边以时间作为key用哈希表收集起来，然后从小到大遍历每个时间点',
        quote_src='—— yiduobo 题解原文',
        idea=['先用哈希表按时间收集边，再从小到大遍历每个时间点建图、BFS 染色',
              '起点只选这一刻图里==已知秘密==的点；把所有知情者都入队，极限会到 `O(mn)`',
              '建图时筛选：两端都知情的边不用加；只有一端知情，知情端进队列；都不知情也要建边'],
        summary=['时间 `O(m)`（外层 `t` 从 1 枚举到 1e5），空间 `O(m)`',
                 '==同一时间的边建成一张图==，不同时间不能混在一起',
                 '都不知情的边也要建：之后可能被别人传到，再传给它的邻居',
                 '起点要去重（`q_set`），只放出现在当前图里的知情者',
                 '对比灵神：灵神按时间分组循环 + DFS；yiduobo 用哈希表收集 + BFS，思路同为「同一时间连通块」'],
    ),
)
