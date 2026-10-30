N0 = 45


def _txt(S):
    if 'digits' not in S:
        return '先把 `n` 转成二进制数位 `digits`，长度 `m`'
    m = S['digits'] and len(S['digits'])
    if 'level' not in S:
        if 'f' not in S:
            return f'`n = {N0}` 的二进制 `digits`，长度 `m = {m}`'
        return f'`f[len]` = 长度恰为 `len` 的二进制回文数个数；先加上所有 `len < m` 的'
    lv = S['level']
    st = S['state']
    lb = '是' if st & 2 else '否'
    ri = '是' if st & 1 else '否'
    return f'`level = {lv}`（填第 {lv} 位和第 {m - 1 - lv} 位）：前缀贴着上界 = {lb}，后缀已超过 = {ri}'


def _col(S, i, v):
    if 'level' in S and 'm' in S:
        m = S['m']
        if i == S['level']:
            return 'blue'
        if i == m - 1 - S['level']:
            return 'pink'
    return None


def _gcol(S, r, c, v):
    if 'level' in S and S.get('_line') is not None and r == S['level'] and c == S.get('state'):
        return 'yellow'
    return None


CONFIG = dict(
    num=3677, title='统计二进制回文数字的数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='数位 DP · 前后同时往中间填',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 2223'],
    code='''
class Solution(object):
    def countBinaryPalindromes(self, n):
        
        if n == 0:
            return 1
        elif n == 1:
            return 2

        digits = []
        while n:
            digits.append(n % 2)
            n //= 2
        digits.reverse()
        m = len(digits)

        f = [0, 2, 1, 2, 2]   
        for length in range(5, m):
            if length % 2 == 1:
                f.append(f[length - 1] + f[length - 1])
            else:
                f.append(f[length - 1])
        
        def calc(level, state, g):
            if state & 2:
                left_bound = True
            else:
                left_bound = False
                
            if state & 1:
                right_invalid = True
            else:
                right_invalid = False
                
            if level * 2 >= m:
                if not left_bound or not right_invalid:
                    return 1
                return 0
            
            if g[level][state] is None:
                g[level][state] = 0

                start = 0
                if left_bound:
                    end = digits[level]
                else:
                    end = 1
                
                nxt_state = 0
                for d in range(start, end + 1):
                    if left_bound and d == digits[level]:
                        nxt_state |= 2
                    if m - 1 - level != level:
                        if digits[m - 1 - level] < d or (digits[m - 1 - level] == d and right_invalid):
                            nxt_state |= 1
                    elif right_invalid:
                        nxt_state |= 1

                    g[level][state] += calc(level + 1, nxt_state, g)
            
            return g[level][state]

        res = sum(f[:m])
        g = [[None] * 4 for _ in range((m + 1) // 2)]
        if digits[-1] == 0:
            res += calc(1, 3, g)
        else:
            res += calc(1, 2, g)
        
        return res
''',
    call=f'Solution().countBinaryPalindromes({N0})',
    expect=13,
    views=[
        dict(type='text', fn=_txt, size=24, h=80),
        dict(type='array', var='digits', label='digits（蓝 = 前缀正在填的位，粉 = 与它对称的后缀位）', cell=84, color=_col, h=190),
        dict(type='array', var='f', label='f[len]：长度为 len 的二进制回文数个数', cell=84, h=170),
        dict(type='table', var='g', label='g[level][state]（记忆化；state = 前缀贴上界 | 后缀已超过）', cell=84, color=_gcol, h=200),
        dict(type='calls', hide=('g',), h=150),
    ],
    watch=['m', 'level', 'state', 'left_bound', 'right_invalid', ('res', 'res', 'green')],
    skip=['if state & 2', 'if state & 1', 'left_bound = ', 'right_invalid = ', 'start = 0', 'nxt_state = 0', 'digits.reverse',
          'if n == 0', 'return 1', 'elif n == 1', 'return 2', 'while n', 'digits.append', 'n //= 2', 'if length % 2 == 1', 'end = ', 'for d in range'],
    captions={
        'digits = []': f'把 `n = {N0}` 转成二进制：`n % 2` 从低位取、`n //= 2`，最后翻转成高位在前的 `digits`',
        'f = [0, 2, 1, 2, 2]': '`f[len]` = 长度恰为 `len` 的回文数个数：`len = 0..4` 手算好（长度 1 含 `0`、`1` 共 2 个）',
        'g = [[None]': '记忆化表 `g`：`(m+1)//2 = {(m+1)//2}` 行（层数）× 4 列（`state`），初始全是 `None`',
        'm = len(digits)': f'`n = {N0}` 的二进制 `' + '{digits}' + '`，长度 `m = ' + '{m}' + '`',
        'f.append(f[length - 1] + f[length - 1])': '`length = {length}` 是奇数：中心填 0 或 1，其余同 `f[{length-1}]` → `f[{length}] = 2 × {f[length-1]}` = {f[length]}',
        'f.append(f[length - 1])': '`length = {length}` 是偶数：中心两位只能同为 00 或 11，只剩 `f[{length - 1}]` 的方案数 → `f[{length}] = {f[length]}`',
        'for length in range': lambda S, B, r: (f'`f` 前几项手算好：`{S.f}`；从长度 5 起用递推' if 'length' not in S else
                                                 (f'继续算 `length = {S.length}`' if S.length != B.get('length') else '长度 `< m` 的 `f` 都算完了')),
        'def calc': '`calc(level, state, g)`：已经填好最外面 `level` 层，状态是 `state`，数还有几种填法',
        'if level * 2 >= m': lambda S, B, r: (f'`level = {S.level}`：前后已在中间会合，填完了；只要前缀没贴上界，或后缀没超过 → 合法返回 1' if S.level * 2 >= S.m
                                              else f'`level = {S.level}`：还没填到中间，继续往里填'),
        'if not left_bound': lambda S, B, r: ('`left_bound` 为假，前缀已小于 digits 的前缀 → 合法，返回 1' if not (S.state & 2)
                                              else ('`right_invalid` 为假，前缀相等但后缀 ≤ 后缀 → 合法，返回 1' if not (S.state & 1)
                                                    else '前缀相等且后缀更大 → 回文数 > n，返回 0')),
        'if g[level][state] is None': lambda S, B, r: (f'`g[{S.level}][{S.state}]` 还没算过 → 算一遍并记下来' if S.g[S.level][S.state] is None
                                                       else f'`g[{S.level}][{S.state}] = {S.g[S.level][S.state]}` 算过了，直接用'),
        'g[level][state] = 0': '开始累加 `g[{level}][{state}]`',
        'if left_bound:': lambda S, B, r: (f'前缀还贴着上界：这一位最大只能填 `digits[{S.level}] = {S.digits[S.level]}`' if (S.state & 2)
                                           else '前缀已经小于上界：这一位 0 或 1 都行'),
        'if left_bound and d == digits[level]': lambda S, B, r: (f'枚举这一位填 `d = {S.d}`（范围 `{S.start}..{S.end}`）：' + (f'等于上界这一位 `digits[{S.level}]`，前缀继续贴着上界，`nxt_state` 前缀位置 1' if (S.state & 2 and S.d == S.digits[S.level])
                                                                else '小于上界这一位（或前缀本来就没贴着），前缀不再贴上界')),
        'if m - 1 - level != level': lambda S, B, r: (f'第 `{S.level}` 位与第 `{S.m - 1 - S.level}` 位对称，不是中心：要比较后缀' if S.m - 1 - S.level != S.level
                                                    else '到回文中心了：这一位自己与自己对称，后缀状态照搬'),
        'if digits[m - 1 - level] < d': lambda S, B, r: (f'后缀这一位也填 `d = {S.d}`，对比 `digits[{S.m-1-S.level}] = {S.digits[S.m-1-S.level]}`：'
                                                         + ('填的更大，或相等且之前已经更大 → 后缀超过，`nxt_state` 后缀位置 1'
                                                            if (S.digits[S.m-1-S.level] < S.d or (S.digits[S.m-1-S.level] == S.d and (S.state & 1)))
                                                            else '没有超过 `digits` 的后缀，后缀位保持 0')),
        'nxt_state |= 1': '后缀位置 1：`nxt_state = {nxt_state}`',
        'nxt_state |= 2': '前缀位置 1：`nxt_state = {nxt_state}`',
        'g[level][state] += calc': '进入下一层：填好这一位后调用 `calc({B.level + 1}, {B.nxt_state}, g)`',
        'return g[level][state]': '`g[{level}][{state}] = {ret}`：从 `level = {level}`、`state = {state}` 往里填，共有 `{ret}` 种合法填法',
        'res = sum(f[:m])': '长度 `< m` 的回文数全部合法：`sum(f[:{m}])` = =={res}==（包含 0）',
        'if digits[-1] == 0': lambda S, B, r: ('最后一位是 0：回文数的末位是 1 > 0，后缀一开始就超过，初始 `state = 3`' if S.digits[-1] == 0
                                               else '最后一位是 1：回文数的首尾都是 1，后缀一开始没超过，初始 `state = 2`'),
        'res += calc(1, 2, g)': '首位填 1 已经定了，从 `level = 1` 开始 `calc(1, 2, g)`',
        'res += calc(1, 3, g)': '首位填 1 已经定了，从 `level = 1` 开始 `calc(1, 3, g)`',
        'return res': '长度 `< m` 的 + 长度 `m` 且 `≤ n` 的 = =={ret}==',
    },
    cards=dict(
        one_liner='长度小于 m 的直接加；长度等于 m 的前后同时往中间填',
        complexity='时间 `O(m^2)`（状态 `m/2 × 4`，每个状态枚举 2 种数），空间 `O(m)`',
        problem=['非负整数的二进制（不含前导零）正反读一样，就是==二进制回文数==，`0` 也是',
                 '求 `0 ≤ k ≤ n` 中二进制回文数的个数，`n` 最大 `10^15`',
                 '示例：`n = 9` → `6`；本视频用 `n = 45`（二进制 `101101`）'],
        quote='由于最终必须填充得到一个回文串，因此实际上前后同时往中间填充。……state 只需要表示填充的前缀是否达到了前缀大小的上限……以及填充的后缀是否小于等于 digits 的后缀',
        quote_src='—— yiduobo 题解',
        idea=['长度小于 `m` 的回文数全合法，用 `f[len]` 累加；奇长度中心填 0/1，偶长度中心只能 00/11',
              '长度等于 `m`：数位 DP，`g[level][state]`，一次填第 `level` 位和第 `m−1−level` 位',
              '`state` 两位：前缀是否贴着上界，后缀是否已经大于 `digits` 的后缀'],
        summary=['时间 `O(m^2)`，空间 `O(m)`',
                 '原文为 Python 2 风格写法，本代码已是 Python 3 可运行，没有改动',
                 '易错：首位固定为 1，所以要看 `digits` 的末位是 0 还是 1 来定初始 `state`',
                 '到达中心位时，只更新前缀状态，后缀状态照搬',
                 '同类：灵神题解里的数学写法，直接数“左半边”，`O(1)`'],
    ),
)
