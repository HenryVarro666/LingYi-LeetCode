CONFIG = dict(
    num=2410, title='运动员和训练师的最大匹配数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='排序 + 单调指针 · 运动员找刚好够的训练师',
    tags=['灵神题单', '贪心与思维', '难度分 1381'],
    code='''
class Solution(object):
    def matchPlayersAndTrainers(self, players, trainers):

        trainers.sort()
        p = 0
        res = 0
        for player in sorted(players):
            while p < len(trainers) and trainers[p] < player:
                p += 1
            
            if p == len(trainers):
                break
            
            res += 1
            p += 1
        
        return res
''',
    call='Solution().matchPlayersAndTrainers([4,7,9,3], [8,2,5,6,7])',
    expect=3,
    views=[
        dict(type='text', size=28, fn=lambda S: (f"运动员 `{S['player']}` 找训练师：当前候选 `trainers[{S['p']}]`" + (f" = {S['trainers'][S['p']]}" if S['p'] < len(S['trainers']) else '：没有了')) if 'player' in S else '先把训练师排序，运动员从弱到强依次找'),
        dict(type='array', var=lambda S: sorted(S['players']), h=200, label='sorted(players)',
             color=lambda S, i, v: 'blue' if 'player' in S and v == S['player'] else None,
             dim=lambda S, i, v: 'player' in S and v < S['player']),
        dict(type='array', var='trainers', pointers={'p': 'pink'}, h=200, label='trainers（排序后）',
             dim=lambda S, i, v: 'p' in S and i < S['p']),
    ],
    watch=[('player', 'player', 'blue'), ('p', 'p', 'pink'), ('res', 'res', 'green')],
    captions={
        'trainers.sort()': '训练师从小到大排序 → `{trainers}`',
        'p = 0': '`p`：能满足当前运动员的最小训练师下标，只会右移',
        'res = 0': '`res` 统计成功匹配数',
        'for player in sorted': '轮到运动员 `player = {player}`（能力值从低到高）',
        'while p < len': lambda S, B, r: (f"`trainers[{S.p}] = {S.trainers[S.p]}` < `{S.player}` → 训练能力不够，`p` 右移" if S.p < len(S.trainers) and S.trainers[S.p] < S.player
                                          else (f"`p = {S.p}` 已到末尾" if S.p >= len(S.trainers) else f"`trainers[{S.p}] = {S.trainers[S.p]}` ≥ `{S.player}` → 这就是刚好够的训练师，停")),
        'p += 1': lambda S, B, r: (f'`trainers[{S.p - 1}]` 不够强，`p` → {S.p}' if S._line == 9 else f'这位训练师已被用掉，`p` → {S.p}，下一位运动员从后面找'),
        'if p == len': lambda S, B, r: ('`p == len(trainers)` → ==成立==：没有训练师能搞定当前运动员，后面的运动员要求更高，也不行 → 结束' if S.p == len(S.trainers)
                                        else f'`p = {S.p}` 还在范围内 → 找到了训练师，匹配'),
        'res += 1': '匹配成功，`res` → {res}',
        'break': '匹配到这里为止',
        'return res': '最多匹配 =={res}== 对',
    },
    cards=dict(
        one_liner='弱的运动员先配，每人挑刚好够格的训练师',
        complexity='时间 `O(n log n + m log m)`，空间 `O(n)`',
        problem=['`players[i] <= trainers[j]` 时可匹配，每人最多一次，求最大匹配数',
                 '示例：`[4,7,9]` 和 `[8,2,5,8]` → `2`',
                 '本视频：`[4,7,9,3]` 和 `[8,2,5,6,7]` → `3`'],
        quote='对于某个运动员而言，最赚的就是让剩余的训练师中，训练能力值刚好大于运动员能力值的训练师来训练该运动员。',
        quote_src='—— yiduobo 题解原文',
        idea=['只要匹配数最多，就让能力低的运动员先匹配',
              '都从小到大排序后，每位运动员的训练师下标 `p` 只会往后走，均摊 `O(1)`',
              '`p` 走到末尾：当前运动员没人能带，后面更强的运动员更不行，直接结束'],
        summary=['时间 `O(n log n + m log m)`，空间 `O(n)`（`sorted(players)` 新建列表）',
                 '`while` 里是 `<`，训练能力等于运动员能力也算匹配',
                 '匹配后 `p += 1`，一位训练师只能用一次',
                 '原文为 Python 2 风格，本视频无需修改，直接运行'],
    ),
)
