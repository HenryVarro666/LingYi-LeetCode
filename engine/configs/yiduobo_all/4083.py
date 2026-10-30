CONFIG = dict(
    num=4083, title='使相邻元素按位异或非零的最少删除次数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='一趟遍历 · 相同就删',
    code='''
class Solution(object):
    def minDeletions(self, nums):
        
        pre = nums[0]
        res = 0
        for v in nums[1:]:
            if pre == v:
                res += 1
            else:
                pre = v
        
        return res
''',
    call='Solution().minDeletions([1,1,2,2,3,3,3,1])',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums（黄 = 当前保留的前一个元素值 pre）', cell=84, h=200,
             color=lambda S, i, v: 'yellow' if 'pre' in S and v == S['pre'] else None),
        dict(type='text', h=120, size=32,
             fn=lambda S: (f'`pre` = ==%s==　`v` = ==%s==　异或 = `%s`' % (S['pre'], S['v'], S['pre'] ^ S['v']))
             if 'v' in S and 'pre' in S else '遍历 nums[1:]，pre 是最近一个保留的元素'),
    ],
    watch=[('pre', 'pre', 'yellow'), ('v', 'v', 'blue'), ('res', 'res', 'green')],
    captions={
        'pre = nums[0]': '第一个元素必须保留，作为 `pre = {pre}`',
        'res = 0': '`res` 统计删除次数',
        'for v in nums[1:]': '取下一个元素 `v = {v}`，和 `pre = {pre}` 比较',
        'if pre == v': lambda S, B, r: (f'`pre = {S.pre}` == `v = {S.v}`：异或为 0 → 必须删掉 ==v==' if S.pre == S.v
                                        else f'`pre = {S.pre}` ≠ `v = {S.v}`：异或非零 → 可以保留'),
        'res += 1': '删除当前元素，`res` → {res}（`pre` 不变，下一个还要和它比）',
        'pre = v': '保留 `v`，它成为新的 `pre = {pre}`',
        'return res': '一共删除 `{res}` 个元素',
    },
    cards=dict(
        one_liner='异或为 0 就是两数相同：遇到和前一个相同的就删',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给整数数组 `nums`，可以删除任意元素，其余保持顺序',
                 '要求剩下的数组里相邻两数的按位异或都 `≠ 0`',
                 '求最少删除次数',
                 '本视频：`[1,1,2,2,3,3,3,1]` → `4`'],
        quote='两个元素异或值为零，意味着这两个元素相同，因此本题实际上就是要将nums变为一个相邻元素互不相同的数组',
        quote_src='—— yiduobo 题解原文',
        idea=['异或为 0 ⇔ 两数相等，所以只需相邻不相等',
              '从下标 1 往后扫，`pre` 记最近保留的那个元素',
              '和 `pre` 相同就删（计数），不同就保留并更新 `pre`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '删除时 `pre` 不更新：被删的和 `pre` 相同，更新与否都一样',
                 '一段连续相同的 k 个数要删 `k-1` 个',
                 '原文为 Python 2 风格，代码未改'],
    ),
)
