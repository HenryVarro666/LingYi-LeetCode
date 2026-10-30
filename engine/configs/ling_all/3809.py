def _dist(S):
    return abs(S['x'] - S['cx']) + abs(S['y'] - S['cy'])


CONFIG = dict(
    num=3809, title='最好可到达的塔', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='遍历 + 元组取最小',
    tags=[],
    code='''
class Solution:
    def bestTower(self, towers: List[List[int]], center: List[int], radius: int) -> List[int]:
        cx, cy = center
        ans = (1, -1, -1)
        for x, y, q in towers:
            if abs(x - cx) + abs(y - cy) <= radius:
                ans = min(ans, (-q, x, y))  # 加个负号，变成求 q 的最大值
        return [ans[1], ans[2]]
''',
    call='Solution().bestTower([[1,3,4], [2,2,4], [4,4,7]], [0, 0], 5)',
    expect=[1, 3],
    views=[
        dict(type='table', var='towers', h=250, rows=['塔 0', '塔 1', '塔 2'], cols=['x', 'y', 'q'],
             color=lambda S, i, j, v: ('yellow' if 'x' in S and S['towers'][i] == [S['x'], S['y'], S['q']] else None)),
        dict(type='text', size=32, fn=lambda S: (f"距离 `|{S['x']}-{S['cx']}| + |{S['y']}-{S['cy']}|` = =={_dist(S)}==，半径 `{S['radius']}` → {'可到达' if _dist(S) <= S['radius'] else '不可到达'}" if 'x' in S and 'cx' in S else '')),
        dict(type='text', size=32, fn=lambda S: (f"当前最优 `(-q, x, y)` = `{S['ans']}`" if 'ans' in S else '')),
    ],
    watch=['x', 'y', 'q', ('ans', 'ans', 'green')],
    captions={
        'cx, cy = center': '拆出中心坐标 `cx = {cx}`，`cy = {cy}`',
        'ans = (1, -1, -1)': '哨兵：第一项 `1` 比任何 `-q ≤ 0` 都大，所以任何可达的塔都会替换它',
        'for x, y, q': lambda S, B, r: ('塔都看完了，循环结束' if B.get('x') == S.get('x') and B.get('q') == S.get('q') and 'x' in B else f'看下一座塔：`({S.x}, {S.y})`，质量 `{S.q}`'),
        'if abs(x - cx)': lambda S, B, r: (f'曼哈顿距离 `{abs(S.x - S.cx) + abs(S.y - S.cy)} <= {S.radius}` → 可到达' if abs(S.x - S.cx) + abs(S.y - S.cy) <= S.radius
                                           else f'曼哈顿距离 `{abs(S.x - S.cx) + abs(S.y - S.cy)} > {S.radius}` → 不可到达，跳过'),
        'ans = min': '`min(旧 {B.ans}, 新 {(-q, x, y)})` = `{ans}`：-q 小 = q 大，q 相同时比 x、y 的字典序',
        'return [ans': '最优元组 `{ans}` → 坐标 `[{ans[1]}, {ans[2]}]`',
    },
    cards=dict(
        one_liner='把「q 最大、坐标字典序最小」压成一个元组，直接取 min',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['塔 `[x, y, q]`，与 `center` 的曼哈顿距离 `<= radius` 才可到达',
                 '在可达的塔中取 `q` 最大的，并列取坐标字典序最小；没有就 `[-1, -1]`',
                 '本视频：三座塔，`center = [0,0]`，`radius = 5`'],
        quote='ans = min(ans, (-q, x, y))  # 加个负号，变成求 q 的最大值',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['Python 元组按顺序比较：先比 `-q`，再比 `x`，再比 `y`',
              '`-q` 越小 ==q 越大==；q 相同再比 x、y 正好是字典序最小',
              '初始值 `(1, -1, -1)`：`1` 比任何 `-q` 都大，没有可达塔时返回 `[-1, -1]`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：求最大 q 却用 `min`，所以要给 q 取负',
                 '初始哨兵元组的后两项就是无解时的答案 `-1, -1`',
                 '距离用 `<=`，边界上的塔也可达'],
    ),
)
