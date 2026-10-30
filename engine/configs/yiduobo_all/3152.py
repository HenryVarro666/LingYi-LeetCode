NUMS = [1, 2, 3, 3, 4, 6]
QUERIES = [[0, 2], [1, 3], [3, 4], [2, 5]]
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
        return []
    return [s[i + 1] - s[i] for i in range(len(s) - 1)]


def _loop(S):
    if 'index' not in S or S.get('_line') not in (4, 5, 6, 7) or 's' not in S:
        return False
    return not (S['_line'] == 4 and len(S['s']) == len(S['nums']))


def _draw_nums(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    nums = S.get('nums')
    if not nums:
        return
    n = len(nums)
    cell, sx = _geom(box, n)
    a = _a(S)
    cur = S['index'] if _loop(S) and S['index'] < n else None
    cv.text((x0 + 18, y0 + 4), 'nums（粉奇青偶）与 01 数组（红 1 = 相邻奇偶相同，绿 0 = 不同）', 24, T['muted'], bold=True)
    top, ch = y0 + 68, 70
    for i, v in enumerate(nums):
        X = sx + i * cell
        c = T['pink'] if v % 2 else T['cyan']
        cv.rect((X + 4, top, X + cell - 4, top + ch), fill=c, r=8)
        cv.text((X + cell / 2, top + ch / 2), v, 30, T['bg'], anchor='mm', bold=True)
        cv.text((X + cell / 2, top - 6), i, 18, T['dim'], anchor='mb', mono=True)
        if cur is not None and i in (cur - 1, cur):
            cv.rect((X + 1, top - 3, X + cell - 1, top + ch + 3), outline=T['yellow'], width=4, r=10)
    my = top + ch + 44
    cv.text((x0 + 18, my), '01', 24, T['purple'], anchor='lm', bold=True, mono=True)
    for i, v in enumerate(a):
        bx = sx + (i + 1) * cell
        c = T['red'] if v else T['green']
        cv.line([(sx + i * cell + cell / 2, top + ch + 6), (bx, my - 18)], T['border'], 2)
        cv.line([(sx + (i + 1) * cell + cell / 2, top + ch + 6), (bx, my - 18)], T['border'], 2)
        cv.rect((bx - 18, my - 18, bx + 18, my + 18), fill=c, r=8,
                outline=T['yellow'] if cur is not None and i == cur - 1 else None, width=3)
        cv.text((bx, my), v, 26, T['bg'], anchor='mm', bold=True)


def _draw_q(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    qs, s = S.get('queries'), S.get('s')
    if not qs or not isinstance(s, list):
        return
    n = len(S.get('nums') or s)
    cell, sx = _geom(box, n)
    done = S.get('_line') == 9
    cv.text((x0 + 18, y0 + 4), 'queries：s[x] == s[y] ？（红 = s[x]，绿 = s[y]）', 24, T['muted'], bold=True)
    rowh = (y1 - y0 - 56) / len(qs)
    for k, (x, y_) in enumerate(qs):
        y = y0 + 56 + k * rowh + rowh / 2
        a, b = sx + x * cell + cell / 2, sx + y_ * cell + cell / 2
        ok = done and s[x] == s[y_]
        cv.text((x0 + 24, y), f'[{x}, {y_}]', 26, T['text'] if done else T['muted'], anchor='lm', bold=True, mono=True)
        cv.line([(a, y), (b, y)], (T['green'] if ok else T['pink']) if done else T['border'], 5)
        cv.rect((a - 9, y - 9, a + 9, y + 9), fill=T['red'], r=9)
        cv.rect((b - 9, y - 9, b + 9, y + 9), fill=T['green'], r=9)
        if done:
            cv.text((sx + n * cell + 20, y), f'{s[x]} == {s[y_]} → {"True" if ok else "False"}', 24,
                    T['green'] if ok else T['pink'], anchor='lm', bold=True)


def _formula(S):
    ln = S.get('_line')
    if ln == 3:
        return '`s[k]` = `nums[0..k]` 里奇偶相同的相邻对数；`s[0] = 0`'
    if _loop(S):
        i, nums = S['index'], S['nums']
        if ln == 4:
            return f'比较 `nums[{i - 1}] = {nums[i - 1]}` 和 `nums[{i}] = {nums[i]}` 这一对'
        if ln == 5:
            return '`s` 先多一项，抄上一项（先假设这对奇偶不同）'
        if ln == 6:
            t = nums[i] + nums[i - 1]
            return f'`{nums[i]} + {nums[i - 1]} = {t}`，和为{"偶" if t % 2 == 0 else "奇"}数 → 奇偶==' + ('相同' if t % 2 == 0 else '不同') + '=='
        return f'奇偶相同：最后一项 +1 → `s[{len(S["s"]) - 1}] = {S["s"][-1]}`'
    if ln == 4:
        return '所有相邻对都看过了，`s` 建好'
    if ln == 9:
        return '`s[x] == s[y]` ⇔ `[x, y]` 里==没有==奇偶相同的相邻对'
    return ''


def _for(S, B, ret):
    if 'index' in B and B.index == S.index:
        return f'所有相邻对都扫完：`s = {S.s}`'
    i = S.index
    return f'`index = {i}`：看 `nums[{i - 1}] = {S.nums[i - 1]}` 和 `nums[{i}] = {S.nums[i]}` 这一对'


def _app(S, B, ret):
    return f'`s` 末尾补一项，先抄上一项 `{S.s[-1]}`：暂时认为这一对奇偶不同'


def _if(S, B, ret):
    i = S.index
    t = S.nums[i] + S.nums[i - 1]
    if t % 2 == 0:
        return f'`({S.nums[i]} + {S.nums[i - 1]}) % 2 = 0` → 两数之和为偶数，==奇偶相同=='
    return f'`({S.nums[i]} + {S.nums[i - 1]}) % 2 = 1` → 两数之和为奇数，奇偶不同，`s` 保持不变'


def _ret(S, B, ret):
    parts = []
    for x, y in S.queries:
        ok = S.s[x] == S.s[y]
        parts.append(f'`[{x},{y}]`：`s[{x}] == s[{y}]` → `{S.s[x]} == {S.s[y]}` → ==' + str(ok) + '==')
    return '；'.join(parts)


CONFIG = dict(
    num=3152, title='特殊数组 II', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和 · 相邻转 01，区间和为 0',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1523'],
    code='''
class Solution(object):
    def isArraySpecial(self, nums, queries):
        s = [0]
        for index in range(1, len(nums)):
            s.append(s[-1])
            if (nums[index] + nums[index - 1]) % 2 == 0:
                s[-1] += 1

        return [s[x] == s[y] for x, y in queries]
''',
    call=f'Solution().isArraySpecial({NUMS}, {QUERIES})',
    expect=[True, False, True, False],
    views=[
        dict(type='text', fn=_formula, h=56),
        dict(type='custom', draw=_draw_nums, h=212),
        dict(type='array', var='s', label='s（s[k] 对齐 nums[k]：前 k+1 个数里奇偶相同的相邻对数）', cell=CELL, h=150,
             min_slots=len(NUMS)),
        dict(type='custom', draw=_draw_q, h=210),
    ],
    watch=['index'],
    captions={
        's = [0]': '`s[0] = 0`：只有 `nums[0]` 一个数，没有相邻对',
        'for index in range': _for,
        's.append(s[-1])': _app,
        'if (nums[index]': _if,
        's[-1] += 1': '奇偶相同 → 最后一项 +1：`s[{len(s) - 1}] = {s[-1]}`',
        'return [s[x]': _ret,
    },
    cards=dict(
        one_liner='相邻奇偶相同记 1，区间和为 0 才是特殊数组',
        complexity='时间 `O(n+q)`，空间 `O(n)`',
        problem=['特殊数组：每一对相邻元素的奇偶性都不同',
                 '每个查询 `[x, y]` 问：子数组 `nums[x..y]` 是不是特殊数组',
                 '示例：`nums = [4,3,1,6]`，`[[0,2],[2,3]]` → `[false,true]`',
                 '本视频：`[1,2,3,3,4,6]`，4 个查询 → `[True,False,True,False]`'],
        quote='对于这类通过相邻元素判断数组是否符合某种条件的问题，一种常见的做法就是先根据相邻元素的具体情况将数组转化为01数组',
        quote_src='—— yiduobo 题解原文',
        idea=['相邻两数同奇偶就置 `1`，否则置 `0`',
              '符合条件的子数组，对应的 01 必然==全为 0==，即区间和为 0',
              '提前预处理前缀和 `s`：`s[x] == s[y]` 就说明 `[x, y]` 里没有相邻同奇偶'],
        summary=['时间 `O(n+q)`，空间 `O(n)`',
                 '判断同奇偶：`(nums[index] + nums[index - 1]) % 2 == 0`，两数之和为偶数 ⇔ 奇偶相同',
                 '易错：`s` 有 `n` 项，`s[x]` 对齐 `nums[x]`，比较 `s[x] == s[y]`，不是 `s[y + 1]`',
                 '对比灵神：灵神用 `pairwise` + `accumulate` 一行建 `s`；这里是显式循环',
                 '同类：3151 特殊数组 I（同样是看相邻对）'],
    ),
)
