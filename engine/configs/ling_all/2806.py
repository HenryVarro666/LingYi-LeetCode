CONFIG = dict(
    num=2806, title='取整购买后的账户余额', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='个位四舍五入公式',
    tags=[],
    code='''
class Solution:
    def accountBalanceAfterPurchase(self, purchaseAmount: int) -> int:
        return 100 - (purchaseAmount + 5) // 10 * 10
''',
    call='[Solution().accountBalanceAfterPurchase(a) for a in (9, 15, 12, 4, 95)]',
    expect=[90, 80, 90, 100, 0],
    views=[
        dict(type='text', size=34, fn=lambda S: (f"`({S['purchaseAmount']} + 5) // 10 * 10` = =={(S['purchaseAmount'] + 5) // 10 * 10}==  （实际支出）" if 'purchaseAmount' in S else '')),
        dict(type='text', size=34, fn=lambda S: (f"余额 `100 − {(S['purchaseAmount'] + 5) // 10 * 10}` = =={100 - (S['purchaseAmount'] + 5) // 10 * 10}==" if 'purchaseAmount' in S else '')),
        dict(type='text', size=26, fn=lambda S: '个位 ≤ 4 舍去；个位 ≥ 5 进位加 10；加 5 再整除 10 正好统一'),
    ],
    watch=[('purchaseAmount', 'purchaseAmount', 'blue')],
    captions={
        'return 100': '先 `+5` 再 `// 10`：`({purchaseAmount} + 5) // 10 = {(purchaseAmount + 5) // 10}`，再 `* 10` 得实际支出 `{(purchaseAmount + 5) // 10 * 10}`；余额 =={ret}==',
    },
    cards=dict(
        one_liner='个位数四舍五入，加 5 再整除 10 一步搞定',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['钱包有 `100`，购买金额向最近的 `10` 的倍数取整，平局取较大者',
                 '返回购买后的余额',
                 '示例：`9` → `90`；`15` → `80`'],
        quote='当个位数 ≥ 5 时，把个位数变成 0，然后增加 10。这两种情况可以统一为公式 ⌊(purchaseAmount+5)/10⌋·10',
        quote_src='—— 灵茶山艾府题解',
        idea=['题意就是把个位数「四舍五入」：`12 → 10`，`15 → 20`',
              '加 `5` 后个位 ≥ 5 的数会向十位进 1，再 `// 10 * 10` 抹掉个位',
              '平局（个位恰为 5）自然进位，符合「取较大倍数」'],
        summary=['时间、空间都是 `O(1)`',
                 '易错点：平局要取较大者，所以是 `+5` 而不是 `+4`',
                 '`// 10 * 10` 的顺序不能反，先乘会得到原数',
                 '示例用 `9 / 15 / 12` 三个数依次演示'],
    ),
)
