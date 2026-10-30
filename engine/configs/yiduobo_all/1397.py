def _txt(S):
    I = S['_inner']
    if 'flag' not in I:
        return '先用 KMP 求 `evil` 的 next 数组，再记忆化搜索：`(位置 index, 匹配到 evil 的 pos, 贴边状态 flag)`'
    nm = {0: '不受限', 1: '贴 s1', 2: '贴 s2', 3: '贴两边'}[I['flag']]
    lo = I.get('bottom')
    hi = I.get('top')
    rng = f'，范围 `{lo}`–`{hi}`' if lo is not None and hi is not None else ''
    return f"`dfs(index={I['index']}, pos={I['pos']}, flag={I['flag']})`：{nm}{rng}"


def _evil_ptr(S):
    return S['_inner'].get('pos') if 'flag' in S['_inner'] else None


def _idx(S):
    return S['_inner'].get('index') if 'flag' in S['_inner'] else None


CONFIG = dict(
    num=1397, title='找到所有好字符串', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='数位 DP + KMP · 记忆化搜索',
    tags=['灵神题单', '字符串'],
    code='''
class Solution(object):
    def findGoodStrings(self, n, s1, s2, evil):

        next = [0]
        pos = 0
        l = len(evil)
        for index in range(1, l):
            while pos > 0 and evil[pos] != evil[index]:
                pos = next[pos - 1]
            if evil[pos] == evil[index]:
                pos += 1
            next.append(pos)
        
        f = [[[None] * 4 for _ in range(l)] for _ in range(n)]
        mod = 10 ** 9 + 7

        return self.dfs(0, 0, 3, evil, next, l, s1, s2, n, f, mod)
    
    def dfs(self, index, pos, flag, evil, next, l, s1, s2, n, f, mod):
        if f[index][pos][flag] is None:
            if index == n:
                f[index][pos][flag] = 1
            else:
                f[index][pos][flag] = 0
                if flag == 1 or flag == 3:
                    bottom = s1[index]
                else:
                    bottom = 'a'
                
                if flag == 2 or flag == 3:
                    top = s2[index]
                else:
                    top = 'z'
                
                for asc in range(ord(bottom), ord(top) + 1):
                    char = chr(asc)
                    next_pos = pos
                    while next_pos > 0 and evil[next_pos] != char:
                        next_pos = next[next_pos - 1]
                    if evil[next_pos] == char:
                        next_pos += 1
                    if next_pos == l:
                        continue
                    
                    if index == n - 1:
                        f[index][pos][flag] += 1
                    else:
                        if flag == 1:
                            if char == s1[index]:
                                next_flag = 1
                            else:
                                next_flag = 0
                        elif flag == 2:
                            if char == s2[index]:
                                next_flag = 2
                            else:
                                next_flag = 0
                        elif flag == 3:
                            if char == s1[index]:
                                if char == s2[index]:
                                    next_flag = 3
                                else:
                                    next_flag = 1
                            elif char == s2[index]:
                                next_flag = 2
                            else:
                                next_flag = 0
                        else:
                            next_flag = 0
                    
                        f[index][pos][flag] += self.dfs(index + 1, next_pos, next_flag, evil, next, l, s1, s2, n, f, mod)
                    
                    f[index][pos][flag] %= mod
        
        return f[index][pos][flag]
''',
    call='Solution().findGoodStrings(2, "ax", "bb", "ba")',
    expect=4,
    views=[
        dict(type='text', h=90, size=26, fn=_txt),
        dict(type='string', var='s1', label='s1（蓝 = 当前位）', cell=80, h=190, color=lambda S, i, v: 'blue' if i == _idx(S) else None),
        dict(type='string', var='s2', label='s2（蓝 = 当前位）', cell=80, h=190, color=lambda S, i, v: 'blue' if i == _idx(S) else None),
        dict(type='string', var='evil', label='evil（绿色 = 已匹配的前 pos 位）', cell=80, h=190, color=lambda S, i, v: 'green' if _evil_ptr(S) is not None and i < _evil_ptr(S) else None),
        dict(type='calls', h=230, hide=('evil', 'next', 'l', 's1', 's2', 'n', 'f', 'mod')),
    ],
    watch=[('index', 'index', 'blue'), ('pos', 'pos', 'pink'), ('flag', 'flag', 'orange'),
           ('char', 'char', 'yellow'), ('next_pos', 'next_pos', 'cyan'), 'next'],
    skip=['pos = 0', 'l = len(evil)', 'mod = 10', 'f[index][pos][flag] = 0', 'char = chr(asc)', 'next_pos = pos',
          'while next_pos > 0', 'if flag == 1:', 'elif flag == 2:', 'elif flag == 3:', 'if char == s1[index]:',
          'elif char == s2[index]:', 'if char == s2[index]:', 'if index == n - 1', 'f[index][pos][flag] %= mod',
          'if flag == 1 or', 'if flag == 2 or', 'f[index][pos][flag] = 1'],
    max_steps=110,
    captions={
        'next = [0]': '先造 `evil` 的 KMP 数组 `next`：`next[i]` = 前缀 `evil[:i+1]` 最长相等前后缀',
        'for index in range(1, l)': '依次求 `next[{index}]`',
        'while pos > 0 and evil[pos] != evil[index]': '失配就沿 `next` 回退：`pos` 越退越短',
        'if evil[pos] == evil[index]': '`evil[{pos}] == evil[{index}]` 吗？相等就把匹配长度 `pos` 加一',
        'next.append(pos)': '记下 `next[{index}] = {pos}` → `next = {next}`',
        'f = [[[None]': '`f[index][pos][flag]` 是记忆表，`None` 表示还没算过',
        'return self.dfs(0, 0, 3': '从第 0 位开始：没匹配到 evil（pos=0），同时贴着 s1 和 s2（flag=3）',
        'if f[index][pos][flag] is None': lambda S, B, r: ('这个状态没算过 → 开始计算' if S._inner.get('f', [[[0]]])[S.index][S.pos][S.flag] is None else '这个状态算过了 → ==直接用记忆值==，不再展开'),
        'if index == n': lambda S, B, r: (f'`index = n = {S.n}`：整串选完且没踩到 evil → 算 ==1 种合法答案==' if S.index == S.n else f'`index = {S.index} < n`：还要继续选下一个字符'),
        'if flag == 1 or flag == 3': '贴着下限（flag 为 1 或 3）→ 下限是 `s1[{index}]`，否则从 `a` 开始',
        'bottom = s1[index]': '下限取 `s1[{index}] = {bottom}`：不能比 s1 小',
        "bottom = 'a'": '没贴下限 → 下限放开到 `a`',
        'if flag == 2 or flag == 3': '贴着上限（flag 为 2 或 3）→ 上限是 `s2[{index}]`，否则到 `z`',
        'top = s2[index]': '上限取 `s2[{index}] = {top}`：不能比 s2 大',
        "top = 'z'": '没贴上限 → 上限放开到 `z`',
        'for asc in range': '枚举下一个字符：从 `{bottom}` 到 `{top}`',
        'char = chr(asc)': '这一步选的字符 `char = {char}`',
        'next_pos = pos': '拿当前匹配长度 `pos = {pos}` 去试着接上 `{char}`',
        'next_pos = next[next_pos - 1]': '`{char}` 接不上 `evil[{B.next_pos}]`，按 KMP 回退到 `next_pos = {next_pos}`',
        'if evil[next_pos] == char': lambda S, B, r: (f'`evil[{S.next_pos}] = {S.evil[S.next_pos]}` 等于 `{S.char}` → 匹配长度加一' if S.evil[S.next_pos] == S.char else f'`evil[{S.next_pos}] = {S.evil[S.next_pos]}` 不等于 `{S.char}` → 匹配长度不变'),
        'next_pos += 1': '匹配长度变成 `next_pos = {next_pos}`',
        'if next_pos == l': lambda S, B, r: (f'`next_pos = {S.next_pos} = len(evil)`：已经含有 evil → ==这个字符不能选==' if S.next_pos == S.l else f'`next_pos = {S.next_pos} < {S.l}`：还没凑成 evil，可以选'),
        'continue': '跳过 `{char}`，这条分支不算',
        'if index == n - 1': lambda S, B, r: ('已经是最后一位且合法 → 直接加一种' if S.index == S.n - 1 else '还没到最后一位 → 要根据贴边情况算 `next_flag`，再递归'),
        'f[index][pos][flag] += 1': '最后一位选 `{char}` 合法，累计 `f[{index}][{pos}][{flag}] = {f[index][pos][flag]}`',
        'next_flag = 1': '继续贴着下限 s1：`next_flag = 1`' ,
        'next_flag = 2': '继续贴着上限 s2：`next_flag = 2`',
        'next_flag = 3': '仍然同时贴 s1 和 s2：`next_flag = 3`',
        'next_flag = 0': '选的字符已经严格在 s1、s2 之间 → 之后不受限制，`next_flag = 0`',
        'f[index][pos][flag] += self.dfs': '递归算下一位：`dfs({B.index + 1}, {B.next_pos}, {B.next_flag})`，结果累加到当前状态',
        'f[index][pos][flag] %= mod': '取模后 `f[{index}][{pos}][{flag}] = {f[index][pos][flag]}`',
        'return f[index][pos][flag]': '这个状态的答案 `{ret}`',
    },
    cards=dict(
        one_liner='数位 DP 记下界/上界贴边，KMP 记 evil 匹配到哪',
        complexity='时间 `O(n·|evil|·4·26)`，空间 `O(n·|evil|·4)`',
        problem=['给定长度 `n` 的 `s1 <= s2`，以及字符串 `evil`',
                 '统计长度为 `n`、字典序在 `[s1, s2]`、==不含子串 evil== 的字符串数，对 `1e9+7` 取模',
                 '本视频：`n=2, s1="ax", s2="bb", evil="ba"` → `4`'],
        quote='令f[index][pos][flag]表示前index个字符，其后缀已经匹配到了evil的pos这个位置，flag则表示当前字符与sa和sb的贴近情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['`flag`：0 不受限，1 贴 s1，2 贴 s2，3 两边都贴 → 决定下一个字符的范围',
              '`pos`：已选串的后缀和 `evil` 前缀最长匹配长度，用 `next` 数组做 KMP 转移',
              '匹配长度到 `len(evil)` 就不合法；选完 `n` 位算 1 种',
              '原文用记忆化搜索，同一状态只算一次'],
        summary=['时间 `O(n·|evil|·4·26)`，空间 `O(n·|evil|·4)`',
                 '`next_pos == l` 的字符必须跳过，别漏掉这个 `continue`',
                 'flag 迁移：只有选的字符恰好等于边界字符才继续贴边',
                 '本题代码本来就是 Python 3 写法，未做修改',
                 '演示用 `n=2` 的小例子，题目里 `n` 最大 500'],
    ),
)
