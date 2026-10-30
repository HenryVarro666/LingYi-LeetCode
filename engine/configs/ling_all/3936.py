CONFIG = dict(
    num=3936, title='将 0 移到末尾的最少交换次数', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='相向双指针 · 缩小子问题',
    tags=['难度分 1346'],
    code='''
class Solution:
    def minimumSwaps(self, nums: list[int]) -> int:
        ans = 0
        l, r = 0, len(nums) - 1
        while l < r:
            if nums[l] != 0:
                l += 1
            elif nums[r] == 0:
                r -= 1
            else:
                # 交换 nums[l] 和 nums[r]
                ans += 1
                l += 1
                r -= 1
        return ans
''',
    call='Solution().minimumSwaps([0,1,0,3,12])',
    expect=2,
    views=[
        dict(type='text', fn=lambda S: (f"剩余子数组 `[{S['l']}, {S['r']}]`，已交换 `{S['ans']}` 次" if 'r' in S else ''), size=30),
        dict(type='array', var='nums', pointers={'l': 'blue', 'r': 'pink'}, h=300,
             window=('l', 'r'),
             dim=lambda S, i, v: 'r' in S and not (S['l'] <= i <= S['r']),
             color=lambda S, i, v: ('blue' if i == S['l'] else 'pink' if i == S['r'] else None) if 'r' in S else None),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'l, r =': '子数组 `[l, r]` = `[0, {r}]`，一开始是整个数组',
        'while l < r': lambda S, B, r: (f"`l = {S.l} < r = {S.r}`：子数组还有 ≥ 2 个数 → 继续" if S.l < S.r else f"`l = {S.l} >= r = {S.r}`：只剩 ≤ 1 个数，结束"),
        'if nums[l] != 0': lambda S, B, r: (f"`nums[{S.l}] = {S.nums[S.l]}` 非 0：已经在前面，无需交换 → 缩小子问题" if S.nums[S.l] != 0 else f"`nums[{S.l}] = 0`：左端是 0，看右端"),
        'l += 1': '`l` → {l}',
        'elif nums[r] == 0': lambda S, B, r: (f"`nums[{S.r}] = 0`：已经在末尾，无需交换 → `r` 左移" if S.nums[S.r] == 0 else f"`nums[{S.r}] = {S.nums[S.r]}` 非 0：左端 0、右端非 0，必须换"),
        'r -= 1': '`r` → {r}',
        'ans += 1': '左 0 右非 0：必须交换一次，`ans` → =={ans}==，两端都就位，`l`、`r` 同时向内缩',
        'return ans': '最少交换 `{ans}` 次',
    },
    cards=dict(
        one_liner='左端非 0、右端是 0 都不用换，缩小范围；左 0 右非 0 才换一次',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每步可交换任意两个下标的元素，求把所有 0 移到数组末尾的最少交换次数',
                 '示例：`[0,1,0,3,12]` → `2`',
                 '示例：`[1,2,0]` → `0`（已经满足）'],
        quote='如果 nums[0]≠0，无需交换，问题变成剩余 n−1 个数的子问题。如果 nums[n−1]=0，无需交换，问题变成剩余 n−1 个数的子问题。',
        quote_src='—— 灵茶山艾府题解 方法二',
        idea=['`[l, r]` 表示还没处理的子数组',
              '左端非 0 或右端是 0：这端已就位，直接丢掉',
              '左 0 且右非 0：必须交换，各自就位，丢掉两端'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '方法一（两次遍历）：`cnt` 是非零个数，答案 = 前 `cnt` 个数里 0 的个数',
                 '方法二（本视频）：相向双指针，每次至少缩小一端',
                 '交换只是计数，并不真的改 `nums`'],
    ),
)
