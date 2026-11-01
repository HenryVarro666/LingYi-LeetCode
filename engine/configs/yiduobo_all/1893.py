CONFIG = dict(
    num=1893, title='检查是否区域内所有整数都被覆盖', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='排序 + 合并区间',
    tags=['灵神题单', '常用数据结构', '难度分 1307'],
    code='''
class Solution(object):
    def isCovered(self, ranges, left, right):

        merged_intervals = []
        sorted_ranges = sorted(ranges, key=lambda d:d[0])
        start, end = sorted_ranges[0]
        for x, y in sorted_ranges[1:]:
            if x <= end + 1:
                end = max(end, y)
            else:
                if start <= left and right <= end:
                    return True
                start, end = x, y

        return start <= left and right <= end
''',
    call='Solution().isCovered([[7,9],[1,3],[2,5]], 2, 5)',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: (f"当前合并段 `[{S['start']}, {S['end']}]`，目标 `[{S['left']}, {S['right']}]`：" + ('==已经包住目标==' if S['start'] <= S['left'] and S['right'] <= S['end'] else '还没包住')) if 'start' in S and 'end' in S else '先按起点排序，再把连续或重叠的区间合并成一段'),
        dict(type='array', var='sorted_ranges', label='sorted_ranges（按起点排序）', h=200, cell=150),
        dict(type='array', var='ranges', label='原始 ranges', h=170, cell=150),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'start', 'end', 'x', 'y'],
    captions={
        'sorted_ranges = sorted': '按起点从小到大排序：`{sorted_ranges}`，这样能边扫边合并',
        'start, end = sorted_ranges[0]': '第一段先当作当前合并段：`[{start}, {end}]`',
        'for x, y in': '取下一个区间 `[{x}, {y}]`',
        'if x <= end + 1': lambda S, B, r: (f"`x = {S['x']} <= end + 1 = {S['end'] + 1}`：连着或重叠 → 合并" if S['x'] <= S['end'] + 1 else f"`x = {S['x']} > end + 1 = {S['end'] + 1}`：中间有空隙 → 合并段到此为止"),
        'end = max(end, y)': '合并：`end = max({B.end}, {y}) = {end}`',
        'if start <= left and right <= end': lambda S, B, r: (f"合并段 `[{S['start']}, {S['end']}]` 包住了 `[{S['left']}, {S['right']}]` → 目标全被覆盖" if S['start'] <= S['left'] and S['right'] <= S['end'] else f"合并段 `[{S['start']}, {S['end']}]` 没包住目标 → 继续找下一段"),
        'return True': '目标整段被一个合并段包住 → 返回 True',
        'start, end = x, y': '从空隙后的区间重新开始：`[{start}, {end}]`',
        'return start <= left': '最后一段也要检查一次：`{start} <= {left} and {right} <= {end}` → {ret}',
    },
    cards=dict(
        one_liner='覆盖得住就必然连续：排序后合并，看一段能否包住目标',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给若干闭区间 `ranges`，判断 `[left, right]` 内每个整数是否都被至少一个区间覆盖',
                 '本视频：`[[7,9],[1,3],[2,5]]`，`left=2, right=5` → `True`'],
        quote='如果能覆盖住，说明覆盖这个区域的区间也必然是连续的，于是在这里可以先将这些区间按起点从小到大进行排序，然后合并连续或重叠的区间',
        quote_src='—— yiduobo 题解原文',
        idea=['按起点排序后，从左到右维护当前合并段 `[start, end]`',
              '下一个区间起点 `x <= end + 1`（整数连续）就并进来，否则断开',
              '断开时检查合并段是否包住 `[left, right]`；最后一段也要检查'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错：是 `x <= end + 1` 而不是 `x <= end`，`[1,2]` 和 `[3,4]` 相邻也算连续',
                 '最后一段合并段循环里不会检查，要在末尾再判断一次',
                 '作者说数据范围极小，随便怎么搞都行；`merged_intervals` 在原代码里没用到',
                 '对比灵神：灵神用差分数组统计覆盖次数，这里用排序合并'],
    ),
)
