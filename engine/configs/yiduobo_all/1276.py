CONFIG = dict(
    num=1276, title='不浪费原料的汉堡制作方案', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='鸡兔同笼 · 解方程',
    code='''
class Solution(object):
    def numOfBurgers(self, tomatoSlices, cheeseSlices):

        diff = tomatoSlices - 2 * cheeseSlices
        if diff < 0 or diff % 2 == 1 or cheeseSlices < diff // 2:
            return []
        
        return [diff // 2, cheeseSlices - diff // 2]
''',
    call='[Solution().numOfBurgers(t, c) for t, c in [(16, 7), (17, 4), (4, 17), (0, 0), (2, 1)]]',
    expect=[[1, 6], [], [], [0, 0], [0, 1]],
    views=[
        dict(type='text', h=120, size=34,
             fn=lambda S: (f"全做小皇堡要 `2×{S['cheeseSlices']} = {2 * S['cheeseSlices']}` 片番茄，实际 `{S['tomatoSlices']}` 片 → `diff` = =={S['diff']}==" if 'diff' in S else f"番茄 `{S['tomatoSlices']}` 片，奶酪 `{S['cheeseSlices']}` 片")),
        dict(type='text', h=120, size=34,
             fn=lambda S: (f"巨无霸 ==`{S['diff'] // 2}`== 个，小皇堡 ==`{S['cheeseSlices'] - S['diff'] // 2}`== 个" if 'diff' in S and S['diff'] >= 0 and S['diff'] % 2 == 0 and S['cheeseSlices'] >= S['diff'] // 2 else '')),
    ],
    watch=[('tomatoSlices', 'tomatoSlices'), ('cheeseSlices', 'cheeseSlices'), ('diff', 'diff', 'blue')],
    captions={
        'diff = ': '全做小皇堡会用 `2 × {cheeseSlices}` 片番茄；实际 `{tomatoSlices}`，多出 `diff = {diff}`',
        'if diff < 0': lambda S, B, r: (
            f"`diff = {S.diff}` < 0：番茄不够每个汉堡 2 片 → 无解" if S.diff < 0
            else f"`diff = {S.diff}` 是奇数：换一个巨无霸多 2 片，凑不出 → 无解" if S.diff % 2 == 1
            else f"`cheeseSlices = {S.cheeseSlices}` < `diff // 2 = {S.diff // 2}`：巨无霸比汉堡总数还多 → 无解" if S.cheeseSlices < S.diff // 2
            else f"`diff = {S.diff}` 非负偶数，且 `diff // 2 = {S.diff // 2}` ≤ 奶酪 `{S.cheeseSlices}` → 有解"),
        'return []': '无解，返回 `[]`',
        'return [diff': '每个巨无霸比小皇堡多 2 片番茄 → 巨无霸 `{diff // 2}` 个，小皇堡 `{cheeseSlices - diff // 2}` 个：`{ret}`',
    },
    cards=dict(
        one_liner='鸡兔同笼：先全按小皇堡算，多出的番茄换成巨无霸',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['巨无霸：4 片番茄 + 1 片奶酪；小皇堡：2 片番茄 + 1 片奶酪',
                 '给定番茄、奶酪片数，求两种汉堡各做几个才能恰好用完，无解返回 `[]`',
                 '示例：番茄 16、奶酪 7 → `[1, 6]`'],
        quote='假设我们都做小皇堡，那么将用掉的番茄片数量就是cheeseSlices * 2。一个巨无霸和一个小皇堡需要的番茄片之差为2，那么计算出cheeseSlices * 2与实际拥有番茄片tomatoSlices的差值diff……',
        quote_src='—— yiduobo 题解原文',
        idea=['每个汉堡一片奶酪 → 汉堡总数 = `cheeseSlices`',
              '全做小皇堡的番茄数与实际之差 `diff`，每换一个巨无霸多用 2 片',
              '所以巨无霸 = `diff // 2`，其余是小皇堡；条件不满足就无解'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '三种无解：`diff < 0`、`diff` 是奇数、巨无霸数超过汉堡总数',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '视频用 5 组输入连跑，覆盖有解和各类无解'],
    ),
)
