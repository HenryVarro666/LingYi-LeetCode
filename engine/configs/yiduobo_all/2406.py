def _cur(S):
    if 'x' not in S or 'y' not in S:
        return None
    for k, p in enumerate(S['intervals']):
        if p[0] == S['x'] and p[1] == S['y']:
            return k
    return None


def _cmp(S):
    if 'x' not in S or 'y' not in S:
        return ''
    if not S['end_pos']:
        return f"当前区间 `[{S['x']}, {S['y']}]`　还没有任何划分"
    return f"当前区间 `[{S['x']}, {S['y']}]`　起点 `x = {S['x']}` 对比 最小终点 `end_pos[0] = {S['end_pos'][0]}`"


def _if(S, B, ret):
    x, e = B.x, B.end_pos
    if not e:
        return '堆为空：没有划分可以接 → 只能另起一个划分'
    if e[0] < x:
        return f'最小终点 `{e[0]} < x = {x}`：这个划分已经结束 → 弹出，让 `[{x}, {B.y}]` ==接在它后面=='
    return f'最小终点 `{e[0]} ≥ x = {x}`：连最早结束的划分都与它重叠 → ==不弹出，必须新增一个划分=='


CONFIG = dict(
    num=2406, title='将区间分为最少组数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='按起点排序 + 堆维护各划分的终点',
    tags=['常用数据结构', '贪心与思维', '难度分 1713'],
    code='''
class Solution(object):
    def minGroups(self, intervals):

        end_pos = []
        for x, y in sorted(intervals, key=lambda d:d[0]):
            if end_pos and end_pos[0] < x:
                heapq.heappop(end_pos)
            heapq.heappush(end_pos, y)
        
        return len(end_pos)
''',
    call='Solution().minGroups([[5,10],[6,8],[1,5],[2,3],[1,10]])',
    expect=3,
    views=[
        dict(type='text', fn=_cmp, h=60),
        dict(type='intervals', var='intervals', pointer=_cur, label='数轴：每条是一个区间（黄 = 当前区间）', h=300),
        dict(type='heap', var='end_pos', label='end_pos：每个划分的右边界（最小堆）', top_color='green', h=140),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('划分数 len(end_pos)', lambda S: len(S['end_pos']) if 'end_pos' in S else 0, 'green')],
    captions={
        'end_pos = []': '`end_pos` 是堆：存==当前每个划分的右边界==',
        'for x, y in sorted': '按起点从小到大取下一个区间 `[{x}, {y}]`',
        'if end_pos and end_pos[0] < x': _if,
        'heapq.heappop': '弹出堆顶：旧划分的末尾让给新区间，等一下换成 `y = {B.y}`',
        'heapq.heappush': '把 `y = {y}` 加入堆：这个划分现在以 `{y}` 结尾，堆 `{end_pos}`',
        'return len(end_pos)': '堆的大小就是划分数：返回 `{ret}`',
    },
    cards=dict(
        one_liner='区间按起点排序，能放到某个划分后面就放，否则新增一个划分',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['每个区间只能属于一个组，同一组内区间不相交，求==最少组数==',
                 '示例：`[[5,10],[6,8],[1,5],[2,3],[1,10]]` → `3`',
                 '示例：`[[1,3],[5,6],[8,10],[11,13]]` → `1`'],
        quote='若其可以放在某个区间的后面，那么从index + 1往后的所有区间都可以放在那个区间的后面。换言之，在这里选择任意可用的区间，让[left[index], right[index]]接在其后面总是最优的。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序后，往后的区间起点只会更大：谁能接，后面的也能接',
              '只需看当前==最小的终点==：它都不行，别的划分更不行',
              '证明：放弃接上去，最坏也只和接上去一样，所以==能放就放=='],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '判断是 `end_pos[0] < x`，端点相等算相交，不能接',
                 '每个区间无论如何都会 `heappush`；能接时先 `heappop` 去掉旧终点',
                 '原文已是可运行的写法，只是类签名为 Python 2 风格（`class Solution(object)`），未改动',
                 '对比灵神：灵神用 `heapreplace` 一步完成弹出和加入'],
    ),
)
