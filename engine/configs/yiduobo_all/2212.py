def _txt(S):
    if 'state' not in S or 'now' not in S:
        return '12 个区域，每个区域「放弃」或「刚好比 Alice 多 1 支」：共 `2^12 = 4096` 种选法'
    pick = [i for i in range(12) if S['state'] >> i & 1]
    return f"枚举到 `state = {S['state']}`：选区域 {pick}，花 `{S.get('cnt', '?')}` 支箭，得 `{S.get('score', '?')}` 分"


def _col(S, i, v):
    if 'state' in S and S['state'] >> i & 1:
        return 'green'
    return None


CONFIG = dict(
    num=2212, title='射箭比赛中的最大得分', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='状态压缩枚举（01 背包的暴力解）',
    tags=['灵神题单·链表树与回溯', '难度分 1869'],
    code='''
class Solution(object):
    def maximumBobPoints(self, numArrows, aliceArrows):

        res = [0] * 12
        max_score = 0

        for state in range(4096):
            score = 0
            cnt = 0
            now = [0] * 12
            for index in range(12):
                if state & (1 << index):
                    now[index] = aliceArrows[index] + 1
                    cnt += now[index]
                    score += index
            
            if cnt <= numArrows and score > max_score:
                max_score = score
                res = now[:]
                res[0] += numArrows - cnt
        
        return res
''',
    call='Solution().maximumBobPoints(3, [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2])',
    expect=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
    views=[
        dict(type='array', var='aliceArrows', label='aliceArrows（Alice 在各区域的箭数，区域 = 下标 = 得分）', h=190, cell=80),
        dict(type='array', var='now', label='now（当前选法：选中的区域放 Alice+1 支，绿 = 选中）', h=190, cell=80,
             color=_col),
        dict(type='array', var='res', label='res（目前最优方案）', h=190, cell=80),
        dict(type='text', h=70, size=26, fn=_txt),
    ],
    watch=['state', 'cnt', 'score', ('max_score', 'max_score', 'green')],
    skip=['score = 0', 'cnt = 0', 'now = [0] * 12', 'for state in range', 'for index in range', 'if state & (1 << index)',
          'now[index] =', 'cnt += now', 'score += index', 'if cnt <= numArrows', 'max_score = score', 'res = now[:]'],
    max_steps=100, max_events=400000,
    captions={
        'res = [0] * 12': '`res` 是答案数组，12 个区域先都放 0 支',
        'max_score = 0': '`max_score` 记录目前最高得分',
        'res[0] += numArrows': '==新纪录==：`state = {state}` 花 `{cnt}` 支箭（≤ `{numArrows}`），得分 `{score}`，刷新最高分 `max_score = {max_score}` → 更新 `res`；多出的 `{numArrows - cnt}` 支箭放区域 0',
        'return res': 'Bob 的最优方案 `{res}`，得分 `{max_score}`',
    },
    cards=dict(
        one_liner='输了一分都拿不到：每个区域要么不射，要么刚好多 1 支',
        complexity='时间 `O(2^12 · 12)`，空间 `O(1)`',
        problem=['Alice、Bob 各射 `numArrows` 支箭，靶有 0~11 共 12 个区域',
                 '某区域 Bob 比 Alice 多才得该区域分，否则 Alice 得；两人都没射则无人得分',
                 '求 Bob 的箭分布，使他总分最大；示例 `numArrows=3`，Alice `[0,0,1,0,0,0,0,0,0,0,0,2]` → Bob 得 27 分'],
        quote='对于某个积分区域，bob要么一支箭都不射，要么就要比alice刚好多出一支箭。',
        quote_src='—— yiduobo 题解原文',
        idea=['赢一个区域代价 `aliceArrows[i] + 1`，收益 `i`，这是 01 背包',
              '但箭数很大不能按容量做 DP；区域只有 12 个，直接枚举 4096 种选法',
              '箭够就用得分更新答案；剩下的箭放哪都行，放区域 0'],
        after=[dict(heading='怎么看这个动画', lines=[
            '内层枚举 12 位、外层 4096 个 `state` 步数太多',
            '动画只在==刷新最高分==的时刻停下来，其余状态一闪而过',
            '`state` 的第 i 位 = 1 表示 Bob 在区域 i 比 Alice 多射 1 支'])],
        summary=['时间 `O(2^12 · 12)`，空间 `O(1)`',
                 '`cnt <= numArrows` 判断箭够不够，再看 `score > max_score`',
                 '多出的箭放进 `res[0]`，保证总箭数恰好等于 `numArrows`',
                 '同分的方案任意一个都可以，所以用严格大于号'],
    ),
)
