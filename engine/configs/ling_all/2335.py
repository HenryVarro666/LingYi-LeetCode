AMT = [5, 4, 4]

CONFIG = dict(
    num=2335, title='装满杯子需要的最短总时长', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='数学结论 · max(ceil(s/2), m)',
    tags=['灵神题单', '难度分 1360'],
    code='''
class Solution:
    def fillCups(self, amount: List[int]) -> int:
        s = sum(amount)
        m = max(amount)
        return max((s + 1) // 2, m)
''',
    call=f'Solution().fillCups({AMT})',
    expect=7,
    views=[
        dict(type='bars', var='amount', label='amount（冷 / 温 / 热 需要的杯数）', h=380,
             color=lambda S, i, v: 'orange' if 'm' in S and v == S['m'] else None),
        dict(type='text', size=30, h=90,
             fn=lambda S: (f"下界一：每秒最多 2 杯 → `ceil({S['s']}/2)` = =={(S['s'] + 1) // 2}==" if 's' in S else '')
             + (f"；下界二：最多的那种 `m = {S['m']}` 每秒只能出一杯" if 'm' in S else '')),
    ],
    watch=[('s', 's', 'cyan'), ('m', 'm', 'orange')],
    captions={
        's = sum': '`s` = 所有杯子总数 = =={s}==',
        'm = max': '`m` = 最多的那种杯子数 = =={m}==：这种杯子每秒最多装 1 杯',
        'return': '至少 `ceil(s/2)` = `{(s + 1) // 2}` 秒（每秒最多 2 杯），也至少 `m` = `{m}` 秒 → 取大者 =={ret}==',
    },
    cards=dict(
        one_liner='两个下界取大：总数的一半、最多那种的数量',
        complexity='时间 `O(1)`（长度固定为 3），空间 `O(1)`',
        problem=['每秒可装 2 杯==不同==类型的水，或 1 杯任意类型',
                 '`amount` 给出冷、温、热水各需几杯，求最少秒数',
                 '示例：`[5,4,4]` → `7`'],
        quote='设 s 是 amount 的元素和，m = max(amount)。定理：最少要用 max(⌈s/2⌉, m) 秒。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每秒至多 2 杯 → 至少 `ceil(s/2)` 秒',
              '同一种水每秒至多 1 杯 → 至少 `m` 秒',
              '定理：这两个下界的最大值总能取到（原文附证明与构造方案）'],
        before=[dict(heading='先看三个例子', lines=['`[1,4,2]` → `4`：温水 4 杯太多，每秒最多配走一杯，要 `m = 4` 秒',
                                              '`[5,4,4]` → `7`：总数 13，两两配对要 `ceil(13/2) = 7` 秒',
                                              '`[5,0,0]` → `5`：只有一种水，每秒只能装 1 杯'])],
        after=[dict(heading='为什么取大者就够', lines=['配对时总是==挑剩余最多的两种==各装一杯',
                                                 '这样最大值不会一直领先，直到全部配完或只剩一种',
                                                 '细节与构造方案见原文给出的证明链接'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '`(s + 1) // 2` 是向上取整',
                 '`m` 特别大时，其他杯子都配它也配不完，答案就是 `m`',
                 '同类题：§1.8 相邻不同'],
    ),
)
