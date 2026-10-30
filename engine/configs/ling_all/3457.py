def _pick(S):
    """(odd, even) once computed, else None"""
    if 'odd' not in S or 'days' not in S:
        return None
    return S['odd'], S['days'] // 2


def _color(S, i, v):
    r = _pick(S)
    if not r:
        return None
    odd, even = r
    if i < odd:
        return 'green'
    if i >= odd + 1 and i < odd + even * 2 and (i - odd) % 2 == 1:
        return 'blue'
    return None


def _dim(S, i, v):
    return _pick(S) is not None and _color(S, i, v) is None


CONFIG = dict(
    num=3457, title='吃披萨', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='降序排序 + 奇数天取最大、偶数天跳着取',
    tags=['灵神题单', '难度分 1704'],
    code='''
class Solution:
    def maxWeight(self, pizzas: List[int]) -> int:
        pizzas.sort(reverse=True)
        days = len(pizzas) // 4
        odd = (days + 1) // 2
        return sum(pizzas[:odd]) + sum(pizzas[odd + 1: odd + days // 2 * 2: 2])
''',
    call='Solution().maxWeight([4,1,8,3,6,2,7,5,9,1,3,2])',
    expect=23,
    views=[
        dict(type='array', var='pizzas', h=230, cell=68, label='pizzas', color=_color, dim=_dim),
        dict(type='text', h=130, fn=lambda S: ('共 `days = %d` 天：奇数天 ==%d== 天（绿色，取当天最大），偶数天 ==%d== 天（蓝色，取次大）' % (S['days'], S['odd'], S['days'] // 2)) if 'odd' in S else ''),
        dict(type='text', h=130, fn=lambda S: ('绿色之和 `%d` + 蓝色之和 `%d`' % (sum(S['pizzas'][:S['odd']]), sum(S['pizzas'][S['odd'] + 1: S['odd'] + S['days'] // 2 * 2: 2]))) if 'odd' in S else ''),
    ],
    watch=['days', 'odd'],
    captions={
        'pizzas.sort': '从大到小排序：这样越靠前的披萨越重，下标就是「第几大」：`{pizzas}`',
        'days =': '每天吃 4 个，共 `days = n / 4 = {days}` 天',
        'odd =': '奇数天有 `odd = ceil(days / 2) = {odd}` 天，偶数天 `{days // 2}` 天',
        'return sum': lambda S, B, r: (f'奇数天吃最大的，所以绿色取前 `{S.odd}` 个 `{S.pizzas[:S.odd]}` = {sum(S.pizzas[:S.odd])}；'
                                      f'偶数天只能拿次大，每次把一个最大的「浪费」掉，从剩下里跳着选 `{S.pizzas[S.odd + 1: S.odd + S.days // 2 * 2: 2]}` = {sum(S.pizzas[S.odd + 1: S.odd + S.days // 2 * 2: 2])}，'
                                      f'合计 =={r}=='),
    },
    max_steps=30,
    cards=dict(
        one_liner='奇数天拿最大，偶数天只拿次大，所以要「跳着选」',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['每天恰好吃 4 个披萨，重量从小到大 `W<=X<=Y<=Z`',
                 '奇数天增重 `Z`（最大），偶数天增重 `Y`（次大）',
                 '本视频：`[4,1,8,3,6,2,7,5,9,1,3,2]` → `23`'],
        quote='根据题意，奇数天选最大的，偶数天只能选次大的。……由于不选的披萨越靠后，元素和就越大，所以可以先考虑奇数天怎么选，再考虑偶数天怎么选。',
        quote_src='—— 灵茶山艾府题解',
        idea=['降序排序后，先让奇数天拿走最大的 `odd` 个',
              '偶数天每天要「浪费」一个最大的，才能拿到次大：选选选 _ 选 _ 选，跳过的位置不选',
              '用交换论证法可证：别的奇偶顺序，下标都会往后移，和不会更大'],
        after=[dict(heading='用示例走一遍', lines=['降序：`9 8 7 6 5 4 3 3 2 2 1 1`，共 3 天：奇数天 2 天、偶数天 1 天', '奇数天拿最大的两个：`9`、`8`', '偶数天：跳过 `7`（被浪费），拿次大 `6`', '合计 `9 + 8 + 6` = ==23==']),],
        summary=['时间 `O(n log n)`；空间 `O(1)`（忽略切片和排序）',
                 '`odd = (days + 1) // 2`，偶数天 `days // 2` 天',
                 '切片 `pizzas[odd+1 : odd+days//2*2 : 2]` 的起点是 `odd+1`，不是 `odd`',
                 '先做简单版本 1561. 你可以获得的最大硬币数目；思考题：把最大改成最小'],
    ),
)
