def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    lights = S.get('lights') or []
    cv.text((x0 + 18, y0 + 4), '每盏灯照亮的区间（竖线 = 当前扫到的位置）', 24, T['muted'], bold=True)
    iv = [(a - b, a + b) for a, b in lights]
    if not iv:
        return
    lo, hi = min(a for a, _ in iv), max(b for _, b in iv)
    L, R = x0 + 60, x1 - 60
    span = max(1, hi - lo)

    def X(v):
        return L + (v - lo) / span * (R - L)
    live = 'p' in S and 'cnt' in S
    sweep = None
    if live:
        sweep = S['p'] // 2 + (0.5 if S['p'] % 2 else 0)
    y = y0 + 54
    for a, b in iv:
        on = sweep is not None and a <= sweep <= b
        fill = T['yellow'] if on else T['blue']
        cv.rect((X(a), y, max(X(b), X(a) + 6), y + 22), fill=fill, r=11)
        cv.text((X(a) - 8, y + 11), str(a), 20, T['muted'], anchor='rm')
        cv.text((max(X(b), X(a) + 6) + 8, y + 11), str(b), 20, T['muted'], anchor='lm')
        y += 34
    yb = y + 10
    cv.line([(L, yb), (R, yb)], T['border'], 2)
    for v in range(lo, hi + 1):
        cv.text((X(v), yb + 6), str(v), 18, T['dim'], anchor='mt', mono=True)
    if sweep is not None:
        cv.line([(X(sweep), y0 + 48), (X(sweep), yb)], T['green'], 3)


def _sorted(S):
    return sorted(S['points']) if 'points' in S else []


def _top(S):
    if 'p' in S and 'cnt' in S:
        p = S['p']
        pos = p // 2
        if p % 2 == 0:
            return f'扫到 ==位置 {pos}==（灯亮起，+1）：当前有 `{S["cnt"]}` 盏灯照着，最大 `{S["ma"]}`'
        return f'扫到 ==位置 {pos}== 的右侧（灯熄灭，−1）：当前有 `{S["cnt"]}` 盏灯照着'
    if 'points' in S:
        return '每盏灯拆成两个事件：左端点 `left×2`（亮）、右端点 `right×2+1`（灭）'
    return '把每盏灯的照亮区间 `[pos−range, pos+range]` 当作区间加一'


CONFIG = dict(
    num=2021, title='街上最亮的位置', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='差分 · 事件排序扫描',
    tags=['常用数据结构'],
    code='''
class Solution(object):
    def brightestPosition(self, lights):

        points = []
        for pos, range in lights:
            left = pos - range
            right = pos + range
            points.append(left * 2)
            points.append(right * 2 + 1)
        
        cnt = 0
        res = 0
        ma = 0
        for p in sorted(points):
            if p % 2 == 0:
                cnt += 1
                if cnt > ma:
                    ma = cnt
                    res = p // 2
            else:
                cnt -= 1
        
        return res
''',
    call='Solution().brightestPosition([[-3,2],[1,2],[3,3]])',
    expect=-1,
    views=[
        dict(type='text', fn=_top, size=24, h=80),
        dict(type='custom', draw=_draw, h=260),
        dict(type='array', var=_sorted, label='排序后的事件（偶数 = 亮，奇数 = 灭）',
             color=lambda S, i, v: ('yellow' if 'p' in S and v == S['p'] else None), cell=70, h=150),
    ],
    watch=[('p', 'p', 'yellow'), ('cnt', 'cnt', 'blue'), ('ma', 'ma', 'orange'), ('res', 'res', 'green')],
    captions={
        'left = pos': '灯位置 `{pos}`，范围 `{range}`：左端点 `{pos} - {range} = {left}`',
        'right = pos': '右端点 `{pos} + {range} = {right}`：这盏灯照亮 `[{left}, {right}]`',
        'res = 0': '`res` 是答案位置（最亮里最靠左的）',
        'left * 2': '左端点 ×2 = `{left*2}`：偶数表示“亮起”，同坐标时排在熄灭前面',
        'right * 2 + 1': '右端点 ×2+1 = `{right*2+1}`：奇数表示“熄灭”，==端点本身仍算被照亮==',
        'cnt = 0': '`cnt` 统计当前位置被几盏灯照到',
        'ma = 0': '`ma` 记录出现过的最大亮度',
        'for p in sorted': '按坐标从小到大处理下一个事件 `p = {p}`',
        'if p % 2 == 0': lambda S, B, r: (f'`{S.p} % 2 == 0` → 成立，是亮起事件' if S.p % 2 == 0 else f'`{S.p} % 2 == 1` → 不成立，是熄灭事件'),
        'cnt += 1': '一盏灯亮起：`cnt` → =={cnt}==',
        'if cnt > ma': lambda S, B, r: (f'`{S.cnt} > {S.ma}`：刷新最大亮度，且是==最靠左==的位置' if S.cnt > S.ma else f'`{S.cnt} > {S.ma}` 不成立：只有严格更大才更新，所以保留更靠左的位置'),
        'ma = cnt': '最大亮度更新为 `{ma}`',
        'res = p': '答案位置 `res = {p} // 2 = {res}`',
        'cnt -= 1': '一盏灯熄灭：`cnt` → {cnt}',
        'return res': '最亮且最靠左的位置是 `{res}`',
    },
    cards=dict(
        one_liner='每盏灯是一段区间加一，排序端点后扫一遍',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`lights[i] = [pos, range]`：灯在 `pos`，照亮 `[pos−range, pos+range]`',
                 '求被最多灯照到的位置；并列时取==最小==的位置',
                 '示例：`[[-3,2],[1,2],[3,3]]` → `-1`'],
        quote='将每个区间的两个端点从小到大排序，然后一趟遍历，统计每个位置最多出现在几个区间内，取其中的最大值作为答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['把街道看成数组，一盏灯 = 区间 `[l, r]` 整体加一，是离线差分问题',
              '左端点编码成 `l×2`，右端点编码成 `r×2+1`：同一坐标==先亮后灭==，端点处也算被照亮',
              '遍历排序后的事件，`cnt` 就是前缀和；严格变大才更新，得到最小位置'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '右端点用 `×2+1`：区间是闭区间，坐标相同时要先加后减',
                 '`cnt > ma` 必须是严格大于，才能保证并列时取最小位置',
                 '原文为 Python 2 写法，`p / 2` 已改为 `p // 2`（整数除法）；变量名 `range` 遮住了内置函数，原样保留'],
    ),
)
