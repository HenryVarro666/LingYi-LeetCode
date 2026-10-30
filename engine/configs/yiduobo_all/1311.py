CONFIG = dict(
    num=1311, title='获取你好友已观看的视频', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='BFS 按层 · 字典计数后排序',
    tags=['灵神题单·图论算法'],
    code='''
class Solution(object):
    def watchedVideosByFriends(self, watchedVideos, friends, id, level):

        n = len(watchedVideos)
        used = [False] * n
        q = [id]
        used[id] = True
        l = 0
        r = 1
        step = 0
        cnt_dict = {}
        while l < r and step < level:
            step += 1
            for now in q[l : r]:
                for f in friends[now]:
                    if not used[f]:
                        q.append(f)
                        used[f] = True
                        if step == level:
                            for v in watchedVideos[f]:
                                cnt_dict[v] = cnt_dict.get(v, 0) + 1
            
            l, r = r, len(q)

        return [x[0] for x in sorted(cnt_dict.items(), key=lambda d:(d[1], d[0]))]
''',
    call="Solution().watchedVideosByFriends([['A','B'],['C'],['B','C'],['D','B'],['B','D','E']], [[1,2],[0,3],[0,3,4],[1,2],[2]], 0, 2)",
    expect=['E', 'B', 'D'],
    views=[
        dict(type='text', fn=lambda S: ('好友关系：' + '，'.join(f'`{i}`:{fs}' for i, fs in enumerate(S['friends']))) if 'friends' in S else '', size=24, h=60),
        dict(type='array', var='used', label='used（True=已被 BFS 访问过；蓝=当前点 now）', cell=90, h=190,
             color=lambda S, i, v: 'blue' if i == S.get('now') and S.get('_line', 0) >= 14 else ('green' if v else None)),
        dict(type='array', var='q', label='q（BFS 队列；l~r 是当前这一层）', cell=80, h=190,
             pointers={'l': 'blue', 'r': 'pink'}),
        dict(type='map', var='cnt_dict', label='cnt_dict（第 level 层的人看过的视频 → 次数）', h=170),
    ],
    watch=[('id', 'id', 'purple'), ('level', 'level', 'yellow'), ('step', 'step', 'orange'), 'now', 'f', 'l', 'r'],
    captions={
        'n = len': '`n` 个人，每个人是图上的一个点，好友关系是边',
        'used = [False]': '`used`：标记谁已经进过队列，避免走回头路',
        'q = [id]': '从自己 `id = {id}` 出发做 BFS：队列 `{q}`',
        'used[id] = True': '自己先标记为已访问',
        'l = 0': '`l ~ r` 框出当前这一层的人',
        'r = 1': '第一层只有自己：`r = 1`',
        'step = 0': '`step` 记录走了几层，等于「和自己的距离」',
        'cnt_dict = {}': '`cnt_dict` 只统计恰好第 `level = {level}` 层的人看的视频',
        'while l < r and step < level': lambda S, B, ret: (f'还没走到第 `{S.level}` 层（`step = {S.step}`）且这一层有人 → 继续扩展' if S.l < S.r and S.step < S.level
                                                           else f'`step = {S.step}` 已达 `level`：BFS 停止，不用再往外扩'),
        'step += 1': '往外走一层：`step` → {step}',
        'for now in q[l : r]': '逐个处理当前这一层 `q[{l}:{r}]` 的人',
        'for f in friends[now]': '遍历好友：`friends[{now}] = {friends[now]}`',
        'if not used[f]': lambda S, B, ret: (f'好友 `{S.f}` 没访问过 → ==是新的一层的人==' if not S.used[S.f]
                                             else f'好友 `{S.f}` 已访问过（距离更近）→ 跳过'),
        'q.append(f)': '`{f}` 入队：`q = {q}`',
        'used[f] = True': '标记 `{f}` 已访问',
        'if step == level': lambda S, B, ret: (f'`step == level`（{S.step}）：`{S.f}` 正好在第 {S.level} 层 → ==统计他看过的视频==' if S.step == S.level
                                               else f'`step = {S.step}` 还没到第 `{S.level}` 层 → 只入队，不统计'),
        'for v in watchedVideos[f]': '遍历 `{f}` 看过的视频：`{watchedVideos[f]}`',
        'cnt_dict[v] = ': '`cnt_dict[{v!r}]` 加一 → =={cnt_dict[v]}==',
        'l, r = r, len(q)': '这一层处理完：新的一层是 `q[{l}:{r}]`',
        'return [x[0]': lambda S, B, ret: f'按「次数、名字」从小到大排序，取视频名：=={ret}==',
    },
    cards=dict(
        one_liner='把人当点、好友当边：BFS 走到第 level 层，数这层人看的视频',
        complexity='时间 `O(n+m+k log k)`，空间 `O(n+k)`',
        problem=['`watchedVideos[i]` 是第 `i` 个人看过的视频，`friends[i]` 是他的好友',
                 '给出 `id` 和 `level`，找出==恰好距离 `id` 为 `level` 层==的朋友们看过的视频',
                 '按出现次数从小到大返回，次数相同按字母序',
                 '本视频：`id=0, level=2` → `["E","B","D"]`'],
        quote='将每个人看做图中的一个点，两个人之间若存在朋友关系，就在这两个人中间连上一条边……问题就转化成了求与id最短距离为level的所有节点看过的视频以及对应的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`bfs` 一层一层往外扩，第 `level` 层的人就是「最短距离 = level」的人',
              '处理到这一层时，用 `dict` 累计每个视频被看了几次',
              '最后按 `(次数, 名字)` 排序，只留名字'],
        summary=['时间 `O(n+m+k log k)`，空间 `O(n+k)`，`m` 是好友关系数，`k` 是不同视频数',
                 '易错：必须是==最短距离恰好==为 `level`，所以要用 `used` 去重，近的人不能再算一次',
                 '易错：排序键是 `(次数, 名字)`，次数相同才比字母',
                 '原文代码在 Python 3 下可直接运行，未做修改'],
    ),
)
