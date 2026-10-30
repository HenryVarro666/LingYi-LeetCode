def _col(S, i, v):
    return 'green' if v else None


CONFIG = dict(
    num=2682, title='找出转圈游戏输家', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='模拟 · vis 标记接过球的人',
    tags=[],
    code='''
class Solution:
    def circularGameLosers(self, n: int, k: int) -> List[int]:
        vis = [False] * n
        i, d = 0, k
        while not vis[i]:
            vis[i] = True
            i = (i + d) % n
            d += k
        return [i for i, b in enumerate(vis, 1) if not b]
''',
    call='Solution().circularGameLosers(7, 3)',
    expect=[2, 6, 7],
    views=[
        dict(type='text', fn=lambda S: f"球在下标 `{S['i']}`（第 {S['i'] + 1} 个朋友），下一次传 `{S['d']}` 步" if 'i' in S and 'd' in S and '_inner' in S and 'vis' in S and S.get('_line', 0) < 10 else ''),
        dict(type='array', var='vis', pointers={'i': 'blue'}, color=_col, h=260, label='vis（绿 = 接过球；下标 = 朋友编号 − 1）'),
    ],
    watch=[('i', 'i', 'blue'), ('d', 'd', 'pink')],
    captions={
        'vis = [False]': '`vis[i]` 表示下标 `i` 的朋友接过球没有；下标从 0 开始，返回时再 +1',
        'i, d = 0, k': '第 1 个朋友（下标 0）先接球；第一次传球走 `d = k = {d}` 步',
        'while not vis[i]': lambda S, B, r: (f'`vis[{S.i}]` = 假：这个人还没接过球 → 游戏继续'
                                             if not S.vis[S.i] else f'`vis[{S.i}]` = 真：这个人第 2 次接球 → 游戏结束'),
        'vis[i] = True': '下标 `{i}` 接到球，标记 ==已接球==',
        'i = (i + d) % n': '顺时针走 `{B.d}` 步，绕圈取模：`({B.i} + {B.d}) % {n}` = =={i}==',
        'd += k': '下一轮要多传 `k` 步：`d` = =={d}==',
        'return [': lambda S, B, r: f'没接过球的就是输家，编号 = 下标 + 1 → =={r}=='.replace('==[', '==').replace(']==', '=='),
    },
    cards=dict(
        one_liner='按题意模拟：谁接过球就标记，第二次接球时停下',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`n` 个朋友围成圈，第 1 个人接球，第 `i` 次传球走 `i*k` 步',
                 '某人第 2 次接到球时游戏结束，没接过球的人是输家',
                 '示例：`n=5, k=2` → `[4,5]`；本视频用 `n=7, k=3`'],
        quote='按题意模拟，用 vis 数组标记接到过球的人。为方便取模运算，循环中的下标可以从 0 开始，在返回时再加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`i` 是当前接球人的下标，`d` 是这次要传的步数',
              '每传一次：`i = (i + d) % n`，`d += k`',
              '`while not vis[i]`：走到已经标记过的人就是第 2 次接球，停止'],
        summary=['时间 `O(n)`，空间 `O(n)`：每人至多被标记一次',
                 '易错点：下标从 0 开始，返回时用 `enumerate(vis, 1)` 转成编号',
                 '`d` 每轮增加 `k`，没有取模，数据小所以不会溢出',
                 '循环先标记再移动，所以最后落到的那个人（已标记）不会被重复标记'],
    ),
)
