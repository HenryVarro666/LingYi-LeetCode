_I = lambda S: S['_inner']


def _lr(S, k):
    v = _I(S).get(k)
    return v if isinstance(v, int) else None


def _win(S):
    l, r = _lr(S, 'l'), _lr(S, 'r')
    return l if l is not None and r is not None else None


def _winr(S):
    l, r = _lr(S, 'l'), _lr(S, 'r')
    return r if l is not None and r is not None else None


def _txt(S):
    d = _I(S)
    if 'x' in d and 'w' in d and S.get('_line') in (30, 31, 32):
        sym = '×' if S['s'][d['i']] == '*' else '+'
        return f"左 `{d['v']}` {sym} 右 `{d['w']}` = =={d['x']}=="
    if 'correct' in S and 'l' not in d:
        return f"正确答案 `correct = {S['correct']}`（先算乘法，再算加法）"
    return '`f(l, r)` = `s[l..r]` 在所有加括号方式下，不超过 1000 的可能值'


def _res(S):
    d = _I(S)
    return sorted(d['res']) if isinstance(d.get('res'), dict) else []


CONFIG = dict(
    num=2019, title='解出数学表达式的学生分数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='区间 DP · 记忆化搜索（Go 原文转写）',
    tags=['灵神题单·动态规划', '难度分 2584'],
    code='''
class Solution:
    def scoreOfStudents(self, s: str, answers: List[int]) -> int:
        n = len(s)
        # 计算正确答案
        correct = 0
        i = 0
        while i < n:
            mul = int(s[i])
            i += 2
            while i < n and s[i - 1] == '*':
                mul *= int(s[i])
                i += 2
            correct += mul

        # 区间 DP
        # dp[l][r] 表示 s[l..r] 内的表达式在不同计算顺序下的不超过 1000 的所有可能值
        dp = [[None] * n for _ in range(n)]

        def f(l: int, r: int) -> dict:
            if l == r:
                return {int(s[l]): True}
            if dp[l][r] is not None:
                return dp[l][r]
            res = {}
            for i in range(l + 1, r, 2):  # 枚举分界点
                for v in f(l, i - 1):  # 计算左边表达式的可能值
                    for w in f(i + 1, r):  # 计算右边表达式的可能值
                        x = v + w
                        if s[i] == '*':
                            x = v * w
                        if x <= 1000:  # 超过 1000 的结果不计入
                            res[x] = True
            dp[l][r] = res
            return res

        res = f(0, n - 1)
        ans = 0
        for v in answers:
            if v == correct:
                ans += 5
            elif v in res:
                ans += 2
        return ans
''',
    call='Solution().scoreOfStudents("3+5*2", [13, 0, 10, 13, 13, 16, 16])',
    expect=19,
    views=[
        dict(type='string', var='s', label='s（框 = 当前这一层的区间 [l, r]）', cell=90, h=170,
             pointers={_win: 'blue', _winr: 'pink'}, pointer_labels={_win: 'l', _winr: 'r'}, window=(_win, _winr)),
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='array', var=_res, label='当前 res（可能的值）', cell=70, h=130, index=False),
        dict(type='calls', h=170),
        dict(type='array', var='answers', label='answers', cell=70, h=130),
    ],
    watch=[('correct', 'correct', 'green'), ('ans', 'ans', 'orange')],
    skip=['for i in range(l + 1', 'dp = [[None]', 'n = len(s)', 'res = {}', 'x = v + w', 'while i < n:', 'i += 2'],
    captions={
        'mul = int(s[i])': '先算乘法：取一个数 `{mul}` 作为乘积起点',
        'mul *= int': '遇到 `*`：连乘 → `mul = {mul}`',
        'correct += mul': '一段乘积结束，加到正确答案：`correct = {correct}`',
        'if l == r': lambda S, B, r: (f'`l == r`：单个数字 `{S.s[S.l]}`，可能值只有它自己' if S.l == S.r else f'区间 `s[{S.l}..{S.r}]` 长度 > 1，继续看有没有缓存'),
        'return {int(s[l])': '返回 `{{{int(s[l])}}}`',
        'if dp[l][r] is not None': lambda S, B, r: ('已算过 → 直接用缓存' if S.dp[S.l][S.r] is not None else '还没算过，往下枚举分界点'),
        'for v in f(l, i - 1)': lambda S, B, r: ('左边的可能值都试完了 → 换下一个分界点' if 'v' in _I(S) and 'v' in _I(B) and _I(B)['v'] == _I(S)['v'] and _I(B).get('i') == _I(S).get('i') and _I(B).get('l') == _I(S).get('l')
                                                  else f'分界点是运算符 `s[{S.i}] = {S.s[S.i]!r}`：先拿到左边 `s[{S.l}..{S.i-1}]` 的所有可能值'),
        'for w in f(i + 1, r)': lambda S, B, r: ('右边的可能值都试完了 → 换左边下一个值' if 'w' in _I(S) and 'w' in _I(B) and _I(B)['w'] == _I(S)['w'] and _I(B).get('i') == _I(S).get('i') and _I(B).get('l') == _I(S).get('l')
                                                  else f'再拿右边 `s[{S.i+1}..{S.r}]` 的所有可能值，两两组合'),
        'return res': '返回 `s[{l}..{r}]` 的所有可能值：{sorted(res)}',
        'if s[i] == ': '`{v}` 与 `{w}` 之间的运算符是 `{s[i]}`',
        'x = v * w': '乘法：`x = {v} × {w}` = {x}',
        'if x <= 1000': '`x = {x}`：不超过 1000 才记录，超过的答案不可能出现',
        'res[x] = True': '`{x}` 加入 `res`：{sorted(res)}',
        'dp[l][r] = res': '缓存 `dp[{l}][{r}]` = {sorted(res)}',
        'res = f(0, n - 1)': '整个表达式所有顺序的可能值：=={sorted(res)}==',
        'for v in answers': '逐个看学生答案 `{v}`',
        'if v == correct': lambda S, B, r: (f'`{S.v} == correct = {S.correct}` → ==5 分==' if S.v == S.correct else f'`{S.v} ≠ {S.correct}`，不是正确答案'),
        'ans += 5': '满分：`ans = {ans}`',
        'elif v in res': lambda S, B, r: (f'`{S.v}` 在可能值里 → 算错顺序但能凑出来，==2 分==' if S.v in S.res else f'`{S.v}` 凑不出来 → 0 分'),
        'ans += 2': '`ans = {ans}`',
        'return ans': '所有学生得分和 =={ret}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='区间 DP：枚举最后算哪个运算符，左右两边的可能值两两组合',
        complexity='时间约 `O(n^3·V^2)`（V ≤ 1001 个值），答案查询 `O(1)`',
        problem=['表达式只含个位数、`+`、`*`，正确顺序是先乘后加',
                 '答案正确得 `5` 分；能由某种错误运算顺序得到得 `2` 分；否则 `0` 分',
                 '示例：`s = "3+5*2"`，`answers = [13,0,10,13,13,16,16]` → `19`'],
        quote='dp[l][r] 表示 s[l..r] 内的表达式在不同计算顺序下的不超过 1000 的所有可能值',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['正确答案：每段连乘先乘完，再把各段相加',
              '所有可能值：枚举分界运算符 `s[i]`，左 `f(l,i-1)` 与右 `f(i+1,r)` 两两运算',
              '超过 1000 的丢掉；`dp[l][r]` 记忆化避免重复'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`map[int]bool` 用 dict，`s[i]&15` 写成 `int(s[i])`）',
                 '分界点 `i` 每次 `+2`：只有运算符位置才能当分界',
                 '易错：错误顺序恰好得到正确值时仍是 5 分，所以先判断 `correct`',
                 '时间 `O(n^3·V^2)`，V 是可能值个数（≤ 1001）'],
    ),
)
