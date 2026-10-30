CONFIG = dict(
    num=1927, title='求和游戏', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='分情况推导 · 问号差 × 9',
    tags=['博弈论', '贪心与思维', '难度分 2005'],
    code='''
class Solution(object):
    def sumGame(self, num):

        left_q = right_q = 0
        left_s = right_s = 0
        n = len(num)
        for char in num[:n // 2]:
            if char == '?':
                left_q += 1
            else:
                left_s += int(char)
        
        for char in num[n // 2:]:
            if char == '?':
                right_q += 1
            else:
                right_s += int(char)

        return (left_s - right_s) * 2 != (right_q - left_q) * 9
''',
    call='Solution().sumGame("?3295???")',
    expect=False,
    views=[
        dict(type='string', var='num', h=200, cell=100, label='num（前一半 | 后一半）',
             color=lambda S, i, v: ('blue' if i < len(S['num']) // 2 else 'pink') if v == '?' else None),
        dict(type='text', h=70, size=30,
             fn=lambda S: f"左半：问号 ==​{S.get('left_q', 0)}== 个，数字和 =={S.get('left_s', 0)}==　　右半：问号 =={S.get('right_q', 0)}== 个，数字和 =={S.get('right_s', 0)}=="),
        dict(type='text', h=70, size=30,
             fn=lambda S: f"2×(左和−右和) = =={(S.get('left_s', 0) - S.get('right_s', 0)) * 2}==　　9×(右问号−左问号) = =={(S.get('right_q', 0) - S.get('left_q', 0)) * 9}==" if 'n' in S else ''),
    ],
    watch=[('left_q', 'left_q', 'blue'), ('left_s', 'left_s', 'cyan'), ('right_q', 'right_q', 'pink'), ('right_s', 'right_s', 'orange')],
    captions={
        'left_q = right_q': '分别统计两侧的问号个数 `left_q`、`right_q`',
        'left_s = right_s': '分别统计两侧已有数字之和 `left_s`、`right_s`',
        'n = len': '`n = {n}`，左半 `num[:{n//2}]`，右半 `num[{n//2}:]`',
        'for char in num[:': '左半：逐个字符扫描，取完这一半就结束循环',
        'for char in num[n': '右半：逐个字符扫描，取完这一半就结束循环',
        'left_q += 1': '左半遇到问号：`left_q` → =={left_q}==',
        'left_s += int': '左半遇到数字 `{char}`：`left_s` → =={left_s}==',
        'right_q += 1': '右半遇到问号：`right_q` → =={right_q}==',
        'right_s += int': '右半遇到数字 `{char}`：`right_s` → =={right_s}==',
        'return': lambda S, B, r: (f'`2×({S.left_s}−{S.right_s}) = {(S.left_s - S.right_s) * 2}`，`9×({S.right_q}−{S.left_q}) = {(S.right_q - S.left_q) * 9}`，'
                                    + ('相等 → Bob 获胜 → ==返回 False==' if not r else '不相等 → Alice 获胜 → ==返回 True==')),
    },
    cards=dict(
        one_liner='问号个数奇数 Alice 必赢；偶数时看两侧差是否等于问号差×9',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['偶数长度字符串，含数字和 `?`，Alice 先手，轮流把 `?` 改成 0~9',
                 '填完后左半数字和 ==等于== 右半则 Bob 赢，否则 Alice 赢',
                 '示例：`"?3295???"` → `false`'],
        quote='alice只需要将较大这边的问号变成9，将较小那边的问号变成0即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['问号总数是奇数：最后一个问号归 Alice，她总能破坏相等',
              '两侧问号一样多：已有数字和相等 → Bob 照着对面的数模仿，Bob 赢；不等 → Alice 赢',
              '问号不一样多：先看 2 个问号都在一侧的小例子，推出 ==差 = 问号差/2 × 9== 时 Bob 才赢'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文为 Python 2 写法，`n / 2` 已改为 `n // 2`',
                 '最终式：`(left_s − right_s) × 2 != (right_q − left_q) × 9` 则 Alice 赢',
                 '奇数个问号时两侧问号差为奇数，右边是奇数乘 9，左边是偶数，等式必不成立 → 自动返回 True',
                 '对比灵神：灵神把问号当权值 9、数字当 2 倍，一趟累加 d；这里分开统计再套公式'],
    ),
)
