CONFIG = dict(
    num=3238, title='求出胜利玩家的数目', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='一次遍历 · 计数 + won 标记',
    code='''
class Solution:
    def winningPlayerCount(self, n: int, pick: List[List[int]]) -> int:
        ans = 0
        cnts = [[0] * 11 for _ in range(n)]
        won = [False] * n
        for x, y in pick:
            cnts[x][y] += 1
            if not won[x] and cnts[x][y] > x:
                won[x] = True
                ans += 1
        return ans
''',
    call='Solution().winningPlayerCount(4, [[0,0],[1,0],[1,0],[2,1],[2,1],[2,0]])',
    expect=2,
    views=[
        dict(type='array', var='pick', label='pick（玩家, 颜色）', h=190, cell=110,
             fmt=lambda v: f'{v[0]},{v[1]}',
             color=lambda S, i, v: 'blue' if S.get('x') == v[0] and S.get('y') == v[1] and False else None),
        dict(type='grid', var='cnts', label='cnts[玩家][颜色]', h=300, cell=44,
             cursors=[('x', 'y', 'yellow', '')],
             color=lambda S, i, j, v: 'green' if S['won'][i] and v > i else None),
        dict(type='array', var='won', label='won[玩家]', h=140, color=lambda S, i, v: 'green' if v else None),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 统计胜利玩家数',
        'cnts = ': '`cnts[x][y]` 表示玩家 `x` 拿到颜色 `y` 的球数',
        'won = ': '`won[x]` 标记玩家 `x` 已经算过胜利，避免重复计数',
        'for x, y in pick': '玩家 `{x}` 拿到一个颜色 `{y}` 的球',
        'cnts[x][y] += 1': '`cnts[{x}][{y}]` → =={cnts[x][y]}==',
        'if not won[x]': lambda S, B, r: (f'`cnts[{S.x}][{S.y}] = {S.cnts[S.x][S.y]}`，玩家 {S.x} 需要 `> {S.x}` 个：'
                                         + ('==达标，且之前没算过==' if (not S.won[S.x] and S.cnts[S.x][S.y] > S.x)
                                            else ('之前已经算过胜利，不重复计' if S.won[S.x] else '还没达标'))),
        'won[x] = True': '玩家 `{x}` 首次达标，标记 `won[{x}] = True`',
        'ans += 1': '胜利玩家数 `ans` → =={ans}==',
        'return ans': '共 `{ans}` 位胜利玩家',
    },
    cards=dict(
        one_liner='边数球边判断：数到 x+1 个同色就记一次胜利',
        complexity='时间 `O(nU + m)`，空间 `O(nU)`',
        problem=['玩家 `i` 只要拿到至少 `i + 1` 个同色球就是胜利玩家',
                 '`pick[i] = [x, y]`：玩家 `x` 拿到颜色 `y` 的一个球，求胜利玩家数',
                 '示例：`n=4`，6 次拿球 → `2`（玩家 0、1）'],
        quote='在统计 cnts[x][y] 的过程中，如果发现玩家 x 获得了至少 x + 1 个相同颜色的球，那么答案加一，同时标记 won[x]=true，避免重复计入答案。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['用 `n × 11` 的矩阵 `cnts` 统计每个玩家每种颜色的球数',
              '每次加一后立刻判断 `cnts[x][y] > x`',
              '同一玩家可能多次满足条件，所以用 `won` 去重'],
        summary=['时间 `O(nU + m)`，空间 `O(nU)`，`U = 11` 是颜色数',
                 '易错：`cnts[x][y] > x` 即「至少 x+1 个」，玩家 0 拿到任意球就胜利',
                 '不加 `won` 会重复计数：玩家继续拿球仍满足条件',
                 '另一种写法（方法一）：先统计完，再逐个玩家 `any(c > i for c in cnt)`'],
    ),
)
