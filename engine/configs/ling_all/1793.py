CONFIG = dict(
    num=1793, title='好子数组的最大分数', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='从 k 出发背向双指针（谁大动谁）',
    tags=['滑动窗口与双指针', '单调栈', '难度分 1946'],
    code='''
class Solution:
    def maximumScore(self, nums: List[int], k: int) -> int:
        n = len(nums)
        ans = min_h = nums[k]
        i = j = k
        for _ in range(n - 1):
            if j == n - 1 or i and nums[i - 1] > nums[j + 1]:
                i -= 1
                min_h = min(min_h, nums[i])
            else:
                j += 1
                min_h = min(min_h, nums[j])
            ans = max(ans, min_h * (j - i + 1))
        return ans
''',
    call='Solution().maximumScore([2,9,7,8,8,1,3], 3)',
    expect=28,
    views=[
        dict(type='text', fn=lambda S: (f"窗口 `[{S['i']}, {S['j']}]`：最小值 `{S['min_h']}` × 长度 `{S['j']-S['i']+1}` = =={S['min_h']*(S['j']-S['i']+1)}==" if 'min_h' in S and 'j' in S else '')),
        dict(type='bars', var='nums', h=420, pointers={'i': 'blue', 'j': 'pink'}, window=('i', 'j'),
             dim=lambda S, i, v: 'j' in S and not (S['i'] <= i <= S['j']),
             color=lambda S, i, v: ('blue' if i == S['i'] else 'pink' if i == S['j'] else None) if 'j' in S else None),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('min_h', 'min_h', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'ans = min_h = nums[k]': '矩形必须包含下标 `k`，先只取 `nums[k] = {nums[k]}`：高 `{min_h}`、宽 1',
        'i = j = k': '双指针都从 `k` 出发，向两侧扩张（类似第 11 题，只是方向相反）',
        'for _ in range': '每次扩张一格，最多扩张 `n - 1 = {n - 1}` 次',
        'if j == n - 1': lambda S, B, r: (f'右端已到头 → 只能向左扩张' if S.j == S.n - 1 else
                                          (f'比较两侧：`nums[{S.i-1}] = {S.nums[S.i-1]}` 对 `nums[{S.j+1}] = {S.nums[S.j+1]}` → '
                                           + ('左边更大，向左扩' if S.nums[S.i-1] > S.nums[S.j+1] else '右边不小于左边，向右扩') if S.i else '左端已到头 → 只能向右扩张')),
        'i -= 1': '谁大扩谁，让最小值==减少得更慢==：`i` → {i}',
        'j += 1': '`j` → {j}',
        'min_h = min(min_h, nums[i])': '新纳入 `nums[{i}] = {nums[i]}`，最小值 `{B.min_h}` → =={min_h}==',
        'min_h = min(min_h, nums[j])': '新纳入 `nums[{j}] = {nums[j]}`，最小值 `{B.min_h}` → =={min_h}==',
        'ans = max(ans': '分数 = `{min_h} × {j - i + 1}` = {min_h * (j - i + 1)}，`ans = max({B.ans}, ...)` = =={ans}==',
        'return ans': '最大好子数组分数为 =={ret}==',
    },
    cards=dict(
        one_liner='从 k 向两边扩，每次扩较大的那一侧',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['子数组分数 = `最小值 × 长度`，好子数组必须包含下标 `k`',
                 '求好子数组的最大分数',
                 '示例：`[1,4,3,7,4,5], k=3` → `15`；本视频：`[2,9,7,8,8,1,3], k=3` → `28`'],
        quote='比较 x=nums[i-1] 和 y=nums[j+1] 的大小，谁大就移动谁（一样大移动哪个都可以），让最小值减少得更慢。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['本质是 84 题最大矩形，多了「必须含下标 `k`」',
              '从 `i=j=k` 出发，往两边扩：先吃掉更大的一侧，==最小值下降最慢==',
              '定理：这样扩张一定会恰好经过最优矩形的左右边界'],
        after=[dict(heading='另一种写法：单调栈', lines=['方法一：和 84 题一样，用单调栈求每个高度的左右第一个更小元素',
                                                       '宽度 `right-left-1`，再要求 `left < k < right`',
                                                       '本视频演示的是方法二的双指针'])],
        summary=['时间 `O(n)`，空间 `O(1)`（单调栈写法空间 `O(n)`）',
                 '循环正好 `n-1` 次：每次扩一格，直到覆盖整个数组',
                 '易错：`j == n-1` 要放在前面，否则 `nums[j+1]` 越界；`i` 为 0 时只能右扩',
                 '每扩一格都要用新的 `min_h` 更新答案'],
    ),
)
