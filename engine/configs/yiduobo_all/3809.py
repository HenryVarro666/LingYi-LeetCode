CONFIG = dict(
    num=3809, title='最好可到达的塔', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='一趟遍历 + 条件更新',
    tags=[],
    code='''
class Solution(object):
    def bestTower(self, towers, center, radius):
        
        ma = -1
        res = [-1, -1]
        for index, (x, y, q) in enumerate(towers):
            if abs(x - center[0]) + abs(y - center[1]) <= radius and q > ma or (q == ma and (res[0] > x or (res[0] == x and res[1] > y))):
                ma = q
                res = [x, y]
        
        return res
''',
    call='Solution().bestTower([[1,3,4], [2,2,4], [4,4,7]], [0, 0], 5)',
    expect=[1, 3],
    views=[
        dict(type='table', var='towers', h=250, rows=['塔 0', '塔 1', '塔 2'], cols=['x', 'y', 'q'],
             color=lambda S, i, j, v: ('yellow' if 'index' in S and i == S['index'] else ('green' if 'res' in S and S['towers'][i][:2] == S['res'] else None))),
        dict(type='text', size=32, fn=lambda S: (f"距离 = `{abs(S['x'] - S['center'][0]) + abs(S['y'] - S['center'][1])}`，半径 `{S['radius']}`；当前最大质量 `ma = {S['ma']}`" if 'x' in S and 'ma' in S else '')),
    ],
    watch=['index', 'x', 'y', 'q', ('ma', 'ma', 'cyan'), ('res', 'res', 'green')],
    captions={
        'ma = -1': '`ma` 记录目前最大质量因子，初值 `-1`（质量都 ≥ 0）',
        'res = [-1, -1]': '`res` 先设成「没有可达塔」的答案 `[-1, -1]`',
        'for index': lambda S, B, r: ('塔都看完了，循环结束' if B.get('index') == S.get('index') and 'index' in B else f'看第 `{S.index}` 座塔 `({S.x}, {S.y})`，质量 `{S.q}`'),
        'if abs(x - center[0])': lambda S, B, r: (
            f'距离 `{abs(S.x - S.center[0]) + abs(S.y - S.center[1])}` 超出半径 `{S.radius}` 且质量 `{S.q}` 不等于 `ma = {S.ma}` → 不可达，不更新'
            if abs(S.x - S.center[0]) + abs(S.y - S.center[1]) > S.radius and S.q != S.ma
            else (f'可达且 `q = {S.q} > ma = {S.ma}` → 质量更大，更新' if S.q > S.ma
                  else (f'质量相同 `q = ma = {S.q}`，比坐标 `[{S.x}, {S.y}]` 和 `{S.res}`：`{S.res[0]} > {S.x}`？`{S.res[0]} == {S.x}`且`{S.res[1]} > {S.y}`？ → 都不成立，不更新' if not (S.res[0] > S.x or (S.res[0] == S.x and S.res[1] > S.y))
                        else '质量相同且新塔坐标字典序更小 → 更新'))),
        'ma = q': '`ma` 更新为 `{ma}`',
        'res = [x, y]': '答案换成这座塔：`res` = `{res}`',
        'return res': '遍历结束，质量最大且字典序最小的可达塔是 `{res}`',
    },
    cards=dict(
        one_liner='一趟遍历，质量更大或（质量相同且坐标更小）就更新答案',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['塔 `[x, y, q]` 与 `center` 的曼哈顿距离 `<= radius` 才可达',
                 '求可达塔中 `q` 最大的坐标；并列取字典序最小；没有则 `[-1, -1]`',
                 '本视频：`center = [0,0]`，`radius = 5`'],
        quote='对于当前的塔，先计算center与这座塔的曼哈顿距离，若小于等于radius，就是用这座塔来更新答案。更新的标准是质量因子更大，或者质量因子相同且坐标字典序更小。',
        quote_src='—— yiduobo 题解原文',
        idea=['按题意一趟遍历，不需要排序',
              '更新条件：`q > ma`，或 `q == ma` 且坐标 `(x, y)` 比 `res` 更小',
              '`res` 初值 `[-1, -1]` 正好是无可达塔时的答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '字典序：先比 `x`，`x` 相同再比 `y`',
                 '原文为 Python 2 风格 `class Solution(object)`，代码无需改动',
                 '注意：`or` 后一支没再检查距离，仅靠 `q == ma` 才进入，本视频数据下结果正确',
                 '对比灵神：灵神把 `(-q, x, y)` 当元组直接 `min`，这里手写比较'],
    ),
)
