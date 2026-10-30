def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    strs = S['strs']
    m = len(strs[0])
    f = S.get('f')
    I, J = S.get('i'), S.get('j')
    live = f is not None and I is not None
    cv.text((x0 + 18, y0 + 4), '每一列 = 各行同位置的字母；蓝 = i 列，粉 = j 列，下方是 f 值', 24, T['muted'], bold=True)
    cell = min(110, (x1 - x0 - 40) / m)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * m) / 2
    top = y0 + 60
    rh = 64
    ok = None
    if live and J is not None and J < I:
        ok = all(s[J] <= s[I] for s in strs)
    for c in range(m):
        X = sx + c * cell
        col = None
        if live and c == I:
            col = T['blue']
        elif live and J is not None and c == J and J < I:
            col = T['pink']
        if col:
            cv.rect((X + 2, top - 6, X + cell - 2, top + rh * len(strs) + 6), outline=col, width=4, r=8)
        for r, s in enumerate(strs):
            cv.text((X + cell / 2, top + r * rh + rh / 2), s[c], 38, col or T['text'], anchor='mm', bold=True, mono=True)
        yb = top + rh * len(strs) + 22
        if live:
            v = f[c]
            kept = v > 0 and c < I
            fill = T['green'] if kept else (70, 76, 86)
            cv.rect((X + 8, yb, X + cell - 8, yb + 52), fill=fill, r=8, alpha=200)
            cv.text((X + cell / 2, yb + 26), v, 30, T['bg'] if kept else T['muted'], anchor='mm', bold=True)
        cv.text((X + cell / 2, yb + 62), c, 18, T['dim'], anchor='mt', mono=True)
    if ok is not None:
        msg = f'最近一次比较：第 {J} 列 ≤ 第 {I} 列（每行都满足）→ 能接上' if ok else f'最近一次比较：第 {J} 列有行比第 {I} 列大 → 接不上'
        cv.text((x0 + 20, top + rh * len(strs) + 150), msg, 28, T['green'] if ok else T['orange'], bold=True)


CONFIG = dict(
    num=960, title='删列造序 III', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='多行版 LIS · 逐列检查可接',
    tags=['灵神题单·动态规划', '难度分 2247'],
    code='''
class Solution(object):
    def minDeletionSize(self, strs):

        n = len(strs)
        l = len(strs[0])
        f = [0] * l
        f[0] = 1
        for i in range(1, l):
            tmp = 0
            for j in range(0, i):
                flag = True
                for k in range(n):
                    if strs[k][i] < strs[k][j]:
                        flag = False
                        break
                if flag:
                    tmp = max(tmp, f[j])
            
            f[i] = tmp + 1
        
        return l - max(f)
''',
    call='Solution().minDeletionSize(["babca","bbazb"])',
    expect=3,
    skip=['flag = True', 'for k in range(n)'],
    max_steps=90,
    views=[
        dict(type='custom', draw=_draw, h=330),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('tmp', 'tmp', 'yellow'), ('f', 'f', 'green')],
    captions={
        'n = len': '`n = {n}` 行',
        'l = len': '`l = {l}` 列。反过来想：删得最少 = ==保留得最多==',
        'f = [0] * l': '`f[i]`：以第 `i` 列结尾，最多能保留几列',
        'f[0] = 1': '最左边的列无条件可以保留：`f[0] = 1`',
        'for i in range': lambda S, B, r: (f'看第 `i = {S.i}` 列：能接在前面哪一列后面？' if S.i != B.get('i') else '每一列都处理完了'),
        'tmp = 0': '`tmp` 记录能接的列里最大的 `f[j]`，先设为 0',
        'for j in range': lambda S, B, r: (f'试着接在第 `j = {S.j}` 列后面' if not (S.j == S.i - 1 and B.get('j') == S.i - 1)
                                           else f'`j` 都试完了，`tmp = {S.tmp}`'),
        'if strs[k][i] < strs[k][j]': '第 {k} 行：`{strs[k][i]} < {strs[k][j]}`？',
        'flag = False': '第 `{k}` 行 `strs[{k}][{i}] < strs[{k}][{j}]`：右列比左列小 → ==这行不满足，接不上==',
        'break': '有一行不行就够了，==不用再查其余行==',
        'if flag': lambda S, B, r: (f'每一行第 `{S.j}` 列都 ≤ 第 `{S.i}` 列 → 可以接' if S.flag else f'第 `{S.j}` 列接不上，换下一个 `j`'),
        'tmp = max': '`tmp = max(tmp, f[{j}])` = =={tmp}==：接在 `j` 后面，长度是 `f[j] + 1`',
        'f[i] = tmp + 1': '`f[{i}] = tmp + 1` = =={f[i]}==（`tmp` 为 0 就是自己单独成列）',
        'return l - max': '最多保留 `{max(f)}` 列，删 `{l} − {max(f)}` = =={ret}== 列',
    },
    cards=dict(
        one_liner='正难则反：求最多保留几列，就是多行版最长上升子序列',
        complexity='时间 `O(n·l^2)`，空间 `O(l)`',
        problem=['`n` 个等长小写字符串，删去若干列，使每一行都按字典序排列',
                 '求最少删几列',
                 '示例：`["babca","bbazb"]` → `3`'],
        quote='题目要求出最少删去多少列，那么我们可以==反过来思考==，将问题变成最多保留下来多少列。',
        quote_src='—— yiduobo 题解原文',
        idea=['一列能保留：要么是最左列，要么==每一行==的数都不比前一个保留列小',
              '`f[i]` 初始化为 1（前面全不要）；接在满足条件的 `j` 后面则 `f[i] = max(f[j]) + 1`',
              '用 `flag` 逐行检查 `j` 能不能接在 `i` 前面'],
        summary=['时间 `O(n·l^2)`，空间 `O(l)`',
                 '答案是 `l - max(f)`：结尾列不一定是最后一列',
                 '比较用 `<`：相等的字母也能保留',
                 '对比灵神：灵神用 `all` 一行判断，并先比 `f[j] > f[i]` 省掉不必要的检查'],
    ),
)
