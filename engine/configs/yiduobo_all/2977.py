SRC, TGT = 'abcc', 'bcdc'
ORIG = ['a', 'b', 'ab', 'c', 'e']
CHG = ['b', 'c', 'bc', 'e', 'd']
COST = [1, 2, 2, 1, 1]
STRS = []
for _s in ORIG + CHG:
    if _s not in STRS:
        STRS.append(_s)

CODE = '''
class Solution(object):
    def minimumCost(self, source, target, original, changed, cost):

        mapping = {}
        length_set = set()
        tot = 0
        for s in original:
            if s not in mapping:
                mapping[s] = tot
                tot += 1
            length_set.add(len(s))

        for s in changed:
            if s not in mapping:
                mapping[s] = tot
                tot += 1
            length_set.add(len(s))
        
        dis = [[-1] * tot for _ in range(tot)]
        m = len(original)
        for index in range(m):
            x = mapping[original[index]]
            y = mapping[changed[index]]
            if dis[x][y] == -1 or dis[x][y] > cost[index]:
                dis[x][y] = cost[index]
        
        for k in range(tot):
            for i in range(tot):
                for j in range(tot):
                    if dis[i][k] != -1 and dis[k][j] != -1 and (dis[i][j] == -1 or dis[i][j] > dis[i][k] + dis[k][j]):
                        dis[i][j] = dis[i][k] + dis[k][j]
        
        f = [0]
        n = len(source)
        for index in range(n):
            if source[index] == target[index]:
                f.append(f[-1])
            else:
                f.append(-1)
            
            for length in length_set:
                if length > index + 1:
                    continue
                
                x = mapping.get(source[index - length + 1 : index + 1], -1)
                if x == -1:
                    continue
                y = mapping.get(target[index - length + 1 : index + 1], -1)
                if y == -1:
                    continue

                if dis[x][y] != -1 and f[index - length + 1] != -1 and (f[-1] == -1 or f[-1] > f[index - length + 1] + dis[x][y]):
                    f[-1] = f[index - length + 1] + dis[x][y]

        return f[-1]
'''
_L = CODE.split('\n')


def _ln(sub, nth=1):
    c = 0
    for i, t in enumerate(_L):
        if sub in t:
            c += 1
            if c == nth:
                return i
    raise KeyError(sub)


L_LEN = _ln('for length in length_set')
L_UPD = _ln('f[-1] = f[index - length + 1] + dis[x][y]')
L_FK = _ln('for k in range(tot)')


def _win(S):
    if S.get('_line', 0) <= L_LEN or S.get('_line', 0) > L_UPD + 1 or 'length' not in S or 'index' not in S:
        return None
    st = S['index'] - S['length'] + 1
    return st if st >= 0 else None


def _fcolor(S, i, v):
    n = len(S.get('f', []))
    if i == n - 1 and S.get('_line', 0) >= _ln('for index in range(n)'):
        return 'blue'
    return None


def _tcolor(S, i, j, v):
    line = S.get('_line', 0)
    if line == L_FK and 'k' in S and (i == S['k'] or j == S['k']) and v != -1:
        return 'yellow'
    if L_LEN < line <= L_UPD + 1 and 'x' in S and 'y' in S and (i, j) == (S['x'], S['y']) and S['x'] != -1 and S['y'] != -1:
        return 'green'
    return None


def _txt(S):
    line = S.get('_line', 0)
    if 'f' not in S or line < _ln('f = [0]'):
        return '`mapping` 给每个字符串编号；`dis[a][b]` = 把 a 变成 b 的最小成本，`-1` 表示变不过去'
    idx = S.get('index')
    if idx is None:
        return ''
    L = S.get('length')
    if L is not None and line > L_LEN and idx - L + 1 >= 0:
        s, t = SRC[idx - L + 1: idx + 1], TGT[idx - L + 1: idx + 1]
        return f'`f[{idx + 1}]`：末尾 `{L}` 位 `{s}` → `{t}`'
    return f'`f[{idx + 1}]`：`source[:{idx + 1}]` = `{SRC[:idx + 1]}` 变成 `{TGT[:idx + 1]}` 的最小成本（`-1` = 做不到）'


def _upd_cond(S, B, r):
    L, idx = S.length, S.index
    s, t = S.source[idx - L + 1: idx + 1], S.target[idx - L + 1: idx + 1]
    d, base = S.dis[S.x][S.y], S.f[idx - L + 1]
    if d == -1 and s == t:
        return f'`{s}` → `{t}`：两段本来就相同，不需要操作（`dis = -1`）→ 跳过，上面「不修改」已经处理'
    if d == -1:
        return f'`{s}` → `{t}`：`dis = -1`，变不过去 → 跳过'
    if base == -1:
        return f'`{s}` → `{t}`：`dis = {d}`，但前面 `f[{idx - L + 1}] = -1` 做不到 → 跳过'
    cur = S.f[-1]
    if cur == -1:
        return f'`{s}` → `{t}`：`dis = {d}`，前缀 `f[{idx - L + 1}] = {base}`，当前 `f[{idx + 1}] = -1`（还没有方案）→ ==可以更新=='
    if cur > base + d:
        return f'`{s}` → `{t}`：`{base} + {d} = {base + d}` 比当前 `{cur}` 更小 → ==更新=='
    return f'`{s}` → `{t}`：`{base} + {d} = {base + d}` 不比当前 `{cur}` 小 → 不更新'


CONFIG = dict(
    num=2977, title='转换字符串的最小成本 II', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='Floyd + 前缀 DP（哈希表查子串）',
    tags=['灵神题单·图论算法', '灵神题单·动态规划', '难度分 2696'],
    code=CODE,
    call=f'Solution().minimumCost({SRC!r}, {TGT!r}, {ORIG!r}, {CHG!r}, {COST!r})',
    expect=4,
    views=[
        dict(type='string', var='source', label='source', cell=56, h=175, window=(_win, 'index')),
        dict(type='string', var='target', label='target（框 = 末尾 length 位）', cell=56, h=175, window=(_win, 'index')),
        dict(type='array', var='f', label='f：前 i 个字符变成 target 前 i 个的最小成本', color=_fcolor, cell=56, h=175),
        dict(type='table', var='dis', label='dis：行 → 列 的最小成本（-1 = 变不过去）', rows=STRS, cols=STRS, color=_tcolor, cell=60, h=360),
    ],
    watch=[('index', 'index', 'blue'), ('length', 'length', 'pink'), ('x', 'x', 'cyan'), ('y', 'y', 'orange'), ('f[-1]', 'f[-1]', 'green')],
    skip=['mapping[s] = tot', 'for s in original', 'for s in changed', 'if s not in mapping', 'tot += 1', 'length_set.add', 'm = len(original)', 'for index in range(m)',
          'x = mapping[original', 'y = mapping[changed', 'if dis[x][y] == -1 or', 'for i in range(tot)', 'for j in range(tot)',
          'if dis[i][k] != -1', 'dis[i][j] = dis[i][k]', 'n = len(source)', 'for length in length_set', 'if length > index + 1', 'continue',
          'x = mapping.get', 'y = mapping.get', 'if x == -1', 'if y == -1', 'tot = 0', 'mapping = {}', 'length_set = set()'],
    captions={
        'mapping[s] = tot': '给字符串 `{s!r}` 编号 `{tot}`：`mapping = {mapping}`（它既是图的一个点，也是 `dis` 的行列号）',
        'dis = [[-1]': '所有出现过的字符串各给一个编号：`mapping = {mapping}`；`tot = {tot}` 个字符串 → `dis` 是 `{tot}×{tot}` 矩阵，`-1` 表示还不能变；`length_set = {sorted(length_set)}` 记下所有可变换串的长度',
        'dis[x][y] = cost[index]': '操作 `{original[index]}` → `{changed[index]}` 成本 `{cost[index]}`：`dis[{x}][{y}] = {dis[x][y]}`（重复边取较小）',
        'for k in range(tot)': lambda S, B, r: ('Floyd 跑完：`dis` 里就是每对字符串之间的最小成本（比如 `c → e → d` 只要 2）' if B.get('k') == S.get('k') else
                                                f'Floyd 枚举中转点 `k = {S.k}`（`{STRS[S.k]}`）：黄色行列是它能到、能被到的点，试试 `i → k → j`'),
        'f = [0]': '`f[i]` 表示前 `i` 个字符匹配上的最小成本；`f[0] = 0`',
        'for index in range(n)': lambda S, B, r: ('所有位置都算完了' if B.get('index') == S.get('index') and 'index' in B else f'算 `f[{S.index + 1}]`：`source[:{S.index + 1}]` = `{S.source[:S.index + 1]}` 变成 `{S.target[:S.index + 1]}`'),
        'f.append(f[-1])': '`source[{index}] = target[{index}]`：这位本来就一样，可以不改 → `f[{index + 1}] = f[{index}] = {f[-1]}`',
        'f.append(-1)': '`source[{index}] = {source[index]}` ≠ `target[{index}] = {target[index]}`：先记 `-1`（做不到），再看有没有整段替换能凑出来',
        'if dis[x][y] != -1 and f[index - length + 1]': _upd_cond,
        'f[-1] = f[index': '`f[{index + 1}] = {f[-1]}`',
        'return f[-1]': lambda S, B, r: f'`f[{len(S.source)}] = {S.f[-1]}`：整个 `source` 转成 `target` 的最小成本 =={r}==',
    },
    cards=dict(
        one_liner='子串是图的点，Floyd 算变换成本，再枚举最后一段做前缀 DP',
        complexity='时间约 `O(tot³ + n·|长度集合|)`，空间 `O(tot²+n)`',
        problem=['`original[i] → changed[i]` 花 `cost[i]`，可对 `source` 的子串做替换，把 `source` 变成 `target`',
                 '两次替换的区间要么完全不相交，要么完全相同；做不到返回 `-1`',
                 '本视频：`source="abcc"`、`target="bcdc"`，可改 `a→b`、`b→c`、`ab→bc`、`c→e`、`e→d` → `4`'],
        quote='如果将本题中的子串视为图中的节点，依然可以使用floyd算法计算将一个子串变换成另一个子串的最小代价。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个出现过的字符串编号当作点，`dis[x][y]` 初始是直接操作的成本，Floyd 补全多步变换',
              '同一段子串被变换后只能当整体：令 `f[i]` = 前 `i` 个字符匹配上的最小代价，枚举==最后一段==的长度',
              '原文用哈希表查子串，偷懒的是只枚举「可变换串的长度」（≤100 种），不枚举所有起点'],
        summary=['`f[i] = min(f[i], f[i-length] + dis[x][y])`；`-1` 代表做不到，更新时必须先判 `-1`',
                 '原文用 `-1` 表示不可达，Floyd 里要同时判 `dis[i][k]` 和 `dis[k][j]` 不是 `-1`',
                 '哈希表算子串哈希要 `O(长度)`，最坏 `O(n³)`；用字典树或滚动哈希可做到 `O(n²)`',
                 '原文就是 Python 3 可运行的写法，没有改动',
                 '对比灵神：灵神按长度分组跑 Floyd，用 `inf` 表示不可达'],
    ),
)
