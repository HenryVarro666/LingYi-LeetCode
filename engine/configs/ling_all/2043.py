def _tr(S, B, ret):
    n, b, a1, a2, m = S['self.n'], S['self.b'], S['account1'], S['account2'], S['money']
    if a1 > n or a2 > n:
        return f'账户号超过 `n = {n}` → ==越界，无效=='
    if b[a1 - 1] < m:
        return f'账户都存在；`b[{a1 - 1}] = {b[a1 - 1]}` < `{m}` → ==余额不足，无效=='
    return f'账户都存在；`b[{a1 - 1}] = {b[a1 - 1]}` >= `{m}` → 余额够，可以转'


def _dep(S, B, ret):
    n, a = S['self.n'], S['account']
    return f'账户号 `{a}` > `n = {n}` → ==越界，返回 false==' if a > n else f'账户号 `{a}` 没越界，存款没有别的限制'


def _wd(S, B, ret):
    n, b, a, m = S['self.n'], S['self.b'], S['account'], S['money']
    if a > n:
        return f'账户号 `{a}` > `n = {n}` → ==越界，返回 false=='
    if b[a - 1] < m:
        return f'账户存在；`b[{a - 1}] = {b[a - 1]}` < `{m}` → ==余额不足，返回 false=='
    return f'账户存在；`b[{a - 1}] = {b[a - 1]}` >= `{m}` → 余额够'


CONFIG = dict(
    num=2043, title='简易银行系统', difficulty='Medium', category='设计',
    author='灵茶山艾府', technique='模拟 · 数组存余额',
    code='''
class Bank:
    def __init__(self, balance: List[int]) -> None:
        self.b = balance
        self.n = len(balance)

    def transfer(self, account1: int, account2: int, money: int) -> bool:
        if account1 > self.n or account2 > self.n or self.b[account1 - 1] < money:
            return False
        self.b[account1 - 1] -= money
        self.b[account2 - 1] += money
        return True

    def deposit(self, account: int, money: int) -> bool:
        if account > self.n:
            return False
        self.b[account - 1] += money
        return True

    def withdraw(self, account: int, money: int) -> bool:
        if account > self.n or self.b[account - 1] < money:
            return False
        self.b[account - 1] -= money
        return True
''',
    call='''bank = Bank([10, 100, 20, 50, 30])
res = [bank.withdraw(3, 10), bank.transfer(5, 1, 20), bank.deposit(5, 20), bank.transfer(3, 4, 15), bank.withdraw(10, 50)]
res''',
    expect=[True, True, True, False, False],
    views=[
        dict(type='array', var='self.b', label='b（账户 1~5 的余额，下标 = 账户号 − 1，黄框 = 刚改动）', cell=110,
             pointers={'account - 1': 'blue', 'account1 - 1': 'pink', 'account2 - 1': 'cyan'},
             pointer_labels={'account - 1': 'account', 'account1 - 1': 'from', 'account2 - 1': 'to'}, h=230),
        dict(type='text', fn=lambda S: (f"本次操作：`money = {S['money']}`" if 'money' in S else ''), size=28, h=60),
        dict(type='calls', label='正在执行的操作', h=150),
    ],
    watch=[('n', 'self.n'), ('b', 'self.b'), ('money', 'money', 'orange')],
    captions={
        'self.b = balance': '`b` 直接存余额：账户 `i` 的钱在 `b[i-1]`',
        'self.n = len(balance)': '`n` 记账户数，越界判断要用',
        'if account1 > self.n': _tr,
        'self.b[account1 - 1] -= money': '转出方扣钱：`b[{account1 - 1}]` → {self.b[account1 - 1]}',
        'self.b[account2 - 1] += money': '转入方加钱：`b[{account2 - 1}]` → {self.b[account2 - 1]}',
        'if account > self.n:': _dep,
        'self.b[account - 1] += money': '存款：`b[{account - 1}]` → {self.b[account - 1]}',
        'if account > self.n or': _wd,
        'self.b[account - 1] -= money': '取款：`b[{account - 1}]` → {self.b[account - 1]}',
        'return False': '无效交易，什么都不改，返回 `False`',
        'return True': '交易成功，返回 `True`',
    },
    cards=dict(
        one_liner='用数组存余额，先判越界和余额，再改数',
        complexity='每个操作 `O(1)`，空间 `O(1)`（直接用传入的数组）',
        problem=['`n` 个账户，编号 `1~n`，初始余额 `balance`',
                 '实现 `transfer`、`deposit`、`withdraw`；账号越界或余额不足 → 无效，返回 `false`',
                 '示例：`withdraw(3,10)`、`transfer(5,1,20)`、`deposit(5,20)`、`transfer(3,4,15)`、`withdraw(10,50)` → `T T T F F`'],
        quote='下面的三个方法，如果下标越界，返回 false。注意 account_i 是从 1 开始的，访问数组需要减一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['账户从 1 开始，数组从 0 开始：访问一律 `b[account - 1]`',
              '`transfer` 要判两个账户是否越界、转出方余额够不够',
              '`deposit` 只判越界；`withdraw` 判越界 + 余额'],
        summary=['所有操作 `O(1)`，空间 `O(1)`',
                 '易错：下标要减一，越界判断是 `account > n`（题目保证 `account >= 1`）',
                 '易错：先判断“无效”再修改，不能先扣后判',
                 '`transfer` 里条件的短路顺序保证了 `b[...]` 不会越界访问'],
    ),
)
