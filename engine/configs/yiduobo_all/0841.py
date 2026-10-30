ROOMS = [[1, 3], [0, 3, 1], [2], [0]]


def _room_color(S, i, v):
    if S.get('_line') and 'now' in S and i == S['now'] and 'used' in S:
        return 'blue'
    if i in (S.get('used') or ()):
        return 'green'
    return None


def _key(S, B, r):
    k = S.key
    if k in B.used:
        return f'钥匙 `{k}`：{k} 号房间已经能进了 → 跳过'
    return f'钥匙 `{k}`：第一次拿到 → =={k} 号房间入队=='


CONFIG = dict(
    num=841, title='钥匙和房间', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='BFS（从 0 号房间出发）',
    tags=['labuladong', '灵神题单·图论算法'],
    code='''
class Solution(object):
    def canVisitAllRooms(self, rooms):

        q = [0]
        l = 0
        r = 1
        used = set([0])
        while l < r:
            now = q[l]
            l += 1
            for key in rooms[now]:
                if key not in used:
                    used.add(key)
                    q.append(key)
                    r += 1
        
        return len(used) == len(rooms)
''',
    call=f'Solution().canVisitAllRooms({ROOMS})',
    expect=False,
    skip=['l = 0', 'r = 1', 'q.append', 'r += 1'],
    views=[
        dict(type='array', var=lambda S: [','.join(map(str, k)) or '空' for k in S['rooms']] if 'rooms' in S else None,
             label='rooms[i] = i 号房间里的钥匙（绿 = 已能进入，蓝 = 正在搜的房间）', cell=150, h=200,
             color=_room_color),
        dict(type='array', var='q', label='q（BFS 队列，暗 = 已出队）', cell=90, h=170,
             pointers={'l': 'blue', 'r': 'pink'}, dim=lambda S, i, v: i < S.get('l', 0)),
        dict(type='set', var='used', label='used（拿到过钥匙的房间）', h=130),
    ],
    watch=[('now', 'now', 'blue'), ('key', 'key', 'yellow'), ('l', 'l', 'blue'), ('r', 'r', 'pink'),
           ('len(used)', lambda S: len(S['used']) if 'used' in S else None, 'green')],
    captions={
        'q = [0]': '==只能从 0 号房间开始==：它入队',
        'used = set([0])': '`used` 记录已经能进的房间',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}`：队列里还有房间' if S.l < S.r
                                        else '`l == r`：再也拿不到新钥匙，BFS 结束'),
        'now = q[l]': '进入 `{now}` 号房间，里面的钥匙是 `{rooms[now]}`',
        'l += 1': '`l` → {l}（出队）',
        'for key in rooms[now]': lambda S, B, r: (f'`{S.now}` 号房间的钥匙看完了' if 'key' in B and B.key == S.key and B.now == S.now
                                                  else f'拿起钥匙 `{S.key}`'),
        'if key not in used': _key,
        'used.add(key)': '`used` 加入 `{key}`：{key} 号房间入队，等着进去拿钥匙',
        'return len': lambda S, B, r: (f'能进 `{len(S.used)}` 间，共 `{len(S.rooms)}` 间 → ' +
                                       ('==全都能进==' if r else '==有房间进不去==，返回 False')),
    },
    cards=dict(
        one_liner='从 0 号房间 BFS，拿到新钥匙就把那间房入队',
        complexity='时间 `O(n + 钥匙总数)`，空间 `O(n)`',
        problem=['`n` 个房间，只有 0 号房间开着；`rooms[i]` 是 i 号房间里的钥匙',
                 '拿到钥匙 `k` 就能进 `k` 号房间，问能否进入==所有==房间',
                 '本视频：`[[1,3],[0,3,1],[2],[0]]` → `false`（2 号钥匙只在 2 号房间里）'],
        quote='乍一看感觉是拓扑排序，但是可以发现……初始必然从0号房间开始，因此无需计算每个点的入度，==只需要从0开始进行bfs==。',
        quote_src='—— yiduobo 题解原文',
        idea=['房间是点，钥匙 `k` 是一条指向 `k` 的边：问从 0 出发能否到达所有点',
              'BFS：拿到没见过的钥匙就把那间房加入队列',
              '结束后比较 `used` 的大小和房间数'],
        summary=['时间 `O(n + 钥匙总数)`，每间房只进一次',
                 '易错：`used` 要在入队时加入，同一把钥匙出现多次也只入队一次',
                 '队列用数组 + 下标 `l`、`r` 模拟，`r` 其实就是 `len(q)`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
