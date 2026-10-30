NR = 4        # 表里画 i = 0 .. 3（视频只演示到 i = 3）
NC = 8        # j = 0 .. 7


def _boxes(cv, T, x, y, n, sel, size, fill_on, mark=None, ghost=None, label=None):
    """一排 n 个字母格：sel 里的位置染色；mark = 被取走的位置（粉色描边）"""
    for p in range(n):
        X = x + p * (size + 8)
        on = (sel >> p) & 1
        cv.rect((X, y, X + size, y + size), fill=fill_on if on else T['panel2'],
                outline=T['pink'] if p == mark else T['border'], width=5 if p == mark else 2, r=10)
        cv.text((X + size / 2, y + size / 2), '●' if False else (1 if on else 0), 26, T['bg'] if on else T['dim'],
                anchor='mm', bold=True, mono=True)
        cv.text((X + size / 2, y + size + 6), p, 18, T['dim'], anchor='mt', mono=True)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    line = S.get('_line') or 0
    i = S.get('i')
    j = S.get('j') if (i is not None and line >= 9) else None
    k = S.get('k') if (j is not None and line >= 10) else None
    pre = S.get('pre_state') if (k is not None and line >= 14) else None
    f = S.get('f')
    size = 50

    cv.text((x0 + 14, y0 + 4), 'f[i][j]：长度为 i 的单词，取走 j 标出的位置', 22, T['muted'], bold=True)
    # 行 A：长度为 i 的单词
    ya = y0 + 56
    if i is not None:
        cv.text((x0 + 14, ya), f'长度 i = {i} 的单词（格里的 1 = 要取走的位置）', 20, T['cyan'], bold=True)
        _boxes(cv, T, x0 + 24, ya + 34, i, j or 0, size, T['cyan'], mark=k if (k is not None and line >= 11) else None)
    else:
        cv.text((x0 + 14, ya), '先对每种长度 i 预处理一张表', 20, T['muted'])
    # 行 B：先取走第 k 位之后
    yb = y0 + 172
    if pre is not None and i is not None and i >= 1:
        cv.text((x0 + 14, yb), f'先取走第 {k} 位 → 单词变成长度 {i - 1}，还要取 pre_state', 20, T['blue'], bold=True)
        _boxes(cv, T, x0 + 24, yb + 34, i - 1, pre, size, T['blue'])
        if i - 1 > 0:
            cv.text((x0 + 24, yb + 34 + size + 30), f'左边 {k} 个字母，右边 {i - 1 - k} 个字母', 20, T['muted'])
        if line >= 15:
            cv.text((x0 + 14, yb + 34 + size + 62), f'代价 = {k} × {i - 1 - k} = {k * (i - 1 - k)}', 24, T['yellow'], bold=True)
    elif k is not None and line >= 11 and not ((j >> k) & 1):
        cv.text((x0 + 14, yb), f'第 {k} 位是 0：不取，看下一位', 20, T['muted'])

    # 表：f[i][j]
    cw, ch, lw = 76, 44, 64
    tx = x0 + 14
    ty = y0 + 418
    cv.text((tx, ty - 34), 'f 表（行 i，列 j；· = None）', 20, T['muted'], bold=True)
    for c in range(NC):
        cv.text((tx + lw + c * cw + cw / 2, ty + 12), c, 20, T['cyan'] if (j is not None and c == j) else T['dim'], anchor='mm', mono=True)
    for r in range(NR):
        Y = ty + 28 + r * ch
        cv.text((tx + 10, Y + ch / 2 - 2), f'i={r}', 20, T['cyan'] if r == i else T['muted'], anchor='lm', mono=True, bold=True)
        row = f[r] if f and r < len(f) else None
        for c in range(NC):
            X = tx + lw + c * cw
            valid = c < (1 << r)
            if not valid:
                continue
            v = row[c] if row else None
            hot = (r == i and j is not None and c == j)
            src = (pre is not None and r == i - 1 and c == pre)
            cv.rect((X + 3, Y + 2, X + cw - 3, Y + ch - 2), fill=T['panel2'] if v is not None else T['panel'],
                    outline=T['pink'] if hot else (T['orange'] if src else T['border']), width=4 if (hot or src) else 1, r=8)
            cv.text((X + cw / 2, Y + ch / 2 - 2), '·' if v is None else v, 24, T['dim'] if v is None else T['text'],
                    anchor='mm', bold=True)


def _bit(S):
    return (S.j >> S.k) & 1


def _cap_j(S, B, r):
    if 'j' in B and S.j == B.j == S.max_state:
        return f'`i = {S.i}` 的所有 `j` 都算完了'
    pos = '、'.join(str(p) for p in range(S.i) if (S.j >> p) & 1)
    return f'枚举取走的位置集合 `j = {S.j}`：取第 {pos} 位（第 k 位为 1 = 取第 k 个字母）'


def _cap_k(S, B, r):
    if 'k' in B and S.k == B.k == S.i - 1 and S.j == B.j:
        return f'`j = {S.j:0{S.i}b}` 的每一位都看过了'
    return f'看第 `{S.k}` 位'


def _cap_if(S, B, r):
    if _bit(S):
        return f'看第 `{S.k}` 位：是 1 → 这个位置要取走'
    return f'看第 `{S.k}` 位：是 0 → 不取，看下一位'


def _cap_pre(S, B, r):
    if S.i == 1:
        return (f'取走第 `{S.k}` 位后重新编号：低 `{S.k}` 位不动 `right_part = {S.right_part:b}`，'
                f'高位右移一位 `left_part = {S.left_part:b}`，拼成 `pre_state = {S.pre_state:b}`')
    return f'重新编号：`right_part = {S.right_part:b}`，`left_part = {S.left_part:b}` → `pre_state = {S.pre_state:b}`'


def _cap_cmp(S, B, r):
    i, k, p = S.i, S.k, S.pre_state
    cand = S.f[i - 1][p] + k * (i - 1 - k)
    cur = S.f[i][S.j]
    if cur is None:
        return f'候选 `f[{i - 1}][{p}] + {k}×{i - 1 - k} = {cand}`，`f[{i}][{S.j}]` 还是 None → 更新'
    if cur > cand:
        return f'候选 `{cand}` < 现有 `{cur}` → 更新'
    return f'候选 `{cand}` 不比现有 `{cur}` 更小 → 不更新'


def _cap_set(S, B, r):
    i, k = S.i, S.k
    return f'`f[{i}][{S.j}]` = `{S.f[i - 1][S.pre_state]} + {k}×{i - 1 - k}` = =={S.f[i][S.j]}==（左 {k} 个 × 右 {i - 1 - k} 个）'


CONFIG = dict(
    num='LCP 69', title='Hello LeetCode!', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='先预处理取字母代价 + 背包',
    tags=['灵神题单·动态规划', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def Leetcode(self, words):

        f = [[None] * 256 for _ in range(9)]
        f[0][0] = 0
        for i in range(1, 9):
            max_state = (1 << i) - 1
            f[i][0] = 0
            for j in range(1, max_state + 1):
                for k in range(i):
                    if j & (1 << k) == (1 << k):
                        right_part = j & ((1 << k) - 1)
                        left_part = (j ^ right_part ^ (1 << k)) >> 1
                        pre_state = left_part | right_part
                        if f[i - 1][pre_state] is not None and (f[i][j] is None or f[i][j] > f[i - 1][pre_state] + k * (i - 1 - k)):
                            f[i][j] = f[i - 1][pre_state] + k * (i - 1 - k)

        max_cnt = [1, 4, 3, 2, 1, 1, 1]
        candidate_list = []
        order = {'h' : 0, 'e' : 1, 'l' : 2, 'o': 3, 't': 4, 'c': 5, 'd': 6}

        for word in words:
            candidate_list.append([])
            max_state = (1 << len(word))
            for j in range(max_state):
                pos_list = []
                for k in range(len(word)):
                    if j & (1 << k) == (1 << k):
                        pos_list.append(k)

                flag = True
                cnt_list = [0] * 7
                for pos in pos_list:
                    if word[pos] not in order:
                        flag = False
                        break
                    cnt_list[order[word[pos]]] += 1

                if flag:
                    for index in range(7):
                        if cnt_list[index] > max_cnt[index]:
                            flag = False
                            break

                if flag:
                    candidate_list[-1].append([cnt_list[:], f[len(word)][j]])

        g = [-1] * 960
        g[0] = 0
        base = [2, 5, 4, 3, 2, 2, 2]
        multi_base = [1, 2, 10, 40, 120, 240, 480]
        for i in range(len(words)):
            for j in range(959, 0, -1):
                cnt_list = []
                tmp = j
                for index in range(7):
                    cnt_list.append(tmp % base[index])
                    tmp //= base[index]

                for candidate in candidate_list[i]:
                    flag = True
                    for index in range(7):
                        if cnt_list[index] < candidate[0][index]:
                            flag = False
                            break

                    if flag:
                        pre_state = 0
                        for index in range(7):
                            pre_state += multi_base[index] * (cnt_list[index] - candidate[0][index])

                        if g[pre_state] != -1 and (g[j] == -1 or g[j] > g[pre_state] + candidate[1]):
                            g[j] = g[pre_state] + candidate[1]

        return g[-1]
''',
    call='Solution().Leetcode(["hold","engineer","cost","level"])',
    expect=5,
    trace_limit=94, snap_maxlen=4, max_steps=60,
    truncated_caption='…… `i` 一直算到 8、`j` 到 255，后面同理；接着枚举单词做背包，快进到结束 ……',
    skip=[7, 10, 12, 13],
    views=[dict(type='custom', draw=_draw, h=640)],
    watch=[('i', 'i', 'cyan'), ('j', 'j', 'pink'), ('k', 'k', 'orange'), ('pre_state', 'pre_state', 'blue')],
    captions={
        'f = [[None]': '`f[i][j]` = 长度为 `i` 的单词，取走 `j` 标出的位置所需的最小代价（None = 还没算）',
        'f[0][0] = 0': '长度 0 的单词什么都不取，代价 0',
        'for i in range': '枚举单词长度 `i = {i}`（题目保证长度 ≤ 8）',
        'f[i][0] = 0': '一个字母都不取，代价 0',
        'for j in range': _cap_j,
        'if j & (1 << k)': _cap_if,
        'pre_state = ': _cap_pre,
        'if f[i - 1][pre_state]': _cap_cmp,
        'f[i][j] = f[i - 1][pre_state]': _cap_set,
    },
    cards=dict(
        one_liner='先预处理「长度 i 的单词取走位置集合 j」的最小代价，再做背包',
        complexity='预处理 `O(8 × 2^8 × 8)`，背包 `O(n × 960 × 取法数 × 7)`',
        problem=['从单词里取字母，代价 = 它左边字母数 × 右边字母数',
                 '要凑出 `helloleetcode` 的 13 个字母，求最小总代价',
                 '示例：`["hold","engineer","cost","level"]` → `5`'],
        quote='令f[i][j]表示长度为i的单词，选择字母的二进制表示为j时所需的代价。',
        quote_src='—— yiduobo 题解原文',
        idea=['长度 ≤ 8，每个单词最多 `2^8` 种取法；代价只和位置有关',
              '先取走第 `k` 位（代价 `k × (i−1−k)`），再接 `f[i−1][pre_state]`',
              '各单词的取法进背包：7 种字母个数编码成 0 ~ 959'],
        after=[dict(heading='预处理之后的背包（视频快进了）', lines=[
            '枚举单词的每种取法：字母要在 `helloleetcode` 里，个数不超上限',
            '`h e l o t c d` 的上限 `1 4 3 2 1 1 1` 编码成 `0 ~ 959`',
            '`g[j]` = 凑出编码 `j` 的最小代价，答案是 `g[959]`',
        ])],
        summary=['预处理 `O(8 × 2^8 × 8)`，背包 `O(n × 960 × 取法数 × 7)`',
                 '预处理在 8 × 255 个状态上写死；视频只演示到 `i = 3`，其余快进',
                 '易错：取走第 `k` 位后位置要重新编号：高位右移一位，再和低位拼起来',
                 '原文为 Python 2 写法，背包里的整数除法 `tmp /= base[index]` 已改为 `//=`'],
    ),
)
