REQ = [[0, 5], [0, 1], [6, 3]]


def _rq(S):
    r = S.get('requests')
    return [f'{a},{b}' for a, b in r] if r else None


def _cell(S, r, c, v):
    st, la = S.get('state'), S.get('last')
    if st is None or la is None:
        return None
    if (r, c) == (st, la):
        return 'yellow'
    ps, pl = S.get('pre_state'), S.get('pre_last')
    if ps and pl is not None and (r, c) == (ps, pl) and S.get('_line', 0) >= 19:
        return 'blue'
    return None


def _formula(S):
    st, la = S.get('state'), S.get('last')
    if st is None or la is None or 'requests' not in S:
        return '`f[state][last]`：已完成 `state` 里的请求，电梯停在 `last` 的楼层，最短时间'
    m = len(S['requests'])
    done = ','.join(str(k) for k in range(m) if st >> k & 1)
    return f'`state` = {st:0{m}b}，完成 {{{done}}}，最后停在 `{la}`'


CONFIG = dict(
    num=4027, title='电梯请求 III', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状压 DP · f[state][last]',
    tags=['状压 DP'],
    code='''
class Solution(object):
    def elevatorRequests(self, n, start, requests):
        
        m = len(requests)
        max_state = 1 << m
        f = [[None] * m for _ in range(max_state)]
        

        for state in range(1, max_state):
            for last in range(m):
                if (state & (1 << last)) == (1 << last):
                    arr, floor = requests[last]
                    pre_state = state ^ (1 << last)
                    if pre_state == 0:
                        f[state][last] = max(abs(floor - start), arr)
                    else:
                        for pre_last in range(m):
                            if (pre_state & (1 << pre_last)) == (1 << pre_last):
                                pre_floor = requests[pre_last][1]
                                cost = max(arr, f[pre_state][pre_last] + abs(floor - pre_floor))
                                if f[state][last] is None or f[state][last] > cost:
                                    f[state][last] = cost
        
        return min(f[-1])
''',
    call=f'Solution().elevatorRequests(7, 3, {REQ!r})',
    expect=8,
    skip=['for last in range', 'for pre_last in range', 'if (state & (1 << last))', 'if (pre_state & (1 << pre_last))',
          'arr, floor = requests', 'pre_floor = requests', 'pre_state = state', 'f[state][last] = cost', 'if f[state][last] is None or', 'max_state = '],
    max_steps=90,
    views=[
        dict(type='array', var=_rq, label='requests：到达,楼层', h=240, cell=100, pointers={'last': 'yellow', 'pre_last': 'blue'}),
        dict(type='text', fn=_formula, size=22, h=50),
        dict(type='table', var='f', label='f[state][last]（行 = 已完成集合，黄 = 正在算，蓝 = 前置状态）', h=380, cell=48,
             rows=lambda S: [format(k, f"0{len(S['requests'])}b") for k in range(len(S['f']))], cols=lambda S: list(range(len(S['requests']))),
             color=_cell),
    ],
    watch=[('state', 'state', 'yellow'), ('last', 'last', 'yellow'), ('pre_state', 'pre_state', 'blue'), ('pre_last', 'pre_last', 'blue'), ('cost', 'cost', 'green')],
    captions={
        'm = len': '请求只有 `{m}` 个，可以用二进制位表示「完成了哪些」',
        'f = [[None]': '`f[state][last]`：完成 `state` 里的请求、最后停在请求 `last` 所在楼层的最短时间；`None` = 还没算',
        'for state in range': lambda S, B, r: (f'`state = {S.state:03b}`：从小到大枚举集合，保证前置集合已算好' if S.get('state') != B.get('state') else '所有集合都算完了'),
        'if pre_state == 0': lambda S, B, r: (f'`last = {S.last}`：去掉这一位，`pre_state = {S.pre_state:03b}` 为空 → 它是==第一个==处理的请求' if S.pre_state == 0 else f'`last = {S.last}`：去掉这一位，`pre_state = {S.pre_state:03b}` 非空 → 枚举上一个处理的请求 `pre_last`'),
        'f[state][last] = max(abs': '第一个请求：从 `start={start}` 走到楼层 `{floor}` 要 `{abs(floor-start)}` 秒，请求要到时刻 `{arr}` 才出现 → `max` = =={f[state][last]}==',
        'cost = max(arr': '上一个是请求 `{pre_last}`：到楼层 `{floor}` 最早 `{f[pre_state][pre_last]} + |{floor}−{pre_floor}|` = {f[pre_state][pre_last] + abs(floor-pre_floor)}；到达时间 `{arr}` 之前要等 → `max` = =={cost}==；`f[{state}][{last}]` 取各个 `pre_last` 里的最小',
        'return min(f[-1])': '全集 `f[-1]` 里最后停在哪个请求都可以：取最小 =={ret}==',
    },
    cards=dict(
        one_liner='只有 16 个请求：二进制记录「完成了谁」，最后停在谁',
        complexity='时间 `O(m^2 · 2^m)`，空间 `O(m · 2^m)`',
        problem=['电梯在 `start`，每秒上、下一层或停留；请求 `[arrival, floor]` 在到达后、电梯在该楼层才算处理',
                 '求处理完所有请求的==最短时间==，请求最多 16 个',
                 '示例：`n=7, start=3, requests=[[0,5],[0,1],[6,3]]` → `8`'],
        quote='与之前的版本相比，这次有了arrival这一项，因此之前的做法就不再使用了……好在本题的数据规模较小，因此可以使用状态压缩。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[state][last]`：完成 `state` 中的请求，最后停在 `last` 的楼层',
              '去掉 `last` 得 `pre_state`，枚举上一个 `pre_last`，移动时间 `|floor − pre_floor|`',
              '到了请求还没来就等：`max(arr, 上一个时间 + 移动)`'],
        summary=['时间 `O(m^2 · 2^m)`，空间 `O(m · 2^m)`',
                 '`pre_state == 0` 是第一个请求，从 `start` 出发',
                 '`None` 表示未赋值，`f[state][last] is None or …` 先判空再比较',
                 '原文 `class Solution(object)` 是 Python 2 风格，但代码无需修改即可在 Python 3 运行',
                 '对比灵神：灵神主推「区间 DP」（逆过程）+ 状压两种，yiduobo 只用状压'],
    ),
)
