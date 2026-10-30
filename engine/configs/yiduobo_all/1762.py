def _top(S):
    if 'now' not in S:
        return ''
    return f"右侧最高 `now = {S['now']}`；已找到能看海的建筑下标 `res = {S['res']}`"


CONFIG = dict(
    num=1762, title='能看到海景的建筑物', difficulty='Medium', category='单调栈',
    author='yiduobo', technique='从右往左维护右侧最高',
    code='''
class Solution(object):
    def findBuildings(self, heights):

        n = len(heights)
        res = [n - 1]
        now = heights[-1]
        for index in range(n - 2, -1, -1):
            if heights[index] > now:
                res.append(index)
                now = heights[index]
        
        res.reverse()
        return res
''',
    call='Solution().findBuildings([4,5,2,3,1])',
    expect=[1, 3, 4],
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='bars', var='heights', label='heights（海在最右边；绿 = 能看到海）', h=330, pointers={'index': 'pink'},
             color=lambda S, i, v: ('green' if 'res' in S and i in S['res'] else None)),
        dict(type='array', var='res', label='res', cell=70, h=120),
    ],
    watch=[('index', 'index', 'pink'), ('now', 'now', 'orange'), ('res', 'res', 'green')],
    captions={
        'n = len': '`n = {n}`，海在最右边',
        'res = [n - 1]': '最右边的建筑右侧没有遮挡，==一定能看到海==：`res = {res}`',
        'now = heights[-1]': '`now` 记录当前建筑右侧==最高的高度==，先是 `{now}`',
        'for index in range': '从右往左看建筑 `{index}`，高度 `{heights[index]}`',
        'if heights[index] > now': lambda S, B, r: (
            f'`{S.heights[S.index]} > now = {S.now}` → 比右边所有建筑都高，能看到海' if S.heights[S.index] > S.now
            else f'`{S.heights[S.index]} <= now = {S.now}` → 被右边挡住，看不到海'),
        'res.append': '建筑 `{index}` 加入答案：`res = {res}`',
        'now = heights[index]': '它成了新的右侧最高：`now = {now}`',
        'res.reverse': '`res` 是从右往左收集的，反转成从小到大：`{res}`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='从右往左扫，只有比右侧最高还高的建筑能看到海',
        complexity='时间 `O(n)`，空间 `O(1)`（不计答案）',
        problem=['一排建筑，海在最右边；一栋建筑右边所有建筑都比它矮才能看到海',
                 '返回能看到海景的建筑下标（升序）',
                 '示例：`heights = [4,5,2,3,1]` → `[1,3,4]`'],
        quote='对于一栋建筑，其能否看到海景取决于其右侧最高的建筑物高度是否比该建筑要矮，于是只需从后向前一趟遍历。',
        quote_src='—— yiduobo 题解原文',
        idea=['最右边的建筑一定能看到海，从它开始',
              '从后向前遍历：先判断当前建筑是否比 `now` 高，再用它的高度更新 `now`',
              '收集下标是倒序的，最后 `reverse` 一下'],
        summary=['时间 `O(n)`，空间 `O(1)`（不计答案）',
                 '易错：要严格大于 `now`；相同高度会被挡住',
                 '易错：`res` 是倒序收集的，别忘了 `reverse()`',
                 '原文为 Python 2 风格，代码无需改动；题面由简报缺失，按 LeetCode 1762 题意编写'],
    ),
)
