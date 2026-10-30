def _g(S, k):
    return S['_inner'].get(k)


def _st(v):
    return f"{v:03b}"


def _txt(S):
    inn = S['_inner']
    if 'level' not in inn or 'state' not in inn or 'n' not in S:
        return '`f[level][last][state]`：state 三位 = 前导零 / 贴 r / 贴 l'
    st = inn['state']
    return (f"第 {inn['level']} 位：last = {inn['last']}；state = {_st(st)}"
            f"（{'前导0' if st & 4 else '已开头'}，{'贴r' if st & 2 else '不贴r'}，{'贴l' if st & 1 else '不贴l'}）")


CONFIG = dict(
    num=3966, title='统计范围内的好整数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='数位 DP（state 三位：前导零 / 贴 r / 贴 l）',
    tags=['灵神题单', '动态规划', '难度分 2006'],
    code='''
class Solution(object):
    def goodIntegers(self, l, r, k):
        
        r = [int(x) for x in str(r)]
        l = [int(x) for x in str(l)]
        l = [0] * (len(r) - len(l)) + l
        n = len(l)

        f = [[[None] * 8 for _ in range(10)] for _ in range(n)]

        def calc(level, last, state, f):
            if level == n:
                return 1
            
            if f[level][last][state] is None:
                f[level][last][state] = 0
                start = 0
                end = 9

                if state & 4:
                    prefix_zero = True
                else:
                    prefix_zero = False
                    start = max(start, last - k)
                    end = min(end, last + k)

                if state & 2:
                    high_bound = True
                    end = min(end, r[level])
                else:
                    high_bound = False

                if state & 1:
                    low_bound = True
                    start = max(start, l[level])
                else:
                    low_bound = False

                for d in range(start, end + 1):
                    nxt_state = 0
                    if prefix_zero and d == 0:
                        nxt_state |= 4
                    if high_bound and d == r[level]:
                        nxt_state |= 2
                    if low_bound and d == l[level]:
                        nxt_state |= 1
                    
                    f[level][last][state] += calc(level + 1, d, nxt_state, f)
            
            return f[level][last][state]
        
        return calc(0, 0, 7, f)
''',
    call='Solution().goodIntegers(9, 14, 1)',
    expect=4,
    views=[
        dict(type='array', var=lambda S: S.get('r') if isinstance(S.get('r'), list) else None, label='r 的数位（上界）', cell=70, h=150,
             color=lambda S, i, v: 'blue' if i == S['_inner'].get('level') else None),
        dict(type='array', var=lambda S: S.get('l') if isinstance(S.get('l'), list) else None, label='l 的数位（下界，补前导 0）', cell=70, h=150,
             color=lambda S, i, v: 'blue' if i == S['_inner'].get('level') else None),
        dict(type='text', fn=_txt, size=24, h=80),
        dict(type='calls', h=240, hide=('f',)),
    ],
    watch=[('level', lambda S: _g(S, 'level'), 'blue'), ('last', lambda S: _g(S, 'last'), 'cyan'),
           ('state', lambda S: _st(_g(S, 'state')) if _g(S, 'state') is not None else None, 'pink'),
           ('start', lambda S: _g(S, 'start'), 'green'), ('end', lambda S: _g(S, 'end'), 'orange'),
           ('d', lambda S: _g(S, 'd'), 'yellow')],
    skip=['n = len(l)', 'f[level][last][state] = 0', 'start = 0', 'end = 9', 'prefix_zero = True', 'prefix_zero = False',
          'high_bound = True', 'high_bound = False', 'low_bound = True', 'low_bound = False', 'nxt_state = 0', 'else:',
          'nxt_state |= ', 'end = min(end', 'start = max(start'],
    captions={
        'l = [0] * ': '`l` 前面补 0，和 `r` 一样长：`l = {l}`，`r = {r}`',
        'f = [[[None]': '`f[level][last][state]` 记忆化；`state` 三位二进制：4 = 还在前导 0，2 = 贴着 r，1 = 贴着 l',
        'return calc(0, 0, 7, f)': lambda S, B, ret: ('从第 0 位出发：`last = 0`，`state = 111`：前导零、贴 r、贴 l 全都成立' if ret is None else f'答案 `{ret}`'),
        'if level == n': lambda S, B, ret: ('填完所有位 → 得到一个好数，返回 `1`' if S.level == S.n else f'`level = {S.level} < n`：继续填第 {S.level} 位'),
        'if f[level][last][state] is None': lambda S, B, ret: ('这个状态还没算过 → 现在算' if S.f[S.level][S.last][S.state] is None else '这个状态已经算过 → 直接返回'),
        'if state & 4': lambda S, B, ret: ('`state & 4`：还在前导 0 → 不看和 last 的差，下界 0、上界 9' if S.state & 4 else
                                           f'`state & 4 = 0`：已经开头 → 这一位必须在 `[last−k, last+k]`：下界 `{max(0, S.last - S.k)}`，上界 `{min(9, S.last + S.k)}`'),
        'if state & 2': lambda S, B, ret: (f'`state & 2`：还贴着 r → 上界再取 `min(end, r[{S.level}])` = `{min(S.end, S.r[S.level])}`' if S.state & 2 else '`state & 2 = 0`：不贴 r → 上界不变'),
        'if state & 1': lambda S, B, ret: (f'`state & 1`：还贴着 l → 下界再取 `max(start, l[{S.level}])` = `{max(S.start, S.l[S.level])}`' if S.state & 1 else '`state & 1 = 0`：不贴 l → 下界不变'),
        'for d in range': lambda S, B, ret: (
            f'`d` 枚举到上限 `end = {S.end}`，这个状态结束' if S.d >= S.end and B.get('d') == S.d and B.get('last') == S.last else
            f'枚举这一位 `d`：从 `start = {S.start}` 到 `end = {S.end}`，轮到 `d = {S.d}`'),
        'if prefix_zero and d == 0': lambda S, B, ret: ('`d = 0` 且还在前导 0 → 下一位仍是前导 0（`nxt_state |= 4`）' if S.prefix_zero and S.d == 0 else
                                                        '这一位已经不是前导 0（要么开头了要么 d > 0）'),
        'if high_bound and d == r': lambda S, B, ret: (f'`d = {S.d}` ' + ('==' if S.d == S.r[S.level] else '≠') + f' `r[{S.level}]`：' +
                                                       ('继续贴 r（`nxt_state |= 2`）' if S.high_bound and S.d == S.r[S.level] else '不再贴 r')),
        'if low_bound and d == l': lambda S, B, ret: (f'`d = {S.d}` ' + ('==' if S.d == S.l[S.level] else '≠') + f' `l[{S.level}]`：' +
                                                      ('继续贴 l（`nxt_state |= 1`）' if S.low_bound and S.d == S.l[S.level] else '不再贴 l')),
        'f[level][last][state] += calc': '填 `d = {d}`，进入下一位：`last = {d}`，`nxt_state = {nxt_state:03b}`',
        'return f[level][last][state]': '这个状态的好数个数 `{f[level][last][state]}`',
    },
    max_steps=80,
    cards=dict(
        one_liner='三位 state 同时记住：前导 0、贴 r、贴 l',
        complexity='时间 `O(D²·log r)`，空间 `O(D·log r)`，`D = 10`',
        problem=['给 `l, r, k`：相邻数位绝对差都 `≤ k` 的数是好数，求 `[l, r]` 内好数个数',
                 '示例：`l=10, r=15, k=1` → `3`（10、11、12）',
                 '本视频：`l=9, r=14, k=1` → `4`（9、10、11、12）'],
        quote='数据规模较大，同时好数的限制又体现在相邻数位的绝对差之间，因此在这里使用数位动态规划是很自然的想法。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把 `l` 补前导 0，和 `r` 一样长，逐位对齐',
              '`state` 三位：最高位 = 还在前导 0（不看相邻差），中间 = 贴 r，最低 = 贴 l',
              '确定 `start / end`：不在前导 0 时限制在 `[last−k, last+k]`，贴 r 取小、贴 l 取大'],
        summary=['时间 `O(D²·log r)`：状态 `O(D·log r·8)`，每个状态枚举 `O(D)`',
                 '前导 0 要单独成一个状态位：此时还没开头，不能用 `last` 限制',
                 '入口 `calc(0, 0, 7, f)`：三个标记全开',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '对比灵神：灵神用「不填数字」的分支处理前导零，yiduobo 把前导零放进 state'],
    ),
)
