CONFIG = dict(
    num=2875, title='无限数组的最短子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='取模 + 两倍数组上滑窗',
    tags=['滑动窗口与双指针', '难度分 1914'],
    code='''
class Solution:
    def minSizeSubarray(self, nums: List[int], target: int) -> int:
        total = sum(nums)
        n = len(nums)
        ans = inf
        left = s = 0
        rem = target % total
        for right in range(n * 2):
            s += nums[right % n]
            while s > rem:
                s -= nums[left % n]
                left += 1
            if s == rem:
                ans = min(ans, right - left + 1)
        return ans + target // total * n if ans < inf else -1
''',
    call='Solution().minSizeSubarray([1,1,1,2,3], 12)',
    expect=7,
    views=[
        dict(type='array', var=lambda S: S['nums'] * 2, label='nums + nums（框 = 窗口，和要等于 rem）', cell=84, h=250,
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', lambda S: max(S['left'], S['right'])),
             dim=lambda S, i, v: 'right' in S and 'left' in S and not (S['left'] <= i <= S['right'])),
        dict(type='text', h=110, size=30,
             fn=lambda S: (f"整段 target = `{S['target']}` = ==`{S['target'] // S['total']}`== 个整组（和 `{S['total']}`）+ 余数 rem = ==`{S['rem']}`==" if 'rem' in S else '')),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"窗口和 s = ==`{S['s']}`==，目标 rem = `{S['rem']}`" if 'rem' in S and 's' in S and 'right' in S else '')),
    ],
    watch=[('total', 'total', 'yellow'), ('rem', 'rem', 'yellow'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('s', 's', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'total = sum': '一整组 `nums` 的和 `total = {total}`',
        'n = len': '`n = {n}`',
        'rem = target': '`rem = target % total = {target} % {total} = {rem}`：去掉中间若干整组后，左右两端要凑出的和',
        'for right in': '枚举窗口右端点 `right = {right}`（对应 `nums[{right % n}]`）；只需要扫两倍长度',
        's += nums': '`nums[{right % n}] = {nums[right % n]}` 进窗口：`s = {s}`',
        'while s > rem': lambda S, B, r: (f'`s = {S.s} > rem = {S.rem}`：窗口太大，全是正数，只能缩左端点' if S.s > S.rem else f'`s = {S.s} <= rem = {S.rem}`：不用缩了'),
        's -= nums': '左端 `nums[{B.left % n}] = {nums[B.left % n]}` 移出：`s = {s}`',
        'left += 1': '`left` → {left}',
        'if s == rem': lambda S, B, r: (f'`s = {S.s} == rem`：找到一个和恰好等于 rem 的窗口，长度 `{S.right - S.left + 1}`' if S.s == S.rem else f'`s = {S.s} != rem = {S.rem}`：这个右端点没有合法窗口'),
        'ans = min': '`ans = min({B.ans}, {right - left + 1}) = {ans}`',
        'return ans': '`ans + target // total * n` = `{ans} + {target // total} * {n}` = ==`{ret}`==：窗口长度 + 中间整组的元素个数',
    },
    cards=dict(
        one_liner='先砍掉中间的整组，余下的和用滑窗在两倍数组里找',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 无限重复拼接成 `infinite_nums`，找和等于 `target` 的最短子数组长度，没有返回 -1',
                 '示例：`nums=[1,2,3], target=5` → `2`',
                 '本视频：`[1,1,1,2,3], target=12` → `7`'],
        quote='去掉中间 k 个 nums 后，剩余元素的个数不会 ≥ n。如果 ≥ n，剩余元素之和 rem ≥ total，这与 rem = target mod total < total 相矛盾。',
        quote_src='—— 灵茶山艾府题解答疑',
        idea=['子数组 = 左端一段 + 中间 k 组完整 `nums` + 右端一段',
              '中间整组越多越划算：先取 `k = target // total`，剩下 `rem = target % total`',
              '左右两段拼起来最多 `< n` 个元素，所以只需在 `nums + nums` 里滑窗找和为 `rem` 的最短窗口'],
        summary=['时间 `O(n)`，空间 `O(1)`；`right % n` 模拟两倍数组，不用真的拼接',
                 '`rem = 0` 不用特判：窗口缩到空，`s == 0` 成立，`ans = 0`',
                 '不存在窗口返回 `-1`，所以用 `ans < inf` 判断',
                 '元素都是正数，所以 `s > rem` 时缩左端点才有单调性'],
    ),
)
