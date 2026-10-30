CONFIG = dict(
    num=3238, title='求出胜利玩家的数目', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='每人一个哈希表 · 取最大颜色数',
    code='''
class Solution(object):
    def winningPlayerCount(self, n, pick):

        balls = [{} for _ in range(n)]
        for x, y in pick:
            balls[x][y] = balls[x].get(y, 0) + 1

        res = 0
        for index in range(n):
            if balls[index] and max(balls[index].values()) > index:
                res += 1

        return res
''',
    call='Solution().winningPlayerCount(4, [[0,0],[1,0],[1,0],[2,1],[2,1],[2,0]])',
    expect=2,
    views=[
        dict(type='array', var='pick', label='pick（玩家, 颜色）', h=190, cell=110, fmt=lambda v: f'{v[0]},{v[1]}'),
        dict(type='array', var='balls', label='balls[玩家] = {颜色: 个数}', h=200, cell=200,
             fmt=lambda v: str(v).replace(' ', ''),
             color=lambda S, i, v: 'yellow' if S.get('x') == i and S.get('index') is None else
             ('green' if S.get('index') == i and v and max(v.values()) > i else None)),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('index', 'index', 'cyan'), ('res', 'res', 'green')],
    captions={
        'balls = ': '每个玩家一个哈希表：`balls[i][颜色] = 个数`',
        'for x, y in pick': '玩家 `{x}` 拿到一个颜色 `{y}` 的球',
        'balls[x][y] = ': '`balls[{x}][{y}]` → =={balls[x][y]}==',
        'res = 0': '`res` 统计胜利玩家数',
        'for index in range': '检查玩家 `{index}`：需要某种颜色 `> {index}` 个',
        'if balls[index] and': lambda S, B, r: (f'玩家 {S.index} 没拿过球 → 不胜利' if not S.balls[S.index]
                                                else f'玩家 {S.index} 最多同色 `{max(S.balls[S.index].values())}` 个，对比编号 `{S.index}`：'
                                                + ('==更大，胜利==' if max(S.balls[S.index].values()) > S.index else '不大于，不胜利')),
        'res += 1': '胜利玩家数 `res` → =={res}==',
        'return res': '共 `{res}` 位胜利玩家',
    },
    cards=dict(
        one_liner='先分人统计颜色，再看最多的同色球是否超过编号',
        complexity='时间 `O(m + n)`，空间 `O(m)`',
        problem=['玩家 `i` 任意一种颜色的球严格多于 `i` 个就是胜利玩家',
                 '`pick[i] = [x, y]`：玩家 `x` 得到颜色 `y` 的球，求胜利玩家数',
                 '示例：`n=4`，6 次拿球 → `2`'],
        quote='先对pick数组进行一趟遍历，使用哈希表统计每个玩家获取的每种颜色的球的数量，接下来再遍历每个玩家的编号，若当前玩家获得的同色球的最大数目大于当前玩家的编号，则更新答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['直接按题意模拟，每个玩家一个哈希表',
              '第一趟遍历 `pick` 统计颜色个数',
              '第二趟遍历玩家，比较 `max(颜色数)` 和编号'],
        summary=['时间 `O(m + n)`，空间 `O(m)`',
                 '易错：玩家没拿过球时哈希表为空，`max` 会报错，要先判断 `balls[index]`',
                 '原文为 Python 2 风格，代码无需改动',
                 '对比灵神：灵神用 11 列矩阵并边数边判；yiduobo 用字典，两趟遍历'],
    ),
)
