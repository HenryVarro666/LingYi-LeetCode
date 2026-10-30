CONFIG = dict(
    num=4063, title='至多一次取反能被 K 整除的最长子数组 I', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举取反元素 + 前缀和模 k',
    code='''
class Solution:
    # 做法类似 974. 和可被 K 整除的子数组
    def longestSubarrayDivByK(self, nums: list[int], k: int) -> int:
        first_pos = {0: -1}  # 前缀和 % k 首次出现的下标
        s = 0  # 前缀和
        res = 0
        for r, x in enumerate(nums):
            s = (s + x) % k
            if s in first_pos:
                res = max(res, r - first_pos[s])
            else:
                first_pos[s] = r
        return res

    def longestSubarray(self, nums: list[int], k: int) -> int:
        # 不取反
        ans = self.longestSubarrayDivByK(nums, k)

        # 枚举取反元素
        for i in range(len(nums)):
            nums[i] *= -1  # 取反
            ans = max(ans, self.longestSubarrayDivByK(nums, k))
            nums[i] *= -1  # 复原

        return ans
''',
    skip=[5, 6], max_steps=90,
    call='Solution().longestSubarray([4,1,2], 3)',
    expect=3,
    views=[
        dict(type='array', var='nums', h=190, label='nums（粉 = 当前被取反的下标 i，蓝 = 内层扫到的 r）',
             pointers={'r': 'blue', 'i': 'pink'},
             color=lambda S, i, v: 'pink' if S.get('i') == i and v < 0 else None),
        dict(type='map', var=lambda S: S['first_pos'] if 'first_pos' in S else {}, label='first_pos：前缀和 % k → 首次出现的下标',
             fmt=lambda k, v: f'{k}: {v}', h=210, font=30),
        dict(type='text', h=90, size=28, fn=lambda S: (f"前缀和 `s % k` = =={S['s']}==，已有的最长长度 `res` = =={S['res']}==  （内层）" if 'first_pos' in S and 'res' in S
                                                       else (f"`ans` = =={S['ans']}==" if 'ans' in S else ''))),
    ],
    watch=[('i', 'i', 'pink'), ('r', 'r', 'blue'), ('s', 's', 'cyan'), ('res', 'res', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'first_pos = {0: -1}': '`first_pos` 记下每个 `前缀和 % k` 首次出现的下标，空前缀余数 `0` 对应 `-1`；`s` 是模后的前缀和，`res` 是这一轮的最长长度',
        's = (s + x)': '`s = ({B.s} + {x}) % k = {s}`',
        'if s in first_pos': lambda S, B, r: (f"余数 `{S.s}` 之前出现过（下标 {S.first_pos[S.s]}）→ 中间这段和能被 `k` 整除" if S.s in S.first_pos
                                              else f"余数 `{S.s}` 第一次出现 → 先记下位置"),
        'res = max(res, r': '子数组 `[{first_pos[s] + 1}..{r}]` 和能被 k 整除，长度 `{r} − {first_pos[s]}`：`res = {res}`',
        'first_pos[s] = r': '首次出现就记下：`first_pos[{s}] = {r}`（只留最早的，这样子数组才最长）',
        'return res': '这一轮最长长度 `{res}`，回到外层和 `ans` 比较',
        'ans = self.longestSubarrayDivByK(nums, k)': '不取反时的答案 `ans = {ans}`',
        'for i in range': lambda S, B, r: ('每个位置都试过了' if B.get('i') == S.i else f'枚举取反的下标 `i = {S.i}`'),
        'nums[i] *= -1  # 取反': '把 `nums[{i}]` 取反，变成 `{nums[i]}`',
        'ans = max(ans, self': '数组已取反：调用上面的函数求最长长度，再和 `ans = {ans}` 取最大',
        'nums[i] *= -1  # 复原': '把 `nums[{i}]` 复原为 `{nums[i]}`，换下一个位置',
        'return ans': '答案 `{ans}`',
    },
    cards=dict(
        one_liner='枚举取反的元素，每次都转成“和能被 k 整除的最长子数组”',
        complexity='时间 `O(n^2)`，空间 `O(min(n,k))`',
        problem=['子数组和能被 `k` 整除，或取反其中一个元素后能被 `k` 整除，就是“有效”的',
                 '求最长有效子数组的长度，没有则返回 `0`',
                 '示例：`nums=[4,1,2]`，`k=3` → `3`（把 `2` 取反后 `4+1−2=3`）'],
        quote='枚举取反的元素是 nums[i]。随后做法类似 974. 和可被 K 整除的子数组。改成维护前缀和模 k 的首次出现的下标，从而计算最大子数组长度。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先不取反求一遍；再枚举每个 `nums[i]`，取反后重新求一遍，最后复原',
              '求法：前缀和模 `k`，同一个余数出现两次，中间那段和就是 `k` 的倍数',
              '只记余数==首次==出现的下标，这样差值就是最长长度'],
        summary=['时间 `O(n^2)`：枚举 `n` 个取反位置，每次 `O(n)`；空间 `O(min(n,k))`',
                 '易错点：取反后==一定要复原==，否则影响后面的枚举',
                 '`first_pos[0] = -1` 处理从下标 0 开始的子数组',
                 '题解还给了一份更快的 `O(n + min(n,k)^2)` 写法，本视频演示主写法',
                 '对应题 II（`n` 到 `10^5`）需要用那份更快的写法'],
    ),
)
