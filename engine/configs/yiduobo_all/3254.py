CONFIG = dict(
    num=3254, title='长度为 K 的子数组的能量值 I', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='一趟遍历 · 连续上升长度 DP',
    code='''
class Solution(object):
    def resultsArray(self, nums, k):

        res = []
        length = 0

        for index in range(len(nums)):
            if index == 0 or nums[index] != nums[index - 1] + 1:
                length = 1
            else:
                length += 1
            
            if index + 1 >= k:
                if length >= k:
                    res.append(nums[index])
                else:
                    res.append(-1)
        
        return res
''',
    call='Solution().resultsArray([1,2,3,4,3,2,5], 3)',
    expect=[3, 4, -1, -1, -1],
    views=[
        dict(type='text', fn=lambda S: (f"以 `nums[{S['index']}]={S['nums'][S['index']]}` 结尾的连续上升长度 `length` = =={S['length']}==，k = {S['k']}" if 'index' in S else ''), h=60),
        dict(type='array', var='nums', pointers={'index': 'blue'}, h=200,
             window=('index - length + 1', 'index'),
             label='nums（框 = 以 index 结尾的连续上升段）'),
        dict(type='array', var='res', pointers={}, h=160, label='res',
             color=lambda S, i, v: 'green' if v != -1 else 'pink'),
    ],
    watch=[('index', 'index', 'blue'), ('length', 'length', 'yellow'), ('k', 'k', 'purple'), ('res', 'res', 'green')],
    captions={
        'length = 0': '`length` 记录以当前元素结尾的==连续上升段长度==',
        'if index == 0 or': lambda S, B, r: (f"`index = 0`，第一个元素，从 1 开始" if S.index == 0 else
            f"`nums[{S.index}] = {S.nums[S.index]}`，`nums[{S.index-1}] + 1 = {S.nums[S.index-1]+1}`："
            + ('不相等 → 连续性断了' if S.nums[S.index] != S.nums[S.index-1] + 1 else '相等 → 接着上一个往上升')),
        'length = 1': '断开，以自己重新开始：`length = 1`',
        'length += 1': '接在上一个后面：`length` → {length}',
        'if index + 1 >= k': lambda S, B, r: (f'`index + 1 = {S.index+1}` ' + ('≥' if S.index + 1 >= S.k else '<') + f' `k = {S.k}`：'
            + ('已经凑够一个长度为 k 的窗口，可以出答案' if S.index + 1 >= S.k else '窗口还没凑够 k 个元素，先不记答案')),
        'if length >= k': lambda S, B, r: (f'`length = {S.length}` ' + ('≥' if S.length >= S.k else '<') + f' `k = {S.k}`：'
            + ('这个窗口整段连续上升，最大值就是最后一个元素' if S.length >= S.k else '窗口里有断点，不满足')),
        'res.append(nums[index])': '能量值 = 窗口末尾 `{nums[index]}`，`res` = {res}',
        'res.append(-1)': '能量值 `-1`，`res` = {res}',
    },
    cards=dict(
        one_liner='连续上升段够长，就取窗口最后一个元素，否则 -1',
        complexity='时间 `O(n)`，空间 `O(1)`（不含答案）',
        problem=['窗口内元素依次连续且上升，能量值是最大元素，否则为 `-1`',
                 '求每个长度为 `k` 的子数组的能量值',
                 '示例：`[1,2,3,4,3,2,5], k=3` → `[3,4,-1,-1,-1]`'],
        quote='一个大小为k的子数组如果是依次连续且上升的，那么其中最大的元素一定是这个子数组的最后一个元素',
        quote_src='—— yiduobo 题解原文',
        idea=['定义 `length`：以 `nums[index]` 结尾的连续上升段长度，用动态规划递推',
              '`length >= k` 说明末尾 k 个数都连续上升，答案是 `nums[index]`',
              '`index + 1 >= k` 才形成完整窗口，之前不更新答案；`length` 只依赖上一轮，用变量代替数组'],
        summary=['时间 `O(n)`，空间 `O(1)`（不含返回的数组）',
                 '易错：必须 `index + 1 >= k` 才能记答案，否则结果长度不对',
                 '易错：连续要求差恰为 1，`nums[i] != nums[i-1] + 1` 才断，相等或下降都算断开',
                 '第 II 题数据更大，同一写法直接通过'],
    ),
)
