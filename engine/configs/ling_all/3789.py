CONFIG = dict(
    num=3789, title='采购的最小花费', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='分类讨论 · 三种方案取最小',
    tags=['贪心算法', '思维题', '难度分 1580'],
    code='''
class Solution:
    def minimumCost(self, cost1: int, cost2: int, costBoth: int, need1: int, need2: int) -> int:
        res1 = cost1 * need1 + cost2 * need2  # 各买各的
        if need1 > need2:
            need1, need2 = need2, need1
            cost2 = cost1
        res2 = costBoth * need2  # 我包了
        res3 = costBoth * need1 + cost2 * (need2 - need1)  # 混合策略
        return min(res1, res2, res3)
''',
    call='Solution().minimumCost(5, 4, 7, 5, 3)',
    expect=31,
    views=[
        dict(type='text', size=34, h=70, fn=lambda S: f"需求：类型 1 要 `{S['need1']}` 个，类型 2 要 `{S['need2']}` 个" if 'need1' in S else ''),
        dict(type='text', size=34, h=70, fn=lambda S: f"单价：`cost1={S['cost1']}`　`cost2={S['cost2']}`　`costBoth={S['costBoth']}`" if 'cost1' in S else ''),
        dict(type='bars', var=lambda S: [S.get('res1', 0), S.get('res2', 0), S.get('res3', 0)], h=330, label='三种方案的花费 res1 / res2 / res3',
             color=lambda S, i, v: ('green' if v and v == min(x for x in (S.get('res1'), S.get('res2'), S.get('res3')) if x) and S['_line'] >= 9 else 'blue') if v else None),
        dict(type='text', size=34, h=80, fn=lambda S: (f"各买各的 ==`{S['res1']}`==" + (f"　我包了 ==`{S['res2']}`==" if 'res2' in S else '') + (f"　混合 ==`{S['res3']}`==" if 'res3' in S else '')) if 'res1' in S else ''),
    ],
    watch=['need1', 'need2', 'cost2', 'res1', 'res2', 'res3'],
    captions={
        'res1 =': '情况一，不用 costBoth：`{cost1} * {need1} + {cost2} * {need2}` = =={res1}==',
        'need1, need2 = need2, need1': '交换后 `need1 = {need1}`、`need2 = {need2}`：让 need1 是较小的那个，多出来的需求是 need2',
        'cost2 = cost1': '多出来的需求原来是类型 1，单买单价要跟着换：`cost2 = cost1` = =={cost2}==',
        'res2 =': '情况二，全买 costBoth：要覆盖较大的需求 `{need2}`，花 `{costBoth} * {need2}` = =={res2}==',
        'res3 =': '情况三，先成对买 `{need1}` 个，剩下 `{need2 - need1}` 个单买：`{costBoth} * {need1} + {cost2} * {need2 - need1}` = =={res3}==',
        'return min': '三种方案取最小：`min({res1}, {res2}, {res3})` = =={ret}==',
    },
    cards=dict(
        one_liner='各买各的、全买套餐、先配对再单买，三种取最小',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['三种物品：类型 1 单价 `cost1`、类型 2 单价 `cost2`、类型 3 单价 `costBoth` 同时算两种各 1 个',
                 '买够 `need1` 个类型 1 的需求和 `need2` 个类型 2 的需求，求最小花费',
                 '示例：`5, 4, 15, 2, 3` → `22`'],
        quote='代码实现时，无需判断 costBoth < cost1 + cost2。如果不满足，那么情况一（各买各的）更优。',
        quote_src='—— 灵茶山艾府题解',
        idea=['情况一：不用 costBoth；情况二：用 costBoth 买 `max(need1, need2)` 个',
              '情况三：先买 `min(need1, need2)` 个套餐，多出的需求单买',
              '不用判断谁更便宜，三种直接算出来取 `min`，不合适的方案自然会输'],
        summary=['时间、空间都是 `O(1)`，只是三个公式的比较',
                 '交换 `need1, need2` 时==必须同步把 `cost2` 换成对应的单价==，这里写作 `cost2 = cost1`',
                 '`need` 可以为 0，三种方案都会算出 0，不用特判',
                 '分类讨论题：先列出所有可能的最优形态，再取最小'],
    ),
)
