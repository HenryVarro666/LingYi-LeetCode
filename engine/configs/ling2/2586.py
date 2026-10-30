WORDS = ['hey', 'aeo', 'mu', 'ooo', 'artro']
LEFT, RIGHT = 1, 4
VOW = 'aeiou'


def _draw(cv, S, B, box, T):
    """生成器表达式在一步之内算完：把每个 s 的判断画成一张静态表"""
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), f'words[left:right+1] = words[{LEFT}:{RIGHT + 1}]（框内才统计）', 24, T['muted'], bold=True)
    n = len(WORDS)
    cw = min(180, (x1 - x0 - 60) / n)
    sx = x0 + 30 + ((x1 - x0 - 60) - cw * n) / 2
    y = y0 + 56
    # 窗口
    wx0, wx1 = sx + LEFT * cw - 6, sx + (RIGHT + 1) * cw + 6
    cv.rect((wx0, y - 8, wx1, y + 244), fill=T['cyan'], alpha=28, r=14)
    cv.rect((wx0, y - 8, wx1, y + 244), outline=T['cyan'], width=3, r=14)
    total = 0
    for i, s in enumerate(WORDS):
        X = sx + i * cw
        inside = LEFT <= i <= RIGHT
        cv.text((X + cw / 2, y + 4), i, 18, T['dim'], anchor='mt', mono=True)
        # 单词：首尾字母上色
        L = len(s)
        lw = min(30, (cw - 16) / L)
        lx = X + (cw - lw * L) / 2
        for k, ch in enumerate(s):
            edge = k == 0 or k == L - 1
            c = T['text']
            if edge and inside:
                c = T['green'] if ch in VOW else T['red']
            cv.text((lx + k * lw + lw / 2, y + 60), ch, 34, c if inside else T['dim'], anchor='mm', bold=edge, mono=True)
        if not inside:
            cv.text((X + cw / 2, y + 120), '不在范围', 20, T['dim'], anchor='mm')
            continue
        a, b = s[0] in VOW, s[-1] in VOW
        cv.text((X + cw / 2, y + 112), f"s[0]='{s[0]}' {'✓' if a else '×'}", 20, T['green'] if a else T['red'], anchor='mm', mono=True)
        cv.text((X + cw / 2, y + 144), f"s[-1]='{s[-1]}' {'✓' if b else '×'}", 20, T['green'] if b else T['red'], anchor='mm', mono=True)
        ok = a and b
        total += ok
        cv.rect((X + 16, y + 176, X + cw - 16, y + 226), fill=T['green'] if ok else T['panel2'], r=10)
        cv.text((X + cw / 2, y + 201), 'True → 1' if ok else 'False → 0', 22, T['bg'] if ok else T['muted'], anchor='mm', bold=True)
    yy = y + 290
    terms = ' + '.join('1' if (w[0] in VOW and w[-1] in VOW) else '0' for w in WORDS[LEFT:RIGHT + 1])
    cv.rich(x0 + 40, yy, f'`sum(...)` = `{terms}` = =={total}==', x1 - x0 - 80, size=30)
    cv.rich(x0 + 40, yy + 70, 'Python 中 `True` 当作 1、`False` 当作 0，所以 `sum` 直接数出 True 的个数', x1 - x0 - 80, size=24,
            color=T['muted'])


CONFIG = dict(
    num=2586, title='统计范围内的元音字符串数', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='遍历 · 一行 sum',
    tags=['List.md'],
    code='''
class Solution:
    def vowelStrings(self, words: List[str], left: int, right: int) -> int:
        return sum(s[0] in "aeiou" and s[-1] in "aeiou" for s in words[left:right+1])
''',
    call=f'Solution().vowelStrings({WORDS}, {LEFT}, {RIGHT})',
    expect=3,
    views=[dict(type='custom', draw=_draw, h=620)],
    watch=[('left', 'left'), ('right', 'right')],
    captions={
        'return sum': '遍历 `words[1:5]`：每个 `s` 只看==首字母和尾字母==是否都在 `"aeiou"` 里，`sum` 数出 True 的个数 → =={ret}==',
    },
    cards=dict(
        one_liner='只看首尾两个字母：都是元音就计数',
        complexity='时间 `O(right − left)`，空间 `O(1)`',
        problem=['给字符串数组 `words` 和整数 `left`、`right`',
                 '==以元音开头并以元音结尾==的字符串叫元音字符串（元音：`a e i o u`）',
                 '统计下标在闭区间 `[left, right]` 内的元音字符串个数',
                 '示例：`["hey","aeo","mu","ooo","artro"]`，`left = 1`，`right = 4` → `3`'],
        quote='遍历下标在 [left,right] 内的字符串 s=words[i]，如果 ==s 的第一个字母和最后一个字母都是元音==，把答案加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['闭区间 `[left, right]` 对应切片 `words[left:right+1]`',
              '`s[0] in "aeiou" and s[-1] in "aeiou"` 得到 True / False',
              '`sum(...)`：True 算 1、False 算 0，一行数完'],
        result='`aeo`、`ooo`、`artro` 是元音字符串，`mu` 不是 → `3` ✓',
        after=[dict(heading='把一行代码展开成循环', lines=[
            '`ans = 0`',
            '`for s in words[left:right+1]:`',
            '`    if s[0] in "aeiou" and s[-1] in "aeiou":`',
            '`        ans += 1`',
            '生成器表达式在 `sum` 内部一次算完，所以动画只有一步'])],
        summary=['时间 `O(right − left)`：每个字符串只取首尾两个字母，==不遍历整个字符串==',
                 '空间 `O(1)`：生成器表达式不建列表（切片本身会复制一段引用）',
                 '易错：右端点是闭区间，切片要写 `right + 1`',
                 '长度为 1 的字符串（如 `"u"`）首尾是同一个字母，同样适用'],
    ),
)
