def _t(S):
    if 'sum_t' not in S:
        return '`last_finish[i]`：第 i 名巫师做完上一瓶药水的时间'
    if S['_line'] in (7, 8, 9, 10):
        return f"本瓶药水 `mana = {S['m']}`：按题意模拟，当前累计完成时间 `sum_t` = =={S['sum_t']}=="
    return f"本瓶药水 `mana = {S['m']}`，最后一名巫师完成时间 =={S['sum_t']}==，往前倒推每人的完成时间"


CONFIG = dict(
    num=3494, title='酿造药水需要的最少总时间', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='正反两次扫描',
    tags=['动态规划', '数学算法', '难度分 2042'],
    code='''
class Solution:
    def minTime(self, skill: List[int], mana: List[int]) -> int:
        n = len(skill)
        last_finish = [0] * n  # 第 i 名巫师完成上一瓶药水的时间
        for m in mana:
            # 按题意模拟
            sum_t = 0
            for x, last in zip(skill, last_finish):
                if last > sum_t: sum_t = last  # 手写 max
                sum_t += x * m
            # 倒推：如果酿造药水的过程中没有停顿，那么 last_finish[i] 应该是多少
            last_finish[-1] = sum_t
            for i in range(n - 2, -1, -1):
                last_finish[i] = last_finish[i + 1] - skill[i + 1] * m
        return last_finish[-1]
''',
    call='Solution().minTime([1,5,2,4], [5,1,4])',
    expect=102,
    views=[
        dict(type='array', var='skill', label='skill', h=170, cell=90,
             pointers={'i': 'pink'}),
        dict(type='array', var='last_finish', label='last_finish', h=170, cell=90,
             pointers={'i': 'pink'}),
        dict(type='array', var='mana', label='mana', h=170, cell=90,
             color=lambda S, i, v: 'blue' if S.get('m') == v and i == S['mana'].index(v) else None),
        dict(type='text', fn=_t, size=26, h=70),
    ],
    watch=[('m', 'm', 'blue'), ('sum_t', 'sum_t', 'yellow'), 'x', 'last', 'i'],
    skip=['n = len', 'for x, last in zip', 'for i in range(n - 2'],
    captions={
        'last_finish = [0]': '`last_finish[i]`：第 `i` 名巫师做完上一瓶药水的时间，一开始都是 0',
        'for m in mana': '依次酿造每瓶药水，法力值 `m = {m}`',
        'sum_t = 0': '先按题意模拟：药水从第 0 名巫师开始，`sum_t` 记录它被传到哪个时刻',
        'if last > sum_t': '药水到达时，巫师还在忙上一瓶吗？`last = {last}` 对比 `sum_t = {B.sum_t}`：{"巫师更晚，药水要等他，sum_t 抬到 " + str(last) if last > B.sum_t else "药水不用等"}',
        'sum_t += x * m': '巫师处理 `{x} × {m} = {x*m}` 个时间，药水离开他的时刻 `sum_t` = =={sum_t}==',
        'last_finish[-1] = sum_t': '最后一名巫师的完成时间就是模拟的结果 =={sum_t}==：它不会被前面拖慢',
        'last_finish[i] = last_finish[i + 1]': '药水不能停顿 → 倒推：`last_finish[{i}] = {last_finish[i+1]} − {skill[i+1]}×{m}` = =={last_finish[i]}=='
                                           '（每人紧贴着后一人开工，中间不停顿）',
        'return last_finish[-1]': '最后一瓶药水被最后一名巫师做完的时间 = =={ret}==',
    },
    cards=dict(
        one_liner='先模拟出最晚的完成时间，再倒推出「不停顿」的真实时间',
        complexity='时间 `O(nm)`，空间 `O(n)`',
        problem=['`n` 个巫师依次处理 `m` 瓶药水，巫师 `i` 处理药水 `j` 要 `skill[i] * mana[j]`',
                 '药水做完一步必须立刻交给下一个巫师（药水不能等人，人可以等药水）',
                 '示例：`skill=[1,5,2,4]`，`mana=[5,1,4,2]` → `110`；本视频取前 3 瓶 → `102`'],
        quote='题目要求「药水在当前巫师完成工作后必须立即传递给下一个巫师并开始处理」，也就是说，酿造药水的过程中是==不能有停顿==的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`last_finish[i]`：巫师 `i` 做完上一瓶的时间；新药水到他手里时，开工时间不能早于它',
              '按「取 max 再加耗时」模拟，得到最后一名巫师的完成时间',
              '从这个时间倒推，每人的完成时间 = 后一人完成时间 − 后一人的耗时'],
        summary=['时间 `O(nm)`，空间 `O(n)`',
                 '易错：倒推时用的是 `skill[i + 1] * m`，是后一名巫师的耗时',
                 '模拟那一遍只为拿到最后一名巫师的完成时间，不能直接把它当作每个人的完成时间',
                 '灵神还给了方法二：前缀和 + `max` 直接递推开始时间；方法三/四用 record、凸包优化到 `O(n+m log n)`，本视频演示方法一'],
    ),
)
