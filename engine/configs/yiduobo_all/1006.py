def _expr(S):
    N = S['N']
    parts = []
    ops = ['*', '/', '+', '-']
    for i, k in enumerate(range(N, 0, -1)):
        parts.append(str(k))
        if k > 1:
            parts.append(ops[i % 4])
    return ' '.join(parts)


def _seg(S):
    if 'res' not in S:
        return f"`clumsy({S['N']})` = {_expr(S)}"
    return f"`{_expr(S)}` → 目前 `res` = =={S['res']}=="


CONFIG = dict(
    num=1006, title='笨阶乘', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='按「+」分段 · 模拟',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def clumsy(self, N):


        if N == 1:
            return 1
        elif N == 2:
            return 2
        else:
            res = N * (N - 1) // (N - 2)
            now = N - 3
            while now >= 4:
                res += now - (now - 1) * (now - 2) // (now - 3)
                now -= 4

            if now > 0:
                res += 1

            return res
''',
    call='Solution().clumsy(10)',
    expect=12,
    views=[
        dict(type='text', size=34, h=90, fn=_seg),
        dict(type='text', size=30, h=70, fn=lambda S: ('第一段 `N × (N-1) ÷ (N-2)`' if 'now' not in S else f"下一段从 `now = {S['now']}` 开始：`now − (now-1)×(now-2)÷(now-3)`" if S['now'] >= 4 else f"剩下 `now = {S['now']}`，凑不出完整一段") if 'res' in S else ''),
        dict(type='array', var=lambda S: list(range(S['N'], 0, -1)), label='数字 N … 1',
             pointers={'now': 'blue'}, h=200,
             color=lambda S, i, v: ('blue' if 'now' in S and v == S['now'] else None)),
    ],
    watch=[('N', 'N', 'cyan'), ('now', 'now', 'blue'), ('res', 'res', 'green')],
    captions={
        'if N == 1': '`N = {N}`：不到 3 个数，凑不出第一段，先特判',
        'elif N == 2': '`N = {N}`：不是 2',
        'res = N *': '第一段 `N × (N-1) ÷ (N-2)` = `{N} × {N-1} ÷ {N-2}` = =={res}==（整除）',
        'now = N - 3': '之后每段 `+ a - b × c ÷ d` 从 `now = N - 3 = {now}` 开始，段首是 ==加号==',
        'while now >= 4': lambda S, B, r: (f"`now = {S['now']} ≥ 4`：还够凑一整段 `+ now − …`" if S['now'] >= 4 else f"`now = {S['now']} < 4`：凑不出完整的一段，退出"),
        'res += now -': '这一段值 = `{now} − {now-1}×{now-2}÷{now-3}` = {now - (now-1)*(now-2)//(now-3)}，累加后 `res` = =={res}==',
        'now -= 4': '一段用掉 4 个数：`now` → {now}',
        'if now > 0': lambda S, B, r: (f"`now = {S['now']} > 0`：还剩 {S['now']} 个数" if S['now'] > 0 else '`now = 0`：数字刚好用完'),
        'res += 1': '剩 3：`+3−2×1` = +1；剩 2：`+2−1` = +1；剩 1：`+1` = +1 → ==都等于 +1==，`res` = {res}',
        'return res': '笨阶乘 `clumsy(10)` = =={ret}==',
    },
    cards=dict(
        one_liner='乘除加减循环 → 以加号分段，每段算好再累加',
        complexity='时间 `O(N)`，空间 `O(1)`',
        problem=['把 `N, N-1, …, 1` 依次用 `*`、`/`、`+`、`-` 循环连接',
                 '乘除先算（整除向下取整），再从左到右算加减',
                 '示例：`clumsy(10)` = `10*9/8 + 7 - 6*5/4 + 3 - 2*1` = `12`'],
        quote='不过可以选择加号作为分隔，具体来说就是两个加号之间的部分作为一段。',
        quote_src='—— yiduobo 题解原文',
        idea=['减号后面是乘除，所以不能拿减号分段，只能拿加号分段',
              '开头 `N*(N-1)/(N-2)` 一段，之后每 4 个数一段 `+a-b*c/d`',
              '最后不足一段时，剩 1、2、3 个数都恰好贡献 `+1`'],
        summary=['时间 `O(N)`，空间 `O(1)`',
                 '原文为 Python 2 写法，`/` 做整数除法，已改为 `//`',
                 '易错：`N < 3` 要先特判；剩余部分 `now > 0` 一律加 1',
                 '本题也可以用栈模拟，yiduobo 用分段避免了栈'],
    ),
)
