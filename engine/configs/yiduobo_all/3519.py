def _g(S, k):
    return S['_inner'].get(k)


def _txt(S):
    inn = S['_inner']
    if 'level' not in inn or 'flag' not in inn or 'l_base_b' not in S:
        return '先把 `l`、`r` 转成 b 进制，再用 `f[level][last][flag]` 做数位 DP'
    fl = inn['flag']
    return (f"第 {inn['level']} 位：last = {inn['last']}；flag = {fl:02b}"
            f"（{'贴 r' if fl & 2 else '不贴 r'}，{'贴 l' if fl & 1 else '不贴 l'}）")


CONFIG = dict(
    num=3519, title='统计逐位非递减的整数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='进制转换 + 数位 DP（flag 两位状态）',
    tags=['灵神题单', '动态规划', '难度分 2246'],
    code='''
class Solution(object):
    def countNumbers(self, l, r, b):
        
        def trans_base(s, base):
            s_list = []
            for char in s:
                s_list.append(int(char))
            
            s_list.reverse()
            res = []
            while s_list:
                for index in range(len(s_list) - 1, 0, -1):
                    s_list[index - 1] += s_list[index] % base * 10
                    s_list[index] //= base
                
                res.append(s_list[0] % base)
                s_list[0] //= base

                while s_list and s_list[-1] == 0:
                    s_list.pop()

            return res[::-1]

        l_base_b = trans_base(l, b)
        r_base_b = trans_base(r, b)

        n = len(r_base_b)
        l_base_b = [0] * (n - len(l_base_b)) + l_base_b

        f = [[[None] * 4 for _ in range(b)] for _ in range(n)]
        mod = 10 ** 9 + 7
        def dfs(level, last, flag, f):
            if level == n:
                return 1
            
            if f[level][last][flag] is None:
                f[level][last][flag] = 0

                start = last
                if flag & 1:
                    start = max(last, l_base_b[level])
                
                end = b - 1
                if flag & 2:
                    end = min(end, r_base_b[level])
                
                for digit in range(start, end + 1):
                    nxt_flag = 0
                    if (flag & 1) and digit == l_base_b[level]:
                        nxt_flag |= 1
                    if (flag & 2) and digit == r_base_b[level]:
                        nxt_flag |= 2
                    f[level][last][flag] += dfs(level + 1, digit, nxt_flag, f)
                    if f[level][last][flag] >= mod:
                        f[level][last][flag] -= mod
            
            return f[level][last][flag]
        
        return dfs(0, 0, 3, f)
''',
    call='Solution().countNumbers("23", "28", 8)',
    expect=3,
    views=[
        dict(type='array', var='r_base_b', label='r 的 b 进制（上界）', cell=70, h=150,
             color=lambda S, i, v: 'blue' if i == S['_inner'].get('level') else None),
        dict(type='array', var='l_base_b', label='l 的 b 进制（下界，补前导 0）', cell=70, h=150,
             color=lambda S, i, v: 'blue' if i == S['_inner'].get('level') else None),
        dict(type='text', fn=_txt, size=24, h=80),
        dict(type='calls', h=240, hide=('f',)),
    ],
    watch=[('level', lambda S: _g(S, 'level'), 'blue'), ('last', lambda S: _g(S, 'last'), 'cyan'),
           ('flag', lambda S: _g(S, 'flag'), 'pink'),
           ('start', lambda S: _g(S, 'start'), 'green'), ('end', lambda S: _g(S, 'end'), 'orange'),
           ('digit', lambda S: _g(S, 'digit'), 'yellow')],
    skip=['s_list', 'res = []', 'res.append', 'for char in s', 'for index in range(len(s_list)', 'while s_list', 'mod = ', 'f[level][last][flag] = 0',
          'f[level][last][flag] >= mod', 'f[level][last][flag] -= mod', 'nxt_flag = 0', 'end = b - 1', 'start = last', 'start = max', 'end = min', 'nxt_flag |= 1', 'nxt_flag |= 2'],
    captions={
        'return res[::-1]': '进制转换完成（倒序记余数再翻转）：`{res[::-1]}`',
        'l_base_b = trans_base': '`l` 转成 {b} 进制：`{l_base_b}`',
        'r_base_b = trans_base': '`r` 转成 {b} 进制：`{r_base_b}`',
        'l_base_b = [0] * ': '`l` 前面补 0，补成和 `r` 一样长 `n = {n}`：`{l_base_b}`',
        'f = [[[None]': '`f[level][last][flag]`：`flag` 两位，高位 = 还贴着 r 的前缀，低位 = 还贴着 l 的前缀',
        'return dfs(0, 0, 3, f)': lambda S, B, ret: ('从第 0 位出发：`last = 0`，`flag = 3`（二进制 11）：上下界都贴着' if ret is None else f'答案 `{ret}`（已按 1e9+7 取模）'),
        'if level == n': lambda S, B, ret: ('填完所有位 → 这是一种合法方案，返回 `1`' if S.level == S.n else f'`level = {S.level} < n`：继续填第 {S.level} 位'),
        'if f[level][last][flag] is None': lambda S, B, ret: ('这个状态还没算过 → 现在算' if S.f[S.level][S.last][S.flag] is None else '这个状态已经算过 → 直接返回'),
        'if flag & 1': lambda S, B, ret: (f'`flag & 1 = {S.flag & 1}`：' + (f'还贴着 l → 下界 `start = max(last, l[{S.level}]) = {max(S.last, S.l_base_b[S.level])}`（不能比 last 小，也不能比 l 这一位小）' if S.flag & 1 else f'不贴 l → 下界就是 `last = {S.last}`（非递减）')),
        'if flag & 2': lambda S, B, ret: (f'`flag & 2 = {S.flag & 2}`：' + (f'还贴着 r → 上界 `end = min(b-1, r[{S.level}]) = {min(S.b - 1, S.r_base_b[S.level])}`' if S.flag & 2 else f'不贴 r → 上界 `b-1 = {S.b - 1}`')),
        'for digit in range': lambda S, B, ret: (
            f'`digit` 已经枚举到上限 `end = {S.end}`，这个状态结束' if S.digit >= S.end and B.get('digit') == S.digit and B.get('last') == S.last else
            f'枚举这一位的数字 `digit`：从 `start = {S.start}` 到 `end = {S.end}`，轮到 `digit = {S.digit}`'),
        'if (flag & 1) and digit ==': lambda S, B, ret: (
            f'`digit = {S.digit}` ' + ('==' if S.digit == S.l_base_b[S.level] else '≠') + f' `l[{S.level}] = {S.l_base_b[S.level]}`' +
            (' → `nxt_flag |= 1`，下一位继续贴 l' if (S.flag & 1) and S.digit == S.l_base_b[S.level] else ' → 不再贴 l（或原本就不贴）')),
        'if (flag & 2) and digit ==': lambda S, B, ret: (
            f'`digit = {S.digit}` ' + ('==' if S.digit == S.r_base_b[S.level] else '≠') + f' `r[{S.level}] = {S.r_base_b[S.level]}`' +
            (' → `nxt_flag |= 2`，下一位继续贴 r' if (S.flag & 2) and S.digit == S.r_base_b[S.level] else ' → 不再贴 r（或原本就不贴）')),
        'f[level][last][flag] += dfs': '填 `digit = {digit}`，进入下一位：`last = {digit}`，`nxt_flag = {nxt_flag}`',
        'return f[level][last][flag]': '这个状态的方案数 `{f[level][last][flag]}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='先转 b 进制，再用 flag 同时记住是否贴着上下界',
        complexity='时间 `O(n²+n·b²)`，空间 `O(n·b)`',
        problem=['给字符串 `l`、`r` 和进制 `b`：数 `[l, r]` 内 b 进制每位都不小于前一位的整数个数，对 `1e9+7` 取模',
                 '示例：`l="2", r="7", b=2` → `2`',
                 '本视频：`l="23", r="28", b=8` → `3`（八进制 27、33、34）'],
        quote='标准的数位动态规划问题，不过在计算之前，需要先将l和r都转化为b进制，然后再执行数位动态规划。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[level][last][flag]`：填到第 `level` 位，上一位是 `last`，`flag` 记贴边情况',
              '`flag` 是两位二进制：低位 = 前缀等于 l 的前缀，高位 = 前缀等于 r 的前缀',
              '下界 `start = last`（还贴 l 就再和 `l[level]` 取大），上界 `end = b-1`（还贴 r 就再和 `r[level]` 取小）'],
        summary=['时间 `O(n²+n·b²)`：进制转换 `O(n²)`（模 b 除 b 的高精度做法）+ DP',
                 '`l` 要补前导 0，和 `r` 一样长，`flag` 才能逐位对齐',
                 '入口 `dfs(0, 0, 3, f)`：`last = 0` 保证第一位不受限制，`flag = 3` 表示上下界都贴着',
                 '原文已是 Python 3 可运行的写法，未做修改',
                 '对比灵神：灵神用 limit_low / limit_high 两个布尔，并用 `@cache`；yiduobo 把它们压成 `flag` 并手写 `f` 数组'],
    ),
)
