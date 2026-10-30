MAT = [[5, 2], [1, 6]]
K = 1


def _inS(S):
    """是否已经进入 search 函数（代码第 25 行起）"""
    return S.get('_line', 0) >= 25


def _fg(S):
    return [S['g'], S['f']]


def _fgcolor(S, r, c, v):
    ln = S['_line']
    i, j = S.get('i'), S.get('j')
    if _inS(S) or i is None or j is None or ln < 11 or ln > 21 or 'g' not in S:
        return None
    if r == 1 and c == j and ln >= 13 and ln <= 19:
        return 'yellow'
    if 11 <= ln <= 19 and i > 0 and j > 0:
        if (r, c) in ((1, j - 1), (0, j)):
            return 'blue'
        if (r, c) == (0, j - 1):
            return 'pink'
    if i > 0 and j == 0 and ln >= 16 and (r, c) == (0, 0):
        return 'blue'
    if i == 0 and j > 0 and ln >= 11 and (r, c) == (1, j - 1):
        return 'blue'
    return None


def _gcolor(S, a, b, v):
    i, j = S.get('i'), S.get('j')
    if _inS(S) or i is None or j is None or S['_line'] < 10:
        return None
    if (a, b) == (i, j):
        return None
    if a < i or (a == i and b < j):
        return 'blue'
    return None


def _ncolor(S, idx, v):
    if not _inS(S):
        if S['_line'] == 21 and idx == len(S['nums']) - 1:
            return 'green'
        return None
    l, r = S.get('left'), S.get('right')
    i, j = S.get('i'), S.get('j')
    ln = S['_line']
    if l is None or r is None or i is None or j is None or ln < 32 or ln in (43, 47):
        return None
    if l <= idx < i:
        return 'blue'
    if j < idx <= r:
        return 'pink'
    return None


def _ndim(S, idx, v):
    if not _inS(S):
        return False
    l, r = S.get('left'), S.get('right')
    return l is not None and not (l <= idx <= r)


def _text(S):
    ln = S['_line']
    i, j = S.get('i'), S.get('j')
    if 'nums' not in S:
        return '`f` 是滚动数组：算完一行就盖掉上一行；`g` 备份上一行'
    if ln < 8:
        return '准备：`f` 存当前行的前缀异或，`nums` 收集所有目标值'
    if ln == 23:
        return f"目标值全部算完：`nums = {S['nums']}`，第 `k = {S['k']}` 大 = 第 `{len(S['nums']) - S['k'] + 1}` 小"
    if not _inS(S):
        if ln == 8 or i is None:
            return f'第 `i` 行：`f` 要被改写成这一行的结果'
        if ln == 9:
            return f"`g` 备份上一行：`g = {S['g']}`"
        if ln == 10:
            return f'枚举 `({i},{j})`'
        if ln in (11, 12, 16):
            return f'`({i},{j})`：看它在哪个边界'
        if ln in (13,):
            return f"`f[0] = matrix[0][0] = {S['f'][0]}`"
        if ln in (15, 17, 19):
            if i == 0 and j == 0:
                return '情形 1：只有 `(0,0)`'
            if i == 0:
                return f'情形 2：第 0 行，`f[{j}] = f[{j-1}] ^ matrix[0][{j}]`'
            if j == 0:
                return f'情形 3：第 0 列，`f[0] = g[0] ^ matrix[{i}][0]`'
            return '情形 4：`f[j] = f[j-1] ^ g[j] ^ g[j-1] ^ matrix[i][j]`（蓝 = 异或进来，粉 = 两边重复的部分）'
        if ln == 21:
            return f"`nums` 收下 `({i},{j})` 的目标值 `{S['nums'][-1]}`"
        return f"`nums = {S['nums']}`"
    left, right = S.get('left'), S.get('right')
    if left is None:
        return f"快速选择：第 `{S['k']}` 小"
    seg = S['nums'][left:right + 1]
    if ln in (29, 30, 31) and 'mid' in S:
        return f"区间 `[{left}, {right}]` = `{seg}`，基准 `mid = {S['mid']}`"
    return f"区间 `[{left}, {right}]` = `{seg}`，找第 `{S['k']}` 小"


def _cap_pair(S, B, r):
    # j == 0 判断：只有 i == 0 才会走到
    return '`j = 0`：第 0 行第 0 列 → 情形 1，只有这个格子' if S.j == 0 else f'`j = {S.j} > 0`：左边还有格子 → 情形 2'


def _cap_mid(S, B, r):
    return f'`mid = nums[({S.left} + {S.right}) // 2] = {S.mid}`：取中间的数当基准，小的放左边，大的放右边'


def _cap_w1(S, B, r):
    if S.i <= S.right and S.nums[S.i] < S.mid:
        return f'`nums[{S.i}] = {S.nums[S.i]} < mid = {S.mid}`：本来就该在左边，`i` 右移'
    if S.i > S.right:
        return f'`i = {S.i}` 越过 `right`：左边已经没有大于等于 `mid` 的数'
    return f'`nums[{S.i}] = {S.nums[S.i]} ≥ mid = {S.mid}`：`i` 停下，它该去右边'


def _cap_w2(S, B, r):
    if S.j >= S.left and S.nums[S.j] > S.mid:
        return f'`nums[{S.j}] = {S.nums[S.j]} > mid = {S.mid}`：本来就该在右边，`j` 左移'
    if S.j < S.left:
        return f'`j = {S.j}` 越过 `left`：右边已经没有小于等于 `mid` 的数'
    return f'`nums[{S.j}] = {S.nums[S.j]} ≤ mid = {S.mid}`：`j` 停下，它该去左边'


def _cap_cmp1(S, B, r):
    cnt = S.j - S.left + 1
    if cnt >= S.k:
        return f'左半区间 `[{S.left}, {S.j}]` 有 `{cnt}` 个数 ≥ `k = {S.k}` → 第 `k` 小在左半，==递归左半=='
    return f'左半区间只有 `{cnt}` 个数 < `k = {S.k}` → 答案不在左半'


def _cap_cmp2(S, B, r):
    cnt = S.i - S.left
    if cnt >= S.k:
        return f'`i - left = {cnt} ≥ k = {S.k}`：中间那段都等于 `mid` → 第 `k` 小就是 `mid`'
    return f'`i - left = {cnt} < k = {S.k}`：左边（含等于 mid 的）加起来还不够'


CONFIG = dict(
    num=1738, title='找出第 K 大的异或坐标值', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='二维前缀异或 · 滚动数组 + 快速选择',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1671'],
    code='''
class Solution(object):
    def kthLargestValue(self, matrix, k):

        m = len(matrix)
        n = len(matrix[0])
        f = [0] * n
        nums = []
        for i in range(m):
            g = f[:]
            for j in range(n):
                if i == 0:
                    if j == 0:
                        f[j] = matrix[i][j]
                    else:
                        f[j] = f[j - 1] ^ matrix[i][j]
                elif j == 0:
                    f[j] = g[j] ^ matrix[i][j]
                else:
                    f[j] = f[j - 1] ^ g[j] ^ g[j - 1] ^ matrix[i][j]

                nums.append(f[j])

        return self.search(nums, 0, len(nums) - 1, len(nums) - k + 1)

    def search(self, nums, left, right, k):
        if left == right:
            return nums[left]

        mid = nums[(left + right) // 2]
        i = left
        j = right
        while i <= j:
            while i <= right and nums[i] < mid:
                i += 1
            while j >= left and nums[j] > mid:
                j -= 1
            if i <= j:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
                j -= 1

        if j - left + 1 >= k:
            return self.search(nums, left, j, k)
        elif i - left >= k:
            return nums[left + k - 1]
        else:
            return self.search(nums, i, right, k - (i - left))
''',
    call=f'Solution().kthLargestValue({MAT}, {K})',
    expect=7,
    max_steps=80,
    skip=['m = len', 'n = len', 'nums = []', 'i = left', 'j = right'],
    views=[
        dict(type='text', fn=_text, size=24, h=64),
        dict(type='grid', var='matrix', label='matrix（蓝 = 已经算过的格子，黄框 = 当前格）', cell=76, h=170,
             color=_gcolor, cursors=[(lambda S: None if _inS(S) else S.get('i') if S['_line'] >= 10 else None,
                                      lambda S: None if _inS(S) else S.get('j') if S['_line'] >= 10 else None, 'yellow')]),
        dict(type='table', var=_fg, label='上排 g = 上一行，下排 f = 当前行（黄 = 正在算，蓝/粉 = 用到的格子）', cell=76, h=150,
             rows=['g', 'f'], color=_fgcolor),
        dict(type='array', var='nums', label='nums（蓝 = 已确认 ≤ mid，粉 = 已确认 ≥ mid，暗 = 区间外）', cell=76, h=250,
             pointers={'i if _line >= 32 else None': 'blue', 'j if _line >= 32 else None': 'pink'},
             pointer_labels={'i if _line >= 32 else None': 'i', 'j if _line >= 32 else None': 'j'},
             window=(lambda S: S.get('left') if _inS(S) else None, lambda S: S.get('right') if _inS(S) else None),
             color=_ncolor, dim=_ndim),
        dict(type='calls', h=140, hide=('nums',)),
    ],
    watch=[('i', lambda S: S['_inner'].get('i'), 'blue'), ('j', lambda S: S['_inner'].get('j'), 'pink'), ('k', 'k', 'green'), ('mid', lambda S: S['_inner'].get('mid'), 'yellow')],
    captions={
        'f = [0] * n': '`f[j]` 存==当前行==的前缀异或：`(0,0)` 到 `(i,j)` 的异或和（滚动数组，省掉一维）',
        'for i in range(m)': lambda S, B, r: ('所有行都算完了' if 'i' in B and B.i == S.i else f'第 `{S.i}` 行'),
        'g = f[:]': '`g` 复制上一行的结果：后面 `f` 会被改写成当前行，`g` 还留着上一行',
        'for j in range(n)': lambda S, B, r: (f'枚举右下角 `({S.i}, {S.j})`' if not ('j' in B and B.j == S.j and B.i == S.i) else '这一行算完了'),
        'if i == 0:': lambda S, B, r: ('`i = 0`：第 0 行，没有上一行' if S.i == 0 else f'`i = {S.i} > 0`：有上一行，接着看 `j`'),
        12: _cap_pair,
        'f[j] = matrix[i][j]': '情形 1：`(0,0)` 只有自己：`f[0] = {f[0]}`',
        'f[j] = f[j - 1] ^ matrix[i][j]': '情形 2：`f[{j}] = f[{j-1}] ^ matrix[0][{j}] = {B.f[j-1]} ^ {matrix[0][j]}` = =={f[j]}==',
        16: lambda S, B, r: (f'`j = 0`：第 0 列，只能靠上一行的 `g[0]`' if S.j == 0 else f'`j = {S.j} > 0`：上、左、左上都有 → 情形 4'),
        'f[j] = g[j] ^ matrix[i][j]': '情形 3：`f[0] = g[0] ^ matrix[{i}][0] = {g[0]} ^ {matrix[i][0]}` = =={f[0]}==',
        'f[j] = f[j - 1] ^ g[j] ^ g[j - 1] ^ matrix[i][j]': lambda S, B, r: (
            f'情形 4：`f[{S.j}] = f[{S.j-1}] ^ g[{S.j}] ^ g[{S.j-1}] ^ matrix[{S.i}][{S.j}]` = `{S.f[S.j-1]} ^ {S.g[S.j]} ^ {S.g[S.j-1]} ^ {S.matrix[S.i][S.j]}` = =={S.f[S.j]}==，'
            f'`g[j-1]` 被异或了两次（抵消），要补上'),
        'nums.append(f[j])': '`(i, j)` 的目标值 `{f[j]}` 收进 `nums`',
        'return self.search(nums, 0': '目标值都算完：第 `k` 大 = 第 `len(nums) - k + 1` 小 → 用快速选择',
        'if left == right': lambda S, B, r: (f'区间只剩一个数：`nums[{S.left}] = {S.nums[S.left]}` 就是答案' if S.left == S.right
                                             else f'区间 `[{S.left}, {S.right}]` 还有 `{S.right - S.left + 1}` 个数，继续划分'),
        'mid = nums[': _cap_mid,
        'while i <= j': lambda S, B, r: (f'`i = {S.i} ≤ j = {S.j}`：两个指针还没交叉，继续划分' if S.i <= S.j else f'`i = {S.i} > j = {S.j}`：指针交叉，划分完成'),
        'while i <= right and nums[i] < mid': _cap_w1,
        'while j >= left and nums[j] > mid': _cap_w2,
        'if i <= j': lambda S, B, r: (f'`i = {S.i} ≤ j = {S.j}`：左边停的数 ≥ mid、右边停的数 ≤ mid → 交换' if S.i <= S.j else f'`i = {S.i} > j = {S.j}`：不用交换'),
        'nums[i], nums[j] = nums[j], nums[i]': '交换：`nums[{i}]` 和 `nums[{j}]` → `{nums[left:right+1]}`，大的去右边，小的去左边',
        'if j - left + 1 >= k': _cap_cmp1,
        'elif i - left >= k': _cap_cmp2,
        'return nums[left + k - 1]': '`nums[{left + k - 1}] = {nums[left + k - 1]}` 就是答案',
        'return self.search(nums, left, j, k)': '递归左半 `[{B.left}, {B.j}]`，还是找第 `{B.k}` 小',
        'return self.search(nums, i, right, k - (i - left))': '递归右半 `[{B.i}, {B.right}]`：左边 `{B.i - B.left}` 个都小于等于答案，所以在右半找第 `{B.k - (B.i - B.left)}` 小',
    },
    cards=dict(
        one_liner='先把每格目标值推出来（滚动前缀异或），再快速选择第 k 大',
        complexity='时间 `O(mn)`（快速选择期望），空间 `O(mn)`',
        problem=['矩阵 `matrix`，坐标 `(a, b)` 的==目标值==是 `(0,0)` 到 `(a,b)` 所有元素的异或',
                 '求所有目标值里==第 `k` 大==的那个',
                 '示例：`[[5,2],[1,6]]`，`k = 1` → `7`；`k = 2` → `5`',
                 '本视频取 `k = 1`：目标值依次是 `5, 7, 4, 0`，最大的是 `7`'],
        quote='由于异或操作是没有单调性的，因此想直接从原始矩阵matrix中就得出异或结果的第K大的值是比较困难的，必须先算出每个位置上的异或结果。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j] = f[i-1][j] ^ f[i][j-1] ^ f[i-1][j-1] ^ m[i][j]`：重叠的左上角异或了两次，抵消，要补上',
              '`f` 每行只依赖上一行 → 滚动成一维，`g` 备份上一行',
              '目标值收进 `nums`，第 `k` 大 = 第 `len - k + 1` 小，用快速选择'],
        after=[dict(heading='公式怎么证', lines=[
            '把 `f[i-1][j]`、`f[i][j-1]` 里按行、按列拆开，再两边同时异或 `f[i-1][j-1]`',
            '`a ^ a = 0` 加上结合律，一步步消去，就得到四项异或的递推式',
            '第 0 行、第 0 列没有上一行/左边，单独处理成三种边界情形'])],
        summary=['时间：推目标值 `O(mn)`，快速选择期望 `O(mn)`；空间 `O(mn)`（`nums`）',
                 '易错：第 `k` 大要换成第 `len(nums) - k + 1` 小',
                 '易错：`g = f[:]` 必须是拷贝，直接 `g = f` 会一起被改写',
                 '原文为 Python 2 写法，`(left + right) / 2` 已改为 `//`；类型说明没有保留',
                 '对比灵神：灵神用 `col_sum` 记每列异或再累积，一样 `O(1)` 推一格；yiduobo 用滚动 `f` + `g`'],
    ),
)
