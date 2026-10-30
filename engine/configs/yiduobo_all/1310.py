ARR = [1, 3, 4, 8]
QUERIES = [[0, 1], [1, 2], [0, 3], [3, 3]]


def _k(S):
    """index of the current num while building s"""
    if 'num' not in S or 's' not in S or S.get('_line') not in (4, 5):
        return None
    k = len(S['s']) if S['_line'] == 4 else len(S['s']) - 1
    return k if k < len(S['arr']) else None


def _arr_color(S, i, v):
    return 'blue' if _k(S) == i else None


def _s_color(S, i, v):
    return 'cyan' if S.get('_line') == 7 else None


def _b(v):
    return format(v, '04b')


def _formula(S):
    ln = S.get('_line')
    if ln == 3:
        return '`s[k]` = `arr[0] ^ … ^ arr[k]`，先放 `s[0] = arr[0]`'
    if ln == 4:
        k = _k(S)
        if k is None:
            return '所有前缀异或都算好了'
        return f'`arr[{k}] = {S["num"]}`（二进制 `{_b(S["num"])}`）：接到前缀后面'
    if ln == 5:
        s = S['s']
        return f'`{_b(s[-2])}` ^ `{_b(S["num"])}` = `{_b(s[-1])}` = =={s[-1]}==（同位相同得 0，不同得 1）'
    if ln == 7:
        return '`l = 0` 取 `s[r]`；否则 `s[l-1] ^ s[r]`，重叠的前缀异或两次抵消'
    return ''


def _draw_q(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    qs, s = S.get('queries'), S.get('s')
    if not qs or not isinstance(s, list):
        return
    n = len(s)
    width = x1 - x0 - 40
    cell = max(24, min(96, width / n))
    sx = x0 + 20 + (width - cell * n) / 2
    done = S.get('_line') == 7
    cv.text((x0 + 18, y0 + 4), 'queries：[l, r] 的异或 = s[l-1] ^ s[r]（红 = s[l-1]，绿 = s[r]）', 24, T['muted'], bold=True)
    rowh = (y1 - y0 - 56) / len(qs)
    for k, (l, r) in enumerate(qs):
        y = y0 + 56 + k * rowh + rowh / 2
        b = sx + r * cell + cell / 2
        a = sx + (l - 1) * cell + cell / 2 if l > 0 else sx - 6
        cv.text((x0 + 24, y), f'[{l}, {r}]', 26, T['text'] if done else T['muted'], anchor='lm', bold=True, mono=True)
        cv.line([(a, y), (b, y)], T['cyan'] if done else T['border'], 5)
        if l > 0:
            cv.rect((a - 9, y - 9, a + 9, y + 9), fill=T['red'], r=9)
        else:
            cv.rect((a - 9, y - 9, a + 9, y + 9), outline=T['dim'], width=3, r=9)
        cv.rect((b - 9, y - 9, b + 9, y + 9), fill=T['green'], r=9)
        if done:
            if l > 0:
                txt = f'{s[l - 1]} ^ {s[r]} = {s[l - 1] ^ s[r]}'
            else:
                txt = f's[{r}] = {s[r]}'
            cv.text((sx + n * cell + 20, y), txt, 26, T['yellow'], anchor='lm', bold=True)


def _for(S, B, ret):
    if len(S.s) == len(S.arr):
        return f'前缀异或算完：`s = {S.s}`'
    return f'取下一个数 `num = arr[{len(S.s)}] = {S.num}`'


def _app(S, B, ret):
    return (f'`s[{len(S.s) - 1}] = s[{len(S.s) - 2}] ^ {S.num}` = `{S.s[-2]} ^ {S.num}` = =={S.s[-1]}==：'
            f'`arr[0..{len(S.s) - 1}]` 的异或')


def _ret(S, B, ret):
    parts = []
    for l, r in S.queries:
        if l == 0:
            parts.append(f'`[{l},{r}]`：`l = 0` 直接取 `s[{r}]` = =={S.s[r]}==')
        else:
            parts.append(f'`[{l},{r}]`：`s[{r}] ^ s[{l - 1}]` = `{S.s[r]} ^ {S.s[l - 1]}` = =={S.s[r] ^ S.s[l - 1]}==')
    return '；'.join(parts)


CONFIG = dict(
    num=1310, title='子数组异或查询', difficulty='Medium', category='位运算',
    author='yiduobo', technique='前缀异或 · A^A=0 抵消',
    tags=['灵神核心路线', '灵神题单·位运算'],
    code='''
class Solution(object):
    def xorQueries(self, arr, queries):
        s = [arr[0]]
        for num in arr[1:]:
            s.append(s[-1] ^ num)

        return [s[r] if l == 0 else s[r] ^ s[l - 1] for l, r in queries]
''',
    call=f'Solution().xorQueries({ARR}, {QUERIES})',
    expect=[2, 7, 14, 8],
    views=[
        dict(type='text', fn=_formula, h=56),
        dict(type='array', var='arr', label='arr', cell=96, h=195, color=_arr_color,
             pointers={_k: 'blue'}, pointer_labels={_k: 'num'}),
        dict(type='array', var='s', label='s（s[k] = arr[0] ^ … ^ arr[k]）', cell=96, h=150, min_slots=len(ARR),
             color=_s_color),
        dict(type='custom', draw=_draw_q, h=230),
    ],
    watch=[],
    captions={
        's = [arr[0]]': '`s[0] = arr[0] = {s[0]}`：`s[k]` 是 `arr[0..k]` 的异或',
        'for num in arr[1:]': _for,
        's.append(s[-1] ^ num)': _app,
        'return [s[r]': _ret,
    },
    cards=dict(
        one_liner='同一个数异或两次会抵消：区间异或 = 两个前缀异或再异或',
        complexity='时间 `O(n+q)`，空间 `O(n)`',
        problem=['给整数数组 `arr` 和查询 `queries[i] = [l, r]`',
                 '每个查询求 `arr[l] ^ arr[l+1] ^ … ^ arr[r]`',
                 '示例：`arr = [1,3,4,8]`，`queries = [[0,1],[1,2],[0,3],[3,3]]`',
                 '输出：`[2,7,14,8]`'],
        quote='注意到异或操作满足A^A = 0，那么这里的区间异或就可以通过前缀操作来完成。',
        quote_src='—— yiduobo 题解原文',
        idea=['`A ^ A = 0`：同一个数异或两遍就消失了',
              '`s[r]` = `arr[0..r]` 的异或，`s[l-1]` = `arr[0..l-1]` 的异或',
              '两者再异或，公共的 `arr[0..l-1]` 抵消，只剩 `arr[l..r]`',
              '`l = 0` 时没有 `s[-1]` 可用，直接取 `s[r]`'],
        summary=['时间 `O(n+q)`，空间 `O(n)`',
                 '易错：`l = 0` 要特判；Python 的 `s[-1]` 不会报错，而是取到最后一项',
                 '异或没有减法，靠 `A ^ A = 0` 来「减掉」前缀',
                 '和前缀和同一个套路：区间 = 两个前缀的「差」'],
    ),
)
