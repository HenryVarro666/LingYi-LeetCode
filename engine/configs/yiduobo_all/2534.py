def _who(S):
    return f"{S['now']}"


CONFIG = dict(
    num=2534, title='通过门的时间', difficulty='Hard', category='模拟',
    author='yiduobo', technique='逐秒模拟 + 两个堆 + 记录上一秒状态',
    tags=['常用数据结构'],
    code='''
class Solution(object):
    def timeTaken(self, arrival, state):

        waiting_in = []
        waiting_out = []
        pre = None
        now = 0
        p = 0
        n = len(arrival)

        res = [0] * n
        while p < n or waiting_in or waiting_out:
            while p < n and arrival[p] == now:
                if state[p] == 0:
                    heapq.heappush(waiting_in, p)
                else:
                    heapq.heappush(waiting_out, p)
                p += 1
            
            if waiting_in:
                if waiting_out:
                    if pre == 0:
                        index = heapq.heappop(waiting_in)
                    else:
                        index = heapq.heappop(waiting_out)
                else:
                    index = heapq.heappop(waiting_in)
                    pre = 0

            elif waiting_out:
                index = heapq.heappop(waiting_out)
                pre = 1

            else:
                index = None
                pre = None

            if index is not None:
                res[index] = now
            
            now += 1
        
        return res
''',
    call='Solution().timeTaken([0,1,1,2,4], [0,1,0,0,1])',
    expect=[0, 3, 1, 2, 4],
    views=[
        dict(type='text', size=26, h=50, fn=lambda S: (
            f"第 =={S['now']}== 秒　上一秒：" + {None: '没人用门', 0: '进', 1: '出'}[S['pre']]
            + (f"　本秒通过：==人 {S['index']}==" if S.get('index') is not None else ''))
            if 'now' in S and 'pre' in S else ''),
        dict(type='array', var='arrival', label='arrival（到达时间；绿 = 想进，橙 = 想出）', pointers={'p': 'blue'}, h=190,
             color=lambda S, i, v: ('green' if S['state'][i] == 0 else 'orange') if 'state' in S else None,
             dim=lambda S, i, v: i < S['p'] if 'p' in S else False),
        dict(type='heap', var='waiting_in', label='waiting_in（想进）', h=110),
        dict(type='heap', var='waiting_out', label='waiting_out（想出）', h=110),
        dict(type='array', var='res', label='res（过门时间）', h=125,
             color=lambda S, i, v: 'yellow' if S.get('index') == i and v == S.get('now') and i != 0 or (i == 0 and S.get('index') == 0 and S.get('now') == 0) else None),
    ],
    watch=[('now', 'now', 'blue'), ('pre', 'pre', 'purple'), ('p', 'p', 'cyan'), ('index', 'index', 'yellow')],
    captions={
        6: '`pre` 记录==上一秒==门的使用：`None` 没人用，`0` 进，`1` 出',
        'now = 0': '从第 `0` 秒开始，一秒一秒往后推',
        'res = [0]': '`res[i]` 将保存第 `i` 个人过门的时间',
        'while p < n or': lambda S, B, r: (f'还有人没到（`p={S.p}`）或还有人在排队 → 继续这一秒' if (S.p < S.n or S.waiting_in or S.waiting_out)
                                         else '人都到了，两个队列也空了 → 结束'),
        'while p < n and arrival': lambda S, B, r: (f'`arrival[{S.p}] = {S.arrival[S.p]}` 等于现在 `{S.now}` → 这个人来了' if S.p < S.n and S.arrival[S.p] == S.now
                                                   else '这一秒没有新人到达'),
        'if state[p] == 0': lambda S, B, r: (f'`state[{S.p}] = 0`：想进 → 放进 `waiting_in`' if S.state[S.p] == 0
                                            else f'`state[{S.p}] = 1`：想出 → 放进 `waiting_out`'),
        'heapq.heappush(waiting_in': '人 `{B.p}` 入队 `waiting_in`，堆顶总是下标最小（最早到）的',
        'heapq.heappush(waiting_out': '人 `{B.p}` 入队 `waiting_out`',
        'p += 1': '`p` → {p}',
        'if waiting_in:': lambda S, B, r: ('有人想进，再看出口队列有没有人' if S.waiting_in else '没有人想进 → 看有没有人想出'),
        21: lambda S, B, r: ('两边都有人：==按上一秒的使用方向决定==' if S.waiting_out else '只有想进的人 → 让他们进'),
        'elif waiting_out:': lambda S, B, r: ('没人想进、有人想出 → 让想出的人走' if S.waiting_out else '两个队列都空 → 门空闲'),
        'if pre == 0': lambda S, B, r: ('上一秒是进 → 这一秒==继续让进的人先走==' if S.pre == 0
                                        else f'上一秒是 `{ {None: "没人用", 1: "出"}[S.pre] }` → 这一秒==出的人优先=='),
        'index = heapq.heappop(waiting_in)': '`waiting_in` 弹出堆顶：人 `{index}` 进门',
        'index = heapq.heappop(waiting_out)': '`waiting_out` 弹出堆顶：人 `{index}` 出门',
        'pre = 0': '只有进的人可用 → 人 `{index}` 进门，`pre = 0`',
        'pre = 1': '只有出的人可用 → 人 `{index}` 出门，`pre = 1`',
        'index = None': '这一秒没人排队 → 门空闲',
        36: '门空闲，`pre` 重置为 `None`（下一秒没有优先级）',
        'if index is not None': lambda S, B, r: ('有人通过门 → 记录时间' if S.index is not None else '门空闲 → 不更新答案'),
        'res[index] = now': '人 `{index}` 在第 `{now}` 秒过门：`res[{index}] = {now}`',
        'now += 1': '时间前进到第 `{now}` 秒',
        'return res': '全部安排完 → 返回 `{ret}`',
    },
    cards=dict(
        one_liner='一秒一秒推进，两个堆排队，用 pre 记住上一秒的方向',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`n` 个人排队过一扇门，每人有到达时间 `arrival[i]` 和意图 `state[i]`（0 进，1 出）',
                 '同一秒只能一人过门；多人想用时：上一秒用了方向的优先，否则出优先，同方向下标小的先',
                 '示例：`[0,1,1,2,4]`、`[0,1,0,0,1]` → `[0,3,1,2,4]`'],
        quote='每个人的到达时间都不超过n，因此在最坏情况下排队时间不会超过2n，因此可以直接暴力遍历时间点now而不需要去计算选取。',
        quote_src='—— yiduobo 题解原文',
        idea=['两个等待队列 `waiting_in` / `waiting_out`，用最小堆保证下标小的先走',
              '用变量 `pre` 记录上一秒门的状态，决定两边都有人时谁先',
              '没人用门时 `pre = None`，下一秒按默认（出优先）'],
        summary=['时间 `O(n log n)`（每人进出堆一次），空间 `O(n)`',
                 '易错点：门空闲的那一秒要把 `pre` 重置为 `None`',
                 '到达时间 `<= n`，所以逐秒枚举最多约 `2n` 秒',
                 '原文就是 Python 3 可运行的写法，`heapq` 由环境注入'],
    ),
)
