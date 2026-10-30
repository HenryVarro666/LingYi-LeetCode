CONFIG = dict(
    num=3207, title='与敌人战斗后的最大分数', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='最小值 · 先吸收再反复战斗',
    tags=['灵神题单', '难度分 1591'],
    code='''
class Solution:
    def maximumPoints(self, enemyEnergies: List[int], currentEnergy: int) -> int:
        mn = min(enemyEnergies)
        if currentEnergy < mn:
            return 0
        return (currentEnergy + sum(enemyEnergies) - mn) // mn
''',
    call='Solution().maximumPoints([3,2,2], 2)',
    expect=3,
    views=[
        dict(type='array', var='enemyEnergies', label='enemyEnergies（蓝 = 最小的敌人）', cell=110,
             color=lambda S, i, v: 'blue' if 'mn' in S and v == S['mn'] and i == S['enemyEnergies'].index(v) else None),
        dict(type='text', size=28, fn=lambda S: (f"能量 `currentEnergy = {S['currentEnergy']}`，最小敌人 `mn = {S['mn']}`" if 'mn' in S else f"能量 `currentEnergy = {S['currentEnergy']}`")),
        dict(type='text', size=28, fn=lambda S: (f"吸收其余敌人后能量 = `{S['currentEnergy']} + {sum(S['enemyEnergies'])} - {S['mn']}` = =={S['currentEnergy'] + sum(S['enemyEnergies']) - S['mn']}==" if 'mn' in S else '')),
    ],
    watch=[('currentEnergy', 'currentEnergy', 'blue'), ('mn', 'mn', 'pink')],
    captions={
        'mn = min': '最小的敌人 `mn = {mn}`：反复和它战斗最划算',
        'if currentEnergy < mn': lambda S, B, r: (f'`currentEnergy = {S.currentEnergy} < mn = {S.mn}`：连最弱的都打不过 → 没有分，也没法吸收' if S.currentEnergy < S.mn
                                                  else f'`currentEnergy = {S.currentEnergy} ≥ mn = {S.mn}`：能先打 mn 一次，拿到 1 分，之后可以吸收'),
        'return (': '先吸收除 mn 外所有敌人：`{currentEnergy} + {sum(enemyEnergies)} - {mn}` = {currentEnergy + sum(enemyEnergies) - mn}，再反复打 mn：`// {mn}` = ==3== 分',
    },
    cards=dict(
        one_liner='先把别的敌人都吸收掉，再不停打最弱的那个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['操作一：能量 ≥ 敌人能量，得 1 分并扣能量；操作二：有分后可吸收未标记敌人的能量',
                 '求最多得多少分',
                 '本视频：`[3,2,2]`，`currentEnergy=2` → `3`'],
        quote='也可以理解为，先得到 s - mn 的能量，再不断对 mn 执行操作一，所以得分为 floor((currentEnergy + s - mn) / mn)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`currentEnergy < mn`：操作一做不了，没有分，操作二也做不了，返回 0',
              '否则顺序：先打 `mn` 得 1 分，再吸收其余所有敌人，最后反复打 `mn`',
              '等价于先得到 `s - mn` 的能量，再整除 `mn`'],
        after=[dict(heading='为什么先吸收再战斗', lines=['吸收不花能量，战斗才花；先吸收只会让能量更多', '`mn` 最便宜，每分花费最少 → 把所有能量都换成打 `mn`', '本例：能量 `2 + 7 - 2 = 7`，`7 // 2 = 3` 分'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：别忘了先判断 `currentEnergy < mn` 返回 0',
                 '`mn` 自己不能被吸收（要留着反复打），所以减去 `mn`'],
    ),
)
