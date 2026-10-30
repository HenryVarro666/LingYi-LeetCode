CONFIG = dict(
    num=2543, title='判断一个点是否可以到达', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='gcd 是否为 2 的幂', tags=['灵神题单', '数学算法', '难度分 2221'],
    code='''
class Solution(object):
    def isReachable(self, targetX, targetY):
        while targetX:
            targetY, targetX = targetX, targetY % targetX

        return targetY & (targetY - 1) == 0
''',
    call='Solution().isReachable(12, 20)',
    expect=True,
    views=[
        dict(type='text', h=120, size=34, fn=lambda S: f"当前 (x, y) = (`{S['targetX']}`, `{S['targetY']}`)，辗转相除只改变数对，不改变 gcd"),
        dict(type='text', h=120, size=34, fn=lambda S: (lambda y: f"gcd = y = `{y}`，二进制 `{y:b}`，`y & (y−1)` = =={y & (y-1)}==" )(S['targetY']) if S['targetX'] == 0 else '辗转相除中：x 变小，最后 x = 0 时 y 就是 gcd'),
    ],
    watch=['targetX', 'targetY'],
    captions={
        'while targetX': lambda S, B, r: (f'`targetX = {S.targetX}` 不为 0，继续辗转相除' if S.targetX else f'`targetX = 0`：辗转相除结束，gcd 就是 ==`targetY = {S.targetY}`=='),
        'targetY, targetX = targetX': '辗转相除：`(x, y)` → `(y % x, x)`，得到 `({targetX}, {targetY})`，gcd 不变',
        'return': lambda S, B, r: f'gcd = `{S.targetY}`，`{S.targetY} & {S.targetY - 1}` = {S.targetY & (S.targetY - 1)} → =={r}==：{"gcd 是 2 的幂，可达" if r else "gcd 不是 2 的幂，不可达"}',
    },
    cards=dict(
        one_liner='前两种操作不改 gcd，后两种让 gcd 翻倍，所以 gcd 必须是 2 的幂',
        complexity='时间 `O(log min(x, y))`，空间 `O(1)`',
        problem=['无限网格从 `(1,1)` 出发，每步 `(x,y)` 可变为：',
                 '`(x,y-x)`、`(x-y,y)`、`(2x,y)`、`(x,2y)` 之一',
                 '问能否到达 `(targetX, targetY)`',
                 '示例：`(4,7)` → `True`，`(6,9)` → `False`'],
        quote='可以发现前两种减法不会影响x和y的最大公约数，而后两种倍增操作则可能使得x和y的最大公约数也倍增。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据太大不能 BFS，只能找规律',
              '正推：gcd 只会乘 2，所以 gcd 必是 2 的幂（必要条件）',
              '倒推：都是奇数时，较大者加较小者变偶数再折半，必能走到 `(1,1)`（充分条件）'],
        summary=['时间 `O(log)`，空间 `O(1)`',
                 '判断 2 的幂：`y & (y-1) == 0`',
                 'Python 里 `&` 优先级高于 `==`，所以不加括号也对',
                 '原文代码未改动，用手写辗转相除求 gcd',
                 '两个方向（正推必要、倒推充分）缺一不可'],
    ),
)
