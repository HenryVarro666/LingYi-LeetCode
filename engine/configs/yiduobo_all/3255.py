CONFIG = dict(
    num=3255, title='长度为 K 的子数组的能量值 II', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='一维 DP · 变量迭代',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1595'],
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
        dict(type='array', var='nums', pointers={'index': 'blue'}, window=('index - length + 1', 'index'), h=240,
             label='nums（框 = 以 index 结尾的连续 +1 段）'),
        dict(type='array', var='res', h=240, label='res（逐个追加）',
             color=lambda S, i, v: 'green' if v != -1 else None),
    ],
    watch=[('index', 'index', 'blue'), ('length', 'length', 'cyan'), 'k'],
    captions={
        'res = []': '`res` 按窗口顺序存每个窗口的能量值',
        'length = 0': '`length`：以 `nums[index]` 结尾的「依次连续且上升」子数组最大长度',
        'for index in range': lambda S, B, r: ('遍历结束' if getattr(B, 'index', None) == S.index and S.index == len(S.nums) - 1 else f'`index = {S.index}`，处理 `nums[{S.index}] = {S.nums[S.index]}`'),
        'if index == 0 or': lambda S, B, r: ('第一个元素，`length = 1`' if S.index == 0 else
                                           (f'`{S.nums[S.index]} ≠ {S.nums[S.index-1]} + 1` → 接不上前一个，`length` 重新记为 1'
                                            if S.nums[S.index] != S.nums[S.index-1] + 1 else
                                            f'`{S.nums[S.index]} = {S.nums[S.index-1]} + 1` → 接得上，走 else 分支')),
        'length = 1': '`length` = 1，只有自己',
        'length += 1': '在上一位的基础上加自己：`length` = {length}',
        'if index + 1 >= k': lambda S, B, r: (f'`index + 1 = {S.index+1} ≥ k = {S.k}` → 已经凑得出长度为 k 的窗口，可以记答案'
                                             if S.index + 1 >= S.k else f'`index + 1 = {S.index+1} < k` → 还凑不出窗口，先不记'),
        'if length >= k': '`length = {length}`，`k = {k}` → {"够 k 个，能量值是末尾元素" if length >= k else "不够 k 个，能量值 -1"}',
        'res.append(nums[index])': '窗口以 `{nums[index]}` 结尾且合格 → 追加 `{nums[index]}`',
        'res.append(-1)': '不合格 → 追加 `-1`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='窗口合格 ⇔ 以末尾结尾的连续段长度 ≥ k，能量值就是末尾元素',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计）',
        problem=['能量值：窗口内元素依次连续且上升 → 最大元素，否则 `-1`',
                 '求所有长为 `k` 的子数组的能量值',
                 '本视频：`[1,2,3,4,3,2,5], k=3` → `[3,4,-1,-1,-1]`'],
        quote='一个大小为k的子数组如果是依次连续且上升的，那么其中最大的元素一定是这个子数组的最后一个元素。',
        quote_src='—— yiduobo 题解原文',
        idea=['定义 `length[index]` = 以 `nums[index]` 结尾的连续上升段最大长度（DP）',
              '`nums[index] == nums[index-1] + 1` 就 `length[index] = length[index-1] + 1`，否则为 1',
              '只依赖上一轮，所以用一个变量代替数组'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：`index + 1 >= k` 之前不能记答案，否则结果长度不对',
                 '判断的是「恰好 +1」，不是单纯递增',
                 '原文是 Python 3 也能运行的写法，未做修改',
                 '对比灵神：灵神直接写 `ans[i-k+1] = x`；yiduobo 按顺序 append，需要先过 `index+1 >= k`'],
    ),
)
