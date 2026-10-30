def _chips(title, items_fn, hl_fn):
    """画一排事件小方块：items_fn(S) -> [(文字, 颜色名)]，hl_fn(S, i, item) -> 是否高亮"""
    def draw(cv, S, B, box, T):
        x0, y0, x1, y1 = box
        cv.text((x0 + 18, y0 + 4), title, 24, T['muted'], bold=True)
        items = items_fn(S)
        if not items:
            cv.text((x0 + 18, y0 + 60), '（空）', 24, T['dim'])
            return
        per = max(1, int((x1 - x0 - 40) // 120))
        for i, (txt, col) in enumerate(items):
            r, c = divmod(i, per)
            X = x0 + 24 + c * 120
            Y = y0 + 60 + r * 90
            cv.rect((X, Y, X + 108, Y + 70), fill=T[col], r=8, alpha=200)
            if hl_fn(S, i, (txt, col)):
                cv.rect((X - 4, Y - 4, X + 112, Y + 74), outline=T['yellow'], width=4, r=10)
            cv.text((X + 54, Y + 35), txt, 26, T['bg'], anchor='mm', bold=True)
    return draw


CONFIG = dict(
    num=3009, title='折线图上的最大交点数量', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='乘 2 处理开闭区间 + 差分',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def maxIntersectionCount(self, y):

        points = []
        for index in range(1, len(y)):
            if y[index] > y[index - 1]:
                left, right = y[index - 1] * 2, y[index] * 2 - 1
            else:
                left, right = y[index] * 2 + 1, y[index - 1] * 2
            
            points.append([left, -1])
            points.append([right, 1])
        
        points.append([y[-1] * 2, -1])
        points.append([y[-1] * 2, 1])

        points.sort()
        now = 0
        res = 0
        for v, delta in points:
            now -= delta
            res = max(now, res)
        
        return res
''',
    call='Solution().maxIntersectionCount([1,3,1,3,2])',
    expect=4,
    views=[
        dict(type='array', var='y', label='折线各点纵坐标 y', pointers={'index': 'blue'}, h=250),
        dict(type='custom', h=330, draw=_chips('事件 [位置, 类型]：绿 = 线段开始(-1)，粉 = 线段结束(1)',
             lambda S: [(f"{p[0]}{'开' if p[1] < 0 else '止'}", 'green' if p[1] < 0 else 'pink') for p in S.get('points', [])],
             lambda S, i, it: 'now' not in S and i == len(S['points']) - 1)),
        dict(type='text', fn=lambda S: (f"本段：`y[{S['index']-1}]={S['y'][S['index']-1]}` → `y[{S['index']}]={S['y'][S['index']]}`，翻成整数区间 `[{S['left']}, {S['right']}]`" if 'left' in S and 'index' in S and 'now' not in S and isinstance(S['index'], int) else (f"扫描事件：位置 `{S['v']}`，当前重叠 `now = {S['now']}`" if 'v' in S else ''))),
    ],
    watch=['index', 'left', 'right', 'now', ('res', 'res', 'green')],
    captions={
        'points = []': '`points` 存“事件”：线段起点、终点各一个',
        'if y[index] > y[index - 1]': '这一段是上行还是下行？`{y[index-1]} → {y[index]}`：线段取==前闭后开==，端点只算一次',
        'left, right = y[index - 1] * 2': '上行：起点闭 → `y*2 = {left}`；终点开 → 乘 2 后往起点靠 `y*2−1 = {right}`',
        'left, right = y[index] * 2 + 1': '下行：起点（较高点）开、终点（较低点）闭，翻成升序：`[{left}, {right}]`',
        'points.append([left, -1])': '起点事件 `[{left}, -1]`：-1 排序时排在同位置的 +1 前面',
        'points.append([right, 1])': '终点事件 `[{right}, 1]`',
        'points.append([y[-1] * 2, -1])': '最后一个点没被任何线段包含 → 单独补一个点区间 `[{y[-1]*2}, {y[-1]*2}]`：起点事件',
        'points.append([y[-1] * 2, 1])': '同一点的终点事件',
        'points.sort()': '按位置排序，同位置时 -1（开始）在前 → 闭端点会被算作重叠',
        'now -= delta': lambda S, B, r: f'事件 `[{S.v}, {S.delta}]`：`now` {B.now} → =={S.now}==（{"一条线段开始" if S.delta < 0 else "一条线段结束"}）',
        'res = max(now, res)': '`res = max({B.res}, {now}) = {res}`：重叠最多的纵坐标',
        'return res': '最多有 `{res}` 个交点',
    },
    cards=dict(
        one_liner='折线拆成线段，乘 2 化开为闭，再差分求最大重叠',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['折线依次连接点 `(i, y[i])`，相邻点连线段',
                 '求一条水平线与折线的==最多交点数==（水平线可取任意高度）',
                 '本视频：`y=[1,3,1,3,2]` → `4`'],
        quote='拆分出来的线段只能是前开后闭或者前闭后开的，因为转折点不能计算多次。……一种经典的处理方法是乘 2：闭点直接乘 2，开点乘 2 之后尽量向另一端靠近。',
        quote_src='—— yiduobo 题解原文',
        idea=['答案一定落在整数或半整数上 → 把纵坐标 ×2，全部落到整点',
              '每段取前闭后开，开端点靠向另一端 1 格（上行终点 `×2−1`，下行起点 `×2+1`）',
              '最后一个点单独成一个点区间；事件排序后扫一遍，==最大重叠数==就是答案'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '`-1` 表示开始、`1` 表示结束：排序后同位置先开始后结束，所以 `now -= delta` 是先加后减',
                 '最后一个点漏了会少算一个交点',
                 '原文为 Python 2 风格，代码无需改动',
                 '同类题：253 会议室 II、732 日程安排表 III'],
    ),
)
