def _win(S):
    if 'right' not in S or 'left' not in S:
        return '先算出子数组要凑出的和 `target = sum(nums) − x`' if 'target' not in S else f"找和恰好为 `target = {S['target']}` 的==最长==子数组"
    l, r = S['left'], S['right']
    sub = S['nums'][l:r + 1]
    rel = '>' if S['s'] > S['target'] else ('=' if S['s'] == S['target'] else '<')
    return f"窗口 `nums[{l}..{r}]` 和 `s = {S['s']}` {rel} `target = {S['target']}`" + (
        f"，长度 =={r - l + 1}==" if rel == '=' else '')


def _while(S, B, ret):
    if S.s > S.target:
        return f'`s = {S.s} > target = {S.target}`：和太大 → ==缩小窗口=='
    return f'`s = {S.s} ≤ target = {S.target}`：不用缩小'


def _if(S, B, ret):
    if S.s == S.target:
        return f'`s == target = {S.target}`：找到一个合法子数组，长度 `{S.right - S.left + 1}`'
    return f'`s = {S.s} ≠ {S.target}`：不是合法子数组'


CONFIG = dict(
    num=1658, title='将 x 减到 0 的最小操作数', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='逆向思维 + 滑动窗口',
    tags=['labuladong', '灵神题单·滑动窗口与双指针', '难度分 1817'],
    code='''
class Solution:
    def minOperations(self, nums: List[int], x: int) -> int:
        target = sum(nums) - x
        if target < 0:
            return -1  # 全部移除也无法满足要求

        ans = -1
        s = left = 0
        for right, num in enumerate(nums):
            s += num
            while s > target:
                s -= nums[left]
                left += 1  # 缩小子数组长度
            if s == target:
                ans = max(ans, right - left + 1)

        return -1 if ans < 0 else len(nums) - ans
''',
    call='Solution().minOperations([3,2,20,1,1,3], 10)',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums（框 = 保留的子数组，灰 = 被移除的两端）', cell=110, h=260,
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'),
             dim=lambda S, i, v: 'right' in S and 'left' in S and not (S['left'] <= i <= S['right'])),
        dict(type='text', fn=_win, size=28, h=90),
        dict(type='text', fn=lambda S: (f"目前最长保留 `ans = {S['ans']}` 个 → 最少操作 ==`{len(S['nums']) - S['ans']}`==" if S.get('ans', -1) >= 0
                                        else '还没找到和为 target 的子数组（`ans = -1`）') if 'ans' in S else '', size=26, h=90),
    ],
    watch=[('target', 'target', 'yellow'), ('left', 'left', 'blue'), ('right', 'right', 'pink'),
           ('s', 's', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'target = sum(nums) - x': '移除的和是 `x` → 剩下的子数组和 = `{sum(nums)} − {x}` = =={target}==',
        'if target < 0': '`target = {target}` 不小于 0，有希望',
        'ans = -1': '`ans = -1`：==子数组长度可以是 0==，所以不能初始化为 0',
        's = left = 0': '窗口和 `s`、左端点 `left` 都从 0 开始',
        'for right, num in enumerate(nums)': lambda S, B, r: ('右端点枚举完毕' if B.get('right') == S.right
                                                               else f'枚举右端点 `right = {S.right}`，`num = {S.num}`'),
        's += num': '`{num}` 进入窗口，`s = {s}`',
        'while s > target': _while,
        's -= nums[left]': '移出 `nums[{left}] = {nums[left]}`，`s = {s}`',
        'left += 1': '左端点右移 → `left = {left}`',
        'if s == target': _if,
        'ans = max(ans': '`ans = max({B.ans}, {right - left + 1}) = {ans}`：保留的越长，移除的越少',
        'return -1 if ans < 0': '最长保留 `{ans}` 个 → 最少操作 `{len(nums)} − {ans}` = =={ret}==',
    },
    cards=dict(
        one_liner='移除两端 = 保留中间：找和为 sum − x 的最长子数组',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次从 `nums` 的最左或最右移除一个数，并从 `x` 中减去它',
                 '求把 `x` ==恰好==减到 0 的最小操作数，做不到返回 `-1`',
                 '示例：`nums = [1,1,4,2,3], x = 5` → `2`',
                 '本视频：`nums = [3,2,20,1,1,3], x = 10` → `5`'],
        quote='移除的是 nums 最左边或最右边的元素，那么剩下的元素是什么？是 nums 的连续子数组。所以剩余的元素和 = s−x。',
        quote_src='—— 灵茶山艾府题解',
        idea=['问题变成：找==最长==的子数组，元素和恰好等于 `sum(nums) − x`',
              '没有负数 → 和随窗口单调变化，可以用不定长滑动窗口',
              '答案 = `n − 最长子数组长度`'],
        summary=['时间 `O(n)`：`left` 最多右移 `n` 次；空间 `O(1)`',
                 '易错：`ans` 初始化为 `-1`，因为子数组长度可以是 0（全部移除）',
                 '`target < 0` 时直接返回 `-1`，否则窗口会越界',
                 '方法二：正向双指针，枚举前缀、维护后缀，和不超过 `x`，写起来稍麻烦'],
    ),
)
