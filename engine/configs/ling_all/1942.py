def _T(S):
    """要画几个时刻（0 .. 最大离开时刻）"""
    return max(t[1] for t in S['times']) + 1


def _tcol(S):
    """当前 e 是 events 里的第几个时刻（e 就是 events[t] 这个列表本身，按身份找）"""
    e = S.get('e')
    if e is None or S.get('events') is None:
        return None
    for k, x in enumerate(S['events'][:_T(S)]):
        if x is e:
            return k
    return None


def _grid(S):
    ev, T = S['events'], _T(S)
    return [[('f' + ','.join(map(str, ev[t][w]))) if ev[t][w] else '' for t in range(T)] for w in (0, 1)]


def _cols(S):
    return list(range(_T(S))) if 'times' in S else []


def _info(S):
    t, e = _tcol(S), S.get('e')
    if t is None or e is None:
        return '每个时刻先让离开的人==还椅子==，再让到达的人==领最小编号的空椅子=='
    if not e[0] and not e[1]:
        return f'时刻 `{t}`：没有人到达也没有人离开'
    parts = []
    if e[0]:
        parts.append('离开 ' + '、'.join(f'朋友{x}' for x in e[0]))
    if e[1]:
        parts.append('到达 ' + '、'.join(f'朋友{x}' for x in e[1]))
    return f'时刻 `{t}`：==先离开，后到达==：' + '；'.join(parts)


CNT = {}


def _id_step(S, which):
    """for id in e[which] 这一行：返回 (这是第几次执行, 本次迭代的朋友编号或 None=循环结束)"""
    t = _tcol(S)
    k = CNT.get((t, which), 0)
    CNT[(t, which)] = k + 1
    lst = S.e[which]
    return (k, lst[k]) if k < len(lst) else (k, None)


def _for_e(S, B, ret):
    t, e = _tcol(S), S.e
    if not e[0] and not e[1]:
        return f'时刻 `{t}`：没有人到达或离开，空转一格'
    return f'扫描到时刻 `{t}`：离开栏 `{e[0]}`，到达栏 `{e[1]}`'


def _for_leave(S, B, ret):
    k, who = _id_step(S, 0)
    if who is None:
        return '离开栏处理完了' if k else '这个时刻没人离开'
    tail = '；==同一时刻先离开、后到达==，空出的椅子马上能给新来的人' if S.e[1] else ''
    return f'朋友 `{who}` 在时刻 `{_tcol(S)}` 离开{tail}'


def _for_arrive(S, B, ret):
    k, who = _id_step(S, 1)
    if who is None:
        return '到达栏处理完了' if k else '这个时刻没人到达'
    return f'朋友 `{who}` 在时刻 `{_tcol(S)}` 到达，要找椅子'


def _if_target(S, B, ret):
    if S.id == S.targetFriend:
        return f'`id = {S.id}` 就是 `targetFriend` → ==找到了==，返回他的椅子编号'
    return f'`id = {S.id}` 不是 `targetFriend = {S.targetFriend}`，继续扫描'


def _for_init(S, B, ret):
    if 'i' in B and B.i == S.i:
        return '`unoccupied` 填成了 `0 .. n-1`：升序数组本身就是合法的最小堆'
    return f'给第 `{S.i}` 张椅子编号'


def _for_build(S, B, ret):
    if 'i' in B and B.i == S.i:
        return '所有朋友的到达、离开事件都登记好了'
    return f'登记朋友 `{S.i}`：到达 `{S.t[0]}`，离开 `{S.t[1]}`'


CONFIG = dict(
    num=1942, title='最小未被占据椅子的编号', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='事件扫描 + 最小堆（Go 原文转写）',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1695'],
    code='''
class Solution:
    def smallestChair(self, times: List[List[int]], targetFriend: int) -> int:
        # 按时间顺序，记录每个到达事件和离开事件相对应的朋友编号
        events = [[[], []] for _ in range(10 ** 5 + 1)]
        for i, t in enumerate(times):
            l, r = t[0], t[1]
            events[l][1].append(i)  # 朋友到达
            events[r][0].append(i)  # 朋友离开

        # 初始化未被占据的椅子
        n = len(times)
        unoccupied = [0] * n
        for i in range(len(unoccupied)):
            unoccupied[i] = i

        # 按时间顺序扫描每个事件
        belong = [0] * n
        for e in events:
            for id in e[0]:  # 朋友离开
                heappush(unoccupied, belong[id])  # 返还椅子
            for id in e[1]:  # 朋友到达
                belong[id] = heappop(unoccupied)  # 记录占据该椅子的朋友编号
                if id == targetFriend:
                    return belong[id]
        return 0
''',
    call='Solution().smallestChair([[1,4],[2,3],[3,6],[4,7]], 3)',
    expect=0,
    max_events=150000, snap_maxlen=10, max_steps=80,
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='table', var=_grid, rows=['离开', '到达'], cols=_cols, cell=60, h=200,
             label='events[t] = [离开的朋友, 到达的朋友]（只画前几个时刻，黄框 = 当前扫描到的 t）',
             cursors=[(0, _tcol, 'yellow'), (1, _tcol, 'yellow')],
             color=lambda S, i, j, v: ('pink' if i == 0 else 'blue') if v else None),
        dict(type='heap', var='unoccupied', label='unoccupied：未被占据的椅子（最小堆，堆顶 = 编号最小）', top_color='green', h=110),
        dict(type='array', var='belong', label='belong[id]：朋友 id 占据的椅子（橙 = 目标朋友）', cell=100,
             pointers={'id': 'pink'}, color=lambda S, k, v: 'orange' if k == S.get('targetFriend') else None, h=170),
    ],
    watch=[('t', lambda S: _tcol(S), 'blue'), ('id', lambda S: S.get('id'), 'pink'), ('belong[id]', lambda S: S['belong'][S['id']] if 'id' in S and 'belong' in S else None, 'green'),
           'targetFriend'],
    captions={
        'events = [': lambda S, B, r: f'`events[t]` 记下时刻 `t` 离开、到达的朋友；时刻最大 `10^5`，所以开 `10^5 + 1` 栏（Go 的 `make(..., 1e5+1)`），这里只画前 {_T(S)} 栏',
        'for i, t in enumerate': _for_build,
        'l, r = t[0], t[1]': '`l = {l}` 是到达时刻，`r = {r}` 是离开时刻',
        'events[l][1].append': '时刻 `{l}` 的==到达栏==记下朋友 `{i}`',
        'events[r][0].append': '时刻 `{r}` 的==离开栏==记下朋友 `{i}`',
        'n = len(times)': '`n = {n}`：最多 `n` 个人同时在场，准备 `n` 张椅子就够了',
        'unoccupied = [0] * n': '先开一个长为 `n` 的数组，下面填上椅子编号',
        'for i in range(len(unoccupied))': _for_init,
        'unoccupied[i] = i': '`unoccupied[{i}] = {i}`：椅子 `{i}` 目前是空的',
        'belong = [0] * n': '`belong[id]` 记录朋友 `id` 占据的椅子编号',
        'for e in events': _for_e,
        'for id in e[0]': _for_leave,
        'heappush(unoccupied': '朋友 `{id}` 坐的椅子是 `{belong[id]}` → 还回堆里：`unoccupied = {unoccupied}`',
        'for id in e[1]': _for_arrive,
        'belong[id] = heappop': '堆顶就是==编号最小的空椅子==：朋友 `{id}` 坐 `{belong[id]}` 号，`unoccupied = {unoccupied}`',
        'if id == targetFriend': _if_target,
        'return belong[id]': '目标朋友 `{id}` 坐的是 =={ret}== 号椅子，提前返回',
    },
    cards=dict(
        one_liner='按时间扫描事件：离开还椅子进堆，到达从堆顶领最小的',
        complexity='时间 `O(U + n log n)`，`U = 10^5` 是时刻数；空间 `O(U + n)`',
        problem=['`n` 个朋友依次到达派对，每人坐==编号最小==的空椅子；离开时椅子立刻空出',
                 '同一时刻有人离开又有人到达，椅子可以直接复用',
                 '给定每人的 `[到达, 离开]`，求 `targetFriend` 坐的椅子编号',
                 '本视频：`[[1,4],[2,3],[3,6],[4,7]]`，目标 `3` → `0`'],
        quote='按时间顺序，记录每个到达事件和离开事件相对应的朋友编号 …… 按时间顺序扫描每个事件：朋友离开，返还椅子；朋友到达，记录占据该椅子的朋友编号。',
        quote_src='—— 灵茶山艾府题解代码注释（原文为 Go）',
        idea=['`events[t] = [离开的人, 到达的人]`：按时刻排好事件，不用排序',
              '`unoccupied` 是最小堆，初始放 `0 .. n-1` 号椅子',
              '每个时刻==先处理离开==：`heappush` 还椅子；==再处理到达==：`heappop` 领最小编号',
              '扫到 `targetFriend` 到达时，他领到的椅子就是答案'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`make([][2][]int, 1e5+1)` → 列表推导式，Go 的 `hp` 堆类型 → `heapq`；原文另有 bitset 写法，这里用堆）',
                 '时间 `O(U + n log n)`：`U = 10^5` 是时间轴长度，每人一次入堆、一次出堆',
                 '易错：同一时刻==先离开后到达==，所以离开栏要放在到达栏之前处理',
                 '椅子最多用到 `n` 张，所以堆初始有 `n` 个编号就够',
                 '视频里 `events` 只画前几栏，后面全是空栏（返回后不再扫描）'],
    ),
)
