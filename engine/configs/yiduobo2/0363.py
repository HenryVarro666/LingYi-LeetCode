MAT = [[4, -2], [-1, 0], [3, 4]]
K = 2


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'matrix（青框 = 列 [left, right]，黄框 = 当前行）→ 压缩成 row_sum', 22, T['muted'], bold=True)
    m, n = len(MAT), len(MAT[0])
    cell = 84
    gx = x0 + 230
    gy = y0 + 66
    L, R, idx = S.get('left'), S.get('right'), S.get('index')
    live = L is not None and R is not None
    if live:
        cv.rect((gx + L * cell - 4, gy - 6, gx + (R + 1) * cell + 4, gy + m * cell + 6), fill=T['cyan'], alpha=45, r=10)
        cv.rect((gx + L * cell - 4, gy - 6, gx + (R + 1) * cell + 4, gy + m * cell + 6), outline=T['cyan'], width=3, r=10)
    for i in range(m):
        cv.text((gx - 16, gy + i * cell + cell / 2), f'行 {i}', 20, T['dim'], anchor='rm')
        for j in range(n):
            X, Y = gx + j * cell, gy + i * cell
            inside = live and L <= j <= R and idx is not None and i <= idx and 'pre_sum' in S
            cv.rect((X + 4, Y + 4, X + cell - 4, Y + cell - 4), fill=(48, 70, 60) if inside else T['panel2'], r=8,
                    outline=T['border'], width=1)
            cv.text((X + cell / 2, Y + cell / 2), MAT[i][j], 30, T['text'], anchor='mm', bold=True, mono=True)
    for j in range(n):
        cv.text((gx + j * cell + cell / 2, gy + m * cell + 12), f'列 {j}', 18, T['dim'], anchor='mt')
    rs = S.get('row_sum')
    rx = gx + n * cell + 70
    cv.text((rx + cell / 2, gy - 10), 'row_sum', 20, T['purple'], anchor='mb', bold=True, mono=True)
    if rs is not None:
        brs = B.get('row_sum')
        for i in range(m):
            Y = gy + i * cell
            ch = brs is not None and len(brs) == len(rs) and brs[i] != rs[i]
            cv.rect((rx + 4, Y + 4, rx + cell - 4, Y + cell - 4), fill=T['panel2'], r=8,
                    outline=T['yellow'] if ch else T['purple'], width=3 if ch else 2)
            cv.text((rx + cell / 2, Y + cell / 2), rs[i], 30, T['text'], anchor='mm', bold=True, mono=True)
    if idx is not None and live:
        Y = gy + idx * cell
        cv.rect((gx - 2, Y, rx + cell + 2, Y + cell), outline=T['yellow'], width=3, r=10)
    # 右侧说明：pre_sum / tmp
    tx = rx + cell + 50
    if 'pre_sum' in S:
        cv.text((tx, gy + 10), f"pre_sum = {S['pre_sum']}", 28, T['green'], bold=True, mono=True)
        cv.text((tx, gy + 46), '（row_sum 的前缀和）', 20, T['dim'])
    if 'tmp' in S and S.get('_line', 0) >= 27:
        cv.text((tx, gy + 110), f"tmp = pre_sum − k = {S['tmp']}", 26, T['orange'], bold=True, mono=True)
        cv.text((tx, gy + 146), '找 sum_list 中 ≥ tmp 的最小值', 20, T['dim'])
    cv.text((tx, gy + 210), f'k = {K}', 26, T['muted'], bold=True, mono=True)


_PL = 'l if (29 <= _line <= 39 or 44 <= _line <= 56) else None'
_PR = 'r if (29 <= _line <= 39 or 44 <= _line <= 56) else None'
_PM = 'mid if (32 <= _line <= 38 or 48 <= _line <= 55) else None'


def _cap_le(S, B, ret):
    if S.pre_sum <= S.k:
        return f'`pre_sum = {S.pre_sum} ≤ k`：从第 0 行开始的矩形本身就合法 → 更新 `res`'
    return f'`pre_sum = {S.pre_sum} > k`：从第 0 行开始的矩形太大，不能直接用'


def _cap_tmp(S, B, ret):
    return (f'若之前某个前缀和 `s ≥ pre_sum − k = {S.tmp}`，则矩形和 `pre_sum − s ≤ k`；'
            f'==s 越小越好==')


def _cap_has(S, B, ret):
    if S.tmp <= S.sum_list[-1]:
        return f'`sum_list` 最大值 `{S.sum_list[-1]} ≥ tmp = {S.tmp}` → 一定有解，==二分==找第一个 ≥ tmp 的'
    return f'`sum_list` 最大值 `{S.sum_list[-1]} < tmp = {S.tmp}` → 没有合法的上边界，跳过'


def _cap_while(S, B, ret):
    if S.l < S.r:
        return f'`l = {S.l} < r = {S.r}`：继续二分'
    return f'`l == r = {S.l}`：二分结束'


def _cap_ins(S, B, ret):
    if S.pre_sum > S.sum_list[-1]:
        return f'`pre_sum = {S.pre_sum}` 比 `sum_list` 里所有数都大 → 直接放到末尾'
    return f'`pre_sum = {S.pre_sum}` 不是最大的 → 二分找插入位置，==保持 sum_list 有序=='


CONFIG = dict(
    num=363, title='矩形区域不超过 K 的最大数值和', difficulty='Hard', category='子串',
    author='yiduobo', technique='枚举左右列 · 前缀和 + 有序数组二分',
    tags=['List.md'],
    code='''
class Solution(object):
    def maxSumSubmatrix(self, matrix, k):
        if not matrix:
            return 0

        m = len(matrix)
        n = len(matrix[0])

        res = -2147483647
        for left in range(n):
            row_sum = [0] * m
            for right in range(left, n):
                pre_sum = 0
                sum_list = []
                for index in range(m):
                    row_sum[index] += matrix[index][right]
                    pre_sum += row_sum[index]

                    if pre_sum <= k:
                        res = max(res, pre_sum)
                        if res == k:
                            return res

                    if not sum_list:
                        sum_list.append(pre_sum)
                    else:
                        tmp = pre_sum - k
                        if tmp <= sum_list[-1]:
                            l = 0
                            r = len(sum_list) - 1
                            while l < r:
                                mid = (l + r) // 2
                                if sum_list[mid] == tmp:
                                    return k
                                if sum_list[mid] < tmp:
                                    l = mid + 1
                                else:
                                    r = mid
                            res = max(res, pre_sum - sum_list[l])

                        if pre_sum > sum_list[-1]:
                            sum_list.append(pre_sum)
                        else:
                            l = 0
                            r = len(sum_list) - 1
                            insert_flag = True
                            while l < r:
                                mid = (l + r) // 2
                                if sum_list[mid] == pre_sum:
                                    insert_flag = False
                                    break
                                if sum_list[mid] < pre_sum:
                                    l = mid + 1
                                else:
                                    r = mid
                            sum_list = sum_list[:l] + [pre_sum] + sum_list[l:]

        return res
''',
    call=f'Solution().maxSumSubmatrix({MAT}, {K})',
    expect=2,
    skip=['l = 0', 'r = len(sum_list) - 1', 'insert_flag = True', 'if not matrix', 'm = len(matrix)', 'pre_sum = 0',
          'if not sum_list', 'l = mid + 1', 'r = mid'],
    views=[
        dict(type='custom', draw=_draw, h=372),
        dict(type='array', var='sum_list', label='sum_list（之前的前缀和，从小到大）', cell=90, h=250,
             pointers={_PL: 'blue', _PR: 'pink', _PM: 'yellow'}, pointer_labels={_PL: 'l', _PR: 'r', _PM: 'mid'}),
    ],
    watch=[('left', 'left', 'cyan'), ('right', 'right', 'cyan'), ('index', 'index', 'yellow'),
           ('pre_sum', 'pre_sum', 'green'), ('tmp', 'tmp', 'orange'), ('res', 'res', 'pink')],
    captions={
        'm = len(matrix)': '`m = {m}` 行',
        'n = len(matrix[0])': '`{m}` 行 `{n}` 列；行数可能远大于列数 → ==枚举列==，在行上做文章',
        'res = -2147483647': '`res` 先设成一个很小的数',
        'for left in range': lambda S, B, ret: f'固定左边界列 `left = {S.left}`',
        'row_sum = [0] * m': '`row_sum[i]`：第 i 行在列 `[left, right]` 上的和；换了 left 要清零',
        'for right in range': lambda S, B, ret: f'右边界列 `right = {S.right}`：列 `[{S.left}, {S.right}]` ==压缩成一维数组== `row_sum`',
        'pre_sum = 0': '`pre_sum`：一维数组 `row_sum` 的前缀和',
        'sum_list = []': '`pre_sum`：`row_sum` 的前缀和；`sum_list`：之前的前缀和，==从小到大有序==',
        'for index in range(m)': lambda S, B, ret: (f'处理第 `index = {S.index}` 行' if S.get('index') != B.get('index')
                                                    else '这组列的所有行处理完，换下一个 right'),
        'row_sum[index] +=': '`row_sum[{index}]` 加上 `matrix[{index}][{right}] = {matrix[index][right]}` → {row_sum[index]}',
        'pre_sum += row_sum': '`pre_sum = {pre_sum}`：第 `0..{index}` 行、第 `{left}..{right}` 列的矩形和',
        'if pre_sum <= k': _cap_le,
        'res = max(res, pre_sum)': '`res = {res}`',
        'if res == k': lambda S, B, ret: ('`res == k`：不可能比 k 更大了 → ==直接返回==' if S.res == S.k else f'`res = {S.res}` < k，继续'),
        'if not sum_list': lambda S, B, ret: ('`sum_list` 为空：没有可以减的前缀和' if not S.sum_list else '`sum_list` 非空'),
        'sum_list.append(pre_sum)': '`pre_sum = {pre_sum}` 加入 `sum_list` → {sum_list}',
        'tmp = pre_sum - k': _cap_tmp,
        'if tmp <= sum_list[-1]': _cap_has,
        'while l < r': _cap_while,
        'mid = (l + r) // 2': '`mid = ({l} + {r}) // 2 = {mid}`，`sum_list[mid] = {sum_list[mid]}`',
        'if sum_list[mid] == tmp': lambda S, B, ret: (f'`sum_list[mid] == tmp`：矩形和恰好等于 k → 直接返回 k' if S.sum_list[S.mid] == S.tmp
                                                       else f'`{S.sum_list[S.mid]} ≠ {S.tmp}`'),
        'if sum_list[mid] < tmp': lambda S, B, ret: (f'`{S.sum_list[S.mid]} < tmp = {S.tmp}`：太小，答案在右边 → `l = mid + 1`' if S.sum_list[S.mid] < S.tmp
                                                      else f'`{S.sum_list[S.mid]} ≥ tmp = {S.tmp}`：可能是答案 → `r = mid`'),
        'l = mid + 1': '`l = mid + 1 = {l}`',
        'r = mid': '`r = mid = {r}`',
        'res = max(res, pre_sum - sum_list[l])': lambda S, B, ret: (
            f'第一个 ≥ tmp 的是 `sum_list[{S.l}] = {S.sum_list[S.l]}`：矩形和 `{S.pre_sum} − {S.sum_list[S.l]} = {S.pre_sum - S.sum_list[S.l]}`，'
            f'`res = max({B.res}, {S.pre_sum - S.sum_list[S.l]}) = {S.res}`'),
        'if pre_sum > sum_list[-1]': _cap_ins,
        'if sum_list[mid] == pre_sum': lambda S, B, ret: (f'`sum_list[mid] == pre_sum`：已存在' if S.sum_list[S.mid] == S.pre_sum
                                                           else f'`{S.sum_list[S.mid]} ≠ {S.pre_sum}`'),
        'if sum_list[mid] < pre_sum': lambda S, B, ret: (f'`{S.sum_list[S.mid]} < {S.pre_sum}` → 插入点在右边，`l = mid + 1`' if S.sum_list[S.mid] < S.pre_sum
                                                          else f'`{S.sum_list[S.mid]} ≥ {S.pre_sum}` → 插入点在 mid 或左边，`r = mid`'),
        'sum_list = sum_list[:l]': lambda S, B, ret: f'把 `{S.pre_sum}` 插到下标 `{S.l}` → `sum_list = {S.sum_list}`（数组插入是 `O(m)`）',
    },
    max_steps=70,
    cards=dict(
        one_liner='固定左右两列压成一维，再用前缀和 + 有序数组二分找 ≤ k 的最大子段和',
        complexity='时间最坏 `O(n²m²)`（数组插入 `O(m)`），用平衡树可做到 `O(n²m log m)`',
        problem=['给你 `m × n` 矩阵和整数 `k`，求矩形区域和==不超过 k== 的最大值（保证存在）',
                 '示例：`[[1,0,1],[0,-2,3]]`，`k = 2` → `2`',
                 f'本视频：`{MAT}`，`k = {K}` → `2`'],
        before=[dict(heading='两步转化', lines=[
            '① 枚举左右两列：每行在这几列的和 → 一维数组 `row_sum`',
            '② 一维：`pre[j] − pre[i−1] ≤ k` ⇔ `pre[i−1] ≥ pre[j] − k`',
            '有负数 → 前缀和不单调，==不能滑动窗口=='])],
        quote='对于一个sum_list[j]，我们的目标是找到对应的i，其满足sum_list[i - 1] >= sum_list[j] - k，sum_list[i - 1]是最大的那一个。',
        quote_src='—— yiduobo 题解原文（这里“最大”应为“最小”：s 越小，pre − s 越大）',
        idea=['扫描到 `pre_sum` 时，在之前的前缀和里找 ==≥ pre_sum − k 的最小值== `s`',
              '`pre_sum − s` 就是以当前行结尾、和 ≤ k 的最大矩形；再把 `pre_sum` 插入有序数组',
              '原文用“数组 + 二分”代替平衡树；从第 0 行开始的矩形用 `pre_sum ≤ k` 单独判断'],
        summary=['枚举列 `O(n²)` × 扫描行 `O(m)` × 数组插入 `O(m)`',
                 '易错：找 ==≥ pre_sum − k 的最小前缀和==（lower_bound）',
                 '易错：`sum_list` 没放空前缀 0，`pre_sum` 本身要单独和 k 比',
                 '原文为 Python 2：二分的 `(l + r) / 2` 改为 `//`，删去 docstring'],
    ),
)
