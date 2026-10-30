def _txt(S):
    if 'st' not in S or 'arr' not in S:
        return ''
    if 'i' in S and S.get('_line') == 7:
        a = S['arr']
        i, r, l = S['i'], S['r'], S['st'][-1]
        return f"`arr[{i}] = {a[i]}`：左 `{i - l}` 种 × 右 `{r - i}` 种 → 贡献 `{a[i]} × {i - l} × {r - i}` = =={a[i] * (i - l) * (r - i)}=="
    return '`arr[i]` 的贡献 = `arr[i] × (i − 左边界) × (右边界 − i)`'


CONFIG = dict(
    num=907, title='子数组的最小值之和', difficulty='Medium', category='单调栈',
    author='灵茶山艾府', technique='单调栈 · 贡献法（一次遍历）',
    tags=['难度分 1976'],
    code='''
class Solution:
    def sumSubarrayMins(self, arr: List[int]) -> int:
        arr.append(-1)
        ans, st = 0, [-1]  # 哨兵
        for r, x in enumerate(arr):
            # 也可以 while arr[st[-1]] > x，效率略高一点
            while len(st) > 1 and arr[st[-1]] >= x:
                i = st.pop()
                ans += arr[i] * (i - st[-1]) * (r - i)  # 累加贡献
            st.append(r)
        return ans % (10 ** 9 + 7)
''',
    call='Solution().sumSubarrayMins([3,1,2,4])',
    expect=17,
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var='arr', label='arr（末尾追加的 -1 是哨兵，保证最后清空栈）', pointers={'r': 'blue'}, cell=90, h=170,
             color=lambda S, i, v: 'yellow' if S.get('_line') == 7 and S.get('i') == i else None),
        dict(type='stack', var=lambda S: ['哨兵' if k < 0 else f"{k}:{S['arr'][k]}" for k in S['st']] if 'st' in S else None,
             label='st（存下标：值；从底到顶递增）', h=280),
    ],
    watch=[('r', 'r', 'blue'), ('x', 'x'), ('ans', 'ans', 'green')],
    captions={
        'arr.append(-1)': '末尾加一个 `-1`：它比所有数都小，遍历到它时会把栈里的元素全部弹出',
        'ans, st = 0': '`st` 存下标，栈底放哨兵 `-1`，这样「栈顶下面那个数」就是左边界，不用判空',
        'while len(st) > 1': lambda S, B, r: (
            f'栈顶 `arr[{B.st[-1]}] = {B.arr[B.st[-1]]}` ≥ `x = {B.x}` → ==`r = {B.r}` 就是它的右边界==，弹出并结算'
            if len(B.st) > 1 and B.arr[B.st[-1]] >= B.x
            else '栈里只剩哨兵，或栈顶 < x：没有更多可弹的了，`x` 入栈'),
        'i = st.pop()': '弹出 `i = {i}`，弹出后的新栈顶 `{st[-1]}` 就是它的==左边界==',
        'ans += arr[i]': '左端点 `{i - st[-1]}` 种、右端点 `{r - i}` 种 → `{arr[i]} × {i - st[-1]} × {r - i}`，`ans` = =={ans}==',
        'st.append(r)': '`{r}` 入栈，栈内下标对应的值保持递增',
        'return ans': '`{ans}` 对 `10^9 + 7` 取模 = ==`{ret}`==',
    },
    cards=dict(
        one_liner='换个视角：算每个数是多少个子数组的最小值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['对 `arr` 的所有连续子数组，求最小值之和，结果对 `10^9 + 7` 取模',
                 '示例：`[3,1,2,4]` → `17`',
                 '子数组最小值依次为 3,1,2,4,1,1,2,1,1,1'],
        quote='不妨换个视角，对每个数，算出它是哪些子数组的最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`arr[i]` 的边界是左右两侧最近的更小值，开区间 `(L, R)`',
              '左端点 `i - L` 种，右端点 `R - i` 种，贡献 `arr[i] × (i-L) × (R-i)`',
              '有重复值时右边界取 ≤，避免同一个子数组被算两次；单调栈出栈时一次得到左右边界'],
        summary=['时间 `O(n)`：每个下标入栈出栈各一次',
                 '==重复元素==：弹出条件用 `>=`，一边严格小于、一边小于等于',
                 '最后加 `-1` 保证栈被清空；哨兵 `-1` 省去判空',
                 '灵神还给出了三次遍历、两次遍历的版本，本视频演示一次遍历版'],
    ),
)
