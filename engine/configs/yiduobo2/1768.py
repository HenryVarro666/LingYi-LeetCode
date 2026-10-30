W1, W2 = 'abcd', 'pq'


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    w1, w2 = S.get('word1', W1), S.get('word2', W2)
    p1, p2 = S.get('p1'), S.get('p2')
    ln = S.get('_line') or 0
    cell = 84
    sx = x0 + 160
    rl = len(S.get('res') or [])
    usedn = ((rl + 1) // 2, rl // 2)  # 交替放入：word1 先放
    for r, (nm, w, p, c) in enumerate((('word1', w1, p1, 'blue'), ('word2', w2, p2, 'pink'))):
        Y = y0 + 20 + r * 150
        cv.text((x0 + 30, Y + 36), nm, 26, T[c], anchor='lm', bold=True)
        for k, ch in enumerate(w):
            X = sx + k * cell
            used = k < usedn[r]
            tail = ln in (14, 16) and p is not None and k >= p and ((r == 0 and ln == 14) or (r == 1 and ln == 16))
            fill = T[c] if used else (T['green'] if tail else T['panel2'])
            cv.rect((X + 4, Y, X + cell - 4, Y + 72), fill=fill, r=10, outline=T['border'])
            cv.text((X + cell / 2, Y + 36), ch, 36, T['bg'] if (used or tail) else T['text'], anchor='mm', bold=True, mono=True)
            cv.text((X + cell / 2, Y + 78), k, 18, T['dim'], anchor='mt', mono=True)
        if p is not None:
            X = sx + p * cell + cell / 2
            cv.tri_up(X, Y + 102, 10, T[c])
            cv.text((X, Y + 118), f'p{r + 1}', 22, T[c], anchor='mt', bold=True)
    res = S.get('res')
    if res is None:
        return
    Y = y0 + 330
    cv.text((x0 + 30, Y - 10), 'res（交替放入；绿 = 最后整体接上的剩余部分）', 22, T['muted'], bold=True)
    bl = len(B.get('res') or [])
    items = list(res)
    cols = []
    for k in range(len(items)):
        cols.append(T['blue'] if k % 2 == 0 else T['pink'])
    for k, ch in enumerate(items):
        X = x0 + 30 + k * cell
        new = k >= bl
        cv.rect((X + 4, Y + 24, X + cell - 4, Y + 96), fill=cols[k], r=10, outline=T['yellow'] if new else T['border'],
                width=3 if new else 1)
        cv.text((X + cell / 2, Y + 60), ch, 36, T['bg'], anchor='mm', bold=True, mono=True)
    if ln in (14, 16):
        rest = w1[p1:] if ln == 14 else w2[p2:]
        X = x0 + 30 + len(items) * cell
        cv.text((X + 10, Y + 60), '+', 36, T['muted'], anchor='lm', bold=True)
        X += 40
        for k, ch in enumerate(rest):
            cv.rect((X + 4, Y + 24, X + cell - 4, Y + 96), fill=T['green'], r=10, outline=T['yellow'], width=3)
            cv.text((X + cell / 2, Y + 60), ch, 36, T['bg'], anchor='mm', bold=True, mono=True)
            X += cell


CONFIG = dict(
    num=1768, title='交替合并字符串', difficulty='Easy', category='双指针',
    author='yiduobo', technique='双指针同步走，短的走完再接上剩余部分',
    tags=['字节30天'],
    code='''
class Solution(object):
    def mergeAlternately(self, word1, word2):
        p1 = p2 = 0
        l1 = len(word1)
        l2 = len(word2)
        res = []
        while p1 < l1 and p2 < l2:
            res.append(word1[p1])
            res.append(word2[p2])
            p1 += 1
            p2 += 1

        if p1 < l1:
            return ''.join(res) + word1[p1:]
        else:
            return ''.join(res) + word2[p2:]
''',
    call=f'Solution().mergeAlternately({W1!r}, {W2!r})',
    expect='apbqcd',
    views=[
        dict(type='custom', draw=_draw, h=600),
    ],
    watch=[('p1', 'p1', 'blue'), ('p2', 'p2', 'pink'), ('l1', 'l1'), ('l2', 'l2'), ('res', 'res', 'green')],
    captions={
        'p1 = p2 = 0': '两个指针分别从两个字符串的头部开始',
        'l1 = len(word1)': '`l1 = {l1}`',
        'l2 = len(word2)': '`l2 = {l2}`',
        'res = []': '`res` 收集交替合并的结果',
        'while p1 < l1 and p2 < l2': lambda S, B, ret: (f'`p1 = {S.p1} < {S.l1}` 且 `p2 = {S.p2} < {S.l2}`：两边都还有 → 继续交替'
                                                        if S.p1 < S.l1 and S.p2 < S.l2 else
                                                        (f'`p2 = {S.p2} == l2`：word2 先走完 → ==停止交替==' if S.p2 >= S.l2
                                                         else f'`p1 = {S.p1} == l1`：word1 先走完 → ==停止交替==')),
        'res.append(word1[p1])': "先放 `word1[{p1}] = '{word1[p1]}'`",
        'res.append(word2[p2])': "再放 `word2[{p2}] = '{word2[p2]}'`",
        'p1 += 1': '`p1` → {p1}',
        'p2 += 1': '`p2` → {p2}',
        'if p1 < l1': lambda S, B, ret: (f'`p1 = {S.p1} < l1 = {S.l1}`：剩下的是 word1' if S.p1 < S.l1 else '剩下的是 word2（也可能为空）'),
        "return ''.join(res) + word1": "合并结果 + 剩余的 `word1[{p1}:] = '{word1[p1:]}'` → =={ret}==",
        "return ''.join(res) + word2": "合并结果 + 剩余的 `word2[{p2}:] = '{word2[p2:]}'` → =={ret}==",
    },
    cards=dict(
        one_liner='两个指针同时往后扫，按先 1 后 2 的顺序合并；一个走完就把另一个剩下的接上',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['从 `word1` 开始，交替地从两个字符串取字母合并',
                 '一个字符串更长时，多出来的字母直接接在末尾',
                 '示例：`"ab"`、`"pqrs"` → `"apbqrs"`',
                 f'本视频：`"{W1}"`、`"{W2}"` → `"apbqcd"`'],
        quote='使用两个指针分别从两个字符串的头部开始向后扫，按照先1后2的顺序进行合并。当某一个指针当前字符串末尾时则停止，然后将合并的结果与剩下的另一个字符串组合后返回即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`while p1 < l1 and p2 < l2`：两个都没走完才交替放',
              '循环结束时至少有一个走完了',
              '`word1` 还有剩就接 `word1[p1:]`，否则接 `word2[p2:]`（可能是空串）'],
        summary=['时间 `O(n + m)`，空间 `O(n + m)`',
                 '循环条件是 `and`：短的一走完就停，剩余部分用切片一次接上',
                 '两个串等长时 `else` 分支接的是空串，结果依然正确',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神用一个下标 `i` 和 `or` 条件，在循环里分别判断是否越界'],
    ),
)
