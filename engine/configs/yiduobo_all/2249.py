def _diff(S):
    if 'q_list' not in S or 'max_y' not in S:
        return None
    return S['q_list'][S['min_y']:S['max_y'] + 2]


def _info(S):
    if 'max_y' not in S:
        return '先求出所有圆的包围盒：x 从 `min_x` 到 `max_x`，y 从 `min_y` 到 `max_y`'
    if 'p' not in S:
        return f"扫描范围 x：`{S['min_x']}..{S['max_x']}`，y：`{S['min_y']}..{S['max_y']}`"
    s = f"竖线 `x = {S['p']}`，已累计格点 `res` = =={S['res']}=="
    if 'cnt' in S and 'q' in S:
        s += f"，当前 `cnt` = {S['cnt']}"
    return s


CONFIG = dict(
    num=2249, title='统计圆内格点数目', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='逐条竖线 + 差分数组',
    tags=[],
    code='''
class Solution(object):
    def countLatticePoints(self, circles):

        min_x = min_y = 200
        max_x = max_y = 0
        for x, y, r in circles:
            min_x = min(min_x, x - r)
            max_x = max(max_x, x + r)
            min_y = min(min_y, y - r)
            max_y = max(max_y, y + r)

        res = 0
        for p in range(min_x, max_x + 1):
            q_list = [0] * 201
            for x, y, r in circles:
                if x - r <= p <= x + r:
                    delta = int(sqrt(r * r - (x - p) * (x - p)))
                    q1, q2 = y - delta, y + delta
                    q_list[q1] += 1
                    if q2 + 1 <= max_y:
                        q_list[q2 + 1] -= 1
            
            cnt = 0
            for q in range(min_y, max_y + 1):
                cnt += q_list[q]
                if cnt > 0:
                    res += 1
        
        return res
''',
    call='Solution().countLatticePoints([[1, 1, 1], [2, 1, 1]])',
    setup='from math import sqrt',
    expect=8,
    views=[
        dict(type='text', fn=_info, size=26),
        dict(type='array', var=_diff, label='q_list 差分（只画 min_y 到 max_y；+1 = 区间开始，−1 = 区间结束的下一格）', h=170, cell=84,
             pointers={'q - min_y if _line >= 24 else None': 'blue'},
             color=lambda S, i, v: 'green' if v > 0 else ('pink' if v < 0 else None)),
    ],
    watch=['p', 'x', 'y', 'r', 'q1', 'q2', 'cnt', ('res', 'res', 'green')],
    skip=['min_x = min_y = 200', 'max_x = max_y = 0', 'for x, y, r in circles', 'for p in range', 'for q in range',
          'min_x = min(', 'max_x = max(', 'min_y = min(', 'max_y = max(', 'cnt = 0', 'if q2 + 1 <= max_y', 'if cnt > 0'],
    max_steps=110,
    captions={
        'q_list = [0] * 201': '竖线 `x = {p}`：新建差分数组 `q_list`，下标 = 纵坐标',
        'if x - r <= p <= x + r': lambda S, B, r: (f'圆 `({S.x},{S.y},{S.r})` 的横向范围 `{S.x - S.r}..{S.x + S.r}`，'
                                                   + ('竖线 `x = %d` 穿过它' % S.p if S.x - S.r <= S.p <= S.x + S.r else '竖线没碰到 → 跳过')),
        'delta = int(sqrt': '解 `(p−x)² + (q−y)² ≤ r²`：纵向半宽 `delta = {delta}`',
        'q1, q2 = y - delta': '这个圆在竖线上盖住纵坐标 `[{q1}, {q2}]`',
        'q_list[q1] += 1': '差分：区间起点 `q1 = {q1}` 处 `+1`',
        'q_list[q2 + 1] -= 1': '差分：区间终点后一格 `q2 + 1 = {q2 + 1}` 处 `-1`',
        'cnt += q_list[q]': lambda S, B, r: f'`cnt` 累加差分 = 覆盖 `q = {S.q}` 的圆数 =={S.cnt}==' + ('，大于 0 → 点被盖住' if S.cnt > 0 else '，等于 0 → 没盖住，不计'),
        'res = 0': '`res` 累计被盖住的格点数',
        'res += 1': lambda S, B, r: f'`cnt > 0`：点 `({S.p},{S.q})` 被盖住 → `res` = =={S.res}==',
        'if cnt > 0': lambda S, B, r: (f'`cnt = {S.cnt} > 0` → 点被盖住' if S.cnt > 0 else f'`cnt = 0` → 点 `({S.p},{S.q})` 没被盖住'),
        'return res': '所有竖线扫完，返回 `{res}`',
    },
    cards=dict(
        one_liner='一条竖线一条竖线扫，用差分数组合并各圆的纵向区间',
        complexity='时间 `O(X·(n + Y))`，空间 `O(Y)`',
        problem=['`circles[i] = [x, y, r]`，圆周上的点也算圆内',
                 '求至少被一个圆盖住的整数格点个数',
                 '示例：`[[2,2,1]]` → `5`；本视频用 `[[1,1,1],[2,1,1]]` → `8`'],
        quote='对于一个圆和一条垂直于x轴的直线x = p，只需要通过解方程就可以求出该直线上位于圆内的各点纵坐标的取值范围。',
        quote_src='—— yiduobo 题解原文',
        idea=['先暴力：枚举 200×200 个点，逐个判断是否在任意圆里',
              '优化：固定竖线 `x = p`，每个圆在线上盖住一段 `[y−delta, y+delta]`',
              '多个圆的区间用差分数组：起点 `+1`、终点后一格 `−1`',
              '前缀和 `cnt > 0` 的纵坐标就是被盖住的格点'],
        summary=['时间约 `O(X·(n + Y))`，比逐点 × 逐圆的暴力少一层循环',
                 '易错点：差分终点写在 `q2 + 1`，并且要判断不越过 `max_y`',
                 '易错点：`delta = int(sqrt(...))` 向下取整，格点只取整数',
                 '原文 `sqrt` 来自 math 库，视频里在 setup 补了 `from math import sqrt`，代码未改',
                 '对比灵神：灵神逐点判断并用 `break` 防重复，yiduobo 用区间差分合并重叠'],
    ),
)
