CONFIG = dict(
    num=2241, title='设计一个 ATM 机器', difficulty='Medium', category='设计',
    author='yiduobo', technique='贪心取钞（list 记库存）',
    tags=[],
    code='''
class ATM(object):

    def __init__(self):
        self.cnt_list = [0] * 5
        self.v = [20, 50, 100, 200, 500]

    def deposit(self, banknotesCount):
        for index, cnt in enumerate(banknotesCount):
            self.cnt_list[index] += cnt

    def withdraw(self, amount):
        res = [0] * 5
        for index in range(4, -1, -1):
            res[index] = amount // self.v[index]
            if res[index] > self.cnt_list[index]:
                res[index] = self.cnt_list[index]
            amount -= res[index] * self.v[index]

        if amount != 0:
            return [-1]

        for index in range(5):
            self.cnt_list[index] -= res[index]
        return res
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
        dict(type='array', var='self.v', label='面额 v', h=110),
        dict(type='array', var='self.cnt_list', label='库存张数 cnt_list', h=150, pointers={'index': 'blue'},
             color=lambda S, i, v: 'green' if v > 0 else None),
        dict(type='array', var='res', label='这次打算取的张数 res', h=150, pointers={'index': 'pink'}),
        dict(type='text', fn=lambda S: (f"还剩 `amount` = =={S['amount']}== 没凑" if 'amount' in S else ''), size=28),
        dict(type='calls', label='正在执行', h=110),
    ],
    watch=['amount', 'index', ('cnt_list', 'self.cnt_list', 'green'), 'res'],
    skip=['atm = ATM()', 'self.cnt_list = [0]', 'self.v = [', 'for index, cnt in enumerate', 'for index in range(4, -1',
          'for index in range(5)', 'amount -= res[index]'],
    max_steps=140,
    captions={
        'self.cnt_list[index] += cnt': '存入 `{self.v[index]}` 元钞票 `{cnt}` 张：`cnt_list[{index}]` → =={self.cnt_list[index]}==',
        'res = [0] * 5': '取款 `{amount}`：`res` 先记下每种钞票打算取几张，还没动库存',
        'res[index] = amount //': lambda S, B, r: (f"面额 `{S.self.v[S.index]}`：`{B.amount} // {S.self.v[S.index]}` = {S.res[S.index]} 张"
                                                   f"，库存 `{S.self.cnt_list[S.index]}` 张"),
        'if res[index] > self.cnt_list': lambda S, B, r: (f'想取 `{S.res[S.index]}` 张 > 库存 `{S.self.cnt_list[S.index]}` 张 → 库存不够，要改' if S.res[S.index] > S.self.cnt_list[S.index] else f'想取 `{S.res[S.index]}` 张 ≤ 库存，够用'),
        'res[index] = self.cnt_list[index]': '想取的比库存多 → 只能取库存的 `{res[index]}` 张',
        'if amount != 0': lambda S, B, r: (f'`amount = {S.amount}` 没凑完 → ==返回 [-1]==' if S.amount != 0
                                           else '`amount = 0`：凑齐了，可以真的取钱'),
        'return [-1]': '返回 `[-1]`：贪心已经取过大面额，剩下的凑不出，库存没动',
        'self.cnt_list[index] -= res[index]': '库存扣掉：`cnt_list[{index}]` → =={self.cnt_list[index]}==',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='存钱就是累加，取钱就按面额从大到小贪心',
        complexity='时间 `O(1)`（只有 5 种面额），空间 `O(1)`',
        problem=['ATM 有 `20 50 100 200 500` 五种钞票，可存可取',
                 '取款先取大面额，凑不出恰好 `amount` 就返回 `[-1]`',
                 '示例：存 `[0,0,1,2,1]` 后取 600 → `[0,0,1,0,1]`'],
        quote='对于存钱操作，使用一个list记录当前机器里每个种类钞票的数量就行了。对于取钱操作，按照题目描述是使用的贪心法一步步执行就好了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`cnt_list` 记每种钞票张数，存钱逐项加',
              '取钱从 500 往 20 走：先取 `amount // 面额`，不够就取库存全部',
              '样例里 600 取不出，说明面额没有倍数关系时贪心不一定凑得出'],
        summary=['每次操作只循环 5 次，`O(1)`',
                 '==凑不齐就整笔拒绝==，必须先算 `res` 再扣库存',
                 '原文为 Python 2 写法，`amount / self.v[index]` 已改为整数除法 `//`，并删去类型说明',
                 '对比灵神：灵神用 `min` 一步取得张数，yiduobo 先除再和库存比较，效果相同'],
    ),
)
