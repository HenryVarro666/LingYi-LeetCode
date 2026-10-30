CONFIG = dict(
    num=2122, title='还原原数组', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='排序 + 枚举 higher[0] + 双指针（Go 原文转写）',
    tags=['滑动窗口与双指针', '贪心与思维', '难度分 2159'],
    code='''
class Solution:
    def recoverArray(self, nums: List[int]) -> List[int]:
        nums.sort()
        n = len(nums)
        for i in range(1, n):
            if nums[i] == nums[i - 1]: continue  # 优化：如果与上一个元素相同，那么我们会得到同样的 k，同样找不到原数组，此时应直接跳过
            d = nums[i] - nums[0]  # 此时 d > 0 必然成立
            if d & 1: continue  # k 必须是整数
            k = d // 2
            vis = [False] * n  # 用来标记出现在 higher 中的数（用 nums 的下标）
            vis[i] = True
            ans = [(nums[0] + nums[i]) // 2]
            lo, hi = 0, i + 1
            while hi < n:  # 双指针：lo 指向 lower，hi 指向 higher
                lo += 1
                while vis[lo]: lo += 1  # 找 lower：跳过出现在 higher 中的数
                while hi < n and nums[hi] - nums[lo] < 2 * k: hi += 1  # 找 higher
                if hi == n or nums[hi] - nums[lo] > 2 * k: break  # 不存在满足等式的 higher 值
                vis[hi] = True
                ans.append((nums[lo] + nums[hi]) // 2)  # 找到一对满足等式的 (lower, higher)
                hi += 1
            if len(ans) == n // 2: return ans
''',
    call='Solution().recoverArray([12, 3, 7, 1, 8, 5])',
    expect=[3, 5, 10],
    skip=['n = len(nums)'],
    views=[
        dict(type='array', var='nums', label='nums（紫 = 已在 higher，黄 = higher[0]）', h=250, cell=84,
             pointers={'lo': 'blue', 'hi': 'pink'},
             color=lambda S, j, x: ('yellow' if S.get('i') == j and S.get('vis') else 'purple' if S.get('vis') and j < len(S['vis']) and S['vis'][j] else None)),
        dict(type='array', var='ans', label='ans（已还原出的原数组元素）', h=170, cell=84, index=False),
        dict(type='text', h=70, size=26,
             fn=lambda S: (f"枚举 `higher[0] = nums[{S['i']}] = {S['nums'][S['i']]}`，`2k = {S['nums'][S['i']]} − {S['nums'][0]} = {S['nums'][S['i']] - S['nums'][0]}`" if 'i' in S and 'nums' in S and S['i'] < len(S['nums']) else '')),
    ],
    watch=[('i', 'i', 'yellow'), ('k', 'k', 'cyan'), ('lo', 'lo', 'blue'), ('hi', 'hi', 'pink')],
    captions={
        'nums.sort()': '排序后 `nums[0]` 一定是 `lower[0]`（所有数都是正数，最小的只能是 lower 里的）',
        'for i in range': '假设 `nums[{i}]` 就是 `higher[0]`，试试看能不能还原',
        'if nums[i] == nums[i - 1]': lambda S, B, r: (f'`nums[{S.i}] = nums[{S.i - 1}] = {S.nums[S.i]}`：和上一个一样，得到的 `k` 也一样，已经试过了 → 跳过' if S.nums[S.i] == S.nums[S.i - 1] else f'`{S.nums[S.i]}` ≠ `{S.nums[S.i - 1]}`：新的候选，往下算 `k`'),
        'd = nums[i] - nums[0]': '`higher[0] − lower[0] = 2k = {d}`',
        'if d & 1': lambda S, B, r: (f'`d = {S.d}` 是奇数：`k` 不是整数 → 这个候选不行' if S.d & 1 else f'`d = {S.d}` 是偶数，`k` 是整数，继续'),
        'k = d // 2': '`k = {k}`',
        'vis = [False] * n': '`vis[j]` 标记 `nums[j]` 是否已被分配给 higher',
        'vis[i] = True': '`nums[{i}]` 是 `higher[0]`，打上标记',
        'ans = [(nums[0] + nums[i]) // 2]': '`arr[0] = (lower[0] + higher[0]) / 2` = =={ans[0]}==',
        'lo, hi = 0, i + 1': '`lo` 指 lower，`hi` 指 higher；`hi` 从 `i + 1` 开始',
        'while hi < n': lambda S, B, r: (f'`hi = {S.hi} < n`：还有数没分配，继续配对' if S.hi < len(S.nums) else '`hi` 到头了，本轮结束'),
        15: '`lo` 往后找下一个 lower，先走一步 → {lo}',
        'while vis[lo]': lambda S, B, r: (f'`nums[{S.lo}] = {S.nums[S.lo]}` 已在 higher 里 → 跳过' if S.vis[S.lo] else f'`nums[{S.lo}] = {S.nums[S.lo]}` 不在 higher 里 → 它就是下一个 lower'),
        'while hi < n and nums[hi]': lambda S, B, r: (f'`nums[{S.hi}] − nums[{S.lo}] = {S.nums[S.hi] - S.nums[S.lo]} < 2k = {2 * S.k}`：higher 还不够大，`hi` 右移' if S.hi < len(S.nums) and S.nums[S.hi] - S.nums[S.lo] < 2 * S.k
                                                      else (f'`hi = {S.hi}` 到头了' if S.hi == len(S.nums) else f'`nums[{S.hi}] − nums[{S.lo}] = {S.nums[S.hi] - S.nums[S.lo]}`，不再小于 `2k = {2 * S.k}`，停')),
        'if hi == n or nums[hi]': lambda S, B, r: ('找不到差恰好为 `2k` 的 higher → 这个 `k` 不行，换下一个候选' if S.hi == len(S.nums) or S.nums[S.hi] - S.nums[S.lo] > 2 * S.k
                                                    else f'`nums[{S.hi}] − nums[{S.lo}] = 2k`：配对成功'),
        'vis[hi] = True': '`nums[{hi}]` 归入 higher',
        'ans.append': '这一对 `({nums[lo]}, {nums[hi]})` 对应原数 `({nums[lo]} + {nums[hi]}) / 2` → `ans` = `{ans}`',
        'hi += 1': '`hi` 右移，准备配下一对',
        'if len(ans) == n // 2': lambda S, B, r: (f'`len(ans) = {len(S.ans)} = n/2`：配齐了 → 返回 `{S.ans}`' if len(S.ans) == len(S.nums) // 2 else f'只配出 `{len(S.ans)}` 个，不够 `{len(S.nums) // 2}` 个 → 这个候选失败，换下一个 `i`'),
    },
    cards=dict(
        one_liner='排序后最小的必是 lower[0]，枚举哪个数是 higher[0]',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['原数组 `arr` 与正整数 `k`：`lower[i] = arr[i] − k`，`higher[i] = arr[i] + k`',
                 '给出 `lower` 和 `higher` 混在一起的 `2n` 个数 `nums`，还原 `arr`',
                 '示例：`[2,10,6,4,8,12]` → `[3,7,11]`；本视频：`[12,3,7,1,8,5]` → `[3,5,10]`'],
        quote='将 nums 排序后，lower[0] 必然是 nums[0]。我们可以在 nums 中枚举 higher[0] 的值，从而得到 k = (higher[0] − lower[0]) / 2。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`higher[i] − lower[i] = 2k` 是定值，所以枚举 `higher[0]` 定下 `k`',
              '`vis` 标记出现在 higher 中的数；每轮先跳过 `vis` 找下一个 `lower`，再用 `hi` 找差恰好是 `2k` 的 `higher`',
              '配不齐就换下一个 `higher[0]`，配齐 `n` 对就返回'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python：外层 `for i, n := 1, len(nums); ; i++` 写成 `for i in range(1, n)`（题目保证有解，一定在循环内返回）',
                 '时间 `O(n^2)`（枚举 `2n` 个候选，每个候选双指针 `O(n)`），空间 `O(n)`',
                 '易错：`d` 为奇数或与上一个相同要跳过；`k` 必须是正整数，所以 `d > 0`',
                 '示例里候选 `i = 1`（`k = 1`）会配对失败，`i = 2`（`k = 2`）才成功'],
    ),
)
