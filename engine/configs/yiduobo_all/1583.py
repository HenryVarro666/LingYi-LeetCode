CONFIG = dict(
    num=1583, title='统计不开心的朋友', difficulty='Medium', category='模拟',
    author='yiduobo', technique='亲密度排名表 · 暴力枚举',
    code='''
class Solution(object):
    def unhappyFriends(self, n, preferences, pairs):

        prefer_dict = {}
        for x, prefer in enumerate(preferences):
            prefer_dict[x] = {}
            for level, y in enumerate(prefer):
                prefer_dict[x][y] = level
        
        pair_dict = {}
        for x, y in pairs:
            pair_dict[x] = y
            pair_dict[y] = x

        res = 0
        for x in pair_dict:
            for y in preferences[x]:
                if y == pair_dict[x]:
                    break
                if prefer_dict[y][x] < prefer_dict[y][pair_dict[y]]:
                    res += 1
                    break
        
        return res
''',
    call='Solution().unhappyFriends(4, [[1,2,3],[3,2,0],[3,1,0],[1,2,0]], [[0,1],[2,3]])',
    expect=2,
    views=[
        dict(type='table', var='preferences', label='preferences（每行从最亲到最不亲；蓝 = 当前 x 的一行，粉 = 正在看的 y）',
             cell=84, h=300, rows=['x=0', 'x=1', 'x=2', 'x=3'], cols=['#1', '#2', '#3'],
             color=lambda S, i, j, v: (('pink' if v == S.get('y') else 'blue') if 'res' in S and 'x' in S and i == S['x'] else None)),
        dict(type='map', var='pair_dict', label='pair_dict（谁和谁配对）', fmt=lambda k, v: f'{k} ↔ {v}', h=130, font=30),
        dict(type='map', var=lambda S: S.get('prefer_dict') if 'pair_dict' in S else None,
             label='prefer_dict[x][y] = y 在 x 心中的排位（0 最亲）', fmt=lambda k, v: f'{k}: {v}', h=250, font=26),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('res', 'res', 'green')],
    captions={
        'prefer_dict = {}': '`prefer_dict[x][y]`：朋友 `y` 在 `x` 心中的排位',
        'prefer_dict[x] = {}': '给 `x = {x}` 建一张排名表',
        'prefer_dict[x][y] = level': '`{x}` 心中 `{y}` 排第 `{level}`（越小越亲）',
        'pair_dict = {}': '`pair_dict[x]`：`x` 当前的配对朋友',
        'pair_dict[x] = y': '`{x}` 和 `{y}` 配对（双向记录）',
        'res = 0': '`res` 统计不开心的人数',
        'for x in pair_dict': '检查 `x = {x}`，他的配对朋友是 `{pair_dict[x]}`',
        'for y in preferences[x]': '从最亲的开始枚举 `y = {y}`：只需看比配对朋友更亲的人',
        'if y == pair_dict[x]': lambda S, B, r: (f'`y = {S.y}` 就是 `x` 的配对朋友 → 后面的都不如他亲，`x` 不会不开心，停' if S.y == S.pair_dict[S.x]
                                                  else f'`y = {S.y}` 比配对朋友 `{S.pair_dict[S.x]}` 更亲，继续看 `y` 怎么想'),
        'if prefer_dict[y][x] <': lambda S, B, r: (
            f'`y = {S.y}` 心中 `x` 排 `{S.prefer_dict[S.y][S.x]}`，自己的配对 `{S.pair_dict[S.y]}` 排 `{S.prefer_dict[S.y][S.pair_dict[S.y]]}`：'
            + ('`x` 更亲 → 两人互相更喜欢' if S.prefer_dict[S.y][S.x] < S.prefer_dict[S.y][S.pair_dict[S.y]] else '`y` 更喜欢自己的配对 → 不成立')),
        'res += 1': '`x = {x}` 不开心：`res` = {res}',
        'break': '`x` 已判定完，换下一个人',
        'return res': '不开心的朋友共 `{res}` 人',
    },
    cards=dict(
        one_liner='x 更爱 y，y 也更爱 x，那 x 就不开心',
        complexity='时间 `O(n²)`，空间 `O(n²)`',
        problem=['`n` 个朋友（偶数）两两配对；`preferences[i]` 是 `i` 对其他人的亲密度，从高到低',
                 '`x` 配给 `u`，`y` 配给 `v`：若 `x` 更亲 `y` 超过 `u`，且 `y` 更亲 `x` 超过 `v`，则 `x` 不开心',
                 '示例 `n=4` → `2`'],
        quote='枚举所有亲密度大于pair[x]的朋友y。若对于y而言，x的亲密度大于其配对的朋友pair[y]的亲密度，那么x就是不开心的。',
        quote_src='—— yiduobo 题解原文',
        idea=['n 很小，直接逐个判断：对每个 `x`，从 `preferences[x]` 头开始枚举 `y`，遇到自己的配对就停',
              '`y` 那边的态度要快速查：预处理 `prefer_dict[y][x]` 表示排位',
              '排位小 = 更亲；满足条件就答案加 1 并 `break`，一个人只算一次'],
        summary=['时间 `O(n²)`，空间 `O(n²)`',
                 '排位越小越亲，比较时别写反',
                 '找到一个满足的 `y` 就要 `break`，否则同一个 `x` 会被重复计数',
                 '代码与原文一致，无需修改'],
    ),
)
