CONFIG = dict(
    num=2241, title='设计一个 ATM 机器', difficulty='Medium', category='设计',
    author='灵茶山艾府', technique='从大到小贪心取钞',
    tags=[],
    code='''
DENOMINATIONS = [20, 50, 100, 200, 500]
KINDS = len(DENOMINATIONS)

class ATM:
    def __init__(self):
        self.banknotes = [0] * KINDS

    def deposit(self, banknotesCount: List[int]) -> None:
        # 存钱
        for i, count in enumerate(banknotesCount):
            self.banknotes[i] += count

    def withdraw(self, amount: int) -> List[int]:
        ans = [0] * KINDS

        # 计算每种钞票所需数量
        for i in range(KINDS - 1, -1, -1):
            ans[i] = min(amount // DENOMINATIONS[i], self.banknotes[i])
            amount -= ans[i] * DENOMINATIONS[i]

        # 无法取恰好 amount
        if amount > 0:
            return [-1]

        # 取钱
        for i, count in enumerate(ans):
            self.banknotes[i] -= count

        return ans
''',
    call='''atm = ATM()
atm.deposit([0, 0, 1, 2, 1])
r1 = atm.withdraw(600)
atm.deposit([0, 1, 0, 1, 1])
r2 = atm.withdraw(600)
r3 = atm.withdraw(550)
[r1, r2, r3]''',
    expect=[[0, 0, 1, 0, 1], [-1], [0, 1, 0, 0, 1]],
    views=[
        dict(type='text', fn=lambda S: '面额从左到右：`20`  `50`  `100`  `200`  `500`（下标 0–4）', size=26),
        dict(type='array', var='self.banknotes', label='ATM 里每种钞票的张数 banknotes', pointers={'i': 'blue'}, h=150,
             color=lambda S, i, v: 'green' if v > 0 else None),
        dict(type='array', var='ans', label='这次取款每种要取的张数 ans', pointers={'i': 'pink'}, h=150),
        dict(type='text', fn=lambda S: (f"还需要凑出 `amount` = =={S['amount']}==" if 'amount' in S else ''), size=28),
        dict(type='calls', label='正在执行', h=110),
    ],
    watch=['amount', 'i', ('banknotes', 'self.banknotes', 'green'), 'ans'],
    skip=['KINDS = len', 'DENOMINATIONS = ', 'atm = ATM()', 'self.banknotes = [0]', 'for i, count in enumerate(banknotesCount)', 'for i in range(KINDS - 1', 'for i, count in enumerate(ans)', 'amount -= ans[i]'],
    max_steps=140,
    captions={
        'self.banknotes[i] += count': '存入面额 `{[20,50,100,200,500][i]}` 共 `{count}` 张：`banknotes[{i}]` → =={self.banknotes[i]}==',
        'ans = [0] * KINDS': '取款 `{amount}`：先准备一个 `ans`，记下每种钞票各取几张（这时还不动库存）',
        'ans[i] = min': lambda S, B, r: (f"面额 `{[20,50,100,200,500][S.i]}`：最多想取 `{B.amount} // {[20,50,100,200,500][S.i]}` = {B.amount // [20,50,100,200,500][S.i]} 张，"
                                         f"库存 `{S.self.banknotes[S.i]}` 张 → 取 =={S.ans[S.i]}== 张，还差 =={B.amount - S.ans[S.i]*[20,50,100,200,500][S.i]}=="),
        'amount -= ans[i]': '剩余 `amount` = `{B.amount} - {ans[i]}×{[20,50,100,200,500][i]}` = =={amount}==，接着看更小的面额',
        'if amount > 0': lambda S, B, r: (f'`amount = {S.amount} > 0`：从大到小取完仍凑不齐 → ==整笔拒绝==，库存不动' if S.amount > 0
                                          else '`amount = 0`：恰好凑齐，可以真正取钱'),
        'return [-1]': '返回 `[-1]`：要么全取、要么全不取，库存保持原样',
        'self.banknotes[i] -= count': '真正扣库存：面额 `{[20,50,100,200,500][i]}` 减 `{count}` 张 → `banknotes[{i}]` = =={self.banknotes[i]}==',
        'return ans': '返回 `{ans}`',
    },
    cards=dict(
        one_liner='先在 ans 里试算，凑齐了才真的扣库存',
        complexity='时间 `O(C)`（`C = 5` 种面额），空间 `O(C)`',
        problem=['ATM 有 `20 50 100 200 500` 五种钞票，支持 `deposit` 存钞、`withdraw` 取款',
                 '取款==优先取大面额==；凑不出恰好 `amount` 就返回 `[-1]` 且不取任何钞票',
                 '示例：存 `[0,0,1,2,1]`，取 600 → `[0,0,1,0,1]`；再存后取 600 → `[-1]`'],
        quote='从大到小枚举钞票面额……可以取出 c = min(⌊amount/d⌋, banknote) 张钞票。然后把 amount 减少 c·d，枚举下一个钞票面额。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`banknotes` 数组存每种钞票的张数，存钱就是逐项相加',
              '取钱时每个面额取 `min(amount // d, 库存)` 张，大面额先取',
              '枚举完 `amount` 还有剩 → 拒绝；否则再统一扣库存',
              '代码里没写死 5，用 `DENOMINATIONS` 和 `KINDS`，加面额只改一处'],
        summary=['复杂度：每个操作 `O(C)`，`C = 5`',
                 '易错点：==先算 ans，确认凑齐再扣库存==，否则拒绝时库存被改坏',
                 '易错点：有 500 就必须先取 500，不能为了凑整而跳过大面额（贪心不回头）',
                 '思考题：去掉“优先取大”后，变成有限个数的背包，要用 DP'],
    ),
)
