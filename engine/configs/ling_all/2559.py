WORDS = ["aba", "bcb", "ece", "aa", "e"]
QUERIES = [[0, 2], [1, 4], [1, 1]]


def _valid(S):
    s = S.get('s')
    if not isinstance(s, list) or 'words' not in S:
        return None
    return [s[i + 1] - s[i] for i in range(len(S['words']))]


def _words_color(S, i, v):
    val = _valid(S)
    return 'green' if val and val[i] else None


def _formula(S):
    ln = S.get('_line')
    if ln == 3:
        return '`is_valid(w)`：`w[0]` 和 `w[-1]` 都是元音 → ==1==，否则 0'
    if ln == 4:
        return f"01 数组 `{_valid(S)}` 的前缀和：`s[k]` = 前 `k` 个里==符合要求的个数=="
    if ln == 5:
        return '区间 `[l, r]` 里的个数 = `s[r+1] − s[l]`'
    return ''


def _draw_q(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    qs, s = S.get('queries'), S.get('s')
    if not qs or not isinstance(s, list):
        return
    n1 = len(s)
    width = x1 - x0 - 40
    cell = max(24, min(96, width / n1))
    sx = x0 + 20 + (width - cell * n1) / 2
    done = S.get('_line') == 5
    cv.text((x0 + 18, y0 + 4), 'queries：每个区间对应 s 上的两个点（红 = s[l]，绿 = s[r+1]）', 24, T['muted'], bold=True)
    rowh = (y1 - y0 - 60) / len(qs)
    for k, (l, r) in enumerate(qs):
        y = y0 + 64 + k * rowh + rowh / 2
        a, b = sx + l * cell + cell / 2, sx + (r + 1) * cell + cell / 2
        cv.text((x0 + 24, y), f'[{l}, {r}]', 26, T['text'] if done else T['muted'], anchor='lm', bold=True, mono=True)
        cv.line([(a, y), (b, y)], T['cyan'] if done else T['border'], 5)
        cv.rect((a - 9, y - 9, a + 9, y + 9), fill=T['red'], r=9)
        cv.rect((b - 9, y - 9, b + 9, y + 9), fill=T['green'], r=9)
        if done:
            cv.text((a, y - 14), f's[{l}]={s[l]}', 20, T['red'], anchor='mb', bold=True)
            cv.text((b, y - 14), f's[{r + 1}]={s[r + 1]}', 20, T['green'], anchor='mb', bold=True)
            cv.text((sx + n1 * cell + 16, y), f'{s[r + 1]} − {s[l]} = {s[r + 1] - s[l]}', 26, T['yellow'], anchor='lm', bold=True)


def _lam(S, B, ret):
    return '`is_valid(s)`：首字母、尾字母都是元音才为真；长度为 1 的单词 `s[0]` 和 `s[-1]` 是同一个字母，也成立'


def _acc(S, B, ret):
    val = _valid(S)
    return f'`is_valid` 把每个单词变成 0/1：`{val}`；`accumulate(..., initial=0)` 求前缀和 → `s = {S.s}`（长 `n+1`，`s[0] = 0`）'


def _ret(S, B, ret):
    parts = [f'`[{l},{r}]`：`s[{r + 1}] − s[{l}]` = =={S.s[r + 1] - S.s[l]}==' for l, r in S.queries]
    return '列表推导式一次回答所有询问：' + '；'.join(parts)


CONFIG = dict(
    num=2559, title='统计范围内的元音字符串数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 · 01 数组',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1435'],
    code='''
class Solution:
    def vowelStrings(self, words: List[str], queries: List[List[int]]) -> List[int]:
        is_valid = lambda s: s[0] in "aeiou" and s[-1] in "aeiou"
        s = list(accumulate(map(is_valid, words), initial=0))
        return [s[r + 1] - s[l] for l, r in queries]
''',
    call=f'Solution().vowelStrings({WORDS}, {QUERIES})',
    expect=[2, 3, 0],
    views=[
        dict(type='text', fn=_formula, h=56),
        dict(type='array', var='words', label='words（绿 = 首尾都是元音，记 1）', cell=96, h=170, color=_words_color),
        dict(type='array', var='s', label='s（s[k] = 前 k 个数的和，长度 n+1）', cell=96, h=170, color=lambda S, i, v: 'cyan'),
        dict(type='custom', draw=_draw_q, h=200),
    ],
    watch=[],
    captions={
        'is_valid = lambda': _lam,
        's = list(accumulate': _acc,
        'return [s[r + 1]': _ret,
    },
    cards=dict(
        one_liner='符合要求记 1，其余记 0：数个数就是区间求和，交给前缀和',
        complexity='时间 `O(n+q)`，空间 `O(n)`',
        problem=['`words` 是小写字符串数组，每个查询 `[l, r]` 问下标 `l..r` 里有几个字符串==首尾都是元音==',
                 '元音字母：`a` `e` `i` `o` `u`',
                 '示例：`words = ["aba","bcb","ece","aa","e"]`',
                 '`queries = [[0,2],[1,4],[1,1]]` → `[2,3,0]`'],
        quote='如果 words[i] 符合要求，视作 1，否则视作 0。计算这个 01 数组的前缀和数组 s，就可以 O(1) 回答每个询问了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['符合要求的字符串记 `1`，其余记 `0`：区间计数变成==区间求和==',
              '前缀和 `s[k]` 是前 `k` 个数的和，`s[0] = 0`',
              '`[l, r]` 里符合要求的个数 = `s[r+1] − s[l]`，每个询问 `O(1)`'],
        result='三个询问依次得到 `[2, 3, 0]` ✓',
        after=[dict(heading='代码里的几个写法', lines=[
            '`is_valid` 是 lambda：首尾字母都在 `"aeiou"` 里，布尔值当 0/1 用',
            '`map(is_valid, words)` 逐个判断，得到 01 序列',
            '`accumulate(..., initial=0)` 在开头垫一个 0，`s` 长度是 `n+1`',
            '列表推导式把所有询问一次算完'])],
        summary=['时间 `O(n+q)`，空间 `O(n)`：`n` 是 `words` 长度，`q` 是询问个数',
                 '易错：`s` 长 `n+1`，答案是 `s[r + 1] − s[l]`，不是 `s[r] − s[l]`',
                 '只看首尾字母：`s[0]` 和 `s[-1]`，单字母单词两个下标指向同一个字母',
                 '同类题：前缀和基础（303、3427、3152）'],
    ),
)
