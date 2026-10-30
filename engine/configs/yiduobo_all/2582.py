CONFIG = dict(
    num=2582, title='递枕头', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='找规律：取模半周期',
    tags=[],
    code='''
class Solution(object):
    def passThePillow(self, n, time):

        time %= (n - 1) * 2
        if time < n - 1:
            return time + 1
        else:
            return n * 2 - 1 - time
''',
    call='Solution().passThePillow(5, 6)',
    expect=3,
    views=[
        dict(type='array', var=lambda S: list(range(1, S['n'] + 1)), label='队伍（编号 1..n）', cell=110, h=210,
             color=lambda S, i, v: 'green' if S['_line'] in (6, 8) and v == (S['time'] + 1 if S['time'] < S['n'] - 1 else 2 * S['n'] - 1 - S['time']) else None),
        dict(type='text', fn=lambda S: f"一整轮 `2×(n-1) = {2 * (S['n'] - 1)}` 秒回到 1 号；time 取模后 = =={S['time']}==", h=90),
        dict(type='text', fn=lambda S: (f"前半区（`time < {S['n'] - 1}`）：正序，`time + 1`" if S['time'] < S['n'] - 1
                                        else f"后半区（`time >= {S['n'] - 1}`）：逆序，`2n - 1 - time`"), h=90),
    ],
    watch=['n', 'time'],
    captions={
        'time %= ': '枕头每 `2×(n-1) = {2*(n-1)}` 秒回到 1 号手里，先取模：`{B.time} % {2*(n-1)} = {time}`',
        'if time <': lambda S, B, r: (f'`time = {S.time} < n-1 = {S.n - 1}`：在前半区，枕头正在==正序==传' if S.time < S.n - 1
                                      else f'`time = {S.time} ≥ n-1 = {S.n - 1}`：在后半区，枕头正在==逆序==传'),
        'return time + 1': '正序：第 `time` 秒到第 `time + 1` 个人，答案 =={ret}==',
        'return n * 2 - 1 - time': '逆序：`2n - 1 - time = {n*2} - 1 - {time}`，答案 =={ret}==',
    },
    cards=dict(
        before=[dict(heading='先看样例找规律', lines=['`n=4`：`1→2→3→4→3→2→1→2…`', '第 6 秒又回到 1 号，周期 = `2×(4-1) = 6`', '周期内前 3 秒正序，后 3 秒逆序'])],
        after=[dict(heading='换个例子验证', lines=['`n=3, time=2`：`time %= 4` 仍是 2', '`2 < n-1 = 2` 不成立 → 后半区', '`2×3 - 1 - 2 = 3`，对照题目：答案 3，正确'])],
        one_liner='找规律：2(n-1) 秒一个来回，再分前半区、后半区',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`n` 个人排成一排，枕头从 1 号开始每秒向后传，到端点掉头',
                 '求 `time` 秒后拿枕头的人',
                 '示例：`n=5, time=6` → `1→2→3→4→5→4→3`，答案 `3`'],
        quote='找规律的题目。通过样例可以发现，每次枕头需要经过2 * (n - 1)轮才会重新回到1的手中，于是可以将time对这个值取模。',
        quote_src='—— yiduobo 题解原文',
        idea=['先 `time %= 2(n-1)`，一个来回之后状态重复',
              '`time < n-1`：正序，答案 `time + 1`',
              '否则逆序，答案 `2n - 1 - time`'],
        summary=['时间、空间 `O(1)`',
                 '易错：一个来回是 `2(n-1)` 秒，不是 `2n`',
                 '后半区公式 `2n - 1 - time`：`time = n-1` 时刚好是 `n`',
                 '代码未改，原文已是 Python 3 可运行的写法'],
    ),
)
