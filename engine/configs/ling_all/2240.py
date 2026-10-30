def _cnts(S):
    return [(S['total'] - S['cost1'] * i) // S['cost2'] + 1 for i in range(S['total'] // S['cost1'] + 1)]


def _text(S):
    t, c1, c2 = S['total'], S['cost1'], S['cost2']
    cs = _cnts(S)
    if 'n' not in S:
        return f'`total={t}`，钢笔 `{c1}` 元，铅笔 `{c2}` 元：先枚举买几支钢笔'
    parts = ' + '.join(str(x) for x in cs)
    return f'每个 i 的方案数 `1 + (total − i×cost1) // cost2`：`{parts}` = =={sum(cs)}=='


CONFIG = dict(
    num=2240, title='买钢笔和铅笔的方案数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='枚举钢笔数 + 整除',
    tags=['灵神题单'],
    code='''
class Solution:
    def waysToBuyPensPencils(self, total: int, cost1: int, cost2: int) -> int:
        n = 1 + total // cost1
        return n + sum((total - cost1 * i) // cost2 for i in range(n))
''',
    call='Solution().waysToBuyPensPencils(20, 10, 5)',
    expect=9,
    views=[
        dict(type='text', fn=_text, h=110),
        dict(type='array', var=_cnts, label='买 i 支钢笔时的铅笔方案数（下标 i = 钢笔数）', h=260),
    ],
    watch=['total', 'cost1', 'cost2', ('n', 'n', 'blue')],
    captions={
        'n = 1 +': '钢笔至多买 `total // cost1 = {total // cost1}` 支，加上 0 支共 ==`n = {n}`== 种取法',
        'return n +': '每个 i：剩 `total − i×cost1` 元，铅笔可买 `0..k` 共 `k+1` 种，所以==先把 n 个“+1”提出来==，再加所有 `k`，结果 =={ret}==',
    },
    cards=dict(
        one_liner='枚举买了几支钢笔，剩下的钱能买几支铅笔就是几种方案',
        complexity='时间 `O(total / cost1)`，空间 `O(1)`',
        problem=['`total` 元，钢笔 `cost1` 元，铅笔 `cost2` 元，花部分或全部的钱买任意数目',
                 '求买钢笔和铅笔的不同方案数',
                 '示例：`total=20, cost1=10, cost2=5` → `9`（5 + 3 + 1）'],
        quote='枚举买了 i 支钢笔。至多能买 ⌊total/cost1⌋ 支钢笔。剩余钱数为 total - i * cost1，至少可以买 0 支铅笔，至多可以买 ⌊(total - i * cost1)/cost2⌋ 支铅笔。',
        quote_src='—— 灵茶山艾府题解',
        idea=['钢笔数 `i` 从 0 到 `total // cost1`，共 `n = 1 + total // cost1` 种',
              '固定 `i` 后，铅笔 0 到 `k` 支都行，有 `1 + k` 种',
              '把每项的 `+1` 合并成 `n`，代码只剩一个 `sum`'],
        before=[dict(heading='示例拆开看', lines=['`i = 0`：剩 20 元，铅笔 0 到 4 支，`1 + 4 = 5` 种',
                                                  '`i = 1`：剩 10 元，铅笔 0 到 2 支，`1 + 2 = 3` 种',
                                                  '`i = 2`：剩 0 元，铅笔只能 0 支，`1 + 0 = 1` 种',
                                                  '合计 `5 + 3 + 1 = 9`；代码里一行 `sum` 就把这三项加完'])],
        summary=['时间 `O(total / cost1)`，空间 `O(1)`',
                 '别忘了买 0 支钢笔、0 支铅笔也算一种方案（`+1`）',
                 '灵神还提到和式可用类欧几里得算法做到 `O(log)`，这里不展开',
                 '把较贵的笔放在外层枚举，循环次数更少'],
    ),
)
