S0 = 'mnmpqpr'


def _L(x):
    return chr(x) if isinstance(x, int) and x else '·'


def _tp(t):
    c = '∞' if t[0] == float('inf') else t[0]
    return f"({c}; {''.join(_L(x) for x in t[1:])})"


def _s_arr(S):
    s = S.get('s')
    if isinstance(s, list):
        return [chr(x) for x in s]
    return list(S0)


def _t_arr(S):
    return [_L(x) for x in S['t']]


def _f_arr(S):
    return [('∞' if x == float('inf') else x) for x in S['f']]


def _win(S):
    i = S.get('i')
    return i


CONFIG = dict(
    num=3441, title='变成好标题的最少代价', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='中位数贪心 + 划分型 DP（长 3/4/5 的段）',
    tags=['灵神题单·动态规划', '灵神题单·贪心与思维', '难度分 2765'],
    code='''
class Solution:
    def minCostGoodCaption(self, s: str) -> str:
        n = len(s)
        if n < 3:
            return ""

        s = list(map(ord, s))
        f = [0] * (n + 1)
        f[n - 1] = f[n - 2] = inf
        t = [0] * (n + 1)
        size = [3] * n

        for i in range(n - 3, -1, -1):
            a, b, c = sorted(s[i: i + 3])
            s3 = t[i + 3]
            res = (f[i + 3] + c - a, b, s3, s3, s3)

            if i + 4 <= n:
                a, b, c, d = sorted(s[i: i + 4])
                s4 = t[i + 4]
                tp = (f[i + 4] + c + d - a - b, b, b, s4, s4)
                if tp < res:
                    res = tp
                    size[i] = 4

            if i + 5 <= n:
                a, b, c, d, e = sorted(s[i: i + 5])
                tp = (f[i + 5] + d + e - a - b, c, c, c, t[i + 5])
                if tp < res:
                    res = tp
                    size[i] = 5

            f[i] = res[0]
            t[i] = res[1]

        ans = []
        i = 0
        while i < n:
            ans.append(chr(t[i]) * size[i])
            i += size[i]
        return ''.join(ans)
''',
    call=f'Solution().minCostGoodCaption({S0!r})',
    expect='mmmpppp',
    skip=['s3 = t[i + 3]', 's4 = t[i + 4]', 'tp = (f[i + 4]', 'tp = (f[i + 5]', 'if i + 4 <= n', 'if i + 5 <= n', 'ans = []', 'i = 0', 'while i < n', 'if n < 3', 'f[i] = res[0]', 'n = len(s)', 't = [0]', 'size = [3] * n', 'res = tp', 'i += size[i]', 'size[i] = 4', 'size[i] = 5'],
    max_steps=100,
    views=[
        dict(type='array', var=_s_arr, label='s（蓝框 = 当前后缀里 s[i] 所在的那一段）', h=170, cell=80,
             pointers={'i': 'blue'},
             window=('i', 'min(i + size[i], len(s)) - 1'),
             color=lambda S, k, v: 'green' if 'ans' in S and k < sum(len(x) for x in S['ans']) else None),
        dict(type='array', var=_f_arr, label='f[i]：后缀 s[i:] 变成好标题的最少操作次数', h=140, cell=80, color=lambda S, k, v: 'blue' if k == S.get('i') else None),
        dict(type='array', var=_t_arr, label='t[i]：s[i] 所在段最终变成的字母', h=140, cell=80, color=lambda S, k, v: 'blue' if k == S.get('i') else None),
        dict(type='array', var='size', label='size[i]：这一段的长度（3 / 4 / 5）', h=140, cell=80, color=lambda S, k, v: 'blue' if k == S.get('i') else None),
    ],
    watch=[('i', 'i', 'blue'), ('res', lambda S: _tp(S['res']) if 'res' in S else '', 'yellow'), ('ans', "''.join(ans)", 'green')],
    captions={
        'if n < 3': '`n = {n}`：长度不足 3，无法成段 → 无解；这里 `n ≥ 3`',
        's = list(map(ord': '字母转成 ASCII 码，方便算操作数',
        'f = [0] * (n + 1)': '`f[i]`：后缀 `s[i:]` 变成好标题的最少操作次数；另有 `t[i]`（所在段变成的字母）和 `size[i]`（段长，默认 3）',
        'f[n - 1] = f[n - 2] = inf': '只剩 1 个或 2 个字母时凑不成长 ≥ 3 的段 → `inf`',
        't = [0]': '`t[i]`：`s[i]` 所在的段最终变成哪个字母',
        'size = [3]': '`size[i]`：从 `i` 开始的第一段长度，默认 3',
        'for i in range(n - 3': lambda S, B, ret: (f'`i = {S.i}`：倒着求后缀 `s[{S.i}:]` 的最优分法' if S.get('i') != B.get('i') or 'i' not in B else '整个字符串算完，开始还原答案'),
        'a, b, c = sorted(s[i: i + 3])': '第一段取 3 个字母，排序后 `{chr(a)} ≤ {chr(b)} ≤ {chr(c)}`：全变成==中位数== `{chr(b)}`，操作数 `c − a = {c - a}`',
        'res = (': lambda S, B, ret: f'候选①：用长 3 的段，候选 `{_tp(S.res)}`（操作数；第 3~6 个字母）',
        'a, b, c, d = sorted': '候选②：第一段取 4 个字母 `{chr(a)}{chr(b)}{chr(c)}{chr(d)}`，全变成较小的中位数 `{chr(b)}`，操作数 `c + d − a − b = {c + d - a - b}`',
        'if tp < res': lambda S, B, ret: (f'比较候选 `{_tp(S.tp)}` 与当前最优 `{_tp(S.res)}`：先比操作数，再比字母 → ' + ('==更优，换成它，段长改为 ' + str(4 if S['_line'] == 22 else 5) + '==' if S.tp < S.res else '不更优，保留原来的')),
        'size[i] = 4': '`size[{i}] = 4`：这一段取长度 4',
        'size[i] = 5': '`size[{i}] = 5`：这一段取长度 5',
        'a, b, c, d, e = sorted': '候选③：第一段取 5 个字母 `{chr(a)}{chr(b)}{chr(c)}{chr(d)}{chr(e)}`，全变成中位数 `{chr(c)}`，操作数 `d + e − a − b = {d + e - a - b}`',
        't[i] = res[1]': lambda S, B, ret: f'记录：`f[{S.i}] = {S.f[S.i]}`，首段变成 `{_L(S.t[S.i])}`，段长 `size[{S.i}] = {S.size[S.i]}`',
        'ans = []': '`f[0]` 就是最少操作数；用 `size`、`t` 从头还原字符串',
        
        'ans.append': lambda S, B, ret: f"第 `{S.i}` 个字母起：`{_L(S.t[S.i])}` 重复 `{S.size[S.i]}` 次 → `{chr(S.t[S.i]) * S.size[S.i]}`，答案目前 `{''.join(S.ans)}`",
        'i += size[i]': '跳到下一段起点 `i = {i}`',
        'return': '答案 `{ret}`',
    },
    cards=dict(
        one_liner='段长只需 3、4、5：每段变成中位数，倒着做 DP',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['字符串中每个字符所在的连续相同段长度都 ≥ 3 才是==好标题==',
                 '每次操作把一个字母改成相邻字母，求最少操作数；多种方案取字典序最小，无解返回 `""`',
                 '示例：`"cdcd"` → `"cccc"`；本视频：`"mnmpqpr"` → `"mmmpppp"`'],
        quote='本题的「基本元素」只有长为 3,4,5 的子串，换句话说，问题相当于：把 s 划分成若干长为 3,4,5 的子串，把每个子串中的字母都变成相同的，求最小操作次数。',
        quote_src='—— 灵茶山艾府题解（六、中位数贪心 + DP）',
        idea=['每段变成相同字母，最优是变成==中位数==：3 个字母代价 `c − a`，4 个 `c + d − a − b`，5 个 `d + e − a − b`',
              '`f[i]` = 后缀 `s[i:]` 的最少操作数，枚举第一段长 3/4/5，从 `f[i+3]`、`f[i+4]`、`f[i+5]` 转移',
              '字典序：==倒着算==，用元组比较“操作数 → 前 6 个字母”，只记 `t[i]` 和 `size[i]`'],
        result='操作数最少，且字典序最小：`"mnmpqpr"` → `"mmmpppp"` ✓',
        after=[dict(heading='题解里的其他写法', lines=[
            '先写 `dfs(i, j)`：枚举 `s[i]` 变成哪个字母，再 1:1 翻译成递推',
            '用 `min_f` 优化到 `O(n·26)`，`nxt` 数组还原方案'])],
        summary=['时间 `O(n)`，空间 `O(n)`（忽略 `k = 3` 的常数）',
                 '易错：`f[n-1] = f[n-2] = inf`，剩 1~2 个字母无法成段',
                 '易错：必须==倒着递推==，字典序要靠后面的信息才能判断',
                 '长 4 段变成 `b`（较小的中位数），长 5 段变成 `c`，保证字典序最小',
                 '同类题：输出具体方案的 DP（打印方案）、中位数贪心'],
    ),
)
