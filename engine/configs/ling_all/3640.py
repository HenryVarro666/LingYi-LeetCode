def _seg(S):
    if 'start' not in S:
        return ''
    s = f"第一段起点 `start={S['start']}`"
    if 'peak' in S:
        s += f"　峰顶 `peak={S['peak']}`"
    if 'bottom' in S:
        s += f"　谷底 `bottom={S['bottom']}`"
    if 'res' in S:
        s += f"　当前和 `res={S['res']}`"
    return s


def _color(S, k, v):
    if 'peak' not in S:
        return None
    p = S['peak']
    if k in (p - 1, p):
        return 'green'
    if 'bottom' in S:
        b = S['bottom']
        if p < k <= b:
            return 'pink'
        if k in (b + 1,):
            return 'cyan'
    return None


CONFIG = dict(
    num=3640, title='三段式数组 II', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='分组循环 · 极大三段式',
    tags=['动态规划', '难度分 2278'],
    code='''
class Solution:
    def maxSumTrionic(self, nums: List[int]) -> int:
        n = len(nums)
        ans = -inf
        i = 0
        while i < n:
            # 第一段
            start = i
            i += 1
            while i < n and nums[i - 1] < nums[i]:
                i += 1
            if i == start + 1:  # 第一段至少要有两个数
                continue

            # 第二段
            peak = i - 1
            res = nums[peak - 1] + nums[peak]  # 第一段的最后两个数必选
            while i < n and nums[i - 1] > nums[i]:
                res += nums[i]  # 第二段的所有元素必选
                i += 1
            if i == peak + 1 or i == n or nums[i - 1] == nums[i]:  # 第二段至少要有两个数，第三段至少要有两个数
                continue

            # 第三段
            bottom = i - 1
            res += nums[i]  # 第三段的前两个数必选（第一个数在上面的循环中加了）
            # 从第三段的第三个数往右，计算最大元素和
            max_s = s = 0
            i += 1
            while i < n and nums[i - 1] < nums[i]:
                s += nums[i]
                max_s = max(max_s, s)
                i += 1
            res += max_s

            # 从第一段的倒数第三个数往左，计算最大元素和
            max_s = s = 0
            for j in range(peak - 2, start - 1, -1):
                s += nums[j]
                max_s = max(max_s, s)
            res += max_s
            ans = max(ans, res)

            i = bottom  # 第三段的起点也是下一个极大三段式子数组的第一段的起点
        return ans
''',
    call='Solution().maxSumTrionic([-1,2,4,1,0,3,5,2])',
    expect=15,
    views=[
        dict(type='array', var='nums', label='nums', h=300, pointers={'i': 'blue'},
             window=('start', 'i'), color=_color,
             dim=lambda S, k, v: 'start' in S and k < S['start']),
        dict(type='text', fn=_seg, size=26, h=100),
    ],
    watch=[('i', 'i', 'blue'), 'start', 'peak', 'bottom', 'res', ('ans', 'ans', 'green')],
    max_steps=90,
    skip=['n = len(nums)', 'ans = -inf'],
    captions={
        'start = i': '开始找一个极大三段式：第一段从 `start = {start}` 起（外层循环：准备工作）',
        10: lambda S, B, ret: (f"`{S['nums'][S['i']-1]} < {S['nums'][S['i']]}` 仍严格递增，第一段继续往右" if S['i'] < len(S['nums']) and S['nums'][S['i']-1] < S['nums'][S['i']] else f"第一段到此为止（`i={S['i']}`）：再往右不是严格递增了"),
        12: lambda S, B, ret: ("第一段只有一个数，不满足至少两个数 → 从 `i` 重新开始" if S['i'] == S['start'] + 1 else f"第一段 `[{S['start']}, {S['i']-1}]` 至少有两个数，通过"),
        'peak = i - 1': '峰顶 `peak = {peak}`（第一、二段共享）',
        'res = nums[peak - 1]': '第一段最后两个数必选：`res = {nums[peak-1]} + {nums[peak]} = {res}`',
        18: lambda S, B, ret: (f"`{S['nums'][S['i']-1]} > {S['nums'][S['i']]}` 严格递减，第二段继续，元素必选" if S['i'] < len(S['nums']) and S['nums'][S['i']-1] > S['nums'][S['i']] else f"第二段到此为止（`i={S['i']}`）"),
        30: lambda S, B, ret: (f"`{S['nums'][S['i']-1]} < {S['nums'][S['i']]}` 第三段继续递增，从第三个数起可选" if S['i'] < len(S['nums']) and S['nums'][S['i']-1] < S['nums'][S['i']] else f"第三段到此为止（`i={S['i']}`）"),
        'res += nums[i]  # 第二段': '第二段的所有元素必选，`res += {nums[i]}` → `{res}`',
        'if i == peak + 1': lambda S, B, ret: ("第二段或第三段不足两个数 → 本段无效，重新开始" if S['i'] == S['peak'] + 1 or S['i'] == len(S['nums']) or S['nums'][S['i']-1] == S['nums'][S['i']] else "第二、三段都有至少两个数，是个合法的三段式"),
        'bottom = i - 1': '谷底 `bottom = {bottom}`（第二、三段共享）',
        'res += nums[i]  # 第三段': '第三段第二个数必选：`res += nums[{i}] = {nums[i]}` → `{res}`',
        28: '从第三段的第三个数往右延伸：累加 `s`，记录最大前缀和 `max_s`（可以一个都不选，所以从 0 起）',
        37: '从第一段倒数第三个数往左延伸：同样累加，取最大值（可以不选）',
        'max_s = max(max_s, s)': '`s = {s}`，`max_s = {max_s}`：延伸只取到和最大的位置',
        34: '右边最多再多加 `{max_s}` → `res = {res}`',
        41: '左边最多再多加 `{max_s}` → `res = {res}`',
        'ans = max(ans, res)': '这个极大三段式的最大和是 `{res}`，`ans = max({B.ans}, {res}) = {ans}`',
        'i = bottom': '第三段的起点（谷底）也是下一个三段式的第一段起点，`i` 退回 `{bottom}`',
        'return ans': '没有更多段了，返回 `{ans}`',
    },
    cards=dict(
        one_liner='把数组按「增—减—增」切成极大三段，每段两侧再贪心延伸',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['三段式子数组：先严格递增，再严格递减，再严格递增，每段 ==至少两个数==',
                 '在所有三段式子数组里，求元素和最大的那个',
                 '示例：`[-1,2,4,1,0,3,5,2]` → 取 `[2,4,1,0,3,5]`，和 `15`（左边的 `-1` 加进来会变小，不要）'],
        quote='峰顶 peak 是第一二段共享的，谷底 bottom 是第二三段共享的。必须包含从 peak-1 到 bottom+1 的所有元素，再加上往左、往右的最大元素和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['分组循环：外层记起点，内层依次走完「增、减、增」三段',
              '必选部分：`peak-1` 到 `bottom+1`；两端可选延伸，取最大累加和（没有则为 0）',
              '第三段起点也是下一个三段式的起点，所以结束后 `i = bottom`'],
        summary=['时间 `O(n)`，空间 `O(1)`；同一元素最多被两个相邻的极大三段式各遍历一次',
                 '易错点：每段至少两个数；峰顶、谷底是相邻两段共享的元素，不要重复加',
                 '易错点：处理完要 `i = bottom` 回退，否则会漏掉以第三段起点开始的下一个三段式',
                 '题解还给了状态机 DP（`f1, f2, f3` 三个状态滚动）写法'],
    ),
)
