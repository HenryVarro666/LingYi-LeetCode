S0, K0 = 'abcac', 2


def _tbl(S, i, j, v):
    if S.get('_line') in (None,):
        return None
    L, jj = S.get('L'), S.get('j')
    if L is not None and jj is not None and i == L and j == jj and S.get('_line') not in (14, 15, 16, 17):
        return 'yellow'
    return None


def _fcol(S, i, v):
    jj = S.get('j')
    if jj is not None and i == jj and 'L' in S:
        return 'yellow'
    return None


def _text(S):
    if 'modify' not in S or 'i' not in S:
        return '`modify[l][r]` = 把 `s[l..r]` 变成半回文串的最少修改数'
    if S.get('_line', 0) >= 29 and 'j' in S:
        j, i = S['j'], S['i']
        return f'`f[{j}]` = `min( f[L-1] + modify[L][{j}] )`，`L` 从 `{i*2}` 到 `{j-1}`'
    return '先预处理所有子串的 `modify`，再做划分型 DP'


CONFIG = dict(
    num=2911, title='得到 K 个半回文串的最少修改次数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='预处理 + 划分型 DP（递推，一维滚动）',
    tags=['灵神题单', '动态规划', '难度分 2608'],
    code='''
MX = 201
divisors = [[] for _ in range(MX)]
for i in range(1, MX):
    for j in range(i * 2, MX, i):
        divisors[j].append(i)

def get_modify(s: str) -> int:
    res = n = len(s)
    for d in divisors[n]:
        cnt = 0
        for i0 in range(d):
            i, j = i0, n - d + i0
            while i < j:
                cnt += s[i] != s[j]
                i += d
                j -= d
        res = min(res, cnt)
    return res

class Solution:
    def minimumChanges(self, s: str, k: int) -> int:
        n = len(s)
        modify = [[0] * n for _ in range(n - 1)]
        for left in range(n - 1):
            for right in range(left + 1, n):
                modify[left][right] = get_modify(s[left: right + 1])

        f = modify[0]
        for i in range(1, k):
            for j in range(n - 1 - (k - 1 - i) * 2, i * 2, -1):  # 左右都要预留空间
                f[j] = min(f[L - 1] + modify[L][j] for L in range(i * 2, j))
        return f[-1]
''',
    call=f'Solution().minimumChanges({S0!r}, {K0})',
    expect=1,
    max_steps=56,
    skip=['cnt = 0', 'i += d', 'j -= d', 'for i0 in range', 'res = n = len', 'modify = [[0]'],
    views=[
        dict(type='string', var=lambda S: S0, label='s', h=120, cell=70),
        dict(type='table', var='modify', label='modify[l][r]（行 = 左端 l，列 = 右端 r）', h=260, cell=64,
             rows=lambda S: [f'{k}{c}' for k, c in enumerate(S0[:-1])], cols=lambda S: [f'{k}{c}' for k, c in enumerate(S0)],
             cursors=[('left', 'right', 'yellow', '(l,r)')]),
        dict(type='array', var='f', label='f[j]：s[0..j] 分成 i+1 段的最少修改（与 modify[0] 共用同一数组）', h=200, cell=80,
             pointers={'j': 'pink'}),
        dict(type='text', fn=_text, size=24, h=60),
    ],
    watch=['left', 'right', 'i', 'j', 'L', ('res', 'res', 'green')],
    captions={
        'n = len(s)': '`n = {n}`：字符串长度',
        'modify = [[0]': '`modify` 先全填 0：行是左端 `l`，列是右端 `r`；长度至少为 2 才有意义，所以只要 `n-1` 行',
        'for left in range': '枚举子串左端 `left = {left}`',
        'for right in range': '枚举右端 `right = {right}`：半回文串长度至少为 2',
        'modify[left][right] =': '对 `s[{left}..{right}]` = `{s[left:right+1]!r}` 调用 `get_modify` 求最少修改数，存入 `modify[{left}][{right}]`（见下方 return）',
        'res = n = len(s)': '`res = n = {n}`：子串长 `{n}`，改动次数最坏不超过长度，当作初值',
        'for d in divisors': '枚举真因子 `d = {d}`（`d` 必须小于子串长度）',
        'cnt = 0': '因子 `d` 把子串分成 `d` 组（下标模 `d` 相同），先清零改动数',
        'for i0 in range': '检查第 `i0 = {i0}` 组：下标 `i0, i0+d, i0+2d, ...`',
        'i, j = i0, n - d + i0': '这组的首尾：`i = {i}`，`j = {j}`，向中间走就是判回文',
        'while i < j': lambda S, B, r: (f'`i = {S.i} < j = {S.j}`：这一对还没配完' if S.i < S.j else f'`i = {S.i} >= j = {S.j}`：这一组配完了'),
        'cnt += s[i] != s[j]': lambda S, B, r: (f'`s[{S.i}] = {S.s[S.i]!r}` ≠ `s[{S.j}] = {S.s[S.j]!r}`：这一对要改 1 个 → `cnt = {S.cnt}`' if S.cnt > B.cnt
                                                 else f'`s[{S.i}] = {S.s[S.i]!r}` = `s[{S.j}] = {S.s[S.j]!r}`：相等，不用改 → `cnt = {S.cnt}`'),
        'i += d': '`i` 向右跳 `d` 步 → {i}',
        'j -= d': '`j` 向左跳 `d` 步 → {j}',
        'res = min(res, cnt)': '因子 `d = {d}` 要改 `{cnt}` 次，取各因子最小：`res = {res}`',
        'return res': '该子串最少修改 =={res}== 次',
        'f = modify[0]': '`f[j]` 初值 = `modify[0][j]`：只分一段时，整个前缀就是那一段',
        'for i in range(1, k)': '现在要分成 `i + 1` 段（`i = {i}`）',
        'for j in range(n - 1 -': lambda S, B, r: (f'倒序枚举 `j = {S.j}`：右边给后面的段留 2 个字符，左边给前面的段留 `2i` 个；倒序才不会覆盖还要用的旧 `f`' if S.get('j') is not None and (B.get('j') is None or S.j != B.j)
                                                   else '这一层的 `j` 都算完了'),
        'f[j] = min(': '最后一段是 `s[L..{j}]`，前面 `s[0..L-1]` 用 `i` 段：`f[{j}] = min(f[L-1] + modify[L][{j}])` = =={f[j]}==',
        'return f[-1]': '`f[-1]` 就是整串分 `k` 段的答案：=={f[-1]}==',
    },
    cards=dict(
        one_liner='先算每个子串变半回文串的代价，再做划分型 DP',
        complexity='时间 `O(n³ log n)`，空间 `O(n²)`',
        problem=['把 `s` 划成 `k` 段，每段改成半回文串（按因子 `d` 分组后每组都是回文），求最少改字符数',
                 '示例：`s = "abcac", k = 2` → `1`（`ab` 改 1 个，`cac` 不用改）',
                 '本视频沿用这个例子'],
        quote='预处理 s 的每个【长度至少为 2 的】子串修改成半回文串至少要修改多少次，记到数组 modify 中',
        quote_src='—— 灵茶山艾府题解',
        idea=['对每个子串枚举真因子 `d`，每组按回文配对统计不同对数，取最小',
              '`f[i][j]` = 前 `j+1` 个字符分 `i+1` 段的最少修改：`min f[i-1][L-1] + modify[L][j]`',
              '`L` 从 `2i` 开始（前面每段至少 2 个字符），到 `j-1` 结束（最后一段至少 2 个）'],
        summary=['预处理占大头：`O(n²)` 个子串 × 平均 `O(log n)` 个因子 × `O(n)` 判断',
                 '`i` 从 1 起：`f = modify[0]` 直接当 `i = 0` 的初值，倒序 `j` 防止覆盖',
                 '易错：`d` 必须严格小于子串长；长度 1 的串没有因子，所以子串至少长 2',
                 '灵神还给了记忆化搜索写法 `dfs(i, j)`，本视频演示最终的一维递推'],
    ),
)
