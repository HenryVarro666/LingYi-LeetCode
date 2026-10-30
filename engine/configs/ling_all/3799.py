def _ok(S):
    t, l, r, b = S.top, S.left, S.right, S.bottom
    return t[0] == l[0] and t[3] == r[0] and b[0] == l[3] and b[3] == r[3]


def _square(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '单词方块（角格：左 = 行里的字母，右 = 列里的字母，相同才绿）', 22, T['muted'], bold=True)
    if 'top' not in S or 'bottom' not in S:
        return
    top, left, right, bottom = S['top'], S['left'], S['right'], S['bottom']
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
    author='灵茶山艾府', technique='排序 + 枚举排列',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1606'],
    code='''
class Solution:
    def wordSquares(self, words: List[str]) -> List[List[str]]:
        words.sort()  # 保证答案有序
        return [[top, left, right, bottom]
                for top, left, right, bottom in permutations(words, 4)
                if top[0] == left[0] and top[3] == right[0] and
                bottom[0] == left[3] and bottom[3] == right[3]]
''',
    call='Solution().wordSquares(["able","area","echo","also"])',
    expect=[['able', 'area', 'echo', 'also'], ['area', 'able', 'also', 'echo']],
    views=[
        dict(type='custom', draw=_square, h=470),
        dict(type='array', var='words', label='words（排序后）', cell=100, h=140),
    ],
    watch=[('top', 'top', 'blue'), ('left', 'left', 'pink'), ('right', 'right', 'cyan'), ('bottom', 'bottom', 'orange')],
    skip=[5, 7],
    captions={
        'words.sort()': '先排序：这样按字典序枚举排列，==结果天然有序== → `{words}`',
        'if top[0] == left[0]': lambda S, B, ret: (
            f"`{S.top}` `{S.left}` `{S.right}` `{S.bottom}`：四个角 "
            f"`{S.top[0]}={S.left[0]}`？`{S.top[3]}={S.right[0]}`？`{S.bottom[0]}={S.left[3]}`？`{S.bottom[3]}={S.right[3]}`？"
            + (' → ==全部成立，收录==' if _ok(S) else ' → 不满足')),
        '[[top, left, right, bottom]': lambda S, B, ret: (
            f'枚举结束，共 `{len(ret)}` 个不同的单词方块' if isinstance(ret, list) else
            ('`permutations(words, 4)`：从 4 个单词里取 4 个，按顺序排好，一共 `24` 种' if 'top' not in S else None) or
            (f"满足条件，把 `[{S.top}, {S.left}, {S.right}, {S.bottom}]` 放进答案" if _ok(S)
             else '这个排列丢弃，换下一个')),
    },
    max_steps=56,
    cards=dict(
        one_liner='排序后枚举 4 个互不相同的单词排列，按四个角检查',
        complexity='时间 `O(n^4)`，空间 `O(1)`（不计返回值）',
        problem=['`words` 是一组互不相同的四字母单词，选 4 个不同的单词做 `top, left, right, bottom`',
                 '四个角要对上：`top[0]==left[0]`，`top[3]==right[0]`，`bottom[0]==left[3]`，`bottom[3]==right[3]`',
                 '返回所有方块，按 `(top, left, right, bottom)` 字典序升序'],
        quote='按题目要求模拟即可。注意为了保证答案有序，可以先对 words 从小到大排序，再枚举排列。',
        quote_src='—— 灵茶山艾府题解',
        idea=['前置题：46. 全排列。`permutations(words, 4)` 就是从 `words` 里选 4 个不同的单词并排好顺序',
              '`words` 最多 15 个，`15·14·13·12` 种排列，直接模拟判断四个角',
              '先 `sort`，`permutations` 按输入顺序产出，答案就已经是字典序'],
        result='两个方块：`able/area/echo/also` 和 `area/able/also/echo`（后者在快进区间里找到）✓',
        summary=['时间 `O(A(n,4)) = O(n^4)`，空间 `O(1)`',
                 '先排序再枚举，才能保证返回值按字典序',
                 '`permutations` 保证 4 个单词互不相同（下标不重复），题目要求单词两两不同',
                 '推导式一行写完；也可以手写排列型回溯，思路相同',
                 '同类题：46. 全排列、47. 全排列 II'],
    ),
)
