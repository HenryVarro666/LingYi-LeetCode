CONFIG = dict(
    num=2410, title='运动员和训练师的最大匹配数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='排序 + 双指针 · 训练师的视角',
    tags=['灵神题单', '难度分 1381'],
    code='''
class Solution:
    def matchPlayersAndTrainers(self, players: List[int], trainers: List[int]) -> int:
        players.sort()
        trainers.sort()
        j, m = 0, len(players)
        for t in trainers:
            if j < m and players[j] <= t:
                j += 1
        return j
''',
    call='Solution().matchPlayersAndTrainers([4,7,9,3], [8,2,5,6,7])',
    expect=3,
    views=[
        dict(type='text', size=28, fn=lambda S: (f"下一个要匹配的运动员 `players[{S['j']}]`" + (f" = {S['players'][S['j']]}" if S['j'] < len(S['players']) else '：没有了，全部匹配') + (f"；当前训练师 `t = {S['t']}`" if 't' in S else '')) if 'j' in S else '先把两个数组排序'),
        dict(type='array', var='players', pointers={'j': 'blue'}, h=200, label='players（排序后）',
             color=lambda S, i, v: 'green' if 'j' in S and i < S['j'] else None),
        dict(type='array', var='trainers', h=200, label='trainers（排序后）',
             color=lambda S, i, v: 'pink' if 't' in S and v == S['t'] else None,
             dim=lambda S, i, v: 't' in S and v < S['t']),
    ],
    watch=[('j', 'j', 'blue'), ('t', 't', 'pink'), ('m', 'm')],
    captions={
        'players.sort()': '运动员从小到大排序 → `{players}`',
        'trainers.sort()': '训练师从小到大排序 → `{trainers}`',
        'j, m = 0, len': '`j` 指向下一个待匹配的运动员（也是已匹配数），`m = {m}`',
        'for t in trainers': lambda S, B, r: ('训练师都看完了，循环结束' if B.get('t') == S.t else f'轮到训练师 `t = {S.t}`（能力值从小到大）'),
        'if j < m and': lambda S, B, r: (f"运动员都匹配完了（`j = {S.j} = m`）→ 不成立" if S.j >= S.m
                                         else (f"`players[{S.j}] = {S.players[S.j]}` ≤ `t = {S.t}` → ==成立==：这位训练师能带这位运动员，匹配"
                                               if S.players[S.j] <= S.t else
                                               f"`players[{S.j}] = {S.players[S.j]}` > `t = {S.t}` → 不成立：训练师太弱，换下一位更强的")),
        'j += 1': '匹配成功，`j` → {j}：下一个运动员（能力值更大）找后面的训练师',
        'return j': '`j` 就是最大匹配数，返回 =={j}==',
    },
    cards=dict(
        one_liner='把运动员当成子序列，在训练师里往后找',
        complexity='时间 `O(n log n + m log m)`，空间 `O(1)`',
        problem=['`players[i] <= trainers[j]` 时可以匹配，每人最多匹配一次，求最大匹配数',
                 '示例：`[4,7,9]` 和 `[8,2,5,8]` → `2`',
                 '本视频：`[4,7,9,3]` 和 `[8,2,5,6,7]` → `3`'],
        quote='训练师的视角不需要写二重循环，更简单。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先排序；运动员只需要考虑能力值最小的一部分人（前缀）',
              '遍历训练师：`players[j] <= t` 就匹配，`j` 加一；否则这位训练师太弱，跳过',
              '像在 `trainers` 里找子序列 `players`，对比第 392 题「判断子序列」'],
        summary=['时间 `O(n log n + m log m)`，瓶颈在排序，空间 `O(1)`',
                 '外层遍历更长的 `trainers`，不匹配就继续，匹配就 `j += 1`，不用二重循环',
                 '另一种写法：外层遍历运动员，内层 while 找训练师，没找到就提前返回 `i`',
                 '易错点：条件是 `players[j] <= t`（可以相等）'],
    ),
)
