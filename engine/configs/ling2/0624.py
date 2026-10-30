ARR = [[3, 5], [1, 4, 9], [2, 6], [4, 7]]


def _cur(S):
    a = S.get('a')
    if a is None or 'mn' not in S:
        return -1
    return ARR.index(a) if a in ARR else -1


def _color(S, i, j, v):
    c = _cur(S)
    row = S['arrays'][i]
    if i == c:
        if j == 0:
            return 'cyan'
        if j == len(row) - 1:
            return 'orange'
        return None
    if i < c:
        firsts = [ARR[k][0] for k in range(c)]
        lasts = [ARR[k][-1] for k in range(c)]
        if j == 0 and v == min(firsts) and firsts.index(v) == i:
            return 'blue'
        if j == len(row) - 1 and v == max(lasts) and lasts.index(v) == i:
            return 'pink'
    return None


def _formula(S, B):
    if S.get('_line') == 6 and 'a' in S:
        a, mn, mx = S['a'], B['mn'], B['mx']
        f = lambda x: '∞' if x == float('inf') else ('-∞' if x == float('-inf') else str(x))
        d1 = a[-1] - mn
        d2 = mx - a[0]
        return (f"`ans = max({B['ans']}, {a[-1]} − {f(mn)}, {f(mx)} − {a[0]})` "
                f"= `max({B['ans']}, {f(d1)}, {f(d2)})` = =={S['ans']}==")
    if 'a' in S:
        return f"当前数组 `a = {S['a']}`：`a[0]` 是最小值，`a[-1]` 是最大值"
    return '只看每个数组的==第一个数（最小）==和==最后一个数（最大）=='


def _cap_ans(S, B, ret):
    a = S.a
    if B.mn == float('inf'):
        return '左边还没有数组：两个差都是 `-∞`，`ans` 不变'
    d1, d2 = a[-1] - B.mn, B.mx - a[0]
    better = '（==更新==）' if S.ans > B.ans else ''
    return f'和左边的数组配对：`{a[-1]} − {B.mn} = {d1}`，`{B.mx} − {a[0]} = {d2}` → `ans = {S.ans}`{better}'


CONFIG = dict(
    num=624, title='数组列表中的最大距离', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='枚举右，维护左',
    tags=['字节30天'],
    code='''
class Solution:
    def maxDistance(self, arrays: List[List[int]]) -> int:
        ans = 0
        mn, mx = inf, -inf
        for a in arrays:
            ans = max(ans, a[-1] - mn, mx - a[0])
            mn = min(mn, a[0])
            mx = max(mx, a[-1])
        return ans
''',
    call=f'Solution().maxDistance({ARR})',
    expect=7,
    views=[
        dict(type='text', fn=_formula, size=24, h=80, lines=2),
        dict(type='grid', var='arrays', label='arrays（青/橙 = 当前数组的首/尾；蓝 = 左边的 mn，粉 = 左边的 mx）',
             rows=['0', '1', '2', '3'], cell=92, h=440, color=_color),
    ],
    watch=[('mn', 'mn', 'blue'), ('mx', 'mx', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans = 0`',
        'mn, mx = inf, -inf': '`mn` / `mx`：==左边==所有数组首元素的最小值 / 尾元素的最大值',
        'for a in arrays': lambda S, B, ret: (f'枚举右边的数组 `a = {S.a}`' if S.get('a') is not None and S.a != B.get('a')
                                              else '所有数组都枚举完了'),
        'ans = max': _cap_ans,
        'mn = min': lambda S, B, ret: (f'再用 `a[0] = {S.a[0]}` 更新 `mn = {S.mn}`'
                                       + ('（==注意顺序==：先算 ans 再更新，否则会在同一个数组里选两个数）' if B.mn == float('inf') else '')),
        'mx = max': lambda S, B, ret: (f'用 `a[-1] = {S.a[-1]}` 更新 `mx = {S.mx}`'
                                       + ('：此时 ==mn、mx 来自同一个数组==，但右边的数组每次只和其中一个配对'
                                          if S.a[0] == S.mn and S.a[-1] == S.mx and B.mx != float('-inf') else '')),
        'return ans': '最大距离为 =={ret}==',
    },
    cards=dict(
        one_liner='枚举右边的数组，和左边数组的最小首元素/最大尾元素配对',
        complexity='时间 `O(m)`，空间 `O(1)`',
        problem=['给定 `m` 个==升序==数组，从==两个不同的==数组中各选一个整数',
                 '距离定义为差的绝对值 `|a-b|`，返回最大距离',
                 '示例：`[[1,2,3],[4,5],[1,2,3]]` → `4`；本视频 `[[3,5],[1,4,9],[2,6],[4,7]]` → `7`'],
        quote='我们可以==枚举 A = arrays[i] 作为右边那个数组==，然后维护左边所选数组的第一个数的最小值 mn 和最后一个数的最大值 mx。',
        quote_src='—— 灵茶山艾府题解',
        idea=['固定两个数组时，最大差一定是 `max(A) − min(B)` 或 `max(B) − min(A)`',
              '升序 → 只看首尾；右边数组 `a` 的最大差：`max(a[-1] − mn, mx − a[0])`',
              '不用取绝对值：负的那项一定不会比另一项大'],
        result='运行结束：返回 `7`（9 − 2）✓；注意全局最小 1 和最大 9 在同一个数组里',
        summary=['时间 `O(m)`，空间 `O(1)`',
                 '==先更新 ans，再更新 mn / mx==：否则可能在同一个数组里选两个数',
                 '不用考虑右边的数组：轮到右边的数组时，会站在它的视角算',
                 '本例陷阱：直接 `max − min = 9 − 1 = 8` 是错的，1 和 9 在同一数组'],
    ),
)
