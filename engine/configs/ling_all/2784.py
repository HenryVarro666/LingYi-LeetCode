CONFIG = dict(
    num=2784, title='检查数组是否是好的', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='原地打标记（取负）',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution:
    def isGood(self, nums: List[int]) -> bool:
        n = len(nums) - 1
        cnt_n = 0
        for x in nums:
            x = abs(x)
            if (x > n or
                x == n and cnt_n > 1 or
                x < n and nums[x] < 0):  # x 之前遇到过，现在又遇到了，所以 x 的出现次数至少是 2
                return False
            if x == n:
                cnt_n += 1
            else:
                nums[x] = -nums[x]  # 标记 x 遇到过
        return True
''',
    call='Solution().isGood([1,3,4,4,2])',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: (f"n = 长度 − 1 = `{S['n']}`，base[n] 里 `{S['n']}` 要出现 2 次，其余各 1 次" if 'n' in S else '')),
        dict(type='array', var='nums', label='nums（负数 = 这个值已经出现过一次）', h=300,
             color=lambda S, i, v: 'purple' if v < 0 else None),
    ],
    skip=['if (x > n or', 'x == n and cnt_n > 1 or'],
    watch=['n', ('x', 'x', 'blue'), ('cnt_n', 'cnt_n', 'orange')],
    captions={
        'n = len': '`n = len(nums) - 1 = {n}`：好数组长度是 n+1，最大值必须是 `{n}`',
        'cnt_n = 0': '`cnt_n` 单独统计 `n` 出现的次数，它最多只能出现 2 次',
        'x = abs(x)': '取出值 `x = {x}`（被标记成负数的格子要取绝对值还原）',
        'x < n and nums': lambda S, B, r: (f'`x = {S.x}` 大于 n，超出范围 → 不是好数组' if S.x > S.n else
            f'`x = n = {S.n}`，已经出现 `{S.cnt_n}` 次，还没超过 2 次 → 继续' if S.x == S.n else
            f'`nums[{S.x}] = {S.nums[S.x]}`：' + ('已经是负数，说明 x 之前出现过 → ==重复== → False' if S.nums[S.x] < 0 else '还是正数，x 第一次出现 → 继续')),
        'cnt_n += 1': '`n` 又出现一次：`cnt_n` → {cnt_n}',
        'nums[x] = -nums[x]': '把 `nums[{x}]` 取负做标记：以后再遇到 `{x}` 就能发现它来过。`nums[{x}] = {nums[x]}`',
        'return True': '每个数都检查完，没有出现异常 → ==好数组==',
    },
    cards=dict(
        one_liner='把 nums 自己当辅助数组：值 x 第一次出现，就把 nums[x] 取负',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`base[n] = [1,2,...,n-1,n,n]`，长度 `n+1`，判断 `nums` 是不是它的排列',
                 '示例：`[1,3,3,2]` → `true`；`[2,1,3]` → `false`',
                 '本视频：`[1,3,4,4,2]` → `true`'],
        quote='我们可以在首次遇到元素 x 时，把 nums[x] 改成 -nums[x]，这样再次遇到 |x| 时，就能通过 nums[x] < 0 得知 nums 中至少有两个 |x|。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['最大值只能是 `n = len - 1`，所以先排除 `x > n`',
              '`n` 允许出现两次，用变量 `cnt_n` 单独数；其余数用取负标记查重',
              '数组里的数都是正数，取负不会和原值混淆，读的时候 `abs` 还原'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '读元素必须先 `abs`：它可能已被前面的步骤标成负数',
                 '`n` 不能用取负标记（它要出现两次），所以单独用 `cnt_n`',
                 '方法一用 `cnt` 数组计数，空间 `O(n)`；同类题：442、448'],
    ),
)
