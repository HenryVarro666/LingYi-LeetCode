EV = [["MESSAGE", "10", "id1 id0"], ["OFFLINE", "11", "0"], ["MESSAGE", "12", "HERE"],
      ["MESSAGE", "71", "HERE"], ["MESSAGE", "75", "ALL"]]


def _ev_short(e):
    return f"{e[0][0]}{e[1]}\n{e[2]}"


def _es_fmt(t):
    names = {1: '离线', -1: '上线', 2: 'HERE'}
    return f'{t[0]}\n{names[t[1]]}' + (f' u{t[2]}' if t[2] >= 0 else '')


def _kind(S, B, r):
    t = S.mention
    return t


def _ev_line(S, k):
    ev = S['events']
    if k >= len(ev):
        return ''
    e = ev[k]
    cur = 'timestamp' in S and 'here' not in S and S['timestamp'] == e[1]
    return ('==▶== ' if cur else '　　') + f"`{e[0]} {e[1]} {e[2]}`"


def _es_line(S):
    es = S.get('es')
    if not es:
        return 'es：(时间, 类型, 用户)，类型 1 = 离线、-1 = 上线、2 = HERE'
    cur = None
    if 'here' in S and '_' in S:
        cur = (S['_'], S['type_'], S['i'])
    parts = [(f'==▶ {t}==' if t == cur else f'{t}') for t in es]
    return 'es（类型 1 = 离线、-1 = 上线、2 = HERE）：' + ' '.join(parts)


CONFIG = dict(
    num=3433, title='统计用户被提及情况', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='模拟 · 方法二：离线期间的 HERE 次数相减',
    code='''
class Solution:
    def countMentions(self, numberOfUsers: int, events: List[List[str]]) -> List[int]:
        ans = [0] * numberOfUsers
        es = []  # (timestamp, type, id)
        all = 0
        for type_, timestamp, mention in events:
            cur_t = int(timestamp)  # 当前时间
            if type_[0] == 'O':  # 离线
                i = int(mention)
                es.append((cur_t, 1, i))
                es.append((cur_t + 60, -1, i))
            elif mention[0] == 'A':  # @所有人
                all += 1
            elif mention[0] == 'H':  # @所有在线用户
                all += 1
                es.append((cur_t, 2, -1))
            else:  # @id
                for s in mention.split():
                    ans[int(s[2:])] += 1
        es.sort()
        here = 0
        for _, type_, i in es:
            if type_ == 2:
                here += 1
            else:
                # 注意 HERE 排在后面，还没有计入发生在此刻的 HERE 消息
                ans[i] += type_ * here  # type=1 是加，-1 是减
        for i in range(numberOfUsers):
            ans[i] += all
        return ans
''',
    call=f'Solution().countMentions(3, {EV})',
    expect=[3, 4, 3],
    skip=['cur_t = int', 'es = []'],
    views=[
        dict(type='text', fn=lambda S: '事件 events（==▶== = 第一遍正在处理）', size=22, h=40),
        *[dict(type='text', fn=(lambda k: lambda S: _ev_line(S, k))(k), size=26, h=48) for k in range(5)],
        dict(type='text', fn=_es_line, size=26, h=150),
        dict(type='array', var='ans', label='ans（各用户被提及次数）', cell=80, h=170,
             color=lambda S, k, v: 'yellow' if S.get('i') == k and S['_line'] in (27, 29) else None),
    ],
    watch=[('all', 'all', 'orange'), ('here', 'here', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = [0] * numberOfUsers': '`ans[i]` 记录用户 `i` 被提及的次数，共 `{numberOfUsers}` 个用户',
        'all = 0': '`all`：==每个人都会被计一次==的消息个数（ALL 和 HERE 先全算上）',
        'for type_, timestamp, mention in events': lambda S, B, r: ('第一遍：把事件分三类处理，离线/上线/HERE 先记进 `es`' if 'type_' not in B else
                                                                     ('第一遍结束，`all = ' + str(S.all) + '`' if S.timestamp == B.timestamp else f'事件 `{S.type_} {S.timestamp} {S.mention}`')),
        "if type_[0] == 'O'": lambda S, B, r: ('离线事件 → 记下离线时刻和 60 秒后的上线时刻' if S.type_[0] == 'O' else f'`{S.type_}` 不是离线，看看是哪种消息'),
        'i = int(mention)': '离线的用户是 `{i}`',
        'es.append((cur_t, 1, i))': '用户 `{i}` 在 `{cur_t}` 离线：记 `(时间, 1, 用户)`，1 表示“加”',
        'es.append((cur_t + 60, -1, i))': '用户 `{i}` 在 `{cur_t + 60}` 重新上线：记 `-1`，表示“减”',
        "elif mention[0] == 'A'": lambda S, B, r: ('是 `ALL` → 每个人都被提及一次，包括离线用户' if S.mention[0] == 'A' else '不是 `ALL`，继续判断'),
        "elif mention[0] == 'H'": lambda S, B, r: ('是 `HERE` → 先按“所有人都提及”算' if S.mention[0] == 'H' else '不是 `HERE`，那就是 `id` 列表'),
        'all += 1': lambda S, B, r: ('`ALL`：`all` 加一 → ' + str(S.all) if S.mention[0] == 'A' else '`HERE` 先让 `all` 加一 → ' + str(S.all) + '，离线者之后再把多算的减掉'),
        'es.append((cur_t, 2, -1))': '记下这条 HERE 的时刻 `{cur_t}`（类型 2，排在同一时刻的离线/上线之后）',
        'for s in mention.split()': lambda S, B, r: (f'`id` 提及：逐个拆开，重复的 id 要分别计数，当前 `{S.s}`' if S.get('s') != B.get('s') else '这条消息里的 id 都处理完了'),
        'ans[int(s[2:])] += 1': '`s[2:]` 去掉 `id` 前缀，用户 `{int(s[2:])}` 被提及 → `{ans[int(s[2:])]}`',
        'es.sort()': lambda S, B, r: '按时间排序，同一时间 HERE（类型 2）排在后面：`' + ' '.join(f'({a},{b},{c})' for a, b, c in S.es) + '`',
        'here = 0': '`here`：到目前为止出现过多少条 HERE 消息',
        'for _, type_, i in es': lambda S, B, r: ('第二遍：按时间顺序扫 `es`，统计 `here`' if False else
                                                  ('第二遍扫完了' if '_' in B and (S._, S.type_, S.i) == (B._, B.type_, B.i) else f'事件 `({S._}, {S.type_}, {S.i})`')),
        'if type_ == 2': lambda S, B, r: ('这是一条 HERE：数一下 `here`' if S.type_ == 2 else '是离线/上线事件'),
        'here += 1': '`here = {here}`：HERE 消息又多了一条',
        'ans[i] += type_ * here': lambda S, B, r: (f'用户 `{S.i}` 离线：加上此前的 HERE 数 `here = {S.here}`，上线时再减当时的 `here`，差就是离线期间的 HERE 数，`ans[{S.i}] = {S.ans[S.i]}`' if S.type_ == 1 else
                                                    f'用户 `{S.i}` 上线：减去 `here = {S.here}`，与离线时加的相抵，净扣掉离线期间的 HERE，`ans[{S.i}] = {S.ans[S.i]}`'),
        'for i in range(numberOfUsers)': lambda S, B, r: ('每个人都加完了' if S.i == B.get('i') and S.i == S.numberOfUsers - 1 else f'最后给用户 `{S.i}` 加上 `all`（所有 ALL 和 HERE）'),
        'ans[i] += all': '用户 `{i}` 加上 `all = {all}` → `{ans[i]}`',
        'return ans': '各用户被提及次数：`{ans}`',
    },
    cards=dict(
        one_liner='HERE 先全算，再把每个人离线期间的 HERE 次数减掉',
        complexity='时间 `O(n + m log m + L)`，空间 `O(n + m)`',
        problem=['`MESSAGE` 事件提及一批用户：`id…` / `ALL`（所有人，含离线）/ `HERE`（仅在线用户）',
                 '`OFFLINE` 事件让某用户离线 60 个单位时间，同一时刻先处理状态变更再处理消息',
                 '求每个用户被提及的次数',
                 '本视频：3 个用户，5 个事件 → `[3,4,3]`'],
        quote='对于 HERE 消息：先认为所有用户都被提及了，把 all 加一。此刻离线的用户不能被计入，需要把这些用户的提及次数减一。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['离线的用户在 `[5,64]` 收到的 HERE 数 = `[0,64]` 的 HERE 数 − `[0,4]` 的 HERE 数，借鉴==前缀和==',
              '离线、上线、HERE 混在一起按时间排序，同一时刻 HERE 排后面',
              '遍历时统计 `here`，离线时 `+here`，上线时 `−here`，一加一减正好是离线期间的 HERE 数'],
        summary=['时间 `O(n + m log m + L)`，空间 `O(n + m)`',
                 '易错：同一时刻的状态变更要先于消息，所以 HERE 的类型编号 2 最大，排序时排在后面',
                 '上线时刻是 `cur_t + 60`：恰好在 `t+60` 的 HERE 能提及到该用户',
                 '方法一（暴力模拟）：按 (时间, 类型) 排序，用 `online_t` 记录下次在线时间，HERE 时逐个判断 `online_t[i] <= cur_t`'],
    ),
)
