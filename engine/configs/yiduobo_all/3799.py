def _ok(S):
    t, l, r, b = S.top, S.left, S.right, S.bottom
    return t[0] == l[0] and t[3] == r[0] and b[0] == l[3] and b[3] == r[3]


def _square(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '单词方块（角格：左 = 行里的字母，右 = 列里的字母，相同才绿）', 22, T['muted'], bold=True)
    top = S.get('top') or '????'
    left = S.get('left') or '????'
    right = S.get('right') or '????'
    bottom = S.get('bottom') or '????'
    if 'top' not in S:
        return
    cell = 92
    gx = x0 + (x1 - x0) / 2 - cell * 2
    gy = y0 + 70
    corners = [(0, 0, top[0], left[0]), (0, 3, top[3], right[0]), (3, 0, bottom[0], left[3]), (3, 3, bottom[3], right[3])]
    ok_all = all(a == b for _, _, a, b in corners)
    for r in range(4):
        for c in range(4):
            if 0 < r < 3 and 0 < c < 3:
                continue
            X, Y = gx + c * cell, gy + r * cell
            cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), fill=T['panel2'], r=10, outline=T['border'], width=2)
            if (r, c) in [(0, 0), (0, 3), (3, 0), (3, 3)]:
                a, b = [(cc[2], cc[3]) for cc in corners if cc[0] == r and cc[1] == c][0]
                col = T['green'] if a == b else T['red']
                cv.rect((X + 3, Y + 3, X + cell - 3, Y + cell - 3), fill=col, r=10, alpha=70)
                cv.text((X + cell * 0.3, Y + cell * 0.5), a, 34, T['text'], anchor='mm', bold=True, mono=True)
                cv.text((X + cell * 0.72, Y + cell * 0.5), b, 34, T['text'], anchor='mm', bold=True, mono=True)
            else:
                if r == 0:
                    ch = top[c]
                elif r == 3:
                    ch = bottom[c]
                elif c == 0:
                    ch = left[r]
                else:
                    ch = right[r]
                cv.text((X + cell / 2, Y + cell / 2), ch, 34, T['text'], anchor='mm', bold=True, mono=True)
    cv.text((gx + cell * 2, gy + cell * 2), ('角全对' if ok_all else '角不对'), 30, T['green'] if ok_all else T['red'], anchor='mm', bold=True)
    for (nm, w, X, Y, anc) in [('top', top, gx - 14, gy + cell * 0.5, 'rm'), ('bottom', bottom, gx - 14, gy + cell * 3.5, 'rm'),
                               ('left', left, gx + cell * 4 + 14, gy + cell * 0.5, 'lm'), ('right', right, gx + cell * 4 + 14, gy + cell * 3.5, 'lm')]:
        pass


CONFIG = dict(
    num=3799, title='单词方块 II', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='排序 + 四重循环枚举',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1606'],
    code='''
class Solution(object):
    def wordSquares(self, words):
        
        res = []
        words.sort()
        for top in words:
            for left in words:
                if top == left or top[0] != left[0]:
                    continue
                for right in words:
                    if top == right or left == right or top[3] != right[0]:
                        continue
                    for bottom in words:
                        if top == bottom or left == bottom or right == bottom or bottom[0] != left[3] or bottom[3] != right[3]:
                            continue
                        res.append((top, left, right, bottom))
        
        return res
''',
    call='Solution().wordSquares(["able","area","echo","also"])',
    expect=[('able', 'area', 'echo', 'also'), ('area', 'able', 'also', 'echo')],
    views=[
        dict(type='custom', draw=_square, h=470),
        dict(type='array', var='words', label='words（排序后）', cell=100, h=140),
    ],
    watch=[('top', lambda S: S.get('top'), 'blue'), ('left', lambda S: S.get('left'), 'pink'), ('right', lambda S: S.get('right'), 'cyan'),
           ('bottom', lambda S: S.get('bottom'), 'orange'), ('找到', 'len(res)', 'green')],
    skip=['res = []', 'continue', 'for left in words', 'for right in words', 'for bottom in words'],
    captions={
        'words.sort()': '先排序：按 top、left、right、bottom 的顺序枚举，结果==自然有序== → `{words}`',
        'for top in words': '第一条边：`top = {top}`',
        'if top == left or top[0] != left[0]': lambda S, B, ret: (
            f'`left = {S.left}` 就是 `top`，同一个词不能用两次 → 跳过' if S.top == S.left else
            (f"`top[0] = {S.top[0]}` ≠ `left[0] = {S.left[0]}`：左上角对不上 → 跳过" if S.top[0] != S.left[0]
             else f"`top[0] = left[0] = {S.top[0]}`：左上角对上了，继续选 `right`")),
        'if top == right or left == right': lambda S, B, ret: (
            f'`right = {S.right}` 已被用过 → 跳过' if (S.top == S.right or S.left == S.right) else
            (f"`top[3] = {S.top[3]}` ≠ `right[0] = {S.right[0]}`：右上角对不上 → 跳过" if S.top[3] != S.right[0]
             else f"`top[3] = right[0] = {S.top[3]}`：右上角对上了，继续选 `bottom`")),
        'if top == bottom or left == bottom': lambda S, B, ret: (
            f'`bottom = {S.bottom}` 已被用过 → 跳过' if (S.top == S.bottom or S.left == S.bottom or S.right == S.bottom) else
            (f"`bottom[0] = {S.bottom[0]}` 对 `left[3] = {S.left[3]}`，`bottom[3] = {S.bottom[3]}` 对 `right[3] = {S.right[3]}`："
             + ('两个下角都对上 → ==成立==' if (S.bottom[0] == S.left[3] and S.bottom[3] == S.right[3]) else '有角对不上 → 跳过'))),
        'res.append': '四个角全部吻合，记录方块 `{res[-1]}`',
        'return res': '全部枚举完，共找到 `{len(ret)}` 个单词方块',
    },
    max_steps=55,
    cards=dict(
        one_liner='words 最多 15 个，直接四重循环，边选边检查角',
        complexity='时间 `O(n^4)`，空间 `O(1)`（不计返回值）',
        problem=['给定互不相同的四字母单词 `words`，选 4 个不同的词做 `top / left / right / bottom`',
                 '角要对上：`top[0]=left[0]`，`top[3]=right[0]`，`bottom[0]=left[3]`，`bottom[3]=right[3]`',
                 '返回所有方块，按 `(top, left, right, bottom)` 字典序升序'],
        quote='由于words的长度不超过15，因此可以直接四重循环暴力，枚举形成四条边的单词，然后检测是否符合构成方块的条件即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['按 top → left → right → bottom 的顺序逐层选词，每层先用已知的角剪枝（不符合就 `continue`）',
              '同一个词不能重复使用：每层都和前面选过的比较',
              '先 `words.sort()`，枚举顺序就是字典序，结果不用再排'],
        result='两个方块：`able/area/echo/also` 和 `area/able/also/echo`（后者在快进区间里找到）✓',
        summary=['时间 `O(n^4)`，`n <= 15` 足够；空间 `O(1)`（不计返回值）',
                 '去重条件别漏：`right` 要和 `top`、`left` 比，`bottom` 要和另三个比',
                 '外层先检查角再进入内层，能提前剪枝',
                 '对比灵神：灵神用 `permutations(words, 4)` 一行枚举；yiduobo 手写四重循环并逐层剪枝',
                 '原文为 Python 2 风格，无需改动即可在 Python 3 运行（返回的是元组列表）'],
    ),
)
