CONFIG = dict(
    num=991, title='坏了的计算器', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='逆向贪心', tags=[],
    code='''
class Solution(object):
    def brokenCalc(self, X, Y):

        res = 0
        while Y != X:
            if X >= Y:
                res += X - Y
                break
            if Y & 1:
                Y += 1
            else:
                Y //= 2
            res += 1
        
        return res
''',
    call='Solution().brokenCalc(3, 10)',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: f"从 ==X={S['X']}== 变到 ==Y={S['Y']}==（倒推：Y 偶数就除以 2，奇数就加 1）", h=70, size=34),
        dict(type='text', fn=lambda S: f"已用操作数 res = =={S.get('res', 0)}==", h=70, size=34),
    ],
    watch=['X', ('Y', 'Y', 'pink'), ('res', 'res', 'green')],
    captions={
        'while Y != X': lambda S, B, r: f'`Y = {S.Y}`，`X = {S.X}`：{"还没到，继续倒推" if S.Y != S.X else "相等了，结束"}',
        'if X >= Y': lambda S, B, r: f'`X = {S.X} >= Y = {S.Y}`？' + ('X 已不小于 Y：剩下只能一直减 1，补 `X - Y` 步' if S.X >= S.Y else '不成立：X 比 Y 小，至少要一次乘 2'),
        'if Y & 1': lambda S, B, r: f'`Y = {S.Y}` 是{"奇" if S.Y & 1 else "偶"}数：' + ('最后一步必是减 1，倒推回去 `Y + 1`' if S.Y & 1 else '最后一步必是乘 2，倒推回去 `Y / 2`'),
        'Y += 1': '倒推：`Y` 变 `{Y}`（对应正向的最后一步“减 1”）',
        'Y //= 2': '倒推：`Y` 变 `{Y}`（对应正向的最后一步“乘 2”）',
        'res += 1': '这一步算一次操作，`res = {res}`',
        'res += X - Y': '`res += {B.X} - {B.Y}` → {res}',
        'return res': '最少操作 `{res}` 次',
    },
    cards=dict(
        one_liner='正着乘 2 或减 1 难选，倒着“除 2 或加 1”只有一种选择',
        complexity='时间 `O(log Y)`，空间 `O(1)`',
        problem=['计算器显示 `X`，每次可“乘 2”或“减 1”',
                 '求把 `X` 变成 `Y` 的最少操作数',
                 '示例：`X = 3, Y = 10` → `3 → 6 → 5 → 10`，共 `3` 步'],
        quote='乘以2之后不应该出现两次连续的减1操作，理由很简单，对于X * 2 -1 - 1这个操作序列而言，(X - 1) * 2显然是更好的选择。',
        quote_src='—— yiduobo 题解原文',
        idea=['`X >= Y` 时只能减 1，直接补 `X - Y` 步',
              '`Y` 为偶数：最后一步必是乘 2，问题变成 X 到 `Y/2`',
              '`Y` 为奇数：最后一步必是减 1，问题变成 X 到 `Y+1`'],
        summary=['时间 `O(log Y)`，空间 `O(1)`',
                 '倒推时 Y 为奇数一定先加 1，因为乘 2 的结果不会是奇数',
                 '易错：`X >= Y` 要立即结束，不能再往下倒推',
                 '原文为 Python 2 写法，`Y /= 2` 已改为 `Y //= 2`'],
    ),
)
