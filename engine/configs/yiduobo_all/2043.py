def _tr(S, B, ret):
    n, b, a1, a2, m = len(S['self.balance']), S['self.balance'], S['account1'], S['account2'], S['money']
    if a1 < 1 or a1 > n:
        return f'转出账号 `{a1}` 不在 1~{n} → ==无效=='
    if a2 < 1 or a2 > n:
        return f'转入账号 `{a2}` 不在 1~{n} → ==无效=='
    if b[a1 - 1] < m:
        return f'两个账号都有效；转出方 `{b[a1 - 1]}` < `{m}` → ==钱不够，无效=='
    return f'两个账号都有效；转出方 `{b[a1 - 1]}` >= `{m}` → 可以转'


def _chk(S, B, ret):
    n, b, a, m = len(S['self.balance']), S['self.balance'], S['account'], S['money']
    if a < 0 or a > n:
        return f'账号 `{a}` 不在 1~{n} → ==无效=='
    return f'账号 `{a}` 有效'


def _wd(S, B, ret):
    n, b, a, m = len(S['self.balance']), S['self.balance'], S['account'], S['money']
    if a < 0 or a > n:
        return f'账号 `{a}` 不在 1~{n} → ==无效=='
    return f'账号 `{a}` 有效，再看余额'


def _wd2(S, B, ret):
    b, a, m = S['self.balance'], S['account'], S['money']
    if b[a - 1] < m:
        return f'`{b[a - 1]}` < 取款 `{m}` → ==钱不够，无效=='
    return f'`{b[a - 1]}` >= 取款 `{m}` → 够，可以取'


CONFIG = dict(
    num=2043, title='简易银行系统', difficulty='Medium', category='设计',
    author='yiduobo', technique='模拟 · 先校验再操作',
    code='''
class Bank(object):

    def __init__(self, balance):
        self.balance = balance[:]

    def transfer(self, account1, account2, money):
        if account1 < 1 or account1 > len(self.balance):
            return False
        if account2 < 1 or account2 > len(self.balance):
            return False
        if self.balance[account1 - 1] < money:
            return False
        
        self.balance[account1 - 1] -= money
        self.balance[account2 - 1] += money
        return True

    def deposit(self, account, money):
        if account < 0 or account > len(self.balance):
            return False
        
        self.balance[account - 1] += money
        return True

    def withdraw(self, account, money):
        if account < 0 or account > len(self.balance):
            return False
        if self.balance[account - 1] < money:
            return False
        
        self.balance[account - 1] -= money
        return True
''',
    call='''bank = Bank([10, 100, 20, 50, 30])
res = [bank.withdraw(3, 10), bank.transfer(5, 1, 20), bank.deposit(5, 20), bank.transfer(3, 4, 15), bank.withdraw(10, 50)]
res''',
    expect=[True, True, True, False, False],
    views=[
        dict(type='array', var='self.balance', label='balance（账户 1~5，下标 = 账号 − 1，黄框 = 刚改动）', cell=110,
             pointers={'account - 1': 'blue', 'account1 - 1': 'pink', 'account2 - 1': 'cyan'},
             pointer_labels={'account - 1': 'account', 'account1 - 1': 'from', 'account2 - 1': 'to'}, h=230),
        dict(type='text', fn=lambda S: (f"本次操作：`money = {S['money']}`" if 'money' in S else ''), size=28, h=60),
        dict(type='calls', label='正在执行的操作', h=150),
    ],
    watch=[('money', 'money', 'orange'), ('balance', 'self.balance', 'green')],
    captions={
        'self.balance = balance[:]': '复制一份余额：`balance[i-1]` 就是账号 `i` 的钱',
        7: lambda S, B, ret: (f"转出账号 `{S['account1']}` 在 1~{len(S['self.balance'])} 里吗？" + ('不在 → ==无效==' if S['account1'] < 1 or S['account1'] > len(S['self.balance']) else '在')),
        9: lambda S, B, ret: (f"转入账号 `{S['account2']}` 在 1~{len(S['self.balance'])} 里吗？" + ('不在 → ==无效==' if S['account2'] < 1 or S['account2'] > len(S['self.balance']) else '在')),
        11: lambda S, B, ret: (f"转出方有 `{S['self.balance'][S['account1'] - 1]}`，要转 `{S['money']}`：" + ('==不够，无效==' if S['self.balance'][S['account1'] - 1] < S['money'] else '够，可以转')),
        'self.balance[account1 - 1] -= money': '转出方扣钱：`balance[{account1 - 1}]` → {self.balance[account1 - 1]}',
        'self.balance[account2 - 1] += money': '转入方加钱：`balance[{account2 - 1}]` → {self.balance[account2 - 1]}',
        19: _chk,
        26: _wd,
        'self.balance[account - 1] += money': '存款：`balance[{account - 1}]` → {self.balance[account - 1]}',
        'if self.balance[account - 1] < money': _wd2,
        'self.balance[account - 1] -= money': '取款：`balance[{account - 1}]` → {self.balance[account - 1]}',
        'return False': '无效交易，余额不动，返回 `False`',
        'return True': '交易成功，返回 `True`',
    },
    cards=dict(
        one_liner='每个操作先逐条校验，全通过才改余额',
        complexity='每个操作 `O(1)`，空间 `O(n)`',
        problem=['`n` 个账户，编号 `1~n`；实现 `transfer`、`deposit`、`withdraw`',
                 '账号不在 `1~n`，或出钱的一方余额不足 → 交易无效，返回 `false`',
                 '示例：`withdraw(3,10)`、`transfer(5,1,20)`、`deposit(5,20)`、`transfer(3,4,15)`、`withdraw(10,50)` → `T T T F F`'],
        quote='对于题目中的三种操作，首先需要判断操作的账号是否在1到n之间，接下来需要判断出钱的这一方账户里面是否有足够的钱。如果都没问题，那么就执行对应的操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['原文说只需要记录每个用户当前的存款数；代码里用一个列表 `balance`，账号 `i` 对应下标 `i-1`',
              '三种操作都是：==先校验，再修改==',
              '`transfer` 要校验两个账号和转出方余额，`withdraw` 校验账号和余额，`deposit` 只校验账号'],
        summary=['每个操作 `O(1)`，空间 `O(n)`',
                 '易错：账号从 1 开始，访问要 `account - 1`',
                 '易错：必须先校验、后修改；转账时先扣后加，校验没过就不能动任何一方',
                 '原文 `deposit` / `withdraw` 里写的是 `account < 0`，账号 0 不在题目范围内，不影响本题',
                 '本题代码是 Python 2 风格但无需改动'],
    ),
)
