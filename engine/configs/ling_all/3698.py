CONFIG = dict(
    num=3698, title='分割数组得到最小绝对差', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='山峰数组 · 分类讨论',
    tags=['灵神题单', '动态规划', '难度分 1649'],
    code='''
class Solution:
    def splitArray(self, nums: List[int]) -> int:
        n = len(nums)
        # 最长严格递增前缀
        pre = nums[0]
        i = 1
        while i < n and nums[i] > nums[i - 1]:
            pre += nums[i]
            i += 1

        # 最长严格递减后缀
        suf = nums[-1]
        j = n - 2
        while j >= 0 and nums[j] > nums[j + 1]:
            suf += nums[j]
            j -= 1

        # 情况一
        if i <= j:
            return -1

        d = pre - suf
        # 情况二
        if i - 1 == j:
            return abs(d)

        # 情况三，suf 多算了一个 nums[i-1]，或者 pre 多算了一个 nums[i-1]
        return min(abs(d + nums[i - 1]), abs(d - nums[i - 1]))
''',
    call='Solution().splitArray([1,3,5,4,2])',
    expect=3,
    views=[
        dict(type='array', var='nums', h=330, cell=90, label='nums：先严格递增，再严格递减',
             pointers={'i': 'blue', 'j': 'pink'},
             color=lambda S, k, v: ('blue' if 'i' in S and k < S['i'] and S.get('_line', 0) <= 10 else None)),
        dict(type='text', h=90, fn=lambda S: (f"递增前缀和 `pre = {S['pre']}`" + (f"，递减后缀和 `suf = {S['suf']}`" if 'suf' in S else '') + (f"，差 `d = {S['d']}`" if 'd' in S else '')) if 'pre' in S else ''),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('pre', 'pre', 'cyan'), ('suf', 'suf', 'orange')],
    captions={
        'pre = nums[0]': '前缀从 `nums[0]` 开始，`pre = {pre}`',
        'while i < n and nums[i] > nums[i - 1]': lambda S, B, r: (f"`nums[{S.i}] = {S.nums[S.i]} > nums[{S.i-1}] = {S.nums[S.i-1]}`，还在严格递增 → 并入前缀" if S.i < len(S.nums) and S.nums[S.i] > S.nums[S.i-1] else ("`i` 到头了，整个数组都是递增" if S.i >= len(S.nums) else f"`nums[{S.i}] = {S.nums[S.i]}` 没有比前一个大 → 递增前缀结束于 `i-1 = {S.i-1}`")),
        'pre += nums[i]': '`pre` += `nums[{i}]` → =={pre}==',
        'i += 1': '`i` → {i}：`i` 是递增前缀之后的第一个位置',
        'suf = nums[-1]': '后缀从最后一个元素开始，`suf = {suf}`',
        'while j >= 0 and nums[j] > nums[j + 1]': lambda S, B, r: (f"`nums[{S.j}] = {S.nums[S.j]} > nums[{S.j+1}] = {S.nums[S.j+1]}`，还在严格递减 → 并入后缀" if S.j >= 0 and S.nums[S.j] > S.nums[S.j+1] else ("`j` 走出数组左端" if S.j < 0 else f"`nums[{S.j}] = {S.nums[S.j]}` 不比右边大 → 递减后缀结束，`j = {S.j}`")),
        'suf += nums[j]': '`suf` += `nums[{j}]` → =={suf}==',
        'j -= 1': '`j` → {j}：`j` 是递减后缀之前的第一个位置',
        'if i <= j': lambda S, B, r: (f"`i = {S.i} <= j = {S.j}`：前缀和后缀之间有空隙，不是山峰 → 返回 -1" if S.i <= S.j else f"`i = {S.i} > j = {S.j}`：前缀和后缀接上了，不是情况一"),
        'd = pre - suf': '`d = pre − suf = {pre} − {suf}` = =={d}==',
        'if i - 1 == j': lambda S, B, r: (f"`i − 1 = {S.i-1} = j`：前后缀恰好相邻、没有重叠 → 分割唯一，返回 `|d|`" if S.i - 1 == S.j else f"`i − 1 = {S.i-1} ≠ j = {S.j}`：前后缀共用了峰顶 `nums[{S.i-1}]`，它可以给任意一边"),
        'return abs(d)': '返回 `|{d}|` = =={abs(d)}==',
        'return min(': lambda S, B, r: f"峰顶 `{S.nums[S.i-1]}` 被两边都算了：给前缀（后缀扣掉它）`|{S.d + S.nums[S.i-1]}|`，给后缀（前缀扣掉它）`|{S.d - S.nums[S.i-1]}|`，取小 =={r}==",
    },
    cards=dict(
        one_liner='数组必须是山峰：找最长递增前缀和最长递减后缀，再看它们怎么接',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把 `nums` 恰好分成两个非空子数组：左边严格递增，右边严格递减',
                 '返回两边元素和的最小绝对差；没有合法分割返回 `-1`',
                 '本视频：`[1,3,5,4,2]` → `3`'],
        quote='从左到右，找最长严格递增前缀 [0,i-1]，最长严格递减后缀 [j+1,n-1]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`nums` 必须先严格递增再严格递减',
              '`i <= j`：中间有空隙 → `-1`；`i-1 == j`：峰顶恰好重复两个 → 分割唯一',
              '否则 `i-2 == j`：峰顶只有一个，给前缀或给后缀各算一遍取小'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '情况三里 `pre` 和 `suf` 都包含了峰顶 `nums[i-1]`，所以要用 `d ± nums[i-1]` 修正',
                 '`[1,2,3,3,3,2]` 这类峰顶重复太多的，会落到 `i <= j` → `-1`',
                 '属于「前后缀分解」专题，思路是预先求出前缀 / 后缀的性质'],
    ),
)
