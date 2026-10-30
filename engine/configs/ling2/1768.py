W1, W2 = 'ab', 'pqrs'


def _src(word1, word2):
    """for each char of the merged answer: (which word, index)"""
    out = []
    for i in range(max(len(word1), len(word2))):
        if i < len(word1):
            out.append((1, i))
        if i < len(word2):
            out.append((2, i))
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    w1, w2 = S.get('word1', W1), S.get('word2', W2)
    i = S.get('i')
    ans = S.get('ans')
    used = len(ans) if ans is not None else 0
    src = _src(w1, w2)[:used]
    taken = set(src)
    cell = 84
    sx = x0 + 160
    for r, (nm, w, c) in enumerate((('word1', w1, 'blue'), ('word2', w2, 'pink'))):
        Y = y0 + 20 + r * 130
        cv.text((x0 + 30, Y + 36), nm, 26, T[c], anchor='lm', bold=True)
        for k, ch in enumerate(w):
            X = sx + k * cell
            on = (r + 1, k) in taken
            cv.rect((X + 4, Y, X + cell - 4, Y + 72), fill=T[c] if on else T['panel2'], r=10, outline=T['border'])
            cv.text((X + cell / 2, Y + 36), ch, 36, T['bg'] if on else T['text'], anchor='mm', bold=True, mono=True)
            cv.text((X + cell / 2, Y + 78), k, 18, T['dim'], anchor='mt', mono=True)
        if i is not None and i >= len(w):
            mx = max(len(w1), len(w2))
            cv.text((sx + mx * cell + 30, Y + 36), f'i ≥ {"n" if r == 0 else "m"}：{nm} 用完了', 22, T['dim'], anchor='lm')
    if i is not None:
        X = sx + i * cell
        cv.rect((X, y0 + 8, X + cell, y0 + 244), outline=T['yellow'], width=3, r=12)
        cv.text((X + cell / 2, y0 + 254), f'i = {i}', 24, T['yellow'], anchor='mt', bold=True)
    if ans is None:
        return
    Y = y0 + 320
    cv.text((x0 + 30, Y - 10), 'ans（蓝 = 来自 word1，粉 = 来自 word2）', 22, T['muted'], bold=True)
    bl = len(B.get('ans') or [])
    for k, ch in enumerate(ans):
        X = x0 + 30 + k * cell
        c = T['blue'] if src[k][0] == 1 else T['pink']
        new = k >= bl
        cv.rect((X + 4, Y + 24, X + cell - 4, Y + 96), fill=c, r=10, outline=T['yellow'] if new else T['border'],
                width=3 if new else 1)
        cv.text((X + cell / 2, Y + 60), ch, 36, T['bg'], anchor='mm', bold=True, mono=True)


CONFIG = dict(
    num=1768, title='交替合并字符串', difficulty='Easy', category='双指针',
    author='灵茶山艾府', technique='一个下标 i 同时遍历两个字符串',
    tags=['字节30天'],
    code='''
class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        ans = []
        i, n, m = 0, len(word1), len(word2)
        while i < n or i < m:
            if i < n:
                ans.append(word1[i])
            if i < m:
                ans.append(word2[i])
            i += 1
        return "".join(ans)
''',
    call=f'Solution().mergeAlternately({W1!r}, {W2!r})',
    expect='apbqrs',
    views=[
        dict(type='custom', draw=_draw, h=600),
    ],
    watch=[('i', 'i', 'yellow'), ('n', 'n', 'blue'), ('m', 'm', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = []': '用列表 `ans` 收集字母，最后再 `join`（比字符串反复相加更快）',
        'i, n, m = 0': '`i` 从 0 开始；`n = {n}`，`m = {m}`',
        'while i < n or i < m': lambda S, B, ret: (f'`i = {S.i}`：至少一个字符串还有字母 → 继续' if S.i < S.n or S.i < S.m
                                                   else f'`i = {S.i}` 已达到两个长度的最大值 → 结束'),
        'if i < n:': lambda S, B, ret: (f'`i = {S.i} < n = {S.n}`：word1 还有字母' if S.i < S.n else f'`i = {S.i} ≥ n = {S.n}`：word1 用完了，跳过'),
        'ans.append(word1[i])': "先放 `word1[{i}] = '{word1[i]}'`",
        'if i < m:': lambda S, B, ret: (f'`i = {S.i} < m = {S.m}`：word2 还有字母' if S.i < S.m else f'`i = {S.i} ≥ m = {S.m}`：word2 用完了，跳过'),
        'ans.append(word2[i])': "再放 `word2[{i}] = '{word2[i]}'`",
        'i += 1': '`i` → {i}',
        'return "".join(ans)': '拼起来：=={ret}==',
    },
    cards=dict(
        one_liner='i 从 0 开始，每轮先放 word1[i] 再放 word2[i]，越界的就跳过',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['从 `word1` 开始，交替地从两个字符串取字母合并',
                 '一个字符串更长时，多出来的字母直接接在末尾',
                 '示例：`"abc"`、`"pqr"` → `"apbqcr"`',
                 f'本视频：`"{W1}"`、`"{W2}"` → `"apbqrs"`'],
        quote='从 i=0 开始遍历，每次循环：如果 i 小于 word1 的长度，把 word1[i] 加到答案末尾；如果 i 小于 word2 的长度，把 word2[i] 加到答案末尾。循环直到 i 达到 word1 的长度和 word2 的长度的最大值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['两个字符串共用一个下标 `i`：每一轮最多放两个字母',
              '`while i < n or i < m`：只要还有一个没用完就继续',
              '循环里分别判断 `i < n`、`i < m`，==不需要单独处理剩余部分=='],
        summary=['时间 `O(n + m)`；答案的空间 `O(n + m)`',
                 '循环条件是 `or`：两个都用完才停',
                 '用列表收集再 `join`，避免字符串反复拼接',
                 '题解另给了库函数写法：`zip_longest` 一行搞定',
                 '对比 yiduobo：两个指针同时走到较短串的末尾，再整体接上剩余部分'],
    ),
)
