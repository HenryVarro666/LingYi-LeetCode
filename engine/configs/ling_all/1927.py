def _w(S):
    return [9 if c == '?' else int(c) * 2 for c in S['num']]


CONFIG = dict(
    num=1927, title='求和游戏', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='问号权值 9，数字权值 2x',
    tags=['博弈论', '贪心与思维', '难度分 2005'],
    code='''
class Solution:
    def sumGame(self, num: str) -> bool:
        m = len(num) // 2
        d = 0
        for i, ch in enumerate(num):
            x = int(ch) * 2 if ch != '?' else 9
            d += x if i < m else -x
        return d != 0
''',
    call='Solution().sumGame("?3295???")',
    expect=False,
    views=[
        dict(type='string', var='num', pointers={'i': 'yellow'}, label='num（前一半 | 后一半）', h=230, cell=100,
             color=lambda S, i, v: ('blue' if i < len(S['num']) // 2 else 'pink') if 'i' in S and i <= S['i'] else None),
        dict(type='array', var=_w, label='权值：数字 = 2×数字，? = 9', h=230, cell=100,
             color=lambda S, i, v: ('blue' if i < len(S['num']) // 2 else 'pink') if 'i' in S and i <= S['i'] else None),
        dict(type='text', fn=lambda S: ('d = 左半权值和 − 右半权值和 = ==' + str(S['d']) + '==' if 'd' in S else ''), size=30, h=70),
    ],
    watch=[('m', 'm', 'cyan'), ('i', 'i', 'yellow'), ('x', 'x', 'orange'), ('d', 'd', 'green')],
    captions={
        'm = len': '`m = {m}`：前 {m} 个是左半，后 {m} 个是右半',
        'd = 0': '`d` = 左半权值和 − 右半权值和，Bob 获胜 ⇔ ==d = 0==',
        'x = int': lambda S, B, r: (f'`{S.ch}` 是问号，权值取 ==9==' if S.ch == '?' else f'`{S.ch}` 是数字，权值 = 数字 × 2 = =={S.x}=='),
        'd += x': lambda S, B, r: (f'`i = {S.i} < m`：在左半，`d += {S.x}` → =={S.d}==' if S.i < S.m else f'`i = {S.i} ≥ m`：在右半，`d -= {S.x}` → =={S.d}=='),
        'return d': lambda S, B, r: (f'`d = {S.d}`，左右权值相等 → Bob 总能模仿、保持平衡 → ==返回 False==' if S.d == 0 else f'`d = {S.d} ≠ 0` → Alice 必胜 → ==返回 True=='),
    },
    cards=dict(
        one_liner='问号当 9、数字当 2 倍，左右权值和相等才是 Bob 赢',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['偶数长度字符串，含数字和 `?`，Alice 先手，轮流把 `?` 改成 0~9',
                 '填完后左半数字和 ==等于== 右半则 Bob 赢，否则 Alice 赢',
                 '示例：`"?3295???"` → `false`（Bob 赢）'],
        quote='把 Bob 获胜的充要条件两边同乘以 2，移项得 9q_L + 2S_L = 9q_R + 2S_R。我们可以把问号视作 9，数字字符的权值等于该数字的值乘以 2。',
        quote_src='—— 灵茶山艾府题解（写法二）',
        idea=['问号个数 q 是奇数：最后一手是 Alice，必赢',
              'q 为偶数：Bob 赢 ⇔ `S_R − S_L = (q_L − q_R)/2 × 9`，Bob 用「模仿」保持平衡',
              '整理后：左右权值和（问号 9，数字 ×2）相等 ⇔ Bob 赢'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`d != 0` 就是 Alice 赢；`d == 0` 是 Bob 赢',
                 '奇数个问号时 `d` 也不会是 0：问号权值 9 为奇数，数字权值为偶数，总权值差为奇数',
                 '写法一：分别统计两侧问号数 `q` 与数字和 `S`，用 `(ql-qr)//2*9 != sr-sl` 判断'],
    ),
)
