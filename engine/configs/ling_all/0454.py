A, B_, C, D = [1, 2], [-2, -1], [-1, 2], [0, 2]


def _table(cv, T, X, Y, rows, cols, rname, cname, val, hi, cell=104):
    """画一个 rows × cols 的二维表：表头 + 每格的值；hi(i, j) 返回颜色名或 None"""
    cv.text((X + cell / 2, Y + cell / 2), f'{rname}\\{cname}', 20, T['muted'], anchor='mm')
    for j, c in enumerate(cols):
        cv.text((X + (j + 1.5) * cell, Y + cell / 2), str(c), 30, T['cyan'], anchor='mm', bold=True)
    for i, r in enumerate(rows):
        cv.text((X + cell / 2, Y + (i + 1.5) * cell), str(r), 30, T['cyan'], anchor='mm', bold=True)
        for j, c in enumerate(cols):
            x, y = X + (j + 1) * cell, Y + (i + 1) * cell
            h = hi(i, j)
            cv.rect((x + 4, y + 4, x + cell - 4, y + cell - 4), fill=T[h] if h else T['panel2'], r=10)
            cv.text((x + cell / 2, y + cell / 2), val(i, j), 28, T['bg'] if h else T['text'], anchor='mm', bold=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cnt = S.get('cnt')
    w = (x1 - x0) / 2
    cv.text((x0 + 18, y0 + 4), '① x+y 计数（nums1 × nums2）', 22, T['muted'], bold=True)
    _table(cv, T, x0 + 40, y0 + 50, A, B_, 'n1', 'n2', lambda i, j: str(A[i] + B_[j]),
           lambda i, j: 'blue' if cnt is not None else None)
    if cnt is not None:
        yy = y0 + 50 + 3 * 104 + 20
        cv.rich(x0 + 40, yy, 'cnt = ' + '，'.join(f'`{k}:{v}`' for k, v in sorted(cnt.items())), w - 40, size=26)
    show2 = S.get('_line') == 4
    cv.text((x0 + w + 18, y0 + 4), '② 查 cnt[−x−y]（nums3 × nums4）', 22, T['muted'], bold=True)
    _table(cv, T, x0 + w + 40, y0 + 50, C, D, 'n3', 'n4',
           lambda i, j: (f'{-C[i] - D[j]}→{cnt[-C[i] - D[j]]}' if show2 else f'{-C[i] - D[j]}'),
           lambda i, j: ('green' if cnt[-C[i] - D[j]] else None) if show2 else None)
    if show2:
        yy = y0 + 50 + 3 * 104 + 20
        tot = sum(cnt[-x - y] for x in C for y in D)
        cv.rich(x0 + w + 40, yy, f'格子里：`−x−y → cnt[−x−y]`', w - 40, size=26)
        cv.rich(x0 + w + 40, yy + 46, f'累加 = =={tot}==', w - 40, size=30, accent=T['green'])
    yb = y1 - 70
    cv.rich(x0 + 40, yb, '移项：`n1 + n2 == −n3 − n4`，左组存表，右组去查', x1 - x0 - 80, size=26)


CONFIG = dict(
    num=454, title='四数相加 II', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='两两分组 + 哈希表计数',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution:
    def fourSumCount(self, nums1: List[int], nums2: List[int], nums3: List[int], nums4: List[int]) -> int:
        cnt = Counter(x + y for x in nums1 for y in nums2)
        return sum(cnt[-x - y] for x in nums3 for y in nums4)
''',
    call=f'Solution().fourSumCount({A}, {B_}, {C}, {D})',
    expect=2,
    views=[dict(type='custom', draw=_draw, h=620)],
    watch=[],
    captions={
        'cnt = Counter': '先枚举 nums1、nums2 的所有组合，把 `x + y` 的==出现次数==记进 `cnt`：`{dict(cnt)}`',
        'return sum': '再枚举 nums3、nums4：每个 `−x − y` 在 cnt 里出现几次，就有几组四元组；累加得 =={ret}==',
    },
    cards=dict(
        one_liner='四个数拆成两组：一组存哈希表，另一组去查',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['四个长度都为 n 的数组，统计 `(i, j, k, l)` 的个数',
                 '使 `nums1[i] + nums2[j] + nums3[k] + nums4[l] == 0`',
                 '示例：`[1,2] [-2,-1] [-1,2] [0,2]` → `2`'],
        quote='将其变形为 nums1[i] + nums2[j] = −nums3[k] − nums4[l]。我们可以==先统计出所有 nums1[i] + nums2[j] 的出现次数==，记在一个哈希表 cnt 中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['移项后左边只和 i、j 有关，右边只和 k、l 有关',
              '左边 `n^2` 种和，用 `Counter` 记次数',
              '右边每种 `−x − y`，`O(1)` 查 `cnt`，次数直接累加'],
        result='`cnt[1] = 1`、`cnt[-1] = 1` → 共 `2` 个四元组',
        after=[dict(heading='两行代码展开', lines=[
            '`(1,−2)`、`(1,−1)`、`(2,−2)`、`(2,−1)` → 和为 `−1, 0, 0, 1`',
            '`cnt = {−1: 1, 0: 2, 1: 1}`',
            '`(−1,0) → cnt[1] = 1`，`(−1,2) → cnt[−1] = 1`',
            '`(2,0) → cnt[−2] = 0`，`(2,2) → cnt[−4] = 0`，合计 `2`'])],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`',
                 '`Counter` 查不存在的键返回 0，不用特判',
                 '不要四重循环 `O(n^4)`；也不要「三个存表一个查」，那样存表就要 `O(n^3)`',
                 '思考题：改成 `i < j < k < l` 怎么做？参考 3404. 统计特殊子序列的数目'],
    ),
)
