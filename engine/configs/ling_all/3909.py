CONFIG = dict(
    num=3909, title='比较双调部分的和', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='一次遍历 · 左和减右和',
    code='''
class Solution:
    def compareBitonicSums(self, nums: list[int]) -> int:
        diff = 0
        inc = True
        for i, x in enumerate(nums):
            if i > 0 and nums[i - 1] < x > nums[i + 1]:
                inc = False
            else:  # 注意峰顶抵消掉了，不算入 diff
                diff += x if inc else -x
        return -1 if diff == 0 else int(diff < 0)
''',
    call='Solution().compareBitonicSums([1,3,6,5,4,2])',
    expect=1,
    views=[
        dict(type='text', size=32, fn=lambda S: (f"diff = 峰顶左侧和 − 峰顶右侧和 = ==​{S['diff']}==" if 'diff' in S else '')),
        dict(type='array', var='nums', label='nums（蓝 = 左侧上升段，粉 = 右侧下降段，黄 = 峰顶）', h=260, cell=100,
             pointers={'i': 'blue'},
             color=lambda S, i, v: None if 'i' not in S or i > S['i'] or (i == S['i'] and S['_line'] == 5) else ('blue' if i < S['nums'].index(max(S['nums'])) else 'yellow' if i == S['nums'].index(max(S['nums'])) else 'pink')),
    ],
    watch=['i', 'x', ('inc', 'inc', 'blue'), ('diff', 'diff', 'green')],
    captions={
        'diff = 0': '`diff` 记录「左侧和 − 右侧和」，初始为 0',
        'inc = True': '`inc` 表示还没越过峰顶，当前在上升段',
        'for i, x': lambda S, B, r: ('全部看完，退出循环' if 'i' in B and B['i'] == S.i else f'看第 `{S.i}` 个数 `x = {S.x}`'),
        'if i > 0 and': lambda S, B, r: (f'`nums[{S.i-1}] = {S.nums[S.i-1]} < {S.x} > {S.nums[S.i+1]}` → ==是峰顶==' if S.i > 0 and S.nums[S.i-1] < S.x > S.nums[S.i+1] else f'`{S.x}` 不是峰顶' if S.i > 0 else '`i = 0` 是第一个数，不可能是峰顶'),
        'inc = False': '峰顶找到：`inc = False`，后面的数都属于右侧',
        'diff += x if inc': lambda S, B, r: (f'峰顶前：左侧和加上 `{S.x}`，`diff` = =={S.diff}==' if S.inc else f'峰顶后：右侧的数要减掉，`diff -= {S.x}` → =={S.diff}=='),
        'return': lambda S, B, r: (f'`diff = {S.diff}` < 0：右侧更大 → 返回 ==1==' if S.diff < 0 else f'`diff = {S.diff}` == 0：两边相等 → 返回 ==-1==' if S.diff == 0 else f'`diff = {S.diff}` > 0：左侧更大 → 返回 ==0=='),
    },
    cards=dict(
        one_liner='峰顶左边的加、右边的减，看差值的正负',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['双调数组：先严格递增到唯一峰顶，再严格递减',
                 '峰顶同时属于两部分，比较「递增部分和」与「递减部分和」',
                 '递增更大 → `0`，递减更大 → `1`，相等 → `-1`',
                 '本视频：`[1,3,6,5,4,2]` → `1`'],
        quote='计算峰顶左侧元素的和，减去峰顶右侧元素的和，记作 diff。根据 diff 与 0 的大小关系，返回答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['峰顶两边都算，加减相互抵消，所以不计入 `diff`',
              '用 `inc` 标记是否还在峰顶左侧，不需要先找峰顶',
              '峰顶判定：`nums[i-1] < x > nums[i+1]`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：峰顶不能漏掉也不能重复算，这里干脆两边抵消',
                 '`diff < 0` 说明右侧更大，对应返回 `1`',
                 '写法二：先二分求峰顶下标（第 852 题），再对左右两侧分别求和'],
    ),
)
