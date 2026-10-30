def _cur(S):
    m = S.get('intervals')
    if 'l' not in S or 'r' not in S or not m:
        return None
    for k, p in enumerate(m):
        if p[0] == S['l'] and p[1] == S['r']:
            return k
    return None


def _cmp(S):
    if 'right' not in S:
        return ''
    return f"当前区间 `[{S.get('l', '-')}, {S.get('r', '-')}]`　　合并区间 `[{S['left']}, {S['right']}]`　　`sum_len = {S['sum_len']}`"


def _if_cap(S, B, ret):
    if S.l <= S.right:
        return f'`l = {S.l}` ≤ 合并区间右端点 `{S.right}`：==可以合并=='
    return f'`l = {S.l}` > `{S.right}`：不相交，当前合并区间固定下来'


CONFIG = dict(
    num=3951, title='维持亮度的最小总能量', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='每时刻灯泡数 × 合并区间总长', tags=['贪心算法', '区间贪心', '难度分 1530'],
    code='''
class Solution:
    def minEnergy(self, _, brightness: int, intervals: list[list[int]]) -> int:
        intervals.sort(key=lambda p: p[0])  # 按照左端点从小到大排序

        # 56. 合并区间（只计算区间长度之和）
        sum_len = 0
        left, right = 0, -1
        for l, r in intervals:
            if l <= right:  # 左端点在合并区间内，可以合并
                right = max(right, r)  # 更新合并区间的右端点
            else:  # 不相交，无法合并
                sum_len += right - left + 1
                left, right = l, r  # 新的合并区间
        sum_len += right - left + 1

        bulbs = (brightness + 2) // 3  # 至少要开启 bulbs 个灯泡
        return bulbs * sum_len
''',
    call='Solution().minEnergy(5, 5, [[6, 12], [1, 3], [2, 4], [14, 15]])',
    expect=26,
    views=[
        dict(type='text', fn=_cmp),
        dict(type='intervals', var='intervals', pointer=_cur, label='数轴：需要照明的时间区间（黄 = 当前 l,r）', h=400),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('l', 'l', 'yellow'), ('r', 'r', 'yellow'),
           ('sum_len', 'sum_len', 'green'), ('bulbs', 'bulbs', 'orange')],
    captions={
        'intervals.sort': '按左端点排序：`{intervals}`',
        '# 56. 合并区间': '先数有多少个单位时间被覆盖，等价于合并区间后的长度之和',
        'sum_len = 0': '`sum_len` 累计被覆盖的单位时间数',
        'left, right = 0, -1': '合并区间初始为空：长度 `right - left + 1 = 0`',
        'for l, r in intervals': lambda S, B, r_: ('所有区间都看完了，退出循环' if B.get('l') == S.l and B.get('r') == S.r else f'看下一个区间 `[{S.l}, {S.r}]`'),
        'if l <= right': _if_cap,
        'right = max': '右端点 `max({B.right}, {r}) = {right}`',
        'sum_len += right - left + 1': '合并区间 `[{B.left}, {B.right}]` 长 `{B.right - B.left + 1}` → `sum_len = {sum_len}`',
        'left, right = l, r': '开始新的合并区间 `[{left}, {right}]`',
        'bulbs =': '一个灯泡照亮 3 个位置，要亮度 `{brightness}` 至少开 `ceil({brightness}/3) = {bulbs}` 个',
        'return bulbs': '答案 = `bulbs * sum_len` = `{bulbs} * {sum_len}` = =={ret}==',
    },
    cards=dict(
        one_liner='灯泡数只看亮度，时间长度只看合并区间',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['一排灯泡，开启的灯泡照亮自己和左右邻居（最多 3 个位置）',
                 '被区间覆盖的每个单位时间，总照明度必须 ≥ `brightness`；开一个灯泡一个时间单位耗 1 能量',
                 '求最小总能量',
                 '本视频：`brightness = 5`，区间 `[6,12] [1,3] [2,4] [14,15]` → `26`'],
        quote='一个灯泡可以照亮 3 个位置。为了满足总照明度至少为 brightness，我们需要开启 ceil(brightness/3) 个灯泡。……等价于 56. 合并区间之后的区间长度之和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每个有要求的时刻，最少开 `bulbs = (brightness + 2) // 3` 个灯泡',
              '有多少个时刻有要求？合并区间后求长度之和 `sum_len`（重叠时刻只算一次）',
              '答案 = `bulbs * sum_len`'],
        summary=['时间 `O(n log n)`，瓶颈在排序；空间 `O(1)`',
                 '`ceil(b/3)` 写成 `(b + 2) // 3`，避免浮点',
                 '区间是闭区间，长度要 `+ 1`；`l <= right` 相接也合并',
                 '循环后要补上最后一个合并区间；同类题：56. 合并区间、3169. 无需开会的工作日'],
    ),
)
