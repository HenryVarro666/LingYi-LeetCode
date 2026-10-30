def _pos(S):
    if 'k' not in S:
        return None
    return S['n'] - S['t'] if S['k'] % 2 else 1 + S['t']


CONFIG = dict(
    num=2582, title='递枕头', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='数学：往返周期',
    tags=[],
    code='''
class Solution:
    def passThePillow(self, n: int, time: int) -> int:
        k, t = divmod(time, n - 1)
        return n - t if k % 2 else 1 + t
''',
    call='Solution().passThePillow(4, 5)',
    expect=2,
    views=[
        dict(type='array', var=lambda S: list(range(1, S['n'] + 1)), label='队伍（编号 1..n，绿 = 最终拿着枕头的人）', cell=110, h=210,
             color=lambda S, i, v: 'green' if _pos(S) == v else None),
        dict(type='text', fn=lambda S: (
            f"到端点要 `n-1 = {S['n'] - 1}` 秒；`{S['time']} = {S['k']}×{S['n'] - 1} + {S['t']}`：已走完 =={S['k']}== 段，这一段走了 =={S['t']}== 步"
            if 'k' in S else f"n = {S['n']}，time = {S['time']}"), h=90),
        dict(type='text', fn=lambda S: (
            ('k 是奇数：这一段从 n 走向 1，答案 `n - t`' if S['k'] % 2 else 'k 是偶数：这一段从 1 走向 n，答案 `1 + t`') if 'k' in S else ''), h=90),
    ],
    watch=['n', 'time', ('k', 'k', 'blue'), ('t', 't', 'pink')],
    captions={
        'divmod': '每走 `n-1 = {n-1}` 秒碰到一次端点就掉头：`{time} ÷ {n-1}` 商 `k = {k}`（走完几段），余 `t = {t}`（本段走了几步）',
        'return': lambda S, B, ret: (f'`k = {S.k}` 是奇数：本段从 n 往 1 走，`n - t = {S.n} - {S.t} = {ret}`' if S.k % 2
                                     else f'`k = {S.k}` 是偶数：本段从 1 往 n 走，`1 + t = 1 + {S.t} = {ret}`') + f'，答案 =={ret}=='
    },
    cards=dict(
        before=[dict(heading='先想想：直接模拟', lines=['每秒传一次，`time` 最多 1000，模拟也能过', '但枕头的位置是==有周期的==：1→n→1 每 `2(n-1)` 秒一轮', '所以可以直接算出答案，不用一步步传'])],
        after=[dict(heading='换个例子验证', lines=['`n=3, time=2`：`divmod(2, 2) = (1, 0)`', '`k=1` 是奇数 → `n - t = 3 - 0 = 3`', '对照题目：`1→2→3`，2 秒后在 3 号，正确'])],
        one_liner='枕头每 n-1 秒碰一次端点，商的奇偶决定方向',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`n` 个人排成一排，枕头从 1 号开始，每秒传给下一个人，到队首或队尾就掉头',
                 '求 `time` 秒后谁拿着枕头',
                 '示例：`n=4, time=5` → `1→2→3→4→3→2`，答案 `2`'],
        quote='到达端点需要 n-1 时间。设 t = time mod (n-1)，如果 time/(n-1) 是偶数，说明正在从 1 到 n，答案为 1+t；如果是奇数，说明正在从 n 到 1，答案为 n-t。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从 1 走到 n（或反过来）恰好 `n-1` 秒，所以按 `n-1` 切段',
              '`divmod` 一次得到：走完几段 `k`、本段走了几步 `t`',
              '`k` 偶数 → 正向，`1 + t`；`k` 奇数 → 反向，`n - t`'],
        summary=['时间、空间都是 `O(1)`，不需要模拟 time 次',
                 '易错：周期段长是 `n-1`，不是 `n`',
                 '奇数反向时答案是 `n - t`，别写成 `n - t + 1`',
                 '同类：3178. 找出 K 秒后拿着球的孩子（完全一致）'],
    ),
)
