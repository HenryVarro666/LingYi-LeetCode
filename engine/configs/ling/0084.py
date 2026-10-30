H = [2, 1, 5, 6, 2, 3, -1]  # 示例 + 代码在末尾补上的 -1


def _hfmt(i):
    return '-1 哨兵' if i == -1 else f'{i}:{H[i]}'


def _active(S):
    """刚弹出 i、算出 left 时，矩形 [left+1, right-1] 有效（只用于画图）"""
    st, i, left, right = S.get('st'), S.get('i'), S.get('left'), S.get('right')
    return (st is not None and isinstance(i, int) and isinstance(left, int) and isinstance(right, int)
            and st and st[-1] == left and left < i < right and i not in st)


def _while_cap(S, B, ret):
    st, hs, h = B.st, B.heights, B.h
    if len(st) <= 1:
        return '栈里只剩哨兵 `-1` → 停止弹栈'
    j = st[-1]
    if hs[j] >= h:
        return f'栈顶 `{j}:{hs[j]}` ≥ `h = {h}` → 栈顶柱子向右扩展不过 `right = {B.right}`，可以结算了'
    return f'栈顶 `{j}:{hs[j]}` < `h = {h}` → 不弹，`right` 入栈'


def _color(S, i, v):
    if v < 0:
        return 'red'
    if _active(S) and i == S['i']:
        return 'yellow'
    if i == S.get('right'):
        return 'pink'
    if i in (S.get('st') or []):
        return 'purple'
    return None


def _dim(S, i, v):
    right, st = S.get('right'), S.get('st') or []
    return right is not None and i < right and i not in st and not (_active(S) and i == S['i'])


def _formula(S):
    if not _active(S):
        return '图例：紫 = 在栈中　粉 = right　黄框 = 正在结算的矩形　灰 = 已结算'
    i, l, r, hs = S['i'], S['left'], S['right'], S['heights']
    ls = l if l >= 0 else f'({l})'
    return f'高 `heights[{i}] = {hs[i]}`，宽 `right − left − 1 = {r} − {ls} − 1 = {r - l - 1}`，面积 =={hs[i] * (r - l - 1)}=='


CONFIG = dict(
    num=84, title='柱状图中最大的矩形', difficulty='Hard', category='栈',
    author='灵茶山艾府', technique='单调栈 · 一次遍历',
    code='''
class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        heights.append(-1)  # 最后大火收汁，用 -1 把栈清空
        # 在栈中只有一个数的时候，栈顶的「下面那个数」是 -1，
        # 对应 left[i] = -1 的情况
        st = [-1]
        ans = 0
        for right, h in enumerate(heights):
            while len(st) > 1 and heights[st[-1]] >= h:
                i = st.pop()  # 矩形的高（的下标）
                left = st[-1]  # 栈顶下面那个数就是 left
                ans = max(ans, heights[i] * (right - left - 1))
            st.append(right)
        return ans
''',
    call='Solution().largestRectangleArea([2, 1, 5, 6, 2, 3])',
    expect=10,
    views=[
        dict(type='bars', var='heights', label='heights', h=380, vmax=7,
             pointers={'right': 'pink', 'left': 'blue'},
             window=(lambda S: S['left'] + 1 if _active(S) else None, lambda S: S['right'] - 1 if _active(S) else None),
             window_color='yellow', color=_color, dim=_dim),
        dict(type='stack', var='st', label='st（下标:高度，底小顶大）', fmt=_hfmt, h=120),
        dict(type='text', fn=_formula, size=27),
    ],
    watch=[('right', 'right', 'pink'), ('h', 'h'), ('i', 'i', 'yellow'), ('left', 'left', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'heights.append(-1)': '末尾补一个 `-1`（==大火收汁==）：它比谁都矮，最后能把栈里的柱子全部弹出结算',
        'st = [-1]': '栈底放哨兵 `-1`：栈里只剩一个数时，栈顶“下面那个数”就是 `-1`，对应 `left = -1`',
        'ans = 0': '`ans = 0`',
        'for right, h in': lambda S, B, ret: (f'枚举 `right = {S.right}`，`h = {S.h}`' if B.get('right') != S.right
                                              else '遍历结束（末尾的 `-1` 已把栈清空）'),
        'while len(st) > 1': _while_cap,
        'i = st.pop()': '弹出 `i = {i}`：以 `heights[{i}] = {heights[i]}` 作为矩形的高，它的右边界就是 `right`',
        'left = st[-1]': '栈底小顶大 → 新栈顶 `left = {left}` 就是 `{i}` 左侧==第一个更矮==的柱子',
        'ans = max': lambda S, B, ret: (f"面积 `{S.heights[S.i]} × ({S.right} − {S.left if S.left >= 0 else f'({S.left})'} − 1)`"
                                        f" = =={S.heights[S.i] * (S.right - S.left - 1)}==，`ans = max({B.ans}, …) = {S.ans}`"),
        'st.append(right)': '`{right}` 入栈，栈从底到顶==高度递增==',
        'return ans': '返回 `ans = {ret}`',
    },
    cards=dict(
        one_liner='弹出栈顶时：右边界是当前下标，左边界是新的栈顶',
        complexity='时间 `O(n)`，空间 `O(min(n, U))`',
        problem=['`heights[i]` 是第 `i` 根柱子的高度，宽度都为 1',
                 '求柱状图中能勾勒出的==最大矩形面积==',
                 '示例：`[2,1,5,6,2,3]` → `10`（高 5、宽 2）'],
        quote='写法二告诉我们，栈顶出栈时，当前下标就是栈顶的 right。如果此刻能顺带求出栈顶的 left，那不就能一步到位？……==栈顶下面的值就是 left==。',
        quote_src='—— 灵茶山艾府题解（写法三：一次遍历）',
        idea=['最大矩形的高一定是某个 `heights[i]`：枚举高，让宽尽量大',
              '宽 = `right − left − 1`，`left/right` 是两侧==最近的更矮==柱子',
              '一步步优化：三次遍历 → 两次 → 一次：弹出时同时得到 `left` 和 `right`'],
        result='最大面积 `10`：以高 5 的柱子为高，宽 2 ✓',
        summary=['时间 `O(n)`：每个下标进出栈各一次',
                 '两个哨兵：栈底 `-1` 处理“左边没有更矮”，末尾 `-1` 把栈清空',
                 '弹栈条件 `>=`：相等的柱子先弹不影响答案（右边那根会算对）',
                 '注意本写法会修改输入 `heights`（追加了 `-1`）'],
    ),
)
