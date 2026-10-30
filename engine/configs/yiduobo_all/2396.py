def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '分两种情况：n = 4 和 n > 4', 24, T['muted'], bold=True)
    cell = 70
    y = y0 + 70
    cv.text((x0 + 30, y + cell / 2), 'n = 4', 28, T['blue'], anchor='lm', bold=True)
    for k, d in enumerate([1, 0, 0]):
        X = x0 + 200 + k * (cell + 8)
        cv.rect((X, y, X + cell, y + cell - 6), fill=T['pink'], r=8)
        cv.text((X + cell / 2, y + (cell - 6) / 2), d, 30, T['bg'], anchor='mm', bold=True)
    cv.text((x0 + 200 + 3 * (cell + 8) + 10, y + cell / 2), '2 进制，不是回文', 24, T['pink'], anchor='lm', bold=True)
    y += 130
    cv.text((x0 + 30, y + cell / 2), 'n > 4', 28, T['orange'], anchor='lm', bold=True)
    for k, d in enumerate([1, 2]):
        X = x0 + 200 + k * (cell + 8)
        cv.rect((X, y, X + cell, y + cell - 6), fill=T['pink'], r=8)
        cv.text((X + cell / 2, y + (cell - 6) / 2), d, 30, T['bg'], anchor='mm', bold=True)
    cv.text((x0 + 200 + 2 * (cell + 8) + 10, y + cell / 2), 'n−2 进制，不是回文', 24, T['pink'], anchor='lm', bold=True)
    cv.text((x0 + 30, y + 130), '两种情况都不是回文 → 答案必然为 false', 28, T['green'], bold=True)


CONFIG = dict(
    num=2396, title='严格回文的数字', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='脑筋急转弯 · 分情况',
    tags=['灵神题单·数学算法', '灵神题单·贪心与思维', '难度分 1329'],
    code='''
class Solution(object):
    def isStrictlyPalindromic(self, n):
        
        return False
''',
    call='Solution().isStrictlyPalindromic(9)',
    expect=False,
    views=[dict(type='custom', draw=_draw, h=520)],
    watch=[('n', 'n', 'blue')],
    captions={
        'return False': '`n = 4` 的 2 进制是 `100`，`n > 4` 的 `n-2` 进制是 `12`，都不是回文 → ==直接返回 False==',
    },
    cards=dict(
        one_liner='n=4 看 2 进制，n>4 看 n−2 进制，都不是回文',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['`n` 在 `2 ~ n-2` 每个进制下都是回文才算严格回文',
                 '返回 `n` 是否严格回文，`n >= 4`',
                 '示例：`n = 9` → `false`'],
        quote='乍一看以为是数学题，再一看数据规模感觉模拟也行，仔细一想发现原来是脑筋急转弯的题目。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n = 4`：只有 2 进制，`100` 不是回文',
              '`n > 4`：转成 `n-2` 进制，一定是 `12`，也不是回文',
              '所以不管 `n` 是多少，答案都是 `false`'],
        after=[dict(heading='为什么 n−2 进制一定是 12', lines=['`n = 1×(n-2) + 2`：商是 1，余数是 2', '`n > 4` 保证 `2 < n-2`，所以 2 是合法的一位数字', '`12` 首尾不同，不是回文，严格回文就被一票否决', '只要有一个进制不是回文，就不是严格回文', '所以连 `n` 的大小都不用看，直接 `return False`'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '先想模拟再发现是脑筋急转弯：看清范围和边界再动手',
                 '对比灵神：灵神用带余除法 `n = q·b + r` 一步证明；yiduobo 把 `n = 4` 单独拿出来看']),
)
