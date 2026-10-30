CONFIG = dict(
    num=3207, title='与敌人战斗后的最大分数', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='挑软柿子捏 · 反复战最弱',
    tags=['灵神题单', '贪心与思维', '难度分 1591'],
    code='''
class Solution(object):
    def maximumPoints(self, enemyEnergies, currentEnergy):

        mi = min(enemyEnergies)
        if currentEnergy < mi:
            return 0
        
        return (currentEnergy + sum(enemyEnergies) - mi) // mi
''',
    call='Solution().maximumPoints([4,2,3,5], 3)',
    expect=7,
    views=[
        dict(type='array', var='enemyEnergies', label='enemyEnergies（蓝 = 最弱的敌人，其余被吸收）', cell=110,
             color=lambda S, i, v: ('blue' if v == S['mi'] else 'green') if 'mi' in S and i != -1 else None),
        dict(type='text', size=28, fn=lambda S: (f"能量 `currentEnergy = {S['currentEnergy']}`，最弱 `mi = {S['mi']}`" if 'mi' in S else f"能量 `currentEnergy = {S['currentEnergy']}`")),
        dict(type='text', size=28, fn=lambda S: (f"战斗次数 = `({S['currentEnergy']} + {sum(S['enemyEnergies'])} - {S['mi']}) // {S['mi']}` = =={(S['currentEnergy'] + sum(S['enemyEnergies']) - S['mi']) // S['mi']}==" if 'mi' in S else '')),
    ],
    watch=[('currentEnergy', 'currentEnergy', 'blue'), ('mi', 'mi', 'pink')],
    captions={
        'mi = min': '战斗次数越多分越高 → 挑软柿子捏：最弱的 `mi = {mi}`',
        'if currentEnergy < mi': lambda S, B, r: (f'`currentEnergy = {S.currentEnergy} < mi = {S.mi}`：找不到对手，分数为 0，无法吸取 → 答案 0' if S.currentEnergy < S.mi
                                                  else f'`currentEnergy = {S.currentEnergy} ≥ mi = {S.mi}`：能和最弱的交战，继续'),
        'return (': '吸取除 mi 外所有敌人：`{currentEnergy} + {sum(enemyEnergies)} - {mi}` = {currentEnergy + sum(enemyEnergies) - mi}，整除 `{mi}` → ==7== 次战斗',
    },
    cards=dict(
        one_liner='挑软柿子捏：只和最弱的打，其他敌人全吸收',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['战斗：能量够就得 1 分、扣敌人能量；吸取：有分后标记敌人、加其能量',
                 '战斗可对同一个敌人重复进行，求最大得分',
                 '本视频：`[4,2,3,5]`，`currentEnergy=3` → `7`'],
        quote='在这里就应该挑软柿子捏，选择与战斗力最低的敌人不断作战，同时将其他敌人的能量值都加以吸收。',
        quote_src='—— yiduobo 题解原文',
        idea=['分数 = 战斗次数，要次数最多，每次就消耗最少 → 总是打最弱的 `mi`',
              '`currentEnergy < mi` 时分数为 0，也就吸取不了，答案 0',
              '否则先吸取 `s - mi`，再 `currentEnergy // mi` 就是战斗次数'],
        after=[dict(heading='为什么挑最弱的打', lines=['每次战斗得 1 分，花费 `mi` 能量越少越划算', '其他敌人只用来吸取能量，不用打', '本例：`3 + 14 - 2 = 15`，`15 // 2 = 7` 次'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`mi` 本身不能吸取，要留着不断战斗',
                 '原文为 Python 2 风格，代码未改',
                 '对比灵神：灵神讲“先打一次 mn 再吸收”的操作顺序，yiduobo 强调“挑软柿子”的贪心直觉'],
    ),
)
