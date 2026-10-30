EV = [["MESSAGE", "10", "id2 id0 id2"], ["OFFLINE", "11", "0"], ["MESSAGE", "12", "ALL"],
      ["MESSAGE", "30", "HERE"], ["MESSAGE", "71", "HERE"]]


def _ev_line(S, k):
    ev = S['events']
    if k >= len(ev):
        return ''
    e = ev[k]
    cur = 'e' in S and S['e'][1] == e[1]
    return ('==▶== ' if cur else '　　') + f"`{e[0]} {e[1]} {e[2]}`"


CONFIG = dict(
    num=3433, title='统计用户被提及情况', difficulty='Medium', category='模拟',
    author='yiduobo', technique='模拟 · 在线集合 + 离线队列',
    code='''
class Solution(object):
    def countMentions(self, numberOfUsers, events):
        
        offline = deque()
        online = set([index for index in range(numberOfUsers)])
        mentions = [0] * numberOfUsers
        all_cnt = 0
        for e in sorted(events, key=lambda d:(-int(d[1]), d[0]), reverse=True):
            while offline and offline[0][0] <= int(e[1]):
                uid = offline[0][1]
                offline.popleft()
                online.add(uid)
            
            if e[0] == 'MESSAGE':
                if e[2] == 'HERE':
                    for uid in online:
                        mentions[uid] += 1
                elif e[2] == 'ALL':
                    all_cnt += 1
                else:
                    for uid in e[2].split():
                        mentions[int(uid[2:])] += 1
            
            else:
                uid = int(e[2])
                online.remove(uid)
                offline.append((int(e[1]) + 60, uid))
        for index in range(numberOfUsers):
            mentions[index] += all_cnt
        
        return mentions
''',
    call=f'Solution().countMentions(3, {EV})',
    expect=[3, 3, 5],
    skip=['online = set', 'mentions = [0]', 'offline = deque'],
    views=[
        dict(type='text', fn=lambda S: '事件（按时间排序后依次处理，==▶== = 当前）', size=22, h=40),
        *[dict(type='text', fn=(lambda k: lambda S: _ev_line(S, k))(k), size=26, h=48) for k in range(5)],
        dict(type='set', var='online', label='online（在线用户集合）', fmt=lambda x: f'u{x}', h=130),
        dict(type='queue', var='offline', label='offline（队列：(重新上线时间, 用户)，队首最先上线）', fmt=lambda x: f'u{x[1]}@{x[0]}', h=130),
        dict(type='array', var='mentions', label='mentions', cell=80, h=170,
             color=lambda S, k, v: 'yellow' if (S['_line'] == 17 and k == S.get('uid')) or (S['_line'] == 22 and k == int(S['uid'][2:])) else None),
    ],
    watch=[('all_cnt', 'all_cnt', 'orange'), ('mentions', 'mentions', 'green')],
    captions={
        'offline = deque()': '`offline` 队列记录离线的用户和==重新上线的时刻==',
        'all_cnt = 0': '`all_cnt`：`ALL` 出现的次数，最后一次性加给每个人',
        'for e in sorted': lambda S, B, r: ('先按时间戳排序，再依次处理每个事件（同一时刻离线事件在前）' if 'e' not in B else
                                            ('所有事件处理完了' if S.e == B.e else f'事件 `{S.e[0]} {S.e[1]} {S.e[2]}`')),
        'while offline and': lambda S, B, r: (f'队首 `u{S.offline[0][1]}` 在 `{S.offline[0][0]}` 上线，当前时刻 `{S.e[1]}` ≥ 它 → ==已经回来了==' if S.offline and S.offline[0][0] <= int(S.e[1])
                                              else ('队列为空，没有人待上线' if not S.offline else f'队首 `u{S.offline[0][1]}` 要到 `{S.offline[0][0]}` 才上线，当前 `{S.e[1]}`，还没回来，停止检查')),
        'uid = offline[0][1]': '取出队首用户 `u{uid}`',
        'offline.popleft()': '先离线的先上线（离线时长统一是 60）→ 从队首弹出',
        'online.add(uid)': '`u{uid}` 重新加入 `online`：`{sorted(online)}`',
        "if e[0] == 'MESSAGE'": lambda S, B, r: ('消息事件：看是 HERE / ALL / id 中的哪一种' if S.e[0] == 'MESSAGE' else '不是消息，是离线事件'),
        "if e[2] == 'HERE'": lambda S, B, r: ('`HERE` → 只提及 `online` 里的用户' if S.e[2] == 'HERE' else '不是 `HERE`'),
        'for uid in online': lambda S, B, r: (f'`HERE`：给在线的 `u{S.uid}` 加一' if not (S.uid == B.get('uid') and S.uid == max(S.online)) else '在线用户都加过了'),
        'mentions[uid] += 1': '`mentions[{uid}]` → `{mentions[uid]}`',
        "elif e[2] == 'ALL'": lambda S, B, r: ('`ALL` → 不用管谁在线，只记个数' if S.e[2] == 'ALL' else '既不是 `HERE` 也不是 `ALL` → 是 id 列表'),
        'all_cnt += 1': '`ALL` 出现一次，`all_cnt = {all_cnt}`（最后统一加给所有人，含离线用户）',
        'for uid in e[2].split()': lambda S, B, r: (f'`id` 提及：拆成单个 id，重复的分别计数，当前 `{S.uid}`' if not (S.uid == B.get('uid') and S.uid == S.e[2].split()[-1]) else '这条消息里的 id 都处理完了'),
        'mentions[int(uid[2:])] += 1': '去掉 `id` 前缀，`mentions[{int(uid[2:])}]` → `{mentions[int(uid[2:])]}`',
        'uid = int(e[2])': '离线事件：用户 `u{uid}` 要离线 60 个单位时间',
        'online.remove(uid)': '`u{uid}` 从 `online` 移除：`{sorted(online)}`',
        'offline.append': '入队 `(上线时刻, 用户) = ({int(e[1]) + 60}, {uid})`，`{e[1]} + 60` 时自动回来',
        'for index in range(numberOfUsers)': lambda S, B, r: (f'最后给用户 `{S.index}` 加上 `all_cnt`' if not (S.index == B.get('index') and S.index == S.numberOfUsers - 1) else '每个人都加完了'),
        'mentions[index] += all_cnt': '`mentions[{index}] += {all_cnt}` → `{mentions[index]}`',
        'return mentions': '各用户被提及次数：`{mentions}`',
    },
    cards=dict(
        one_liner='排序后一趟模拟：在线集合 + 离线队列，每次先让回来的人上线',
        complexity='时间 `O(m log m + mn)`，空间 `O(n + m)`',
        problem=['`MESSAGE` 提及一批用户：`id…` / `ALL`（所有人，含离线）/ `HERE`（仅在线）',
                 '`OFFLINE` 让某用户离线 60 个单位时间，同一时刻先处理状态变更再处理消息',
                 '求每个用户被提及的次数',
                 '本视频：3 个用户，5 个事件'],
        quote='由于离线的时间统一为60，且只会作用在当前在线的用户上，那么就意味着先离线的用户必然先重新连接。于是可以使用一个队列offline记录当前离线的用户以及离线的时间。',
        quote_src='—— yiduobo 题解原文',
        idea=['`online` 集合记在线用户，`offline` 队列记 `(上线时刻, 用户)`',
              '每处理一个事件前，先检查队首是否已到上线时刻，到了就弹出并加回 `online`',
              '`HERE` 遍历 `online`；`ALL` 只累加 `all_cnt`，最后统一加；`id` 逐个拆开计数'],
        summary=['时间 `O(m log m + mn)`，空间 `O(n + m)`',
                 '易错：`ALL` 包含离线用户，`HERE` 不包含；同一 id 重复出现要分别计数',
                 '排序键写成 `(-时间戳, 类型)` 再 `reverse`，保证同一时刻 `OFFLINE` 排在 `MESSAGE` 前',
                 '原文为 Python 2 风格，代码无需修改，Python 3 直接可运行（`deque` 已预置）',
                 '对比灵神：灵神用“HERE 先全算再减离线期间的 HERE 数”；这里直接维护在线集合'],
    ),
)
