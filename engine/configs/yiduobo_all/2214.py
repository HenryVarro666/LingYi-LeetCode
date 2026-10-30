CONFIG = dict(
    num=2214, title='通关游戏所需的最低生命值', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='护盾挡最大伤害',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def minimumHealth(self, damage, armor):

        return sum(damage) - min(max(damage), armor) + 1
''',
    call='Solution().minimumHealth([2,7,4,3], 4)',
    expect=13,
    views=[
        dict(type='bars', var='damage', label='每一关的伤害 damage（绿 = 被护盾挡掉的最大一关）', h=400,
             color=lambda S, i, v: 'green' if v == max(S['damage']) and i == S['damage'].index(v) else None),
        dict(type='text', fn=lambda S: f"总伤害 `{sum(S['damage'])}`，护盾 `armor = {S['armor']}`，最大一关 `{max(S['damage'])}` → 最多挡 `min({max(S['damage'])}, {S['armor']}) = {min(max(S['damage']), S['armor'])}`", size=28, h=110),
        dict(type='text', fn=lambda S: f"实际受伤 `{sum(S['damage'])} − {min(max(S['damage']), S['armor'])}` = {sum(S['damage']) - min(max(S['damage']), S['armor'])}，再 +1 才能活着通关", size=28, h=90),
    ],
    watch=[('armor', 'armor', 'cyan'), ('总伤害', 'sum(damage)', 'pink'), ('最大一关', 'max(damage)', 'orange')],
    captions={
        'return sum(damage)': '`sum(damage) − min(max(damage), armor) + 1` = `{sum(damage)} − min({max(damage)}, {armor}) + 1` = =={ret}==：护盾==只用一次==，挡最大的那关，生命值至少 {ret}',
    },
    cards=dict(
        one_liner='护盾只能用一次，当然挡最大的那一关伤害',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['依次通过 `n` 关，第 `i` 关受到 `damage[i]` 伤害，生命值不能降到 0 及以下',
                 '护盾 `armor` 最多用一次，可抵消最多 `armor` 点某一关的伤害',
                 '示例：`damage=[2,7,4,3], armor=4` → `13`'],
        quote='如果使用护盾去格挡较低的伤害，可能会浪费掉部分护盾，因此在这里就应该使用护盾去格挡最高的那次伤害。',
        quote_src='—— yiduobo 题解原文',
        idea=['挡低伤害关，护盾可能用不完 → ==挡最高的那一关==',
              '被挡掉的伤害 = `min(max(damage), armor)`',
              '受伤 = 总伤害 − 被挡掉的；生命值至少还要剩 1，所以 +1'],
        after=[dict(heading='为什么不挡小的', lines=['`[2,7,4,3]`，`armor=4`：挡 `2` 只省 `2`，挡 `7` 省 `4`',
                                                    '护盾挡得越多越好：每关最多挡 `armor`，所以挡最大的那关最划算',
                                                    '总伤害 `16` − `4` = `12`，生命值至少 `13`'])],
        summary=['时间 `O(n)`，空间 `O(1)`，一行公式',
                 '最后别漏掉 `+ 1`：生命值必须大于 0',
                 '护盾不足以挡完最大伤害时，挡掉的就是 `armor`（所以取 min）',
                 '原文变量名写作 arror，代码里是 armor；本题只有一行代码，动画只有一步',
                 '题面库里没有，题意按 LeetCode 2214 与原文整理'],
    ),
)
