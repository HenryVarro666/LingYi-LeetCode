def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    s = S['s']
    n = len(s)
    cell = min(100, (x1 - x0 - 150) / (n + 1))
    sx = x0 + 130
    cv.text((x0 + 10, y0 + 4), '预处理表（从每个下标开始的原始分割）与 f / g', 24, T['muted'], bold=True)
    names = [('s', 's'), ('min_k', 'min_k'), ('max_k', 'max_k'), ('full_k', 'full_k'), ('f', 'f'), ('g', 'g')]
    cur = S.get('index')
    in_dp = 'f' in S and S.get('_line', 0) >= 62
    for r, (nm, var) in enumerate(names):
        y = y0 + 84 + r * 68
        cv.text((x0 + 10, y + 26), nm, 22, T['muted'], anchor='lm', bold=True, mono=True)
        arr = S.get(var) if var != 's' else list(s)
        for c in range(n + (1 if var in ('f', 'g') else 0)):
            X = sx + c * cell
            v = arr[c] if arr is not None and c < len(arr) else None
            hl = (cur == c)
            fill = (T['blue'] if hl else (60, 66, 76)) if v is not None else (38, 42, 50)
            if var in ('f', 'g') and v is not None and in_dp and hl:
                fill = T['green']
            cv.rect((X + 2, y, X + cell - 2, y + 56), fill=fill, r=8)
            if v is not None:
                if isinstance(v, bool):
                    v = '是' if v else '否'
                cv.text((X + cell / 2, y + 28), v, 28, T['bg'] if hl else T['text'], anchor='mm', bold=True, mono=True)
            if r == 0:
                cv.text((X + cell / 2, y - 4), c, 18, T['dim'], anchor='mb', mono=True)
    if cur is not None and 0 <= cur < n:
        X = sx + cur * cell + cell / 2
        cv.tri_up(X, y0 + 84 + 6 * 68 + 6, 10, T['blue'])
        cv.text((X, y0 + 84 + 6 * 68 + 20), 'index', 22, T['blue'], anchor='mt', bold=True)


def _info(S):
    ln = S.get('_line', 0)
    if 'f' in S and 'index' in S and ln >= 62:
        return (f"`f[index]` = 不修改的最大段数；`g[index]` = 最多改一次的最大段数；`k_point = {S.get('k_point', '?')}`")
    return '预处理：滑动窗口求 `min_k`（第 k 种字母首次出现位置）、`max_k`（原始分割的终点）'


CONFIG = dict(
    num=3003, title='执行操作后的最大分割数量', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='滑动窗口预处理 + 倒序 DP（f / g 两个数组）',
    tags=['其他线性 DP', '多维 DP', '难度分 3039'],
    code='''
class Solution(object):
    def maxPartitionsAfterOperations(self, s, k):

        if k == 26:
            return 1

        n = len(s)
        p = q = 0
        min_k = []
        max_k = []
        char_state = []
        full_k = []

        min_freq = {}
        max_freq = {}
        
        state = 0
        for index in range(n):
            while p < n and len(min_freq) < k:
                min_freq[s[p]] = min_freq.get(s[p], 0) + 1
                state |= (1 << (ord(s[p]) - 97))
                p += 1
            min_k.append(p - 1)
            char_state.append(state)
            full_k.append(len(min_freq) == k)

            min_freq[s[index]] -= 1
            if min_freq[s[index]] == 0:
                min_freq.pop(s[index])
                state ^= (1 << (ord(s[index]) - 97))

            while q < n and (len(max_freq) < k or (len(max_freq) == k and s[q] in max_freq)):
                max_freq[s[q]] = max_freq.get(s[q], 0) + 1
                q += 1
            max_k.append(q - 1)

            max_freq[s[index]] -= 1
            if max_freq[s[index]] == 0:
                max_freq.pop(s[index])
    

        f = [0] * (n + 1)
        g = [0] * (n + 1)
        for index in range(n - 1, -1, -1):
            f[index] = f[max_k[index] + 1] + 1
            g[index] = g[max_k[index] + 1] + 1

            k_point = min_k[index]

            if k_point - index + 1 > k and full_k[index]:
                g[index] = max(g[index], f[k_point] + 1)

            if k_point - index + 1 == k:
                g[index] = max(g[index], f[k_point + 1] + 1)

            if k_point < n - 1 and min_k[index] != max_k[index]:
                change_point = k_point + 1
                if change_point + 1 == n:
                    g[index] = max(g[index], 2)
                else:
                    nxt_point = change_point + 1
                    if (char_state[index] | char_state[nxt_point]) != (1 << 26) - 1:
                        if full_k[nxt_point]:
                            g[index] = max(g[index], f[min_k[nxt_point]] + 2)
                        elif min_k[nxt_point] == n - 1:
                            g[index] = max(g[index], 2)

        print(f, g)

        return g[0]
''',
    call='Solution().maxPartitionsAfterOperations("accca", 2)',
    expect=3,
    views=[
        dict(type='text', fn=_info, size=24, h=60),
        dict(type='custom', draw=_draw, h=520),
    ],
    watch=[('index', lambda S: S.get('index', ''), 'blue'), ('p', lambda S: S.get('p', ''), 'cyan'), ('q', lambda S: S.get('q', ''), 'pink'),
           ('k_point', lambda S: S.get('k_point', ''), 'yellow'), ('g[0]', lambda S: S['g'][0] if 'g' in S else '', 'green')],
    captions={
        'if k == 26': '`k = 26`：字母表只有 26 个，不可能分割 → 答案必为 1',
        'min_k.append': '`min_k[{index}] = {p - 1}`：从 {index} 开始，第 `k` 种不同字母首次出现的位置',
        'while p < n and len(min_freq) < k': lambda S, B, r: (f'窗口内种类 `{len(S.min_freq)} < k = {S.k}` → 右端 `p` 继续右扩'
                                                              if S.p < S.n and len(S.min_freq) < S.k else f'种类已满 `k = {S.k}`（或到头），停下'),
        'max_k.append': '`max_k[{index}] = {q - 1}`：原始分割（不改字母）从 {index} 开始的段终点',
        'while q < n and': lambda S, B, r: ('已满 k 种但下一个字母是旧字母，还能继续并入 → `q` 右扩'
                                            if S.q < S.n and len(S.max_freq) == S.k and S.s[S.q] in S.max_freq
                                            else (f'种类 `{len(S.max_freq)} < k` → `q` 右扩' if S.q < S.n and len(S.max_freq) < S.k
                                                  else '再加就超过 k 种，段到此为止')),
        'g = [0] * (n + 1)': '`f`、`g` 都要倒着填：分割是切前缀，所以从后往前转移',
        'f[index] = f[max_k[index] + 1] + 1': '不修改：`f[{index}] = f[{max_k[index] + 1}] + 1 = {f[index]}`（切掉 {index}..{max_k[index]} 这一段）',
        'g[index] = g[max_k[index] + 1] + 1': '`g` 先取“不修改”的做法：`g[{index}] = {g[index]}`',
        'k_point = min_k[index]': '`k_point = {k_point}`：改字母的关键位置，第 k 种字母首次出现处',
        'if k_point - index + 1 > k and full_k[index]': lambda S, B, r: (
            f'段长 `{S.k_point - S.index + 1} > k = {S.k}` 且已满 k 种 → 有重复字母，改掉一个重复的，就能在 `k_point` 前多切一刀'
            if (S.k_point - S.index + 1 > S.k and S.full_k[S.index]) else '没有可替换的重复字母，这条路走不通'),
        'if k_point - index + 1 == k': lambda S, B, r: (
            f'段长恰好 = k：改其中一个字母，把 `k_point` 与后一位隔断，段到 `k_point` 结束'
            if S.k_point - S.index + 1 == S.k else f'段长 ≠ k，不适用'),
        'if k_point < n - 1 and min_k[index] != max_k[index]': lambda S, B, r: (
            '后面还有字母，且原本就能切得更远 → 值得改 `change_point = k_point + 1` 的字母'
            if (S.k_point < S.n - 1 and S.min_k[S.index] != S.max_k[S.index]) else '没有改 `change_point` 的价值，跳过'),
        'change_point = k_point + 1': '`change_point = {change_point}`：把它改成新字母，就在它前面切开',
        'if change_point + 1 == n': lambda S, B, r: ('`change_point` 是最后一位：单独成一段，至少 2 段' if S.change_point + 1 == S.n
                                                    else '后面还有字母，要看 `nxt_point` 开头那一段'),
        'nxt_point = change_point + 1': '`nxt_point = {nxt_point}`：`min_k[nxt_point]` 依然有效',
        'if (char_state[index] | char_state[nxt_point])': lambda S, B, r: (
            '两段合起来没用满 26 个字母 → 有字母可改' if (S.char_state[S.index] | S.char_state[S.nxt_point]) != (1 << 26) - 1
            else '两段字母用满了，没有空闲字母可改'),
        'if full_k[nxt_point]': lambda S, B, r: ('`nxt_point` 开头的段凑满 k 种 → 改后再多切一刀：`f[min_k[nxt_point]] + 2`'
                                                 if S.full_k[S.nxt_point] else '`nxt_point` 开头不满 k 种'),
        'g[index] = max(g[index], f[min_k[nxt_point]] + 2)': '`g[{index}] = {g[index]}`',
        'elif min_k[nxt_point] == n - 1': '`nxt_point` 开头已是最后一段 → 把它切出去，共 2 段',
        'g[index] = max(g[index], 2)': '`g[{index}] = {g[index]}`',
        'g[index] = max(g[index], f[k_point] + 1)': '`g[{index}] = {g[index]}`',
        'g[index] = max(g[index], f[k_point + 1] + 1)': '`g[{index}] = {g[index]}`',
        'print(f, g)': '看一眼 `f`、`g`：`g[0]` 就是答案',
        'return g[0]': '最多改一次的最大分割数 `g[0] = {g[0]}`',
    },
    skip=[32, 25, 44, 'p += 1', 'q += 1', 'state |=', 'state ^=', 'min_freq[s[index]] -= 1', 'max_freq[s[index]] -= 1',
          'min_freq[s[p]] =', 'max_freq[s[q]] =', 'if min_freq[s[index]] == 0', 'if max_freq[s[index]] == 0',
          'char_state.append', 'min_freq.pop', 'max_freq.pop', 'n = len(s)', 'p = q = 0', 'min_freq = {}', 'max_freq = {}',
          'min_k = []', 'max_k = []', 'char_state = []', 'full_k = []', 'state = 0'],
    max_steps=95,
    cards=dict(
        one_liner='先用滑动窗口预处理，再倒着 DP：f 不改，g 最多改一次',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次删掉至多含 `k` 种字母的最长前缀，最后删完的次数就是段数',
                 '最多把一个字母改成别的小写字母，求最大段数',
                 '示例：`s = "accca"`，`k = 2` → `3`（把中间的 `c` 改成 `b`）'],
        quote='由于题目执行的分割是分割掉前缀，因此在这里需要从后向前进行状态转移。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]`：从 `i` 开始、不改字母的最大段数 = `f[max_k[i] + 1] + 1`',
              '`g[i]`：最多改一次。先取不改的值，再分三类改法：改段内重复字母、隔断 `k_point`、改 `change_point`',
              '改 `change_point` 要求两段字母没用满 26 种，而且改后值得多切一段'],
        summary=['时间 `O(n)`，空间 `O(n)`；`k == 26` 必须先特判',
                 '易错点：不止「改 `k_point+1`」一种，`aabca`（`k=3`）改段内重复字母才对',
                 '`min_k` 与 `max_k` 区别：前者是第 k 种字母首次出现，后者是原始分割的终点',
                 '原文为 Python 2 写法，`print f, g` 已改为 `print(f, g)`'],
    ),
)
