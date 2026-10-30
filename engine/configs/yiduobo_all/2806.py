CONFIG = dict(
    num=2806, title='取整购买后的账户余额', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='模 10 分离个位后分情况',
    tags=[],
    code='''
class Solution(object):
    def accountBalanceAfterPurchase(self, purchaseAmount):

        x = purchaseAmount % 10
        if x < 5:
            return 100 - (purchaseAmount - x)
        else:
            return 100 - (purchaseAmount + 10 - x)
''',
    call='[Solution().accountBalanceAfterPurchase(a) for a in (9, 15, 12, 4, 95)]',
    expect=[90, 80, 90, 100, 0],
    views=[
        dict(type='text', size=34, fn=lambda S: (f"个位 `x = {S['purchaseAmount']} % 10` = =={S['purchaseAmount'] % 10}==" if 'purchaseAmount' in S else '')),
        dict(type='text', size=32, fn=lambda S: (('x < 5：抹零，支出 = ' + f"`{S['purchaseAmount']} − {S['purchaseAmount'] % 10}` = =={S['purchaseAmount'] - S['purchaseAmount'] % 10}==") if S['purchaseAmount'] % 10 < 5 else ('x ≥ 5：反向抹零，支出 = ' + f"`{S['purchaseAmount']} + 10 − {S['purchaseAmount'] % 10}` = =={S['purchaseAmount'] + 10 - S['purchaseAmount'] % 10}==")) if 'purchaseAmount' in S else ''),
    ],
    watch=[('purchaseAmount', 'purchaseAmount', 'blue'), ('x', 'x', 'pink')],
    captions={
        'x = purchaseAmount': '`% 10` 把个位分离出来：`x = {x}`',
        'if x < 5': '`x = {x}`，和 `5` 比 → {"小于 5，往下抹零" if x < 5 else "不小于 5，要进位"}',
        'purchaseAmount - x': '抹零：支出 `{purchaseAmount} - {x} = {purchaseAmount - x}`，余额 =={ret}==',
        'purchaseAmount + 10': '反向抹零：支出 `{purchaseAmount} + 10 - {x} = {purchaseAmount + 10 - x}`，余额 =={ret}==',
    },
    cards=dict(
        one_liner='模 10 取出个位，小于 5 抹零，否则反向抹零',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['账户有 `100`，购买金额向最近的 `10` 的倍数取整，平局取较大者',
                 '返回购买后的余额',
                 '示例：`9` → `90`；`15` → `80`'],
        quote='题目实际上可以理解成对于整数的个位数在做四舍五入，那么只需通过模10将个位x分离出来，若x小于5，那么抹零……反之则是反向抹零。',
        quote_src='—— yiduobo 题解',
        idea=['个位 `x = 金额 % 10`',
              '`x < 5`：直接抹掉个位，支出 `金额 - x`',
              '`x >= 5`：凑到下一个十，支出 `金额 + 10 - x`'],
        summary=['时间、空间都是 `O(1)`',
                 '易错点：`x == 5` 属于进位一侧（取较大倍数）',
                 '边界：金额为 `100` 时 `x = 0`，支出 `100`，余额 `0`',
                 '示例用 `9 / 15 / 12` 三个数依次演示'],
    ),
)
