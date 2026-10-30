TK = [2, 3, 1]
ST = 3


def _names(S, x):
    t = S['tasks']
    return '{' + ','.join(str(t[i]) for i in range(len(t)) if x >> i & 1) + '}'


def _col(S, i, v):
    ns = S.get('now_state')
    if ns is None or S.get('_line', 0) < 14:
        return None
    if S.get('index') == i and S.get('_line', 0) >= 17:
        return 'pink'
    if ns >> i & 1:
        return 'blue'
    return None


def _txt(S):
    ns = S.get('now_state')
    if ns is None or 'used_part_time' not in S or S.get('_line', 0) < 16:
        return '`f[state]`：做完 state 里的任务最少要多少小时（按“排满一个时间段再开新的”累计）'
    u = S['used_part_time']
    s = f"当前 `state={ns:03b}` = =={_names(S, ns)}==，已花 `f={S['f'][ns]}` 小时，最后一个时间段用了 `{u}` 小时"
    return s


def _c_if(S, B, ret):
    t, u = S.tasks[S.index], S.used_part_time
    if t + u <= S.sessionTime:
        return f'`{t} + {u} = {t + u} <= {S.sessionTime}`：任务 {t} 还能塞进当前时间段 → 直接累加'
    return f'`{t} + {u} = {t + u} > {S.sessionTime}`：当前时间段放不下任务 {t} → ==新开一个时间段=='


def _c_next(S, B, ret):
    t, u, ns = S.tasks[S.index], S.used_part_time, S.now_state
    if t + u <= S.sessionTime:
        return f'`next_time = {S.f[ns]} + {t}` = =={S.next_time}=='
    return f'`next_time = {S.f[ns]} - {u} + {S.sessionTime} + {t}` = =={S.next_time}==：把没用完的 {S.sessionTime - u} 小时补齐，再做任务 {t}'


def _c_upd(S, B, ret):
    nx = S.next_state
    if nx in B.f and B.f[nx] != S.f[nx]:
        return f'`f[{nx:03b}]` 已有 `{B.f[nx]}`，取更小的 `{S.next_time}` → ==更新== 为 `{S.f[nx]}`'
    return f'`f[{nx:03b}]` 已有 `{B.f[nx]}`，`{S.next_time}` 不更小 → 不变'


CONFIG = dict(
    num=1986, title='完成任务的最少工作时间段', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='状压 DP · 记录总小时数 (BFS)',
    tags=['灵神题单·动态规划', '难度分 1877'],
    code='''
class Solution(object):
    def minSessions(self, tasks, sessionTime):

        n = len(tasks)
        max_state = (1 << n)
        f = {}
        f[0] = 0
        q = [0]
        l = 0
        r = 1

        while l < r:
            now_state = q[l]
            l += 1
            used_part_time = f[now_state] % sessionTime
            for index in range(n):
                if (now_state & (1 << index)) == 0:
                    next_state = now_state | (1 << index)
                    if tasks[index] + used_part_time <= sessionTime:
                        next_time = f[now_state] + tasks[index]
                    else:
                        next_time = f[now_state] - used_part_time + sessionTime + tasks[index]
                    
                    if next_state not in f:
                        f[next_state] = next_time
                        q.append(next_state)
                        r += 1
                    else:
                        f[next_state] = min(f[next_state], next_time)
        
        res = f[max_state - 1] // sessionTime
        if f[max_state - 1] % sessionTime != 0:
            res += 1
        return res
''',
    call=f'Solution().minSessions({TK}, {ST})',
    expect=2,
    skip=['l += 1', 'r += 1', 'l = 0', 'r = 1', 'q = [0]', 'while l < r', 'for index in range', 'max_state = '],
    max_steps=50,
    views=[
        dict(type='array', var='tasks', label='tasks（蓝 = 已做的，粉 = 正要加入的）', h=190, cell=100, color=_col),
        dict(type='text', fn=_txt, size=24, h=80),
        dict(type='map', var='f', label='f[state]：已用总小时数（key 是二进制状态）', fmt=lambda k, v: f'{k:03b} → {v}', h=320, font=30),
    ],
    watch=[('now_state', 'now_state', 'blue'), ('used_part_time', 'used_part_time', 'cyan'), ('next_state', 'next_state', 'pink'),
           ('next_time', 'next_time', 'green')],
    captions={
        'f[0] = 0': '`f[0] = 0`：没做任何任务，用时 0 小时；`f[state]` 记的是==总小时数==而不是时间段数',
        'now_state = q[l]': '取出队首状态 `now_state = {now_state}`（二进制 `{now_state:03b}`）',
        'used_part_time =': '`used_part_time = f[{now_state}] % {sessionTime}` = =={used_part_time}==：最后一个时间段已经用了的小时数',
        'if (now_state & (1 << index)) == 0': lambda S, B, r: (f'任务 `{S.tasks[S.index]}`（第 {S.index} 个）还没做 → 尝试把它加进来'
                                                              if S.now_state >> S.index & 1 == 0
                                                              else f'任务 `{S.tasks[S.index]}` 已经在 state 里 → 跳过'),
        'next_state = now_state |': '`next_state = {next_state:03b}`：state 加上第 `{index}` 个任务',
        'if tasks[index] + used_part_time': _c_if,
        'next_time = f[now_state] + tasks[index]': _c_next,
        'next_time = f[now_state] - used_part_time': _c_next,
        'if next_state not in f': lambda S, B, r: ('`next_state` 第一次出现 → 直接记录，并入队' if S.next_state not in S.f
                                                   else '`next_state` 已经有值 → 取更小的'),
        'f[next_state] = next_time': '`f[{next_state}] = {next_time}`，`next_state` 入队，之后它也要向外扩展',
        'f[next_state] = min': _c_upd,
        'res = f[max_state - 1]': '总共需要 `f[{max_state - 1}] = {f[max_state - 1]}` 小时 → 除以 `{sessionTime}` 得 =={res}== 个时间段',
        'if f[max_state - 1] %': '`{f[max_state - 1]} % {sessionTime} = {f[max_state - 1] % sessionTime}`：有余数才要再多一个时间段',
        'return res': '至少需要 `{res}` 个工作时间段',
    },
    cards=dict(
        one_liner='f 记小时数：放得下就累加，放不下就先补满再开新段',
        complexity='时间 `O(n·2^n)`，空间 `O(2^n)`',
        problem=['`tasks[i]` 是任务耗时，一个工作时间段最多连续工作 `sessionTime` 小时',
                 '一个任务必须在同一个时间段内做完，顺序随意，求最少时间段数',
                 '本视频：`tasks=[2,3,1], sessionTime=3` → `2`'],
        quote='令f[state]表示选择state中的任务所需的最少工作时间，这里的保存的是具体的小时而不是时间段的数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['`used_part_time = f[state] % sessionTime`：最后一段已用的小时',
              '放得下：`f[next] = f[state] + tasks[i]`',
              '放不下：`f[state] - used + sessionTime + tasks[i]`，把当前段补满再开新段',
              '最后 `f[全集] / sessionTime` 向上取整就是时间段数'],
        summary=['时间 `O(n·2^n)`，空间 `O(2^n)`（本题 n ≤ 14）',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '按“小时数”记录能让 `%` 直接求出最后一段已用多少，这是它的关键技巧',
                 '用 BFS 队列按状态从小到大扩展，每个状态入队一次'],
    ),
)
