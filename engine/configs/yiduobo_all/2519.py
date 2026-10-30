CONFIG = dict(
    num=2519, title='统计 K-Big 索引的数量', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='正反两遍树状数组', tags=['常用数据结构'],
    code='''
class Solution(object):
    def kBigIndices(self, nums, k):

        def get(x):
            s = 0
            while x > 0:
                s += f[x]
                x -= x & -x
            return s
        
        def add(x):
            while x <= 100000:
                f[x] += 1
                x += x & -x

        n = len(nums)

        f = [0] * 100001
        left = [False] * 100000
        for index in range(n):
            if get(nums[index] - 1) >= k:
                left[index] = True
            
            add(nums[index])
        
        f = [0] * 100001
        right = [False] * 100000
        for index in range(n - 1, -1, -1):
            if get(nums[index] - 1) >= k:
                right[index] = True
            
            add(nums[index])

        res = 0
        for index in range(n):
            if left[index] and right[index]:
                res += 1
        
        return res
''',
    call='Solution().kBigIndices([2,3,6,5,2,3], 2)',
    expect=2,
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue'}, label='nums（index = 当前下标）', h=190,
             color=lambda S, i, v: ('green' if S.get('left') and S.get('right') and S['_line'] >= 36 and S['left'][i] and S['right'][i] else None)),
        dict(type='array', var=lambda S: S['left'][:len(S['nums'])] if 'left' in S else [], label='left[i]：左边至少 k 个比它小', h=170,
             color=lambda S, i, v: 'green' if v else None),
        dict(type='array', var=lambda S: S['right'][:len(S['nums'])] if 'right' in S else [], label='right[i]：右边至少 k 个比它小', h=170,
             color=lambda S, i, v: 'green' if v else None),
        dict(type='text', h=70, fn=lambda S: (f"树状数组里已经放进去的数：`{sorted(S['nums'][:S['index']]) if S['_line'] < 28 else sorted(S['nums'][S['index'] + 1:])}`" if 'index' in S and 'left' in S else '')),
    ],
    watch=['index', 'k', ('res', 'res', 'green')],
    skip=['n = len', 'while x', 's += f[x]', 'x -= x & -x', 'f[x] += 1', 'x += x & -x', 's = 0', 'left = [False]', 'right = [False]', 'f = [0]'],
    max_steps=90,
    captions={
        21: '树状数组里（左边已出现的数）`< {nums[index]}` 的有 `get({nums[index]}-1)` 个，要 `>= {k}` 才算左边够大',
        29: '树状数组里（右边已出现的数）`< {nums[index]}` 的有 `get({nums[index]}-1)` 个，要 `>= {k}` 才算右边够大',
        'left[index] = True': '左侧至少 `{k}` 个更小 → `left[{index}] = True`',
        'right[index] = True': '右侧至少 `{k}` 个更小 → `right[{index}] = True`',
        'add(nums[index])': '把 `{nums[index]}` 放进树状数组，供后面的下标查询',
        'return s': '前缀和 `{s}`：已经放进去且小于查询值的个数',
        'res += 1': '左右都满足 → 下标 `{index}` 是 K-Big，`res` = {res}',
        'if left[index] and right[index]': '`left[{index}] = {left[index]}`，`right[{index}] = {right[index]}` → 两边都要满足才统计',
        'return res': 'K-Big 下标一共 =={res}== 个',
    },
    cards=dict(
        one_liner='左右各扫一遍，树状数组数「已出现且更小」的个数',
        complexity='时间 `O(n log U)`，空间 `O(U)`（U = 值域 10^5）',
        problem=['找下标 `i`：左边有至少 `k` 个数小于 `nums[i]`，右边也有至少 `k` 个',
                 '示例：`nums=[2,3,6,5,2,3]`，`k=2` → `2`（下标 2 和 3）'],
        quote='可以将左右两侧分开计算，即正反分别遍历，使用树状数组记录前缀或后缀中出现过的数，然后利用树状数组判断左侧或右侧是否至少有k个数小于nums[i]。',
        quote_src='—— yiduobo 题解原文',
        idea=['从左往右：树状数组里是 `nums[:i]`，查 `< nums[i]` 的个数，记入 `left`',
              '清空后从右往左同样做一遍，记入 `right`',
              '最后一趟统计 `left` 与 `right` 同时为真的下标'],
        summary=['时间 `O(n log U)`，树状数组按值域 `100000` 开',
                 '第二遍前必须重新 `f = [0] * 100001`，否则左边的数会混进来',
                 '先查询、后 `add`：当前数不能算自己',
                 '本视频省略了树状数组内部循环的逐步展示，只看每次查询的结果'],
    ),
)
