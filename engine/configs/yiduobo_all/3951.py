def _cur(S):
    m = S.get('intervals')
    if 'x' not in S or 'y' not in S or not m:
        return None
    for k, p in enumerate(m):
        if p[0] == S['x'] and p[1] == S['y']:
            return k
    return None


def _cmp(S):
    if 'pre_y' not in S:
        return ''
    return f"当前区间 `[{S.get('x', '-')}, {S.get('y', '-')}]`　　合并区间 `[{S['pre_x']}, {S['pre_y']}]`　　`res = {S['res']}`"


def _if_cap(S, B, ret):
    if S.x <= S.pre_y:
        return f'`x = {S.x}` ≤ `pre_y = {S.pre_y}`：==重叠==，起点不变，终点取较大者'
    return f'`x = {S.x}` > `pre_y = {S.pre_y}`：不重叠，`[pre_x, pre_y]` 成为独立区间'


CONFIG = dict(
    num=3951, title='维持亮度的最小总能量', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='模 3 余 1 开灯 + 区间合并', tags=['贪心算法', '区间贪心', '难度分 1530'],
    code='''
class Solution(object):
    def minEnergy(self, n, brightness, intervals):
        
        intervals.sort()
        pre_x, pre_y = intervals[0]
        res = 0
        for x, y in intervals[1:]:
            if x <= pre_y:
                pre_y = max(y, pre_y)
            else:
                res += pre_y - pre_x + 1
                pre_x, pre_y = x, y
        
        res += pre_y - pre_x + 1
        return res * ((brightness - 1) // 3 + 1)
''',
    call='Solution().minEnergy(5, 5, [[6, 12], [1, 3], [2, 4], [14, 15]])',
    expect=26,
    views=[
        dict(type='text', fn=_cmp),
        dict(type='intervals', var='intervals', pointer=_cur, label='数轴：需要照明的时间区间（黄 = 当前 x,y）', h=400),
    ],
    watch=[('pre_x', 'pre_x', 'blue'), ('pre_y', 'pre_y', 'pink'), ('x', 'x', 'yellow'), ('y', 'y', 'yellow'), ('res', 'res', 'green')],
    captions={
        'intervals.sort': '按起点排序：`{intervals}`',
        'pre_x, pre_y = intervals[0]': '第一个区间作为当前合并区间 `[{pre_x}, {pre_y}]`',
        'res = 0': '`res` 累计需要照明的总时间',
        'for x, y in': lambda S, B, r: ('所有区间都看完了，退出循环' if B.get('x') == S.x and B.get('y') == S.y else f'看下一个区间 `[{S.x}, {S.y}]`'),
        'if x <= pre_y': _if_cap,
        'pre_y = max': '终点 `max({y}, {B.pre_y}) = {pre_y}`；起点已排序，不会更小',
        'res += pre_y - pre_x + 1': '`[{pre_x}, {pre_y}]` 独立成段，长度 `{pre_y - pre_x + 1}` 加入 → `res = {res}`',
        'pre_x, pre_y = x, y': '换成新区间 `[{pre_x}, {pre_y}]`',
        'return res': '每时刻灯泡数 `({brightness} - 1) // 3 + 1 = {(brightness - 1) // 3 + 1}`，总能量 `{res} * {(brightness - 1) // 3 + 1}` = =={ret}==',
    },
    cards=dict(
        one_liner='开模 3 余 1 的灯，每个灯 cover 三个位置，再数总时长',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['一排灯泡，开启的灯泡照亮自己和相邻位置',
                 '被区间覆盖的每个单位时间，总照明度必须 ≥ `brightness`；每个开着的灯泡每时刻耗 1 能量',
                 '求最小总能量',
                 '本视频：`brightness = 5`，区间 `[6,12] [1,3] [2,4] [14,15]` → `26`'],
        quote='应该打开1、4、7这写模3余1的位置，也就是说尽量让一个灯泡能cover三个位置。……每次照明所需的灯泡数量，就是(brightness - 1) // 3 + 1。',
        quote_src='—— yiduobo 题解原文',
        idea=['灯泡开在 1、4、7…，互不重叠，一个灯泡照亮 3 个位置',
              '每个有要求的时刻需要 `(brightness - 1) // 3 + 1` 个灯泡',
              '有要求的时刻数 = 区间合并后各段长度之和，最后相乘'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '`(b - 1) // 3 + 1` 就是向上取整 `ceil(b / 3)`',
                 '区间是闭区间，长度 `pre_y - pre_x + 1`；最后一段要在循环后补上',
                 '`n` 参数在代码里没用到',
                 '同类题：56. 合并区间、3169. 无需开会的工作日'],
    ),
)
