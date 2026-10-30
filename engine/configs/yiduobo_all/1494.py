def _b(x, n=4):
    return format(x, f'0{n}b')


def _set(x, n=4):
    s = [str(j + 1) for j in range(n) if x >> j & 1]
    return '{' + ','.join(s) + '}' if s else '{}'


def _top(S):
    if 'now_state' not in S:
        return '`f[state]` = 学完 `state` 这些课的最少学期数（BFS 从空集往全集扩展）'
    ns = S['now_state']
    s = f'当前状态 `{_b(ns)}`：已学 =={_set(ns)}=='
    if 'candidate' in S and S['_line'] >= 25:
        s += '，可学 ' + '{' + ','.join(str(c.bit_length()) for c in S['candidate']) + '}'
    return s


def _fcolor(S, k, v):
    if 'now_state' not in S:
        return None
    if k == S['now_state']:
        return 'yellow'
    if S['_line'] >= 40 and 'next_state' in S and k == S['next_state']:
        return 'green'
    return 'green' if v is not None else None


def _qcolor(S, k, v):
    if 'l' in S and k == S['l'] - 1:
        return 'yellow'
    if 'l' in S and k >= S['l']:
        return 'blue'
    return None


def _choose(S, B, ret):
    ch = sorted(S['choose'])
    show = ' '.join(_b(c) for c in ch[:4]) + (' …' if len(ch) > 4 else '')
    return f'凑出 {S["index"] + 1} 门的选法共 {len(ch)} 种：{show}'


CONFIG = dict(
    num=1494, title='并行课程 II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状压 DP · 类 BFS 扩展状态',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def minNumberOfSemesters(self, n, relations, k):

        max_state = (1 << n) - 1
        prev_state = [0] * n
        for x, y in relations:
            x -= 1
            y -= 1
            prev_state[y] |= 1 << x
        
        f = [None] * (max_state + 1)
        f[0] = 0
        q = [0]
        l = 0
        r = 1
        while l < r:
            now_state = q[l]
            l += 1

            candidate = []
            for index in range(n):
                if (now_state & (1 << index) == 0) and (now_state & prev_state[index] == prev_state[index]):
                    candidate.append(1 << index)
            
            choose = set([0])
            for index in range(k):
                tmp = set()
                for x in choose:
                    for y in candidate:
                        if x & y == 0:
                            tmp.add(x | y)
                
                if len(tmp) == 0:
                    break

                choose = tmp
            
            for choose_state in choose:
                next_state = now_state | choose_state
                if f[next_state] is None or f[next_state] > f[now_state] + 1:
                    f[next_state] = f[now_state] + 1
                    if next_state not in q:
                        q.append(next_state)
                        r += 1

        return f[-1]
''',
    call='Solution().minNumberOfSemesters(4, [[1,4],[2,4]], 2)',
    expect=2,
    skip=['x -= 1', 'y -= 1', 'for x in choose', 'for y in candidate', 'tmp = set()', 'choose = set([0])',
          'for index in range(n)', 'for index in range(k)', 'if x & y == 0', 'tmp.add', 'candidate = []', 'l += 1',
          'for x, y in', 'if (now_state &', 'for choose_state in choose', 'r += 1', 'if len(tmp) == 0', 'break', 'if f[next_state] is None', 'if next_state not in q'],
    max_steps=110,
    views=[
        dict(type='text', fn=_top, size=24, h=70),
        dict(type='array', var='f', label='f[state]（下标 = 已学课程集合；空 = 还没到达）', h=200, cell=70,
             pointers={'now_state': 'blue'}, color=_fcolor),
        dict(type='array', var='q', label='队列 q（黄 = 正在处理，蓝 = 等待处理）', h=200, cell=70, color=_qcolor),
        dict(type='array', var='prev_state', label='prev_state[index]：课程 index+1 的前置课程位掩码', h=200, cell=80),
    ],
    watch=[('now_state', 'now_state', 'blue'), ('next_state', 'next_state', 'green'), ('k', 'k', 'yellow')],
    captions={
        'max_state =': '全集 `max_state = {max_state}`：{n} 门课全部学完',
        'prev_state[y] |=': '课程 `{y+1}` 的前置课程集合 `prev_state[{y}] = {prev_state[y]}`',
        'f = [None]': '`f[state]` 先设为 None：还没到达过这个状态',
        'f[0] = 0': '起点：什么都没学，用了 0 个学期',
        'q = [0]': '队列里先放入起点状态 `0`',
        'while l < r': lambda S, B, r: (f'队列里还有状态要处理（`l={S.l}` < `r={S.r}`）' if S.l < S.r else '队列空了：所有可达状态都处理过'),
        'now_state = q[l]': '取出队首 `now_state = {now_state}`（二进制 `' + '{format(now_state, "04b")}' + '`）：已学 {_set(now_state)}',
        'candidate.append': '课程 `{index+1}` 没学过，且前置课程都学过 → ==可学==',
        'choose = tmp': _choose,
        'next_state = now_state | choose_state': lambda S, B, r: (
            f'学 `{_b(S.choose_state)}` → 到达 `{_b(S.next_state)}`（已学 {_set(S.next_state)}）'
            + ('，==第一次到达== → 记下学期数' if S.f[S.next_state] is None
               else f'，已有 `f = {S.f[S.next_state]}`，不比 `{S.f[S.now_state] + 1}` 更好 → 不动')),
        'f[next_state] = f[now_state] + 1': '更新 `f[{next_state}] = f[{now_state}] + 1` = =={f[next_state]}==',
        'q.append': '`{next_state}` 第一次出现 → 加入队尾，以后再从它扩展',
        'return f[-1]': '全集 `f[{max_state}]` = =={ret}== 个学期',
    },
    cards=dict(
        one_liner='没有贪心解：用二进制状态 + 类 BFS，每学期扩展一步',
        complexity='时间 `O(3^n)`，空间 `O(2^n)`',
        problem=['`n` 门课，`relations` 给出先修关系，一学期最多上 `k` 门，且先修课必须在之前的学期上完',
                 '求上完所有课最少要几个学期',
                 '示例：`n=4, relations=[[2,1],[3,1],[1,4]], k=2` → `3`',
                 '本视频：`n=4, relations=[[1,4],[2,4]], k=2` → `2`'],
        quote='相当有难度的题目。……后来我还特意去查了一些资料，发现这个问题确实是==没有贪心解==的。……课程数目只有15门，那么也可以使用状态压缩动态规划去做。',
        quote_src='—— yiduobo 题解原文',
        idea=['拓扑深度之外还多了并行度 `k`，贪心都有反例',
              '`f[state]`：学完 `state` 表示的课程所需最少时间',
              '先找可学课程 `candidate`，再凑出所有选法 `choose`',
              '受拓扑序影响，不能从 0 到 max_state 枚举 → 用队列类 BFS'],
        summary=['时间 `O(3^n)`：状态为 m 门课时选法至多 `2^m` 种，二项式定理',
                 '可学 = 没学过 + 前置课全在 `state` 里',
                 '`choose` 逐轮扩张，最多凑 k 门；不足 k 门时取到能凑的最大数',
                 '对比灵神：灵神倒着看「剩余集合」，只枚举恰好 k 门的子集；这里正着 BFS，把所有选法枚举出来',
                 '原文已是 Python 3 可运行写法，无需改动'],
    ),
)
