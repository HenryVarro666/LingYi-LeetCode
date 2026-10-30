def _txt(S):
    if 'start' not in S:
        return ''
    return f"当前合并段 `[{S['start']}, {S['end']}]`，目标 `[{S['left']}, {S['right']}]`"


CONFIG = dict(
    num=1893, title='检查是否区域内所有整数都被覆盖', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='排序 + 合并连续区间',
    tags=['差分', '难度分 1307'],
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
    call='Solution().isCovered([[5,6],[1,2],[3,4]], 2, 5)',
    expect=True,
    views=[
        dict(type='intervals', var='sorted_ranges', pointer='sorted_ranges.index([x, y])', h=300, label='sorted_ranges（按起点排序，黄=正在看）'),
        dict(type='text', fn=_txt, size=26, h=70),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('start', 'start', 'green'), ('end', 'end', 'green')],
    captions={
        'sorted_ranges = sorted': '按起点排序：能覆盖目标的区间必须首尾相连，排序后只看相邻的就够了',
        'start, end = sorted_ranges[0]': '合并段先从第一个区间开始：`[{start}, {end}]`',
        'if x <= end + 1': '新区间起点 `{x}` {"≤" if x <= end + 1 else ">"} `end + 1 = {end + 1}` → ==' '{"和当前段连续（整数之间没有空洞），合并" if x <= end + 1 else "中间隔了整数，断开"}==',
        'end = max': '合并：右端延长到 `max({B.end}, {y})` = =={end}==',
        'if start <= left': '断开之前先检查：合并段 `[{start}, {end}]` 是否已盖住 `[{left}, {right}]` → {"是，直接返回 True" if start <= left and right <= end else "不是"}',
        'return True': '提前返回：这一段已经把目标区间整个盖住了',
        'start, end = x, y': '换新的合并段 `[{x}, {y}]`',
        'return start <=': '最后一段也要判断：`{start} <= {left}` 且 `{right} <= {end}` → =={ret}==',
    },
    cards=dict(
        one_liner='排序后把连续或重叠的区间合并，看合并段能否盖住目标',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给若干闭区间 `ranges` 和目标 `[left, right]`',
                 '目标里的每个整数都被至少一个区间覆盖则返回 `true`',
                 '示例：`[[5,6],[1,2],[3,4]]`，`left=2, right=5` → `true`'],
        quote='覆盖这个区域的区间也必然是连续的，于是可以先将这些区间按起点从小到大进行排序，然后合并连续或重叠的区间，然后检测合并后的区间是否覆盖住了题目要求的区域。',
        quote_src='—— yiduobo 题解',
        idea=['整数区间 `[1,2]` 和 `[3,4]` 虽不重叠，但整数上==首尾相接==，所以条件是 `x <= end + 1`',
              '一旦出现空洞，就拿手里这一段去检查目标是否已被盖住',
              '作者也提到数据范围极小，暴力标记也行'],
        summary=['复杂度：排序 `O(n log n)`',
                 '易错点：合并条件是 `end + 1`，不是 `end`',
                 '最后一段别忘了判断；`merged_intervals` 在原文中未使用',
                 '更简洁的做法：差分数组统计覆盖次数',
                 '原文已是 Python 3 写法，未做修改'],
    ),
)
