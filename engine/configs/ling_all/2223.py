def _top(S):
    if 'i' not in S or 'z' not in S:
        return '`z[i]` = 后缀 `s[i:]` 和 `s` 的最长公共前缀；答案 = 所有 `z[i]` 之和（`z[0]` 按 `n` 算）'
    i, z, l, r, s = S['i'], S['z'], S['l'], S['r'], S['s']
    box = f'z-box = `[{l}, {r}]`' if r >= l and r > 0 else 'z-box 还是空的'
    return f'算 `z[{i}]`：{box}，当前累计 `ans = {S["ans"]}`'


def _while(S, B, ret):
    i, z, n, s = S.i, S.z, S.n, S.s
    k = z[i]
    if i + k >= n:
        return f'`i + z[i] = {i + k} ≥ n = {n}`，已经比到末尾 → 停止扩展'
    a, b = s[k], s[i + k]
    if a == b:
        return f"比较 `s[{k}] = '{a}'` 和 `s[{i + k}] = '{b}'` → ==相等==，继续往右扩展"
    return f"比较 `s[{k}] = '{a}'` 和 `s[{i + k}] = '{b}'` → ==不等==，`z[{i}] = {k}` 定下来"


def _zline(S, B, ret):
    i, l, r = S.i, S.l, S.r
    if i > r:
        return f'`i = {i} > r = {r}`：不在 z-box 里，没有现成信息，`z[{i}] = 0`，从头暴力比'
    return (f'`i = {i}` 在 z-box `[{l}, {r}]` 里：`s[{i}:]` 和 `s[{i - l}:]` 相同，'
            f'先抄 `min(z[{i - l}], {r - i + 1})` = =={S.z[i]}==')


CONFIG = dict(
    num=2223, title='构造字符串的总得分和', difficulty='Hard', category='字符串',
    author='灵茶山艾府', technique='Z 函数（扩展 KMP）',
    tags=['灵神题单', '字符串', '难度分 2220'],
    code='''
class Solution:
    def sumScores(self, s: str) -> int:
        n = len(s)
        z = [0] * n
        ans, l, r = n, 0, 0
        for i in range(1, n):
            z[i] = max(min(z[i - l], r - i + 1), 0)  # 注：不用 min max，拆开用 < > 比较会更快（仅限于 Python）
            while i + z[i] < n and s[z[i]] == s[i + z[i]]:
                l, r = i, i + z[i]
                z[i] += 1
            ans += z[i]
        return ans
''',
    call='Solution().sumScores("azbazbzaz")',
    expect=14,
    views=[
        dict(type='text', fn=_top, size=26, h=70),
        dict(type='string', var='s', label='s（框 = z-box；粉 = s[i+z[i]]，青 = s[z[i]]）', cell=76, h=250,
             window=('l', 'r'), pointers={'i': 'blue', 'i + z[i]': 'pink', 'z[i]': 'cyan'},
             pointer_labels={'i': 'i', 'i + z[i]': 'i+z', 'z[i]': 'z[i]'}),
        dict(type='array', var='z', label='z 数组（z[i] = s[i:] 与 s 的最长公共前缀）', cell=76, h=200,
             pointers={'i': 'blue'}, color=lambda S, k, v: 'green' if k == S.get('i') and S.get('_line') in (10, 11) else None),
    ],
    watch=[('i', 'i', 'blue'), ('l', 'l', 'cyan'), ('r', 'r', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'n = len': '`n = {n}`',
        'z = [0] * n': '`z[i]` 记录 `s[i:]` 与 `s` 的最长公共前缀，先全部置 0',
        'ans, l, r = n': '`z[0]` 本身就是整个串，得分为 `n = {n}`，所以 `ans` 从 `n` 开始；`[l, r]` 是 z-box：目前最靠右的匹配区间',
        'for i in range': lambda S, B, ret: (f'枚举后缀起点 `i = {S.i}`' if B.get('i') != S.i else '`i` 枚举完了，循环结束'),
        'z[i] = max': _zline,
        'while i + z[i] < n': _while,
        'l, r = i, i + z[i]': 'z-box 向右推进：`[l, r] = [{l}, {r}]`（`s[l..r]` 与 `s` 的前缀相同）',
        'z[i] += 1': '匹配长度加一：`z[{i}] = {z[i]}`',
        'ans += z[i]': '`s_{n-i}` 的得分 = `z[{i}] = {z[i]}`，`ans` = {ans}',
        'return ans': '所有得分加起来 = `{ret}`',
    },
    cards=dict(
        one_liner='得分就是 Z 数组：每个后缀与整串的最长公共前缀',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['从空串开始，每次在前面加一个字符，得到 `s_1 … s_n`（`s_n = s`）',
                 '`s_i` 的得分 = `s_i` 与 `s` 的最长公共前缀长度，求得分之和',
                 '示例：`s = "azbazbzaz"` → `14`（`az` 得 2，`azbzaz` 得 3，整串得 9）'],
        quote='题目求的就是扩展 KMP（Z 数组）的所有元素之和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`s_i` 就是 `s` 的后缀，所以得分 = 后缀与 `s` 的 LCP = ==Z 数组==',
              '`[l, r]` 记录最靠右的匹配区间：`i` 落在里面时，直接抄 `z[i - l]`，再和剩余长度取 `min`',
              '只有往右越过 `r` 才需要逐个比较，所以总比较次数是线性的'],
        summary=['时间 `O(n)`：`r` 只会右移，扩展比较总共不超过 `n` 次',
                 '`ans` 初值是 `n`：`z[0]` 按整串长度算，循环从 `i = 1` 开始',
                 '`z[i - l]` 不能越过 z-box，要和 `r - i + 1` 取小；`i > r` 时这一项为负，用 `max(…, 0)` 兜底',
                 '灵神注释：不用 `min`/`max` 而改成 `<`、`>` 比较在 Python 里更快',
                 '同类题：3031 / 3388（Z 函数的应用）'],
    ),
)
