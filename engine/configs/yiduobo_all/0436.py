CONFIG = dict(
    num=436, title='寻找右区间', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='按起点排序 + 二分',
    code='''
class Solution(object):
    def findRightInterval(self, intervals):

        if not intervals:
            return []
        
        n = len(intervals)

        res = [-1] * n
        sorted_intervals = sorted([x + [index] for index, x in enumerate(intervals)], key=lambda d:d[0])
        
        for index, interval in enumerate(sorted_intervals):
            left, right, pos = interval
            if index < n - 1 and right <= sorted_intervals[-1][0]:
                l = index + 1
                r = n - 1
                while l < r:
                    mid = (l + r) // 2
                    if sorted_intervals[mid][0] >= right:
                        r = mid
                    else:
                        l = mid + 1
                res[pos] = sorted_intervals[l][2]

        return res
''',
    call='Solution().findRightInterval([[4,5],[2,3],[1,2],[6,7],[3,4]])',
    expect=[3, 4, 1, -1, 0],
    views=[
        dict(type='array', var='sorted_intervals', label='按起点排序后的 [起点, 终点, 原下标]', h=270, cell=150,
             pointers={'index': 'pink', 'l': 'blue', 'r': 'orange', 'mid': 'green'},
             color=lambda S, i, v: 'pink' if 'index' in S and i == S['index'] else None,
             dim=lambda S, i, v: 'l' in S and 'r' in S and S['_line'] in range(0, 99) and False),
        dict(type='array', var='res', label='res（按原下标存答案）', h=230),
        dict(type='text', h=110, fn=lambda S: f"当前区间终点 `right = {S['right']}`：在排好序的起点里找 ==最小的、不小于它的起点==" if 'right' in S else ''),
    ],
    watch=['index', 'right', 'l', 'r', 'mid', ('res', 'res', 'green')],
    captions={
        'sorted_intervals = sorted': '每个区间附上原下标再按起点排序（题目保证起点不重复）：`{sorted_intervals}`',
        'if index < n - 1': '最后一个区间右边没有区间；且终点 `{right}` 若大于最大起点 `{sorted_intervals[-1][0]}` 也找不到，这两种都跳过',
        'l = index + 1': '二分范围从 `index+1` 开始：起点已排序，右区间一定在后面',
        'r = n - 1': '上界 `r = {r}`：最大起点已经确认 >= right，答案必在范围内',
        'mid =': '取中点 `mid = ({l} + {r}) // 2 = {mid}`',
        'if sorted_intervals[mid][0] >= right': '`起点 {sorted_intervals[mid][0]} >= 终点 {right}`？成立则答案在左半（含 mid），否则在右半',
        'r = mid': '`mid` 满足条件，可能还有更小的：`r = {r}`',
        'l = mid + 1': '`mid` 的起点太小，排除它：`l = {l}`',
        'res[pos]': '`l = {l}` 就是最小满足的起点，记下它的原下标：`res[{pos}] = {res[pos]}`',
        'return res': '全部处理完，返回 `{res}`',
    },
    cards=dict(
        one_liner='起点排好序，对每个终点二分找最小的起点',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给定区间数组，每个区间起点互不相同',
                 '区间 i 的右区间是：起点 >= i 的终点，且起点 ==最小==的那个区间',
                 '返回每个区间右区间的下标，没有则为 -1',
                 '示例：`[[4,5],[2,3],[1,2],[6,7],[3,4]]` → `[3,4,1,-1,0]`'],
        quote='题目保证起点不重复，那么一个自然的想法就是再按起点进行排序。……由于此时的起点x已经是排好序了的，因此直接在x里面做二分就可以了。',
        quote_src='—— yiduobo 题解',
        idea=['先把每个区间附上原下标，再按起点排序',
              '对终点 y，目标是最小的 `x[p] >= y`，起点有序所以用二分',
              '二分只在 `index+1` 之后找；结果写回原下标 `res[pos]`'],
        summary=['排序 `O(n log n)`；二分共 `log n + log(n-1) + ... = log(n!)`，仍是 `O(n log n)`',
                 '易错点：答案要写回==原下标==，而不是排序后的下标',
                 '先判断 `right <= 最大起点`，保证二分一定有解',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`'],
    ),
)
