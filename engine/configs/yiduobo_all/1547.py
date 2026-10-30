def _live(S):
    return S.get('_line') in (17, 18, 20) and 'cut_pos' in S or S.get('_line') in (14, 20) and 'j' in S


def _color(S, r, c, v):
    ln = S.get('_line')
    if 'j' not in S or 'i' not in S or S['j'] >= len(S['cuts']) or ln not in (14, 16, 17, 18, 20):
        return None
    i, j = S['i'], S['j']
    if (r, c) == (i, j):
        return 'yellow'
    if ln in (17, 18) and 'cut_pos' in S and (r, c) in ((i, S['cut_pos']), (S['cut_pos'], j)):
        return 'blue'
    return None


def _formula(S):
    ln = S.get('_line')
    if 'l' not in S or 'cuts' not in S:
        return '`f[i][j]` = 完成 `cuts[i]` 到 `cuts[j]` 这一段切割的最小代价'
    l = S['l']
    if ln in (17, 18) and 'cut_pos' in S:
        i, j, k, f, c = S['i'], S['j'], S['cut_pos'], S['f'], S['cuts']
        return f'分割点 `cuts[{k}]` = {c[k]}：`f[{i}][{k}] + f[{k}][{j}]` = `{f[i][k]} + {f[k][j]}` = =={f[i][k] + f[k][j]}=='
    if ln == 20:
        i, j, c = S['i'], S['j'], S['cuts']
        return f'加上棍长 `cuts[{j}] − cuts[{i}]` = `{c[j]} − {c[i]}` = =={c[j] - c[i]}==，得 `f[{i}][{j}]` = =={S["f"][i][j]}=='
    return f'区间下标跨度 `l` = =={l}==：先算短的，再算长的'


CONFIG = dict(
    num=1547, title='切棍子的最小成本', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='区间 DP（按区间长度递推）',
    tags=['灵神题单', '动态规划', '难度分 2116'],
    code='''
class Solution(object):
    def minCost(self, n, cuts):

        cuts = [0] + sorted(cuts) + [n]
        m = len(cuts)
        f = [[None] * m for _ in range(m)]
        for l in range(1, m + 1):
            for i in range(m):
                j = i + l - 1
                if j >= m:
                    continue
                
                if l <= 2:
                    f[i][j] = 0
                else:
                    for cut_pos in range(i + 1, j):
                        if f[i][j] is None or f[i][j] > f[i][cut_pos] + f[cut_pos][j]:
                            f[i][j] = f[i][cut_pos] + f[cut_pos][j]

                    f[i][j] += cuts[j] - cuts[i]

        return f[0][m - 1]
''',
    call='Solution().minCost(5, [3, 1])',
    expect=8,
    skip=['j = i + l - 1', 'if j >= m', 'continue', 'if l <= 2'],
    max_steps=70,
    views=[
        dict(type='array', var='cuts', label='cuts（含隐藏边界 0 和 n）', h=215, cell=80, pointers={'i': 'blue', 'j': 'pink'},
             window=('i', 'j')),
        dict(type='text', fn=_formula, size=26, h=110),
        dict(type='table', var='f', label='f[i][j]（None 表示还没算；黄 = 正在算，蓝 = 当前比较的两段）', h=340, cell=70,
             rows=lambda S: [str(x) for x in S['cuts']] if len(S['cuts']) == len(S['f']) else None,
             cols=lambda S: [str(x) for x in S['cuts']] if len(S['cuts']) == len(S['f']) else None,
             color=_color),
    ],
    watch=[('l', 'l', 'yellow'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('cut_pos', 'cut_pos', 'cyan')],
    captions={
        'cuts = [0]': '先排序，再把隐藏边界 `0` 和 `n` 加进去：`{cuts}`',
        'm = len': '`m = {m}`',
        'f = [[None]': '`f[i][j]`：完成 `cuts[i]` 到 `cuts[j]` 这一段的最小代价；`None` 表示还没算',
        'for l in range': lambda S, B, r: (f'区间下标跨度 `l = {S.l}`：子段比它短，==必须先算完更短的跨度==' if S.get('l') != B.get('l')
                                           else '所有跨度都算完了'),
        'for i in range(m)': lambda S, B, r: ('这一跨度的所有左端点都试完了' if S.get('i') == B.get('i') and S.get('l') == B.get('l') else (f'`l = {S.l}`，左端 `i = {S.i}` → 右端 `j = i + l − 1 = {S.i + S.l - 1}`' if S.i + S.l - 1 < S.m
                                                else f'`i = {S.i}`：右端 `j = {S.i + S.l - 1}` 超出范围，跳过')),
        'f[i][j] = 0': '`l = {l} ≤ 2`：`cuts[{i}]` 到 `cuts[{j}]` 之间没有分割点 → `f[{i}][{j}] = 0`',
        'for cut_pos in range': '`l = {l} > 2`：区间里有分割点，枚举分割点 `cut_pos`（`{i+1}` ~ `{j-1}`）',
        'if f[i][j] is None or': lambda S, B, r: ('`f[i][j]` 还是 `None`，直接取第一个候选' if S.f[S.i][S.j] is None
                                                  else f'已有 `{S.f[S.i][S.j]}`，新候选 `{S.f[S.i][S.cut_pos]} + {S.f[S.cut_pos][S.j]}` = {S.f[S.i][S.cut_pos] + S.f[S.cut_pos][S.j]}'
                                                       f' → ' + ('更小，替换' if S.f[S.i][S.j] > S.f[S.i][S.cut_pos] + S.f[S.cut_pos][S.j] else '不更小，保留')),
        'f[i][j] = f[i][cut_pos]': '`f[{i}][{j}]` 更新为 =={f[i][j]}==（以 `cuts[{cut_pos}]` 为分割点）',
        'f[i][j] += cuts': '再加上这一刀的代价（棍长）`{cuts[j]} − {cuts[i]}` = {cuts[j]-cuts[i]} → `f[{i}][{j}]` = =={f[i][j]}==',
        'return f[0][m - 1]': '整根棍子 `f[0][{m-1}]` = =={ret}==',
    },
    cards=dict(
        one_liner='f[i][j] 表示切完一段的最小代价，按区间跨度从小到大填表',
        complexity='时间 `O(m^3)`，空间 `O(m^2)`',
        problem=['长度为 `n` 的木棍，要在 `cuts` 指定的位置切开，每次切割代价 = 当前棍子长度',
                 '切割顺序可以任意安排，求最小总代价',
                 '本视频：`n = 5, cuts = [3,1]` → `8`'],
        quote='切割时除了cuts中的位置之外，还存在隐藏边界0和n，方便起见也将这两个数加入到cuts当中。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][j]`：完成 `cuts[i]` 到 `cuts[j]` 这段切割的最小代价',
              '`i < j−1` 时枚举分割点：`f[i][j] = min(f[i][cut_pos] + f[cut_pos][j]) + cuts[j] − cuts[i]`',
              '子段必须先算：先枚举下标跨度 `l`，再枚举左端 `i`，由 `j = i + l − 1` 得右端'],
        summary=['时间 `O(m^3)`，空间 `O(m^2)`，`m` 是加了 0 和 n 后的长度',
                 '`f` 初值用 `None`，用来判断是不是第一个候选；`l ≤ 2` 时直接为 0',
                 '易错：先排序再加边界；最后别忘了加上整根棍长 `cuts[j] − cuts[i]`',
                 '对比灵神：灵神 `i` 倒序、`j` 正序填表，这里是按区间长度由短到长填表'],
    ),
)
