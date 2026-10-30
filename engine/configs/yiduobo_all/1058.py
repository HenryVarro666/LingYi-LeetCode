def _r(v):
    return [round(c, 3) for c in v]


CONFIG = dict(
    num=1058, title='最小化舍入误差以满足目标', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='先全部向下取整 · 挑代价最小的 k 个改向上',
    tags=['贪心与思维'],
    code='''
class Solution(object):
    def minimizeError(self, prices, target):
        res = 0
        cost = []
        for p in prices:
            p = float(p)
            if math.floor(p) != math.ceil(p):
                res += p - math.floor(p)
                cost.append(math.ceil(p) - p - (p - math.floor(p)))
            
            target -= int(math.floor(p))
        
        if target < 0:
            return "-1"
        
        if target > len(cost):
            return "-1"

        cost.sort()
        res += sum(cost[:target])
        return "%.3f" % res
''',
    setup='import math',
    call='Solution().minimizeError(["0.700", "2.800", "4.900", "3.000"], 11)',
    expect='1.000',
    views=[
        dict(type='array', var='prices', label='prices（字符串）', cell=130, h=200),
        dict(type='array', var=lambda S: _r(S['cost']) if 'cost' in S else [], label='cost：floor 改 ceil 的误差变化（越小越划算）', cell=110, h=190,
             color=lambda S, i, v: 'green' if S.get('_line', 0) >= 17 and i < max(S.get('target', 0), 0) else None),
        dict(type='text', fn=lambda S: (f'向下取整的误差累计 `res = {round(S.get("res", 0), 3)}`，`target = {S.get("target")}`（逐个扣掉各数的 floor，剩下的就是要改向上取整的个数）'), size=26, h=60),
    ],
    watch=[('res', 'round(res, 3)', 'green'), ('target', 'target', 'orange'), ('cost', '[round(c, 3) for c in cost]', 'blue')],
    captions={
        'res = 0': '`res` 累计误差（先假设每个数都向下取整）',
        'cost = []': '`cost` 记录：把 floor 改成 ceil，总误差变化多少',
        'for p in prices': lambda S, B, r: ('价格遍历完了，进入后面的检查' if B.get('p') == S.get('p') and 'p' in B else f'取出价格 `p = {S.p}`'),
        'p = float(p)': '转成浮点数 `p = {p}`',
        'if math.floor(p) != math.ceil(p)': lambda S, B, r: (f'`p = {S.p}` 有小数部分，floor ≠ ceil → 还有操作空间' if math.floor(S.p) != math.ceil(S.p)
                                                              else f'`p = {S.p}` 是整数，floor = ceil，无论怎么取都不产生误差'),
        'res += p - math.floor(p)': '向下取整的误差：`p − floor(p)` → `res = {round(res, 3)}`',
        'cost.append': '改成向上取整的误差 `ceil(p) − p`，减去原来的 `p − floor(p)`，变化量 `{round(cost[-1], 3)}`',
        'target -= int(math.floor(p))': '`target` 先减去 `floor(p) = {int(p)}` → `{target}`：剩下的数里还需要几个改向上取整',
        'if target < 0': lambda S, B, r: (f'`target = {S.target} < 0`：全部向下取整都已经超过目标 → 无解' if S.target < 0
                                          else f'`target = {S.target} ≥ 0`：最小和不超过目标'),
        'if target > len(cost)': lambda S, B, r: (f'`target = {S.target} > len(cost) = {len(S.cost)}`：全部向上取整也凑不够 → 无解' if S.target > len(S.cost)
                                                  else f'`target = {S.target} ≤ len(cost) = {len(S.cost)}`：mi ≤ target ≤ mi + n 成立，可行'),
        'cost.sort()': '`cost` 从小到大排序 → `{[round(c, 3) for c in cost]}`，前面的改了最划算',
        'res += sum(cost[:target])': '取最小的 `{target}` 个 cost 加到 `res` 上 → `res = {round(res, 3)}`',
        'return "%.3f" % res': '保留三位小数，返回 `"{ret}"`',
    },
    cards=dict(
        one_liner='先全部向下取整，再选代价最小的 k 个改向上',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`prices` 是若干小数字符串，每个数可以向下或向上取整，取整后的和必须等于 `target`',
                 '误差 = 所有 `|取整后 − 原值|` 之和，求最小误差，保留三位小数',
                 '无法凑出 `target` 则返回 `"-1"`；示例：`["0.700","2.800","4.900"]`，`8` → `"1.000"`'],
        quote='若满足这个条件，则说明可以将mi中的若干项从floor变为ceil，而需要变换的项数就是k = target - mi。',
        quote_src='—— yiduobo 题解原文',
        idea=['整数没有操作空间：直接从 `target` 里减掉；其余数 `floor(p) = ceil(p) − 1`',
              '最小和 `mi = Σfloor`，最大和 `mi + n`，需要 `mi ≤ target ≤ mi + n`，否则 `-1`',
              '要改 `k = target − mi` 个为 ceil：把 `cost` 排序，取最小的 `k` 个累加'],
        result='`3.000` 是整数先剔除；三个小数改 2 个，误差 `2.4 − 1.4 = 1.000`',
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：整数 floor = ceil，不能算进 `cost`，也不会使 `target` 多算',
                 '易错：`target` 减完所有 floor 后，要同时判断 `< 0` 和 `> len(cost)` 两种无解',
                 '代码原样照搬（Python 3 可运行），`import math` 放在 setup 中补上',
                 '返回的是字符串 `"%.3f"`，不是浮点数'],
    ),
)
