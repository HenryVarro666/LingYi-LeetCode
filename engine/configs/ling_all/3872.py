CONFIG = dict(
    num=3872, title='替换最多一个元素后的最长等差子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='前后缀分解 · 枚举被改的元素',
    tags=['灵神题单·动态规划'],
    code='''
class Solution:
    def calc(self, nums: List[int]) -> List[int]:
        n = len(nums)
        pre = [0] * n
        pre[0] = 1
        pre[1] = 2
        for i in range(2, n):
            if nums[i - 2] + nums[i] == nums[i - 1] * 2:  # 三个数等差
                pre[i] = pre[i - 1] + 1
            else:
                pre[i] = 2
        return pre

    def longestArithmetic(self, nums: List[int]) -> int:
        n = len(nums)
        pre = self.calc(nums)
        ans = max(pre) + 1
        if ans >= n:  # 整个数组是等差的，或者修改端点元素后是等差的
            return n

        suf = self.calc(nums[::-1])[::-1]
        # 注意 max(pre) == max(suf)，无需重复计算

        for i in range(1, n - 1):
            # 把 nums[i] 改成 d2 / 2
            d2 = nums[i + 1] - nums[i - 1]
            if d2 % 2:  # d2 / 2 必须是整数
                continue

            ok_left = i > 1 and nums[i - 1] - nums[i - 2] == d2 // 2
            ok_right = i + 2 < n and nums[i + 2] - nums[i + 1] == d2 // 2

            if ok_left and ok_right:
                ans = max(ans, pre[i - 1] + 1 + suf[i + 1])
            elif ok_left:
                ans = max(ans, pre[i - 1] + 2)
            elif ok_right:
                ans = max(ans, suf[i + 1] + 2)

        return ans
''',
    call='Solution().longestArithmetic([9,7,5,10,1])',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums（第二次 calc 时是反转后的数组）', pointers={'i': 'blue'}, h=210,
             color=lambda S, i, v: 'yellow' if 'i' in S and i == S['i'] and S['_line'] >= 25 else None),
        dict(type='array', var='pre', label='pre：以 i 结尾的最长等差子数组', h=170),
        dict(type='array', var='suf', label='suf：以 i 开头的最长等差子数组', h=170),
        dict(type='text', h=70, size=28, fn=lambda S: (f"改 `nums[{S['i']}]` 为 `{S['d2']}/2`：左边{'能' if S.get('ok_left') else '不能'}接，右边{'能' if S.get('ok_right') else '不能'}接" if 'ok_right' in S and S['_line'] >= 33 else '')),
    ],
    watch=['i', 'd2', ('ok_left', 'ok_left', 'blue'), ('ok_right', 'ok_right', 'pink'), ('ans', 'ans', 'green')],
    max_steps=100,
    captions={
        'pre[0] = 1': '`pre[0] = 1`：只有一个数，长度 1',
        'pre[1] = 2': '`pre[1] = 2`：任意两个数都是等差的，长度 2',
        'if nums[i - 2] + nums[i]': lambda S, B, r: (f"`nums[{S.i-2}] + nums[{S.i}] = {S.nums[S.i-2] + S.nums[S.i]}`，`nums[{S.i-1}] × 2 = {S.nums[S.i-1]*2}` → " + ('三个数等差，可以接在前面那段后面' if S.nums[S.i-2] + S.nums[S.i] == S.nums[S.i-1]*2 else '不是等差，只能和前一个数组成长为 2 的新段')),
        'pre[i] = pre[i - 1] + 1': '`pre[{i}] = pre[{i-1}] + 1` = =={pre[i]}==',
        'pre[i] = 2': '`pre[{i}] = 2`：重新开始',
        'return pre': '`calc` 返回 `{pre}`',
        'pre = self.calc': '`pre[i]`：以 `i` 结尾的最长等差子数组长度 → `{pre}`',
        'ans = max(pre) + 1': '不改中间元素：把最长等差段的左邻或右邻改一下，能再长 1 → `ans = {max(pre)} + 1` = =={ans}==',
        'if ans >= n': lambda S, B, r: (f"`ans = {S.ans} >= n = {S.n}` → 整个数组能变成等差，直接返回 n" if S.ans >= S.n else f"`ans = {S.ans} < n = {S.n}` → 还不能覆盖整个数组，继续枚举改哪个"),
        'suf = self.calc': '把数组反转再算 `calc` 再反转回来，就得到 `suf[i]`：以 `i` 开头的最长等差长度 → `{suf}`',
        'for i in range(1, n - 1)': lambda S, B, r: (f"枚举被改的元素 `nums[{S.i}]`（端点另有 `ans` 初值覆盖，只管中间）" if B.get('i') != S.i or B.get('d2') is None else '枚举完毕 → 返回答案'),
        'd2 = nums[i + 1]': '改后 `nums[{i}]` 必须是两邻居的平均 → `d2 = {nums[i+1]} - {nums[i-1]}` = =={d2}==，公差 = d2 / 2',
        'if d2 % 2': lambda S, B, r: (f"`d2 = {S.d2}` 是奇数 → 平均值不是整数，这个位置改不了 → 跳过" if S.d2 % 2 else f"`d2 = {S.d2}` 是偶数 → 可以改成整数 `{S.d2 // 2}` 后的公差"),
        'continue': '跳过这个 `i`',
        'ok_left =': lambda S, B, r: (f"左边能接吗：`nums[{S.i-1}] - nums[{S.i-2}]` = {S.nums[S.i-1]-S.nums[S.i-2]}，公差 `{S.d2//2}` → ==ok_left 为 {S.ok_left}==" if S.i > 1 else f"`i = {S.i}`：左边没有 `nums[i-2]`，接不了 → ==ok_left 为 False=="),
        'ok_right =': lambda S, B, r: (f"右边能接吗：`nums[{S.i+2}] - nums[{S.i+1}]` = {S.nums[S.i+2]-S.nums[S.i+1]}，公差 `{S.d2//2}` → ==ok_right 为 {S.ok_right}==" if S.i + 2 < S.n else f"`i + 2 = {S.i+2}` 越界：右边没有 `nums[i+2]`，接不了 → ==ok_right 为 False=="),
        'if ok_left and ok_right': lambda S, B, r: ("左右两段都能接：拼成 `pre[i-1] + 1 + suf[i+1]`" if S.ok_left and S.ok_right else "左右不是都能接 → 看单边"),
        'ans = max(ans, pre[i - 1] + 1': '左 `{pre[i-1]}` + 被改的 1 + 右 `{suf[i+1]}` → `ans` = =={ans}==',
        'elif ok_left': lambda S, B, r: ("只有左边能接" if S.ok_left else "左边也不行 → 看右边"),
        'ans = max(ans, pre[i - 1] + 2)': '左段 `{pre[i-1]}` 后面接被改的 `nums[{i}]` 和 `nums[{i+1}]` → `ans = max({B.ans}, {pre[i-1]}+2)` = =={ans}==',
        'elif ok_right': lambda S, B, r: ("只有右边能接" if S.ok_right else "两边都接不上"),
        'ans = max(ans, suf[i + 1] + 2)': '右段 `{suf[i+1]}` 前面接被改的 `nums[{i}]` 和 `nums[{i-1}]` → `ans` = =={ans}==',
        'return ans': '最长等差子数组长度 `{ans}`',
    },
    cards=dict(
        one_liner='枚举改哪个数：左边以它前一个结尾的等差段，接右边以后一个开头的等差段',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['最多把一个元素改成任意整数，然后选一个等差子数组（相邻差为常数）',
                 '求能选到的最长长度',
                 '示例：`[9,7,5,10,1]` 把 `10` 改成 `3` → `[9,7,5,3,1]`，答案 `5`'],
        quote='假设修改的是 a[i]，我们需要知道：以 i-1 结尾的最长等差子数组的长度 pre[i-1]，以 i+1 开头的最长等差子数组的长度 suf[i+1]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`pre[i]` 递推：三个数等差就 `pre[i-1] + 1`，否则回到 2；`suf` 靠反转数组复用',
              '改 `a[i]` 为两邻居平均 `d`，要求 `a[i+1]-a[i-1]` 是偶数',
              '左边公差等于 `d` 就能接左段，右边同理；两边都能接 → `pre + 1 + suf`'],
        after=[dict(heading='另外两种写法', lines=['分组循环：改的只会是等差段端点旁边的数，`O(n)` 时间 `O(1)` 空间', '状态机 DP：`dfs(i, j)`，`j` 记录替换发生在哪个位置'])],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`d2 = a[i+1] - a[i-1]` 为奇数时不能改（改后必须是整数）',
                 '`ans` 先设 `max(pre) + 1`：改最长段的邻居；若 `>= n` 直接返回 n',
                 '三种情况：两边都能接 / 只接左 / 只接右，别漏掉',
                 '`calc` 用了 `pre[1] = 2`，所以要求 `n >= 2`（题目保证 `n >= 4`）'],
    ),
)
