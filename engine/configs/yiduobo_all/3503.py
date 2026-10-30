CODE = '''
class Solution(object):
    def longestPalindrome(self, s, t):
        t = t[::-1]
        m = len(s)
        n = len(t)
        f = [[0] * n for _ in range(m)]
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if s[i] == t[j]:
                    f[i][j] = 1
                    if i + 1 < m and j + 1 < n:
                        f[i][j] += f[i + 1][j + 1]

        def calc(s):
            n = len(s)
            g = [[False] * n for _ in range(n)]
            for length in range(1, n + 1):
                for left in range(n):
                    right = left + length - 1
                    if right >= n:
                        break

                    if left == right:
                        g[left][right] = True
                    elif left == right - 1:
                        g[left][right] = (s[left] == s[right])
                    else:
                        g[left][right] = (s[left] == s[right]) and g[left + 1][right - 1]

            best = [0] * (n + 1)
            for i in range(n):
                for j in range(n - 1, -1, -1):
                    if g[i][j]:
                        best[i] = j - i + 1
                        break

            return best

        gs = calc(s)
        gt = calc(t)
        res = max(max(gs), max(gt))
        for i in range(m):
            for j in range(n):
                res = max(res, f[i][j] * 2 + max(gs[i + f[i][j]], gt[j + f[i][j]]))

        return res
'''

def _top(S):
    ln = S.get('_line', 0)
    if ln <= 12:
        if 'i' in S and 'j' in S:
            return f"`f[i][j]`：`s[{S['i']}..]` 与翻转后 `t[{S['j']}..]` 从头开始能连续相同的长度"
        return '先把 `t` 翻转，「s 的子串」和「t 的子串」对称 ⇔ 翻转后相同'
    if ln <= 37:
        return '`g[left][right]`：`s[left..right]` 是不是回文；`best[i]`：以 `i` 开头的最长回文子串长度'
    return '拼接串 = `s 的前缀` + ==中间回文== + `t 的后缀`，长度 = `f × 2 + max(gs, gt)`'


def _gcol(S, r, c, v):
    if S.get('_line') in (24, 26, 28) and (r, c) == (S.get('left'), S.get('right')):
        return 'yellow'
    if S.get('_line') in (33, 34) and (r, c) == (S.get('i'), S.get('j')):
        return 'yellow'
    return 'green' if v else None


def _fcol(S, r, c, v):
    ln = S.get('_line', 0)
    if ln in (9, 10, 11, 12) and (r, c) == (S.get('i'), S.get('j')):
        return 'yellow'
    if ln >= 44 and (r, c) == (S.get('i'), S.get('j')):
        return 'yellow'
    return 'green' if v else None


def _if9(S, B, ret):
    i, j = S.i, S.j
    if S.s[i] == S.t[j]:
        return f"`s[{i}] = '{S.s[i]}'` == `t[{j}] = '{S.t[j]}'` → 能匹配"
    return f"`s[{i}] = '{S.s[i]}'` ≠ `t[{j}] = '{S.t[j]}'` → `f[{i}][{j}]` 保持 ==0=="


def _res44(S, B, ret):
    i, j = S.i, S.j
    k = S.f[i][j]
    cand = k * 2 + max(S.gs[i + k], S.gt[j + k])
    return (f"`f[{i}][{j}] × 2 + max(gs[{i + k}], gt[{j + k}])` = `{k * 2} + max({S.gs[i + k]}, {S.gt[j + k]})` = {cand}"
            f"，`res` = =={S.res}==" + ('（刷新答案）' if S.res != B.get('res') else ''))


CONFIG = dict(
    num=3503, title='子字符串连接后的最长回文串 I', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='翻转 t 的最长公共前缀 DP + 回文 DP',
    tags=[],
    code=CODE,
    call='Solution().longestPalindrome("abc", "ba")',
    expect=5,
    views=[
        dict(type='text', fn=_top, size=24, h=60),
        dict(type='string', var='s', label='s（calc 内是它的参数）', cell=56, h=150,
             pointers={'i': 'blue', 'left': 'blue', 'right': 'pink'}),
        dict(type='string', var='t', label='t（翻转后）', cell=56, h=150, pointers={'j': 'pink'}),
        dict(type='table', var='f', label='f[i][j]', cell=64, h=170, color=_fcol),
        dict(type='table', var='g', label='g[left][right]（绿 = 回文）', cell=64, h=170, color=_gcol),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), 'best', 'res'],
    skip=['m = len', 'n = len', 'for length', 'for left', 'right = left', 'if right >= n', 'break',
          'for i in range', 'for j in range', 'f = [[0]', 'g = [[False]', 'best = [0]', 'def calc', 'if left == right:'],
    max_steps=110,
    captions={
        3: '先翻转 `t` → `{t}`：判断「两个子串对称」就变成判断「两个子串相同」',
        9: _if9,
        10: '`f[{i}][{j}] = 1`：这个字符匹配上了，至少长 1',
        11: lambda S, B, ret: ('`i + 1 < m and j + 1 < n` ==成立==：后面还有字符，可以接着往后连' if S.i + 1 < len(S.s) and S.j + 1 < len(S.t)
                               else '`i + 1 < m and j + 1 < n` 不成立：已经到头，不能再延长'),
        12: '`f[{i}][{j}] += f[{i+1}][{j+1}]`：在后一位的基础上多一个 → =={f[i][j]}==',
        39: '`calc(s)`：用回文 DP 算出 `s` 中每个起点的最长回文子串长度 `gs`',
        40: '`calc(t)`：同样算出翻转后 `t` 的 `gt`',
        23: lambda S, B, ret: (f'`left == right`：单个字符一定是回文' if S.left == S.right else f'`left = {S.left}`，`right = {S.right}`，长度 {S.right - S.left + 1}：不是单个字符'),
        24: '`g[{left}][{right}] = True`：长度 1 必为回文',
        25: lambda S, B, ret: (f'`left == right - 1`：长度 2，只要两个字符相等就是回文' if S.left == S.right - 1 else f'长度 {S.right - S.left + 1} ≥ 3：看两端 + 里面'),
        26: lambda S, B, ret: f"`s[{S.left}] = '{S.s[S.left]}'` vs `s[{S.right}] = '{S.s[S.right]}'` → `g[{S.left}][{S.right}] = ` =={S.g[S.left][S.right]}=="
                              ,
        28: lambda S, B, ret: (f"两端 `'{S.s[S.left]}'` 与 `'{S.s[S.right]}'` 相等且 `g[{S.left + 1}][{S.right - 1}] = {S.g[S.left + 1][S.right - 1]}` → `g[{S.left}][{S.right}] = ` =={S.g[S.left][S.right]}=="),
        33: lambda S, B, ret: (f'倒序枚举终点：`g[{S.i}][{S.j}]` 是回文 → ==最长的找到了==' if S.g[S.i][S.j] else f'`g[{S.i}][{S.j}]` 不是回文，终点再往前缩'),
        34: '`best[{i}] = {j} − {i} + 1` = =={best[i]}==：以 `{i}` 开头的最长回文子串长度，直接 `break`',
        37: '返回 `best`：=={ret}==',
        41: '只用 `s` 或只用 `t` 的情形：`res = max(max(gs), max(gt))` = =={res}==',
        44: _res44,
        46: '枚举完所有 `(i, j)`，最长回文串长度 = =={ret}==',
    },
    cards=dict(
        one_liner='翻转 t 找对称的前后缀，中间再接一段回文',
        complexity='时间 `O(m·n + m² + n²)`，空间同阶',
        problem=['从 `s` 取一个子串、从 `t` 取一个子串（可为空），按顺序拼接',
                 '求能拼出的==最长回文串==的长度',
                 '示例：`s = "abcde"`，`t = "ecdba"` → `5`（`"abc" + "ba"`）；本视频 `"abc"`、`"ba"` → `5`'],
        quote='拼接后的字符串形如 [sub_s的前缀] [空串 或者 sub_s的后缀 或者 sub_t的前缀] [sub_t的后缀]，其中两侧必须是对称的，而中间这个部分必须自成回文。',
        quote_src='—— yiduobo 题解原文',
        idea=['翻转 `t`，两侧「对称」变成「相同」：`f[i][j]` = `s[i..]` 与 `t[j..]` 的最长公共前缀',
              '`calc` 用回文 DP 求 `g`，再得到 `best[i]` = 以 `i` 开头的最长回文子串',
              '答案 = `max(f[i][j] × 2 + max(gs[i + f], gt[j + f]))`；只用一个串时就是 `max(gs)`、`max(gt)`'],
        summary=['时间 `O(m·n + m² + n²)`，空间同阶；`s`、`t` 都不超过 30',
                 '`f` 要从后往前算（依赖 `f[i+1][j+1]`），所以两层循环都倒序',
                 '`gs[i + f]` 的下标可达 `len(s)`，所以 `best` 开了 `n + 1`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串（代码本身未改）',
                 '同系列：3504 数据范围到 1000，思路相同但需要更快的回文预处理'],
    ),
)
