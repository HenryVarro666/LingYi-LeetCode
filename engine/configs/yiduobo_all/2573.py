def _r(fa, x):
    while fa[x] != x:
        x = fa[x]
    return x


CONFIG = dict(
    num=2573, title='找出对应 LCP 矩阵的字符串', difficulty='Hard', category='贪心算法',
    author='yiduobo', technique='并查集 + 逐项检查',
    tags=['灵神题单', '贪心与思维', '难度分 2682'],
    code='''
class Solution(object):
    def findTheString(self, lcp):

        n = len(lcp)
        fa = list(range(n))

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        check_list = []
        for i in range(n):
            for j in range(n):
                if i == j:
                    if lcp[i][j] != n - i:
                        return ""
                    continue
                
                if j < i:
                    if lcp[i][j] != lcp[j][i]:
                        return ""
                    continue
                
                if lcp[i][j] == 0:
                    check_list.append([i, j])
                else:
                    if j + 1 < n and lcp[i][j] - 1 != lcp[i + 1][j + 1]:
                        return ""

                    if lcp[i][j] > n - j:
                        return ""

                    fa_i = find(i)
                    fa_j = find(j)
                
                    if fa_i < fa_j:
                        fa[fa_j] = fa_i
                    else:
                        fa[fa_i] = fa_j

        for i, j in check_list:
            if find(i) == find(j):
                return ""

        res = []
        now = 0
        mapping = {}
        for i in range(n):
            if find(i) == i:
                if now < 26:
                    mapping[i] = chr(now + 97)
                    now += 1
                else:
                    return ""
            
            res.append(mapping[fa[i]])
        
        return ''.join(res)
''',
    call='Solution().findTheString([[3, 0, 1], [0, 2, 0], [1, 0, 1]])',
    expect='aba',
    max_steps=90,
    skip=['continue', 'if i == j:', 'if j < i:', 'if fa[x] != x', 'return fa[x]', 'fa[x] = find', 'for j in range(n)', 'for i in range(n)', 'fa_i = find', 'fa_j = find', 'n = len', 'now = 0',
          'check_list = []', 'res = []', 'mapping = {}', 'for i, j in check_list'],
    views=[
        dict(type='text', size=26, h=60,
             fn=lambda S: ('用并查集把“必须相同”的下标并到一起，lcp 为 0 的对必须不同' if 'res' not in S
                           else f"按下标先后给每个连通块分配字母：`{S.get('res')}`")),
        dict(type='table', var='lcp', label='lcp（黄 = 当前 (i,j)）', cell=84, h=290,
             color=lambda S, i, j, v: 'yellow' if S.get('i') == i and S.get('j') == j and 'res' not in S else None),
        dict(type='array', var='fa', label='fa（并查集：fa[x] = x 所在连通块的代表）', cell=84, h=190, pointers={'i': 'blue', 'j': 'pink'},
             color=lambda S, k, v: 'green' if v == k else None),
        dict(type='array', var=lambda S: S.get('check_list') and [f'{a}≠{b}' for a, b in S['check_list']],
             label='check_list（lcp = 0，待检查必须不连通）', cell=96, h=150),
    ],
    watch=['i', 'j', 'now', ('mapping', 'mapping')],
    captions={
        'fa = list(range(n))': '并查集初始化：每个下标自成一块，`fa = {fa}`',
        'if lcp[i][j] != n - i': lambda S, B, r: (f'`lcp[{S.i}][{S.i}] = {S.lcp[S.i][S.i]}`，应等于后缀长度 `n - i = {S.n - S.i}` → 一致'
                                                  if S.lcp[S.i][S.i] == S.n - S.i else '自己和自己的 LCP 必须是后缀长度 → 不符，返回空串'),
        'if lcp[i][j] != lcp[j][i]': lambda S, B, r: (f'`lcp[{S.i}][{S.j}] = lcp[{S.j}][{S.i}] = {S.lcp[S.i][S.j]}`：矩阵对称，只需检查 `i < j`'
                                                      if S.lcp[S.i][S.j] == S.lcp[S.j][S.i] else '不对称 → 返回空串'),
        'if lcp[i][j] == 0': lambda S, B, r: (f'`lcp[{S.i}][{S.j}] = 0`：`{S.i}` 和 `{S.j}` 必须不同，先记到 `check_list`，等并查集建完再查'
                                              if S.lcp[S.i][S.j] == 0 else f'`lcp[{S.i}][{S.j}] = {S.lcp[S.i][S.j]} > 0`：`word[{S.i}] == word[{S.j}]`，要合并'),
        'check_list.append': '`check_list` = {check_list}',
        'if j + 1 < n and': '非 0 的 `lcp[i][j]` 必须等于 `lcp[i+1][j+1] + 1`；`{lcp[i][j]} - 1` 对 `lcp[{i}+1][{j}+1]`，一致',
        'if lcp[i][j] > n - j': '`lcp[i][j]` 不能超过后缀 `j` 的长度 `n - j = {n - j}`，通过',
        'if fa_i < fa_j': '`fa_i = {fa_i}`，`fa_j = {fa_j}`：比较代表，小的做根',
        'fa[fa_j] = fa_i': '合并：`fa[{fa_j}] = {fa_i}` → `fa = {fa}`',
        'fa[fa_i] = fa_j': '合并：`fa[{fa_i}] = {fa_j}` → `fa = {fa}`',
        'if find(i) == find(j)': lambda S, B, r: (f'`{S.i}` 和 `{S.j}` 已连通，却要求不同 → 矛盾，返回空串' if _r(S.fa, S.i) == _r(S.fa, S.j)
                                                  else f'`{S.i}` 和 `{S.j}` 不连通 → 满足 `lcp = 0`'),
        'if find(i) == i': lambda S, B, r: (f'`{S.i}` 是连通块的代表 → 分配新字母' if _r(S.fa, S.i) == S.i
                                            else f'`{S.i}` 属于代表 `{S.fa[S.i]}` 的块，沿用它的字母'),
        'if now < 26': '字母数 `now = {now} < 26`，还有字母可用',
        'mapping[i] = chr': '代表 `{i}` 对应字母 `{mapping[i]}` → `{mapping}`',
        'now += 1': '下一个块用下一个字母，`now = {now}`',
        'res.append': '`word[{i}] = {mapping[fa[i]]}` → `res = {res}`',
        "return ''.join": '拼起来返回 `{ret}`',
    },
    cards=dict(
        one_liner='lcp 非零的下标必须同字母：用并查集合并，再检查为零的对',
        complexity='时间 `O(n²·α(n))`，空间 `O(n²)`（check_list）',
        problem=['`lcp[i][j]` 是后缀 `word[i:]` 与 `word[j:]` 的最长公共前缀长度',
                 '给定 `n×n` 的 `lcp`，返回对应的字典序最小字符串，不存在返回空串',
                 '本视频：`[[3,0,1],[0,2,0],[1,0,1]]` → `"aba"`'],
        quote='对于一组lcp[i][j] = 0，若i和j属于同一个连通块，说明其通过其他lcp值建立起了相等关系，此时的lcp[i][j]就不能等于0，于是可以直接返回空字符串。',
        quote_src='—— yiduobo 题解原文',
        idea=['先排除明显不合法：`lcp[i][i] = n - i`、矩阵对称、`lcp[i][j] ≤ n - j`',
              '非零的 `lcp[i][j]` 必须 `= lcp[i+1][j+1] + 1`，且 `word[i] == word[j]` → 并查集合并',
              '零的位置要等所有合并完成后再检查；连通块超过 26 个无解，按下标顺序依次分配 a~z'],
        summary=['时间 `O(n²·α(n))`，空间 `O(n²)`',
                 '易错：`lcp = 0` 的检查必须放在所有非零合并之后',
                 '连通块按首个下标顺序分配字母，保证字典序最小',
                 '原文为 Python 2 风格，`fa = range(n)` 已改为 `fa = list(range(n))`（Python 3 的 range 不能赋值）',
                 '对比灵神：灵神贪心逐个字母填，再 DP 验证整个矩阵；yiduobo 用并查集 + 逐项检查'],
    ),
)
