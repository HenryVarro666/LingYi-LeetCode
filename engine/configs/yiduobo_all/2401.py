def _now(S):
    n = S.get('now')
    if n is None:
        return ''
    s = f"now = `{n:06b}`（{n}）"
    if 'index' in S:
        s += f"　nums[index] = `{S['nums'][S['index']]:06b}`　`now & nums[index]` = =={n & S['nums'][S['index']]}=="
    return s


CONFIG = dict(
    num=2401, title='最长优雅子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举右端点 · 左边界 p 单调不回头',
    tags=['位运算', '难度分 1750'],
    code='''
class Solution(object):
    def longestNiceSubarray(self, nums):

        p = 0
        now = nums[0]
        res = 1
        for index in range(1, len(nums)):
            while (now & nums[index]) > 0:
                now ^= nums[p]
                p += 1
            
            now |= nums[index]
            res = max(res, index - p + 1)
        
        return res
''',
    call='Solution().longestNiceSubarray([1,3,8,48,10])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = p，粉 = index）', pointers={'p': 'blue', 'index': 'pink'},
             window=('p', 'index'), h=260, cell=110),
        dict(type='text', h=90, size=30, fn=_now),
    ],
    watch=[('p', 'p', 'blue'), ('index', 'index', 'pink'), ('now', 'now', 'orange'), ('res', 'res', 'green')],
    captions={
        'p = 0': '`p` 记录当前右边界对应的最小左边界，先是 `0`',
        'now = nums[0]': '`now` = `nums[p..index-1]` 的按位或，先放入第一个数 `{now}`',
        'res = 1': '一个数一定优雅，`res = 1`',
        'for index in range': '枚举右边界 `index = {index}`，新数 `{nums[index]}`',
        'while (now': lambda S, B, r: (f'`now & nums[index] = {S.now & S.nums[S.index]}` > 0：存在某一位两边都是 1 → ==nums[p] 留不住==' if S.now & S.nums[S.index] > 0
                                       else '`now & nums[index] = 0`：和窗口里所有数都两两与为 0，停止收缩'),
        'now ^= nums[p]': '窗口内的数两两与为 0，各自的 1 互不重叠，异或直接去掉 `nums[{B.p}] = {nums[B.p]}` → `now = {now}`',
        'p += 1': '`p` 右移到 {p}',
        'now |= nums[index]': '把 `nums[index]` 并入：`now = {now}`',
        'res = max': '窗口长度 `{index} − {p} + 1` = {index - p + 1}，`res = max({B.res}, {index - p + 1}) = {res}`',
        'return res': '答案 `{res}`',
    },
    cards=dict(
        one_liner='右边界右移，左边界 p 只会往右走',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['子数组里不同位置的每对数按位与都等于 `0`，就是优雅子数组',
                 '求最长优雅子数组长度',
                 '示例：`[1,3,8,48,10]` → `3`'],
        quote='index对应的左边界p\'就必然大于等于p。证明也很简单，因为若p\' < p，那么说明p\'到p - 1之间的数与p到index - 1之间的数两两之间按位与都等于0',
        quote_src='—— yiduobo 题解原文',
        idea=['用 `now` 保存 `nums[p..index-1]` 的或，一次与运算就能判断新数能否加入',
              '`now & nums[index]` 非 0，说明 `nums[p]` 不可能留下，异或去掉它，`p += 1`',
              '直到与为 0，此时 `p` 就是 `index` 的最小左边界'],
        summary=['时间 `O(n)`：`p` 和 `index` 都只前进',
                 '去掉用异或：窗口内各数的 1 互不重叠，异或恰好抹掉 `nums[p]`',
                 '`now` 的初值是 `nums[0]`，循环从下标 1 开始',
                 '对比灵神：灵神从空窗口出发，yiduobo 先放入第一个数再枚举'],
    ),
)
