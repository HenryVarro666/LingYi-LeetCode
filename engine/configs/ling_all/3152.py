NUMS = [4, 3, 1, 6, 5, 2]
QUERIES = [[0, 2], [2, 3], [3, 5], [1, 5]]
CELL = 84


def _geom(box, n):
    x0, y0, x1, y1 = box
    width = x1 - x0 - 40
    cell = max(24, min(CELL, width / n))
    sx = x0 + 20 + (width - cell * n) / 2
    return cell, sx


def _a(S):
    s = S.get('s')
    if not isinstance(s, list):
        return None
    return [s[i + 1] - s[i] for i in range(len(s) - 1)]


def _draw_nums(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S.get('nums')
    if not nums:
        return
    n = len(nums)
    cell, sx = _geom(box, n)
    a = _a(S)
    cv.text((x0 + 18, y0 + 4), 'nums（粉奇青偶）与 a[i]（红 1 = 相邻奇偶相同，绿 0 = 不同）', 24, T['muted'], bold=True)
    top, ch = y0 + 68, 70
    for i, v in enumerate(nums):
        X = sx + i * cell
        c = T['pink'] if v % 2 else T['cyan']
        cv.rect((X + 4, top, X + cell - 4, top + ch), fill=c, r=8)
        cv.text((X + cell / 2, top + ch / 2), v, 30, T['bg'], anchor='mm', bold=True)
        cv.text((X + cell / 2, top - 6), i, 18, T['dim'], anchor='mb', mono=True)
    if a is None:
        return
    my = top + ch + 44
    cv.text((x0 + 18, my), 'a[i]', 24, T['purple'], anchor='lm', bold=True, mono=True)
    for i, v in enumerate(a):
        bx = sx + (i + 1) * cell
        c = T['red'] if v else T['green']
        cv.line([(sx + i * cell + cell / 2, top + ch + 6), (bx, my - 18)], T['border'], 2)
        cv.line([(sx + (i + 1) * cell + cell / 2, top + ch + 6), (bx, my - 18)], T['border'], 2)
        cv.rect((bx - 18, my - 18, bx + 18, my + 18), fill=c, r=8)
        cv.text((bx, my), v, 26, T['bg'], anchor='mm', bold=True)


def _draw_q(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    qs, s = S.get('queries'), S.get('s')
    if not qs or not isinstance(s, list):
        return
    n = len(s)
    cell, sx = _geom(box, n)
    done = S.get('_line') == 4
    cv.text((x0 + 18, y0 + 4), 'queries：s[from] == s[to] ？（红 = s[from]，绿 = s[to]）', 24, T['muted'], bold=True)
    rowh = (y1 - y0 - 56) / len(qs)
    for k, (f, t) in enumerate(qs):
        y = y0 + 56 + k * rowh + rowh / 2
        a, b = sx + f * cell + cell / 2, sx + t * cell + cell / 2
        ok = s[f] == s[t]
        cv.text((x0 + 24, y), f'[{f}, {t}]', 26, T['text'] if done else T['muted'], anchor='lm', bold=True, mono=True)
        cv.line([(a, y), (b, y)], (T['green'] if ok else T['pink']) if done else T['border'], 5)
        cv.rect((a - 9, y - 9, a + 9, y + 9), fill=T['red'], r=9)
        cv.rect((b - 9, y - 9, b + 9, y + 9), fill=T['green'], r=9)
        if done:
            cv.text((sx + n * cell + 20, y), f'{s[f]} == {s[t]} → {"True" if ok else "False"}', 24,
                    T['green'] if ok else T['pink'], anchor='lm', bold=True)


def _formula(S):
    ln = S.get('_line')
    if ln == 3:
        return '`s[k]` = `a[0] + … + a[k−1]`：`nums[0..k]` 里奇偶相同的相邻对数'
    if ln == 4:
        return '`s[from] == s[to]` ⇔ `a[from..to−1]` 全是 0 ⇔ 没有奇偶相同的相邻对'
    return ''


def _acc(S, B, ret):
    return (f'相邻两数奇偶相同记 `1`、不同记 `0`：`a = {_a(S)}`；`accumulate(..., initial=0)` 求前缀和 → '
            f'`s = {S.s}`，`s[0] = 0`')


def _ret(S, B, ret):
    parts = []
    for f, t in S.queries:
        ok = S.s[f] == S.s[t]
        parts.append(f'`[{f},{t}]`：`s[{f}] == s[{t}]` → `{S.s[f]} == {S.s[t]}` → ==' + str(ok) + '==')
    return '；'.join(parts)


CONFIG = dict(
    num=3152, title='特殊数组 II', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 · 相邻奇偶转 01',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1523'],
    code='''
class Solution:
    def isArraySpecial(self, nums: List[int], queries: List[List[int]]) -> List[bool]:
        s = list(accumulate((x % 2 == y % 2 for x, y in pairwise(nums)), initial=0))
        return [s[from_] == s[to] for from_, to in queries]
''',
    call=f'Solution().isArraySpecial({NUMS}, {QUERIES})',
    expect=[False, True, True, False],
    views=[
        dict(type='text', fn=_formula, h=56),
        dict(type='custom', draw=_draw_nums, h=212),
        dict(type='array', var='s', label='s（s[k] 对齐 nums[k]；长度 n，s[0] = 0）', cell=CELL, h=150),
        dict(type='custom', draw=_draw_q, h=210),
    ],
    watch=[],
    captions={
        's = list(accumulate': _acc,
        'return [s[from_]': _ret,
    },
    cards=dict(
        one_liner='相邻奇偶相同记 1：子数组里 1 的个数为 0，才是特殊数组',
        complexity='时间 `O(n+q)`，空间 `O(n)`（返回值不计入）',
        problem=['数组里==每一对相邻元素奇偶性都不同==，就是特殊数组',
                 '每个查询 `[from, to]`：问 `nums[from..to]` 是不是特殊数组',
                 '示例：`nums = [4,3,1,6]`，`queries = [[0,2],[2,3]]` → `[false,true]`',
                 '本视频：`[4,3,1,6,5,2]`，4 个查询'],
        quote='如果 a 的下标从 from 到 to-1 的子数组和等于 0，就说明 nums 的下标从 from 到 to 的这个子数组，其所有相邻元素的奇偶性都不同，该子数组为特殊数组。',
        quote_src='—— 灵茶山艾府题解（方法一）',
        idea=['只要有一对相邻元素奇偶性相同，就不是特殊数组',
              '定义 `a[i]`：相同记 `1`，不同记 `0`；子数组和为 `0` ⇔ 全是 `0`',
              '对 `a` 算前缀和 `s`：`a[from..to-1]` 的和 = `s[to] − s[from]`，等于 0 就是 `s[from] == s[to]`'],
        result='四个查询的答案：`[False, True, True, False]` ✓',
        after=[dict(heading='另外两种写法', lines=[
            '位运算：`(x ^ y ^ 1) & 1` 就是 `a[i]`，异或的最低位取反',
            '方法二：记录最近一次奇偶相同的位置 `last_same[i]`，`O(1)` 判断 `last_same[to] <= from_`',
            '⚠ `last_same[to] == from` 时 `j-1` 在区间外，仍然是特殊数组'])],
        summary=['时间 `O(n+q)`，空间 `O(n)`',
                 '易错：`a` 只有 `n−1` 项，`s` 有 `n` 项；`a[from..to−1]` 的和是 `s[to] − s[from]`',
                 '不用再减一：`initial=0` 让 `s[k]` 恰好是前 `k` 个 `a` 的和',
                 '同类题：前缀和基础（303、3427、2559）'],
    ),
)
