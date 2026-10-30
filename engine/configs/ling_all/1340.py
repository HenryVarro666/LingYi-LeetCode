ARR = [4, 2, 6, 3, 5]
D = 2


def _txt(S):
    if 'right' not in S or S.get('_line', 0) < 20:
        return f'`d = {D}`：先用单调栈求每个数左右最近的更大数，再倒着记忆化搜索'
    return f'`left = {S["left"]}`    `right = {S["right"]}`'


def _col(S, i, v):
    cur = S.get('i')
    if cur is None or cur < 0:
        return None
    return 'blue' if i == cur else None


def _pick(S, B, ret):
    i = S.i
    return (f'`i = {i}`：左边最近更大是 `left[{i}] = {S.left[i]}`，右边是 `right[{i}] = {S.right[i]}`；'
            f'答案 = 两边较大者 + 1')


CONFIG = dict(
    num=1340, title='跳跃游戏 V', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='倒着跳：单调栈 + 记忆化搜索',
    tags=['灵神题单·单调栈', '灵神题单·动态规划', '难度分 1866'],
    code='''
class Solution:
    def maxJumps(self, arr: List[int], d: int) -> int:
        n = len(arr)

        # 计算 arr[i] 左边最近的更大元素 arr[left[i]]
        left = [0] * n
        st = []
        for i, x in enumerate(arr):
            while st and arr[st[-1]] <= x:
                st.pop()
            # 如果左边没有更大的数，或者跳跃距离超过 d，都标记为 -1
            left[i] = st[-1] if st and i - st[-1] <= d else -1
            st.append(i)

        # 计算 arr[i] 右边最近的更大元素 arr[right[i]]
        right = [0] * n
        st.clear()
        for i in range(n - 1, -1, -1):
            x = arr[i]
            while st and arr[st[-1]] <= x:
                st.pop()
            # 如果右边没有更大的数，或者跳跃距离超过 d，都标记为 -1
            right[i] = st[-1] if st and st[-1] - i <= d else -1
            st.append(i)

        @cache  # 缓存装饰器，避免重复计算 dfs（一行代码实现记忆化）
        def dfs(i: int) -> int:
            if i < 0:  # 没有更大的数，或者跳跃距离超过 d
                return 0
            # 往左跳 vs 往右跳
            return max(dfs(left[i]), dfs(right[i])) + 1

        # 枚举终点，倒着跳
        return max(dfs(i) for i in range(n))
''',
    call=f'Solution().maxJumps({ARR!r}, {D})',
    expect=3,
    views=[
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='bars', var='arr', label='arr（蓝 = 当前 i，黄 = 栈里的下标）', h=230, pointers={'i': 'blue'},
             color=lambda S, i, v: 'yellow' if i in S.get('st', ()) and i != S.get('i') else None),
        dict(type='stack', var='st', label='st（下标，底大顶小）', fmt=lambda i: f'{i}:{ARR[i]}', h=110),
        dict(type='calls', h=170),
    ],
    watch=[('i', 'i', 'blue'), ('st', 'st', 'purple'), ('left', 'left', 'cyan'), ('right', 'right', 'orange')],
    max_steps=110,
    skip=['st.append(i)', 'x = arr[i]', 'st.clear()', 'st = []'],
    captions={
        'left = [0]': '`left[i]`：左边最近的更大数的下标，-1 表示跳不到',
        'while st and arr[st[-1]] <= x': lambda S, B, r: ('栈空，停止弹出' if not S.st else
            f'栈顶 `arr[{S.st[-1]}] = {S.arr[S.st[-1]]}` ≤ `x = {S.x}`？' + ('是：它不比 x 大，不可能是 x 的「更大元素」，弹出' if S.arr[S.st[-1]] <= S.x else '否：栈顶比 x 大，它就是最近的更大数')),
        'left[i] = st[-1]': lambda S, B, r: (f'`left[{S.i}] = {S.left[S.i]}`' + ('：没有更大的数，或距离超过 `d`' if S.left[S.i] < 0 else f'：距离 `{S.i - S.left[S.i]}` ≤ `d = {D}`，能跳')),
        'st.pop()': '`arr[{B.st[-1]}] = {arr[B.st[-1]]}` 弹出：它不比 `x` 大，对 x 右边的数也没用',
        'right = [0]': '`right[i]`：右边最近的更大数的下标，从右往左扫',
        'right[i] = st[-1]': lambda S, B, r: (f'`right[{S.i}] = {S.right[S.i]}`' + ('：没有更大的数，或距离超过 `d`' if S.right[S.i] < 0 else f'：距离 `{S.right[S.i] - S.i}` ≤ `d = {D}`，能跳')),
        'def dfs': '`dfs(i)`：==以 i 为终点==，倒着跳，最多经过多少个下标',
        'if i < 0': lambda S, B, r: ('`i < 0`：没有可来的位置，返回 0' if S.i < 0 else '`i` 有效，继续往下算'),
        'return 0': '该方向走不通：返回 `0`',
        'return max(dfs(left': '`dfs({B.i})`：两个来源 `left[{B.i}] = {B.left[B.i]}`、`right[{B.i}] = {B.right[B.i]}` 各递归一次，取较大者再 +1',
    },
    cards=dict(
        one_liner='倒着跳：每个数只会从左右最近的更大数跳过来',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['从下标 `i` 一次最多跳 `d` 格，只能跳到更矮的柱子，且中途的柱子都要比 `arr[i]` 矮',
                 '可以从任意下标出发，求最多能访问多少个下标',
                 '示例：`arr = [4,2,6,3,5]`，`d = 2` → `3`'],
        quote='一般地，跳到左右最近的更大元素是最优的。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['倒着看：到达 `j` 的前一步 `i`，`i..j` 之间的数都要小于 `arr[j]`',
              '`7 → 9 → 13` 一定比 `7 → 13` 更优：近的更大数更好',
              '所以每个位置只剩两个来源：左右最近更大数；单调栈 `O(n)` 求出，再记忆化搜索'],
        after=[dict(heading='另一种写法：正着跳（方法一）',
                    lines=['`dfs(i)`：枚举左右 `d` 格内能跳到的位置，遇到不矮的就停',
                           '同样加 `@cache` 记忆化，时间 `O(nd)`',
                           '本视频演示的是更快的倒着跳写法'])],
        summary=['时间 `O(n)`：单调栈每个下标进出各一次，记忆化每个状态一次 `O(1)`',
                 '弹栈条件是 `<=`：相等的也不能越过，所以要弹出',
                 '`-1` 表示跳不到（没有更大数或超过 `d`），`dfs(-1) = 0`',
                 '终点要枚举所有下标，答案取最大',
                 '同类：动态规划题单「专题：跳跃游戏」'],
    ),
)
