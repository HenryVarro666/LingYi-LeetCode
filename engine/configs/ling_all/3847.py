CONFIG = dict(
    num=3847, title='计算比赛分数差', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='模拟 · 异或切换主动玩家',
    tags=[],
    code='''
class Solution:
    def scoreDifference(self, nums: List[int]) -> int:
        score = [0] * 2
        active = 0  # 主动玩家一开始是第一位玩家
        for i, x in enumerate(nums):
            active ^= x % 2  # 如果 x 是奇数，主动玩家换人
            if i % 6 == 5:
                active ^= 1  # 主动玩家换人
            score[active] += x
        return score[0] - score[1]
''',
    call='Solution().scoreDifference([2,4,2,1,2,1,3,4])',
    expect=11,
    views=[
        dict(type='array', var='nums', label='nums（第 i 场的得分）', pointers={'i': 'blue'}, cell=90, h=190),
        dict(type='array', var='score', label='score[0] = 第一位，score[1] = 第二位', pointers={'active': 'pink'}, cell=150, h=210),
        dict(type='text', h=90, size=30, fn=lambda S: ('当前主动玩家：==第一位==' if S['active'] == 0 else '当前主动玩家：==第二位==') if 'active' in S else ''),
    ],
    watch=['i', 'x', ('active', 'active', 'pink'), ('score', 'score', 'green')],
    captions={
        'active = 0': '`active` 是 0/1 下标：==0 = 第一位玩家主动==',
        'active ^= x % 2': '`x = {x}` {"是奇数 → 换人" if x % 2 else "是偶数 → 不换"}：`active ^= {x % 2}` → ==`{active}`==',
        'active ^= 1': '`i = {i}`，`i % 6 == 5`，每第 6 场再换一次人：`active ^= 1` → ==`{active}`==',
        'if i % 6 == 5': '`i % 6 = {i % 6}` → {"第 6 场，要再换人" if i % 6 == 5 else "不是第 6 场"}',
        'score[active] += x': '主动玩家 `{active}` 得 `{x}` 分 → `score = {score}`',
        'return': '分数差 `{score[0]} − {score[1]}` = ==`{ret}`==',
    },
    cards=dict(
        one_liner='用 0/1 表示谁主动，奇数分和第 6 场都是异或 1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['两位玩家，第一位一开始是主动玩家；每场主动玩家得 `nums[i]` 分',
                 '得分是奇数时先换人；每第 6 场（`i = 5, 11, ...`）再换一次人',
                 '返回第一位总分减第二位总分；示例 `[2,4,2,1,2,1]` → `4`'],
        quote='active ^= x % 2  # 如果 x 是奇数，主动玩家换人',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['`active` 取 0 或 1，对应 `score` 的下标',
              '「换人」就是 `active ^= 1`；奇数时异或 `x % 2` 一步搞定',
              '先换人、后加分：换人发生在这场得分之前'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：先处理换人，再给新的主动玩家加分',
                 '第 6 场是 `i % 6 == 5`（下标从 0 开始）',
                 '奇数和第 6 场同时出现时，换两次等于没换'],
    ),
)
