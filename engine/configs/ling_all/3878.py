def _bin(v):
    return format(v, 'b')


def _info(S):
    if 'ans' in S:
        i = S.get('i')
        if i is not None and 'right' in S and S.get('_line', 0) >= 28:
            return f"`nums[{i}]` 当 OR 值：左端点 {i - S['left'][i]} 种 × 右端点 {S['right'] - i} 种"
        return '第二趟（从右往左）：算右边界，同时累加贡献；相等的数不能跨过，防重复'
    if 'st' in S and 'left' in S:
        return '第一趟（从左往右）：弹出 x 的子集，剩下的栈顶就不是 x 的子集 → 它是左边界'
    return ''


CONFIG = dict(
    num=3878, title='统计好子数组', difficulty='Hard', category='单调栈',
    author='灵茶山艾府', technique='单调栈 · 把 y<=x 换成子集判断',
    tags=['灵神题单', '单调栈', '难度分 2230'],
    code='''
class Solution:
    def countGoodSubarrays(self, nums: List[int]) -> int:
        n = len(nums)
        left = [0] * n
        st = [-1]  # 哨兵
        for i, x in enumerate(nums):
            while len(st) > 1 and (nums[st[-1]] | x) == x:
                st.pop()
            left[i] = st[-1]  # nums[left[i]] 不是 x 的子集
            st.append(i)

        st = [n]
        ans = 0
        for i in range(n - 1, -1, -1):
            x = nums[i]
            # 比如 nums = [...,1,...,1,...]，我们规定，包含左边的 1 的子数组，不能包含右边的 1，从而避免重复统计子数组
            # 注：包含右边的 1 的子数组，可以包含左边的 1
            while len(st) > 1 and nums[st[-1]] != x and (nums[st[-1]] | x) == x:
                st.pop()
            right = st[-1]  # nums[right] 不是 x 的子集
            st.append(i)

            # 子数组左端点可以从 left[i]+1 到 i，一共 i-left[i] 个
            # 子数组右端点可以从 i 到 right-1，一共 right-i 个
            ans += (i - left[i]) * (right - i)

        return ans
''',
    call='Solution().countGoodSubarrays([1, 3, 1, 1])',
    expect=10,
    skip=['n = len(nums)', 'left = [0] * n', 'ans = 0'],
    views=[
        dict(type='array', var='nums', label='nums', pointers={'i': 'blue'}, cell=100, h=210,
             color=lambda S, i, v: 'blue' if S.get('i') == i else None),
        dict(type='stack', var='st', label='st（下标；第一个是哨兵）', h=130, font=26),
        dict(type='array', var='left', label='left：左边第一个不是 x 子集的下标', cell=80, h=130, index=False),
        dict(type='text', fn=_info, size=24, h=60),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'yellow'), ('right', 'right', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'st = [-1]': '栈底放哨兵 `-1`：表示「左边没有墙」',
        'while len(st) > 1 and (nums[st[-1]] | x) == x': lambda S, B, r: (
            f'`{S.nums[S.st[-1]]} | {S.x} = {S.nums[S.st[-1]] | S.x}` == x：栈顶是 x 的子集，包含它 OR 值不变 → 弹出'
            if len(S.st) > 1 and (S.nums[S.st[-1]] | S.x) == S.x
            else '栈顶不是 x 的子集（或只剩哨兵）：包含它 OR 值就会变大 → 它就是墙'),
        'left[i] = st[-1]': '`left[{i}] = {st[-1]}`：子数组左端点只能在 `{st[-1] + 1}` 到 `{i}`',
        'st.append(i)': '`{i}` 入栈',
        'st = [n]': '第二趟从右往左，哨兵换成 `n`：右边没有墙',
        'x = nums[i]': '枚举 `nums[{i}] = {x}` 作为子数组的 OR 值',
        'while len(st) > 1 and nums[st[-1]] != x': lambda S, B, r: (
            f'栈顶 `{S.nums[S.st[-1]]}` 是 `{S.x}` 的子集且不等于 x → 弹出'
            if len(S.st) > 1 and S.nums[S.st[-1]] != S.x and (S.nums[S.st[-1]] | S.x) == S.x
            else ('栈顶和 x ==相等==：规定包含左边的 x 不能含右边的 x → 不弹，当墙' if len(S.st) > 1 and S.nums[S.st[-1]] == S.x
                  else '栈顶不是 x 的子集（或只剩哨兵）→ 它就是右边的墙')),
        'right = st[-1]': '`right = {right}`：子数组右端点只能在 `{i}` 到 `{right - 1}`',
        'ans += ': '`nums[{i}]` 贡献 `({i} − {left[i]}) × ({right} − {i})` = =={(i - left[i]) * (right - i)}==，累计 =={ans}==',
        'return ans': '好子数组一共 =={ret}== 个',
    },
    cards=dict(
        one_liner='OR 值一定在子数组里 → 枚举谁是 OR 值，用单调栈数子数组',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['子数组的 ==按位或== 等于子数组里某个元素，就叫「好」子数组，数一数有多少个',
                 '示例：`[4,2,3]` → `4`；`[1,3,1]` → `6`',
                 '本视频用 `[1,3,1,1]`，含重复数字'],
        quote='把常规单调栈中的 `y <= x` 替换成 `(y | x) == x` 即可。',
        quote_src='—— 灵茶山艾府题解',
        idea=['子数组的每个数都是 OR 值的子集：OR 值为 `x` 时，里面的数都满足 `(y|x)==x`',
              '「比 x 大」换成「不是 x 的子集」，正是常规单调栈的集合版',
              '重复的 x：包含左边的 x 的子数组，不能再含右边的 x，避免重复统计'],
        summary=['时间 `O(n)`，空间 `O(n)`；对照 907 题，贡献法 + 单调栈',
                 '易错：只在右边那趟加 `nums[st[-1]] != x`，左右不对称才能去重',
                 '另一种写法：LogTrick，维护以 i 结尾的 OR 值分段 + `last[x]`，`O(n log U)`',
                 '前置题：907 子数组的最小值之和'],
    ),
)
