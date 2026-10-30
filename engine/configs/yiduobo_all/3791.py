_L = lambda S: S['_inner'].get('level')
_LOW = lambda S: S['low'] if isinstance(S.get('low'), list) else None


def _bin(x):
    return format(x, '02b')


def _nxt(bi):
    d, lv = bi['d'], bi['level']
    ns = bi['s'] + d if lv % 2 == 0 else bi['s'] - d
    st = bi['state']
    nst = (1 if (st & 1) and d == bi['low'][lv] else 0) | (2 if (st & 2) and d == bi['high'][lv] else 0)
    return ns, nst


def _call(S, B, ret):
    bi = B['_inner']
    ns, nst = _nxt(bi)
    return (f"填 `d = {bi['d']}`：`s` 变成 `{ns}`（差值 {ns - 65}），`nxt_state = {_bin(nst)}`（只有等于边界值才继续贴着）"
            f" → 递归 `calc({bi['level'] + 1}, {ns}, {nst})`")


def _for(S, B, ret):
    bi = B['_inner']
    if 'd' not in bi:
        return f"从 `start = {bi['start']}` 到 `end = {bi['end']}` 枚举这一位填的数字 `d`"
    if bi['d'] == bi['end']:
        return f"子问题返回，累计 `f = {bi['f'][bi['level']][bi['s']][bi['state']]}`；`d` 已枚举到 `end = {bi['end']}`"
    return f"子问题返回，累计 `f = {bi['f'][bi['level']][bi['s']][bi['state']]}`；换下一个 `d = {bi['d'] + 1}`"


CONFIG = dict(
    num=3791, title='给定范围内平衡整数的数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='数位 DP · state 两位二进制 + 偏移量',
    tags=['灵神题单', '难度分 2132'],
    code='''
class Solution(object):
    def countBalanced(self, low, high):
        
        low = [int(x) for x in list(str(low))]
        high = [int(x) for x in list(str(high))]
        n = len(high)
        low = [0] * (n - len(low)) + low

        f = [[[None] * 4 for _ in range(140)] for _ in range(n)]

        def calc(level, s, state):
            if level == n:
                if s == 65:
                    return 1
                return 0
            
            if f[level][s][state] is None:
                f[level][s][state] = 0

                if state & 1:
                    start = int(low[level])
                else:
                    start = 0
                
                if state & 2:
                    end = int(high[level])
                else:
                    end = 9

                for d in range(start, end + 1):
                    if level % 2 == 0:
                        nxt_s = s + d
                    else:
                        nxt_s = s - d
                    
                    nxt_state = 0

                    if (state & 1) and d == low[level]:
                        nxt_state |= 1
                    
                    if (state & 2) and d == high[level]:
                        nxt_state |= 2
                    
                    f[level][s][state] += calc(level + 1, nxt_s, nxt_state)

            return f[level][s][state]
        

        return calc(0, 65, 3)
''',
    call='Solution().countBalanced(95, 121)',
    expect=3,
    views=[
        dict(type='array', var=lambda S: S.get('high') if isinstance(S.get('high'), list) else None, label='high（上界 121）', cell=70, h=175, pointers={_L: 'pink'}, pointer_labels={_L: 'level'}),
        dict(type='array', var=lambda S: S.get('low') if isinstance(S.get('low'), list) else None, label='low（下界 95，已补前导 0）', cell=70, h=175, pointers={_L: 'pink'}, pointer_labels={_L: 'level'}),
        dict(type='text', size=32, fn=lambda S: (f"s = ==`{S['_inner']['s']}`==（偏移 65）→ 实际差值 ==`{S['_inner']['s'] - 65}`==；state = `{_bin(S['_inner']['state'])}`"
                                                   if 's' in S['_inner'] and 'state' in S['_inner'] else '')),
        dict(type='calls', h=220),
    ],
    watch=[('level', _L, 'pink'), ('s', lambda S: S['_inner'].get('s'), 'cyan'), ('state', lambda S: S['_inner'].get('state'), 'yellow'),
           ('start', lambda S: S['_inner'].get('start'), 'blue'), ('end', lambda S: S['_inner'].get('end'), 'orange')],
    skip=['n = len(high)', 'f[level][s][state] = 0', 'nxt_state = 0', 'nxt_state |= 1', 'nxt_state |= 2',
          'if (state & 1) and d', 'if (state & 2) and d', 'if level % 2 == 0', 'else:', 'return f[level][s][state]'],
    max_steps=52,
    captions={
        'low = [int(x)': lambda S, B, r: f"把 low 拆成数位 `{S.low}`" if isinstance(S.low, list) else '把 low 拆成数位',
        'high = [int(x)': '把 high 拆成数位 `{high}`',
        'low = [0] *': '给 low 补前导 0，和 high 一样长：`{low}`。==前导 0 不影响 s==，所以不用特判',
        'f = [[[None]': '`f[level][s][state]`：记忆化表，`s` 的取值 −62~72，加偏移 65 后放进 140 格',
        'return calc(0, 65': '入口 `calc(0, 65, 3)`：差值 0（偏移后 65），`state = 11`（上下界都贴着）',
        'if level == n': lambda S, B, r: (f"`level = {B['_inner']['level']}` 填满了" if B['_inner']['level'] == S.n else f"`level = {B['_inner']['level']}`，还没填满")
                                           if 'level' in B['_inner'] else '',
        'if s == 65': lambda S, B, r: ('`s == 65`：差值为 0 → ==平衡，返回 1==' if B['_inner']['s'] == 65 else f"`s = {B['_inner']['s']}` ≠ 65：不平衡 → 返回 0"),
        'return 1': '返回 1：这个数平衡',
        'return 0': '返回 0：这个数不平衡',
        'if f[level][s][state] is None': lambda S, B, r: ('这个状态没算过，往下枚举' if B['_inner']['f'][B['_inner']['level']][B['_inner']['s']][B['_inner']['state']] is None else '这个状态算过了，直接用'),
        'start = int(low': '`state` 低位 = 1：贴着 low，这一位下界 `start = low[{level}] = {start}`',
        'start = 0': '`state` 低位 = 0：不再受 low 限制，`start = 0`',
        'end = int(high': '`state` 高位 = 1：贴着 high，这一位上界 `end = high[{level}] = {end}`',
        'end = 9': '`state` 高位 = 0：不再受 high 限制，`end = 9`',
        'for d in range': _for,
        'nxt_s = s + d': lambda S, B, r: f"`level = {B['_inner']['level']}` 是偶数（从左数第 {B['_inner']['level'] + 1} 位）→ 加：`s + d = {S['_inner']['nxt_s']}`" if 'nxt_s' in S['_inner'] else '',
        'nxt_s = s - d': lambda S, B, r: f"`level = {B['_inner']['level']}` 是奇数（从左数第 {B['_inner']['level'] + 1} 位）→ 减：`s - d = {S['_inner']['nxt_s']}`" if 'nxt_s' in S['_inner'] else '',
        'f[level][s][state] += calc': _call,
    },
    cards=dict(
        one_liner='数位 DP：s 记“偶数位和 − 奇数位和”，state 记贴不贴边界',
        complexity='时间 `O(n·140·4·10)`，空间 `O(n·140·4)`',
        problem=['至少两位、且偶数位数字和等于奇数位数字和的整数叫平衡整数',
                 '求 `[low, high]` 内的平衡整数个数，`high ≤ 10^15`',
                 '本视频：`[95, 121]` → `3`（99、110、121）'],
        quote='在这里并不需要区分填充的偶数位在原数中是奇数位还是偶数位，因为最终的目标是数位之和相同，因此只需要二者之差为0就行了。',
        quote_src='—— yiduobo 题解',
        idea=['`f[level][s][state]`：填了前 level 位，差值为 s，边界状态为 state 的方案数',
              '`state` 是两位二进制：低位贴 low，高位贴 high，入口 `11`',
              '`s` 可能为负，加偏移 65：最大差 72、最小 −62，开 140 格',
              'low 补前导 0 与 high 等长；low ≥ 1，所以 0 和一位数都不会被算进去'],
        summary=['时间 `O(n·140·4·10)`，状态只算一次',
                 '终点 `s == 65` 才计 1：偶数位和 = 奇数位和',
                 '下标为偶数的位加、奇数的位减；符号与灵神的 `diff` 相反，判 0 的结论一样',
                 '原文是 Python 2 风格，代码无需改动即可运行',
                 '对比灵神：他用 `@cache` + `limit` 布尔值；这里手写 `f` 表 + 二进制 state'],
    ),
)
