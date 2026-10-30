NUMS = [1, 2, 3, 4]


def _f(t):
    a, b = t
    if b == 1:
        return str(a)
    if b < 0:
        a, b = -a, -b
    return f'{a}/{b}'


def _bits(k):
    return [i for i in range(4) if k >> i & 1]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    rd = S.get('res_dict')
    cv.text((x0 + 18, y0 + 4), 'res_dict[k]：k 的二进制表示选了哪些数，值是所有结果 (分子, 分母)', 24, T['muted'], bold=True)
    if rd is None:
        return
    line = S.get('_line')
    phase2 = line is not None and line >= 16
    k = S.get('k')
    for r, key in enumerate(sorted(rd)):
        Y = y0 + 48 + r * 66
        idx = _bits(key)
        is_k = phase2 and key == k
        is_o = phase2 and k is not None and key == 15 - k
        if is_k or is_o:
            cv.rect((x0 + 14, Y - 6, x1 - 14, Y + 52), fill=T['blue'] if is_k else T['pink'], alpha=40, r=10)
        lab = f'k={key:04b}'
        cv.text((x0 + 24, Y + 8), lab, 22, T['blue'] if is_k else (T['pink'] if is_o else T['muted']), mono=True, bold=True)
        cv.text((x0 + 24, Y + 34), '(' + ', '.join(str(NUMS[i]) for i in idx) + ')', 20, T['dim'], mono=True)
        xx = x0 + 170
        for t in rd[key]:
            s_ = _f(t)
            w = cv.tlen(s_, 24, mono=True) + 20
            on = (is_k and (S.get('x1'), S.get('y1')) == t) or (is_o and (S.get('x2'), S.get('y2')) == t)
            cv.rect((xx, Y, xx + w, Y + 44), fill=T['yellow'] if on else T['panel2'], r=8, outline=T['border'])
            cv.text((xx + w / 2, Y + 22), s_, 24, T['bg'] if on else T['text'], anchor='mm', mono=True, bold=True)
            xx += w + 8
        if not rd[key]:
            cv.text((xx, Y + 22), '{ }', 22, T['dim'], anchor='lm', mono=True)


def _check(S):
    line = S.get('_line')
    if 'x2' not in S or line not in (21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32):
        return '结果存成 `(分子, 分母)`；两组结果 a、b 再试 6 种运算'
    a, b = _f((S['x1'], S['y1'])), _f((S['x2'], S['y2']))
    return f'`a = {a}`（左边两个数），`b = {b}`（右边两个数）'


def _cap_cond(expr, desc):
    def f(S, B, ret):
        x1, y1, x2, y2 = S.x1, S.y1, S.x2, S.y2
        ok = eval(expr, {}, dict(x1=x1, y1=y1, x2=x2, y2=y2))
        a, b = _f((x1, y1)), _f((x2, y2))
        a, b = (f'({a})' if '/' in a or a.startswith('-') else a), (f'({b})' if '/' in b or b.startswith('-') else b)
        return f'`{desc.format(a=a, b=b)}`' + (' = 24 ✓ → ==找到了==' if ok else ' ≠ 24')
    return f


CONFIG = dict(
    num=679, title='24 点游戏', difficulty='Hard', category='回溯',
    author='yiduobo', technique='状态压缩 · 分子分母存所有结果',
    tags=['字节30天'],
    code='''
class Solution(object):
    def judgePoint24(self, nums):
        res_dict = {}
        for i in range(3):
            for j in range(i + 1, 4):
                k = (1 << i) + (1 << j)
                x, y = nums[i], nums[j]
                res_dict[k] = set()
                res_dict[k].add((x + y, 1))
                res_dict[k].add((x - y, 1))
                res_dict[k].add((y - x, 1))
                res_dict[k].add((x * y, 1))
                res_dict[k].add((x, y))
                res_dict[k].add((y, x))

        for i in range(3):
            for j in range(i + 1, 4):
                k = (1 << i) + (1 << j)
                for (x1, y1) in res_dict[k]:
                    for (x2, y2) in res_dict[15 - k]:
                        if x1 * y2 + x2 * y1 == 24 * y1 * y2:
                            return True
                        elif x1 * y2 - x2 * y1 == 24 * y1 * y2:
                            return True
                        elif x2 * y1 - x1 * y2 == 24 * y1 * y2:
                            return True
                        elif x1 * x2 == 24 * y1 * y2:
                            return True
                        elif x1 != 0 and x1 * y2 * 24 == x2 * y1:
                            return True
                        elif x2 != 0 and x1 * y2 == x2 * y1 * 24:
                            return True

                for l in range(4):
                    if k & (1 << l) == 0:
                        tmp = k + (1 << l)
                        if tmp not in res_dict:
                            res_dict[tmp] = set()
                        for (x, y) in res_dict[k]:
                            res_dict[tmp].add((x + nums[l] * y, y))
                            res_dict[tmp].add((x - nums[l] * y, y))
                            res_dict[tmp].add((nums[l] * y - x, y))
                            res_dict[tmp].add((x * nums[l], y))
                            res_dict[tmp].add((x, y * nums[l]))
                            if x != 0:
                                res_dict[tmp].add((y * nums[l], x))

        for i in range(4):
            j = 15 - (1 << i)
            for (x, y) in res_dict[j]:
                if nums[i] * y + x == 24 * y:
                    return True
                elif nums[i] * y - x == 24 * y:
                    return True
                elif x - nums[i] * y == 24 * y:
                    return True
                elif x * nums[i] == 24 * y:
                    return True
                elif x == 24 * y * nums[i]:
                    return True
                elif x != 0 and nums[i] * y == 24 * x:
                    return True


        return False
''',
    call=f'Solution().judgePoint24({NUMS})',
    expect=True,
    skip=['res_dict[k].add', 'x, y = nums[i], nums[j]', 4, 5],
    views=[
        dict(type='text', fn=_check, h=56, size=26),
        dict(type='custom', draw=_draw, h=500),
    ],
    watch=[('i', 'i'), ('j', 'j'), ('k', 'k', 'blue'), ('(x1, y1)', '(x1, y1)', 'blue'), ('(x2, y2)', '(x2, y2)', 'pink')],
    captions={
        'res_dict = {}': '`res_dict[k]`：k 的二进制里为 1 的那些数，能算出的==所有结果==',
        6: lambda S, B, r: (f'选 `nums[{S.i}] = {S.nums[S.i]}` 和 `nums[{S.j}] = {S.nums[S.j]}`：`k = 2^{S.i} + 2^{S.j}` = `{S.k:04b}`'
                            if S.k == 3 else f'数对 `({S.nums[S.i]}, {S.nums[S.j]})`：`k = {S.k:04b}`'),
        'res_dict[k] = set()': lambda S, B, r: (f'`{S.x}`、`{S.y}` 的六种结果 `x+y, x−y, y−x, x·y, x/y, y/x` '
                                                f'以 ==(分子, 分母)== 存进集合，不用浮点数' if S.k == 3
                                                else f'`{S.x}`、`{S.y}` 的六种结果存进 `res_dict[{S.k:04b}]`'),
        'for i in range(3)': lambda S, B, r: f'第二步：枚举左边的数对 `i = {S.i}`',
        'for j in range(i + 1, 4)': lambda S, B, r: f'`j = {S.j}`',
        18: lambda S, B, r: (f'左边选 `({S.nums[S.i]}, {S.nums[S.j]})`：`k = {S.k:04b}`；'
                             f'右边就是剩下两个数 `15 − k = {15 - S.k:04b}`'),
        'for (x1, y1) in res_dict[k]': lambda S, B, r: f'左边取一个结果 `a = {_f((S.x1, S.y1))}`',
        'for (x2, y2) in res_dict[15 - k]': lambda S, B, r: f'右边取一个结果 `b = {_f((S.x2, S.y2))}`',
        'if x1 * y2 + x2 * y1 == 24 * y1 * y2': _cap_cond('x1 * y2 + x2 * y1 == 24 * y1 * y2', 'a + b = {a} + {b}'),
        'elif x1 * y2 - x2 * y1 == 24 * y1 * y2': _cap_cond('x1 * y2 - x2 * y1 == 24 * y1 * y2', 'a − b = {a} − {b}'),
        'elif x2 * y1 - x1 * y2 == 24 * y1 * y2': _cap_cond('x2 * y1 - x1 * y2 == 24 * y1 * y2', 'b − a = {b} − {a}'),
        'elif x1 * x2 == 24 * y1 * y2': _cap_cond('x1 * x2 == 24 * y1 * y2', 'a × b = {a} × {b}'),
        'elif x1 != 0 and x1 * y2 * 24 == x2 * y1': _cap_cond('x1 != 0 and x1 * y2 * 24 == x2 * y1', 'b ÷ a = {b} ÷ {a}'),
        'elif x2 != 0 and x1 * y2 == x2 * y1 * 24': _cap_cond('x2 != 0 and x1 * y2 == x2 * y1 * 24', 'a ÷ b = {a} ÷ ({b})'),
        'return True': '左组 `1 ÷ 2`、右组 `3 × 4`：`(3 × 4) ÷ (1 ÷ 2) = 24` → 返回 ==True==',
    },
    cards=dict(
        one_liner='先两两配对存下所有结果，再看两组结果能否凑出 24；分子分母分开存，避免浮点误差',
        complexity='时间 `O(1)`（4 张牌，状态数固定），空间 `O(1)`',
        problem=['给 4 张牌，每张是 `[1, 9]` 的数字',
                 '用 `+ − × /`（实数除法）和括号组成表达式，问能否==得到 24==',
                 '示例：`[4,1,8,7]` → `true`：`(8−4) × (7−1)`；`[1,2,1,2]` → `false`',
                 '本视频：`[1,2,3,4]`'],
        quote='先两两配对，用set记录下某两个数通过加减乘除可以形成的所有结果，然后枚举这些数对看是否存在两个结果可以构成24。若不能，将第三个数加入到这些数对中……然后看这些结果能否与第四个数构成24。',
        quote_src='—— yiduobo 题解原文',
        idea=['`res_dict[k]`：k 的二进制表示选了哪些数（状态压缩），值是它们能算出的所有结果',
              '情况一：==两两分组==，左组结果 a、右组结果 b，检查六种运算',
              '情况二：三个数一组再和第四个数运算（本例在情况一就找到了）',
              '结果存成 `(分子, 分母)`，比较时交叉相乘，==不会有浮点误差=='],
        result='`(3 × 4) ÷ (1 ÷ 2) = 24` → `True`',
        after=[dict(heading='情况二：3 + 1（原文后半段代码）', lines=[
            '对每个两数组 k，枚举不在 k 里的第三个数 l：`tmp = k + (1 << l)`',
            '把 `res_dict[k]` 里的每个结果和 `nums[l]` 做六种运算，存进 `res_dict[tmp]`',
            '最后枚举第四个数 i：`res_dict[15 − (1 << i)]` 的结果和 `nums[i]` 运算看能否得 24',
            '除法 `(y·nums[l], x)` 要先判 `x != 0`，避免分母为 0',
        ])],
        summary=['只有 4 张牌，状态和结果数都是常数级',
                 '易错：两两分组和 3+1 两种结构都要考虑，缺一不可',
                 '技巧：`a/b = 24` 写成 `a = 24·b` 的交叉相乘形式，全程整数运算',
                 '对比灵神：灵神每次合并两张牌递归，代码更短；yiduobo 按状态压缩逐层枚举',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
