CONFIG = dict(
    num=3789, title='采购的最小花费', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='先判套餐划不划算，再成对买',
    tags=['贪心算法', '思维题', '难度分 1580'],
    code='''
class Solution(object):
    def minimumCost(self, cost1, cost2, costBoth, need1, need2):
        
        if costBoth > cost1 + cost2:
            return cost1 * need1 + cost2 * need2
        
        res = costBoth * min(need1, need2)
        if need1 < need2:
            c = cost2
        else:
            c = cost1
        
        if costBoth < c:
            res += costBoth * abs(need1 - need2)
        else:
            res += c * abs(need1 - need2)
        
        return res
''',
    call='Solution().minimumCost(5, 4, 7, 5, 3)',
    expect=31,
    views=[
        dict(type='text', size=34, h=70, fn=lambda S: f"需求：类型 1 要 `{S['need1']}` 个，类型 2 要 `{S['need2']}` 个" if 'need1' in S else ''),
        dict(type='text', size=34, h=70, fn=lambda S: f"单价：`cost1={S['cost1']}`　`cost2={S['cost2']}`　`costBoth={S['costBoth']}`" if 'cost1' in S else ''),
        dict(type='text', size=34, h=80, fn=lambda S: f"套餐 `{S['costBoth']}` vs 两件单买 `{S['cost1'] + S['cost2']}`" if 'cost1' in S else ''),
        dict(type='bars', var=lambda S: [S['need1'], S['need2']] if 'need1' in S else [], h=300, label='两种需求的数量（短的一截用套餐配对）',
             color=lambda S, i, v: 'green' if v == min(S['need1'], S['need2']) else 'orange'),
        dict(type='text', size=34, h=80, fn=lambda S: f"已花 ==`{S['res']}`==" + (f"，剩余单价 `c = {S['c']}`" if 'c' in S else '') if 'res' in S else ''),
    ],
    watch=['need1', 'need2', 'c', ('res', 'res', 'green')],
    captions={
        'if costBoth > cost1': '套餐 `{costBoth}` 比两件单买之和 `{cost1 + cost2}` 还贵吗？不贵，继续往下走',
        'return cost1 * need1': '套餐不划算，直接分开买：`{cost1} * {need1} + {cost2} * {need2}` = =={ret}==',
        'res = costBoth': '套餐不贵，先成对买 `min({need1}, {need2})` = {min(need1, need2)} 个套餐：`res` = =={res}==',
        'if need1 < need2': '看哪一种需求有剩余：`need1 < need2` 吗（{need1} < {need2}）',
        'c = cost2': '类型 2 需求更多，剩余部分单买的单价 `c = cost2` = =={c}==',
        'c = cost1': '类型 1 需求更多（或相等），剩余部分单买的单价 `c = cost1` = =={c}==',
        'if costBoth < c': '剩余部分：套餐 `{costBoth}` 比单买 `{c}` 便宜吗？',
        'res += costBoth': '套餐更便宜，剩余 `{abs(need1 - need2)}` 个继续买套餐：`res` = =={res}==',
        'res += c': '单买更便宜，剩余 `{abs(need1 - need2)}` 个单买：`res` = =={res}==',
        'return res': '两步花费相加，答案 =={ret}==',
    },
    cards=dict(
        one_liner='套餐不划算就分开买，划算就先成对买，余下的再比价',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['类型 1 单价 `cost1`，类型 2 单价 `cost2`，类型 3 单价 `costBoth` 同时满足两种需求各 1 个',
                 '要使类型 1 的需求至少 `need1`、类型 2 的至少 `need2`，求最小花费',
                 '示例：`5, 4, 15, 2, 3` → `22`'],
        quote='若costBoth比cost1和cost2之和更大，那么就分开买显然是更划算的……若costBoth比cost1和cost2之和更小，那么尽量成对的买是更划算的。',
        quote_src='—— yiduobo 题解',
        idea=['第一步：套餐比两件之和还贵，直接 `cost1 * need1 + cost2 * need2`',
              '第二步：否则先买 `min(need1, need2)` 个套餐',
              '第三步：剩下 `abs(need1 - need2)` 个需求，在单价 `c` 和套餐间取便宜的',
              '两步的花费相加就是答案'],
        summary=['时间、空间都是 `O(1)`',
                 '剩余部分的单价 `c` 由==哪边需求多==决定，别弄反',
                 '`need1 == need2` 时剩余为 0，走哪个分支都不影响',
                 '原文为 Python 2 写法，本题无需改动，直接可在 Python 3 运行'],
    ),
)
