CONFIG = dict(
    num=1560, title='圆形赛道上经过次数最多的扇区', difficulty='Easy', category='模拟',
    author='yiduobo', technique='整圈抵消 · 只看起点到终点',
    code='''
class Solution(object):
    def mostVisited(self, n, rounds):

        l = rounds[0]
        r = rounds[-1]
        
        if l <= r:
            return list(range(l, r + 1))
        else:
            return list(range(1, r + 1)) + list(range(l, n + 1))
''',
    call='Solution().mostVisited(4, [3, 4, 1, 2, 3, 1])',
    expect=[1, 3, 4],
    views=[
        dict(type='array', var=lambda S: list(range(1, S['n'] + 1)), label='扇区 1..n（蓝 = 起点 l，粉 = 终点 r）', cell=110, h=220,
             color=lambda S, i, v: ('blue' if v == S.get('l') else 'pink' if v == S.get('r') else None)),
        dict(type='array', var='rounds', label='rounds：每一圈结束的扇区', cell=90, h=200),
        dict(type='text', fn=lambda S: (f"`l = {S['l']}` > `r = {S['r']}`：跨过了赛道末尾" if S['l'] > S['r'] else f"`l = {S['l']}` <= `r = {S['r']}`：不跨圈") if 'r' in S else '', size=30, h=70),
    ],
    watch=['n', ('l', 'l', 'blue'), ('r', 'r', 'pink')],
    captions={
        'l = rounds[0]': '起点 `l = {l}`：整圈都会回到这里，多跑的整圈每个扇区各经过一次，==互相抵消==',
        'r = rounds[-1]': '终点 `r = {r}`：只需要看==起点 l 到终点 r== 这一段路',
        'if l <= r': lambda S, B, r: (f'`{S.l} <= {S.r}`：起点不在终点之后 → 这一段不用绕过末尾' if S.l <= S.r else f'`{S.l} > {S.r}`：起点在终点之后 → 这一段要跨过赛道末尾，分成两部分'),
        'return list(range(l, r + 1))': '经过 `{l}` 到 `{r}` 的所有扇区 → `{ret}`',
        'return list(range(1, r + 1))': '两部分：赛道开头 `1..{r}` 加上 `{l}..{n}`（从起点跑到末尾）→ `{ret}`',
    },
    cards=dict(
        one_liner='整圈互相抵消，只看起点到终点这一段',
        complexity='时间 `O(n)`，空间 `O(1)`（不计返回值）',
        problem=['环形赛道有 `n` 个扇区（1 到 n），`rounds[i]` 是第 i 圈的终点，起点是 `rounds[0]`',
                 '马拉松按逆时针 1 → 2 → … → n → 1 跑，求经过次数最多的扇区（升序返回）',
                 '本视频：`n = 4`，`rounds = [3,4,1,2,3,1]` → `[1,3,4]`'],
        quote='从起点开始跑任意的整圈，最终都会回到起点。一个整圈将经过每个扇区一次，因此跑任意整圈经过各个扇区的次数都是一样的。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个整圈让所有扇区各加 1，不影响谁最多',
              '剩下的只有 ==起点 l 到终点 r== 这一段，这一段里的扇区多经过一次',
              '`l > r` 时这一段绕过了末尾：`1..r` 和 `l..n` 两部分'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：`l > r` 要拼接两段，不要写成 `range(l, r)`',
                 '`l == r` 时只有起点一个扇区',
                 '原文为 Python 2 写法，`range` 返回列表，在 Python 3 里已改为 `list(range(...))`'],
    ),
)
