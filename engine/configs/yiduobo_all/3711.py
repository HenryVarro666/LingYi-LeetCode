CONFIG = dict(
    num=3711, title='不出现负余额的最大交易', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='反悔堆：撤销负得最多的交易',
    tags=['堆（优先队列）', '反悔贪心'],
    code='''
class Solution(object):
    def maxTransactions(self, transactions):
        
        s = 0
        neg = []
        res = 0
        for t in transactions:
            s += t
            if t < 0:
                heapq.heappush(neg, t)
            if s < 0:
                s -= heapq.heappop(neg)
            else:
                res += 1
        
        return res
''',
    call='Solution().maxTransactions([2,-3,-1,4,-5,1])',
    expect=5,
    views=[
        dict(type='text', fn=lambda S: (f"当前交易 `t={S['t']}`；余额 `s=`==`{S['s']}`==；已执行交易数 `res=`==`{S['res']}`==" if 't' in S else '账户余额从 0 开始，必须始终非负'), size=26),
        dict(type='array', var='transactions', label='transactions（正 = 收入，负 = 支出）', h=230, cell=96,
             color=lambda S, i, v: ('yellow' if 't' in S and v == S['t'] else None)),
        dict(type='heap', var='neg', label='neg：已执行的支出（堆顶 = 负得最多的）', h=300),
    ],
    watch=[('s', 's', 'blue'), ('t', 't', 'yellow'), ('res', 'res', 'green')],
    captions={
        4: '`s`：当前余额（所有已执行交易之和）',
        'neg = []': '`neg` 是小顶堆，存已执行的负交易，堆顶 = 负得最多的那笔',
        6: '`res`：已执行的交易数',
        'for t in': '看下一笔交易 `t = {t}`',
        's += t': '先假设执行：`s` → =={s}==',
        'if t < 0': lambda S, B, r: (f'`t = {S.t} < 0`：是支出，记入堆里，以后可能要撤销' if S.t < 0 else f'`t = {S.t} ≥ 0`：收入，无条件执行'),
        'heappush': '支出 `{t}` 入堆：{neg}',
        'if s < 0': lambda S, B, r: (f'`s = {S.s} < 0`：余额为负 → 必须撤销之前负得最多的一笔' if S.s < 0 else f'`s = {S.s} ≥ 0`：余额没问题 → 这笔交易算数'),
        's -= heapq.heappop': lambda S, B, r: f'撤销最负的那笔 `{B.s - S.s}`（`s` 加回 `{S.s - B.s}`）：`s` = =={S.s}==；执行一笔又撤销一笔，`res` 不变',
        'res += 1': '多执行一笔，`res` → =={res}==',
        'return res': '最多能执行 `{res}` 笔交易',
    },
    cards=dict(
        one_liner='先假设都执行，余额为负就撤销负得最多的那笔',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`transactions[i]`：正数是收入，负数是支出，账户初始为 0',
                 '必须按顺序，可以跳过某些交易，任何时刻余额都要 `≥ 0`',
                 '求最多能执行多少笔交易',
                 '本视频：`[2,-3,-1,4,-5,1]` → `5`'],
        quote='对于金额非负的交易就应该无条件执行交易，而对于金额为负数的交易，则可以先尝试执行，如果执行后金额变成了负数，则必须取消之前已经进行的某次交易。',
        quote_src='—— yiduobo 题解原文',
        idea=['收入一定执行；支出先执行，并把它放进堆',
              '余额变负：取消堆顶，即==支出最大的那笔==，余额恢复得最多',
              '这一进一出交易数不变，但余额最大 → 后面更有空间'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：`s < 0` 时 `res` 不加；`s -= heappop(neg)` 是减一个负数，即加回钱',
                 '题意说明：题面库里没有，按 yiduobo 文章理解题意',
                 '原文为 Python 2 风格，本题代码无需修改'],
    ),
)
