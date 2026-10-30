A, B_ = [2, 3, 5, 6, 8, 10, 13, 14], [1, 4, 7, 9, 11, 12]


def _rb(S, i, v):
    if 'left' not in S:
        return None
    if i <= S['left']:
        return 'red'
    if i >= S['right']:
        return 'blue'
    return None


def _fmtv(x):
    return '-∞' if x == float('-inf') else ('+∞' if x == float('inf') else str(x))


def _state(S):
    if 'max1' in S or 'min2' in S:
        s = f"max1 = max(ai, bj) = =={_fmtv(S['max1'])}=="
        if 'min2' in S:
            s += f"   ·   min2 = min(ai1, bj1) = =={_fmtv(S['min2'])}=="
        return s
    if 'i' in S and 'j' in S and S['i'] < S['m'] and S['j'] + 1 < S['n']:
        a, b, i, j = S['a'], S['b'], S['i'], S['j']
        s = f"第一组：a 的前 {i + 1} 个 + b 的前 {j + 1} 个 = {i + j + 2} 个"
        if 'ai' not in S and i >= 0:
            s += f"\n检查 `a[{i}] = {a[i]} ≤ b[{j + 1}] = {b[j + 1]}`？" + ('==成立==' if a[i] <= b[j + 1] else '==不成立==')
        return s
    if 'm' in S:
        return f"第一组要放 `(m + n + 1) // 2 = {(S['m'] + S['n'] + 1) // 2}` 个数（黄框）"
    return '保证 a 是较短的数组'


def _legend(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    x, y = x0 + 22, (y0 + y1) / 2
    for c, s in [(T['red'], '红：a[i] ≤ b[j+1]'), (T['blue'], '蓝：a[i] > b[j+1]'), (T['yellow'], '黄框：第一组')]:
        if c == T['yellow']:
            cv.rect((x, y - 14, x + 28, y + 14), outline=c, width=3, r=6)
        else:
            cv.rect((x, y - 14, x + 28, y + 14), fill=c, r=6, outline=T['border'])
        cv.text((x + 38, y), s, 23, T['muted'], anchor='lm')
        x += 38 + cv.tlen(s, 23) + 34


def _swap(S, B, ret):
    if len(B.a) > len(B.b):
        return f'`len(a) = {len(B.a)} > len(b) = {len(B.b)}` → 交换，==保证 a 更短==（`m ≤ n`）'
    return f'`len(a) = {len(B.a)} ≤ len(b) = {len(B.b)}`，不用交换'


def _while(S, B, ret):
    if B.left + 1 < B.right:
        return f'开区间 `({B.left}, {B.right})` 非空 → 继续二分 i'
    return f'`left + 1 = right = {B.right}`：开区间为空 → 结束'


def _cmp(S, B, ret):
    x, y = S.a[S.i], S.b[S.j + 1]
    if x <= y:
        return f'`a[{S.i}] = {x} ≤ b[{S.j + 1}] = {y}`：成立 → i 还可以更大，==i 染红=='
    return f'`a[{S.i}] = {x} > b[{S.j + 1}] = {y}`：a[i] 比第二组的数还大 → i 太大，==染蓝=='


def _ret(S, B, ret):
    if (S.m + S.n) % 2:
        return f'`m + n = {S.m + S.n}` 是奇数 → 中位数就是第一组的最大值 =={ret}=='
    return f'`m + n = {S.m + S.n}` 是偶数 → 中位数 = `({S.max1} + {S.min2}) / 2` = =={ret}=='


CONFIG = dict(
    num=4, title='寻找两个正序数组的中位数', difficulty='Hard', category='二分查找',
    author='灵茶山艾府', technique='均匀分组 · 二分第一组的分割点',
    code='''
class Solution:
    def findMedianSortedArrays(self, a: List[int], b: List[int]) -> float:
        if len(a) > len(b):
            a, b = b, a

        m, n = len(a), len(b)
        # 循环不变量：a[left] <= b[j+1]
        # 循环不变量：a[right] > b[j+1]
        left, right = -1, m
        while left + 1 < right:  # 开区间 (left, right) 不为空
            i = (left + right) // 2
            j = (m + n - 3) // 2 - i
            if a[i] <= b[j + 1]:
                left = i  # 缩小二分区间为 (i, right)
            else:
                right = i  # 缩小二分区间为 (left, i)

        # 此时 left 等于 right-1
        # a[left] <= b[j+1] 且 a[right] > b[(j-1)+1] = b[j]，所以答案是 i=left
        i = left
        j = (m + n - 3) // 2 - i
        ai = a[i] if i >= 0 else -inf
        bj = b[j] if j >= 0 else -inf
        ai1 = a[i + 1] if i + 1 < m else inf
        bj1 = b[j + 1] if j + 1 < n else inf
        max1 = max(ai, bj)
        min2 = min(ai1, bj1)
        return max1 if (m + n) % 2 else (max1 + min2) / 2
''',
    call=f'Solution().findMedianSortedArrays({A}, {B_})',
    expect=7.5,
    views=[
        dict(type='text', fn=_state, size=26, lines=2, h=84),
        dict(type='array', var='a', label='a', cell=100, h=230,
             pointers={'left': 'red', 'right': 'blue', 'i': 'yellow'},
             window=('0', 'i'), window_color='yellow', color=_rb),
        dict(type='array', var='b', label='b', cell=100, h=200,
             pointers={'j': 'cyan', 'j + 1': 'purple'}, pointer_labels={'j + 1': 'j+1'},
             window=('0', 'j'), window_color='yellow'),
        dict(type='custom', draw=_legend, h=56),
    ],
    watch=[('left', 'left', 'red'), ('right', 'right', 'blue'), ('i', 'i', 'yellow'), ('j', 'j', 'cyan'),
           ('max1', 'max1', 'green'), ('min2', 'min2', 'green')],
    captions={
        3: _swap,
        4: '交换后 `a = {a}`：只在短数组上二分，复杂度 `O(log min(m, n))`',
        6: '`m = {m}`，`n = {n}`：第一组要放 `(m + n + 1) // 2 = {(m + n + 1) // 2}` 个数',
        9: '开区间 `(-1, {right})`：`i = -1`（a 一个都不放）一定满足，`i = m` 视为 +∞ 一定不满足',
        10: _while,
        11: '`i = ({left} + {right}) // 2 = {i}`：设 a 的前 `{i + 1}` 个数在第一组',
        12: '`j = (m + n - 3) // 2 - i = {j}`：b 的前 `{j + 1}` 个也进第一组，凑够 `{i + j + 2}` 个',
        13: _cmp,
        14: '`left = i = {left}`：范围缩小为 `({left}, {right})`',
        16: '`right = i = {right}`：范围缩小为 `({left}, {right})`',
        20: '`i = left = {i}`：==最大的满足 a[i] ≤ b[j+1] 的 i==，同时 `a[i+1] > b[j]`',
        21: '`j = {j}`：第一组 = `a[0..{i}]` + `b[0..{j}]`，第一组最大值 ≤ 第二组最小值',
        22: '`ai = a[{i}] = {ai}`（`i < 0` 时视为 -∞）',
        23: '`bj = b[{j}] = {bj}`（`j < 0` 时视为 -∞）',
        24: '`ai1 = a[{i + 1}] = {ai1}`（越界时视为 +∞）',
        25: '`bj1 = b[{j + 1}] = {bj1}`（越界时视为 +∞）',
        26: '第一组的最大值 `max1 = max({ai}, {bj}) = {max1}`',
        27: '第二组的最小值 `min2 = min({ai1}, {bj1}) = {min2}`',
        28: _ret,
    },
    cards=dict(
        one_liner='均匀分成两组，第一组最大值 ≤ 第二组最小值；二分 a 的分割点',
        complexity='时间 `O(log min(m, n))`，空间 `O(1)`',
        problem=['两个正序数组 `nums1`（长 m）和 `nums2`（长 n），返回合并后的==中位数==；要求 `O(log(m+n))`',
                 '示例：`[1,3]`, `[2]` → `2.0`；`[1,2]`, `[3,4]` → `2.5`'],
        before=[dict(heading='灵神的循序渐进', lines=[
            '排序：合并后排序取中间，`O((m+n) log(m+n))`',
            '双指针：i 增大、j 减小，直到 `a[i] ≤ b[j+1]` 且 `a[i+1] > b[j]`，`O(m+n)`',
            '二分：`a[i] ≤ b[j+1]` 随 i 增大从成立变成不成立 → ==二分 i==，`O(log min(m, n))`'])],
        quote='这里的关键是「==均匀分组==」……只要==第一组的最大值 ≤ 第二组的最小值==，我们就找到了答案。',
        quote_src='—— 灵茶山艾府题解 · 引入：均匀分组',
        idea=['第一组放 `⌈(m+n)/2⌉` 个：a 的前 `i+1` 个 + b 的前 `j+1` 个，`j = (m+n-3)//2 - i`',
              '只要 `a[i] ≤ b[j+1]` 且 `a[i+1] > b[j]`，两组就分好了',
              '二分==最大的==满足 `a[i] ≤ b[j+1]` 的 i：红色满足、蓝色不满足'],
        result='返回 `7.5`：合并后是 `1..14`，中间两个数 7 和 8 的平均 ✓',
        summary=['时间 `O(log min(m, n))`，比题目要求的 `O(log(m+n))` 还好；空间 `O(1)`',
                 '先交换保证 `m ≤ n`：这样对任意 i，算出的 j 都不会越界',
                 '越界的 `a[-1]`、`b[-1]` 视为 `-∞`，`a[m]`、`b[n]` 视为 `+∞`',
                 '有重复元素也正确：只用到了“a 和 b 有序”',
                 '思考题：改成求两个有序数组的第 k 小？'],
    ),
)
