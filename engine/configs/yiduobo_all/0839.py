STRS = ["tars", "rats", "star"]
COLS = ['blue', 'pink', 'green', 'purple', 'cyan', 'yellow', 'orange', 'red']


def _root(fa, x):
    while fa[x] != x:
        x = fa[x]
    return x


def _color(S, i, v):
    fa = S.get('fa')
    if fa is None:
        return None
    r = _root(fa, i)
    return COLS[r % len(COLS)] if any(_root(fa, j) == r and j != i for j in range(len(fa))) else None


def _pair(S):
    if 'i' not in S or 'j' not in S:
        return '两两枚举字符串，相似的就合并到同一个集合'
    a, b = STRS[S['i']], STRS[S['j']]
    diff = [k for k in range(len(a)) if a[k] != b[k]]
    sa = ''.join(f'=={c}==' if k in diff else c for k, c in enumerate(a))
    sb = ''.join(f'=={c}==' if k in diff else c for k, c in enumerate(b))
    return f'`strs[{S["i"]}]` = {sa}　`strs[{S["j"]}]` = {sb}　不同位置 {len(diff)} 处'


def _groups(S):
    fa = S.get('fa')
    if fa is None:
        return ''
    roots = sorted({_root(fa, i) for i in range(len(fa))})
    return '当前分组：' + ' '.join('{' + ','.join(STRS[i] for i in range(len(fa)) if _root(fa, i) == r) + '}' for r in roots)


CONFIG = dict(
    num=839, title='相似字符串组', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='两两枚举 + 并查集',
    tags=[],
    code='''
class Solution(object):
    def numSimilarGroups(self, strs):

        n = len(strs)
        m = len(strs[0])
        fa = [x for x in range(n)]
        for i in range(n - 1):
            for j in range(i + 1, n):
                cnt = 0
                for index in range(m):
                    if strs[i][index] != strs[j][index]:
                        cnt += 1
                        if cnt > 2:
                            break
                if cnt <= 2:
                    fa_i = self.find(i, fa)
                    fa_j = self.find(j, fa)
                    if fa_i < fa_j:
                        fa[fa_j] = fa_i
                    else:
                        fa[fa_i] = fa_j
        
        res = 0
        for index in range(n):
            if self.find(index, fa) == index:
                res += 1
        
        return res

    def find(self, now, fa):
        if fa[now] != now:
            tmp = self.find(fa[now], fa)
            fa[now] = tmp
        return fa[now]
''',
    call=f'Solution().numSimilarGroups({STRS})',
    expect=2,
    views=[
        dict(type='text', fn=_pair, size=24, h=70),
        dict(type='array', var='fa', label='fa（同色 = 同一组；下标 = 字符串编号）', color=_color, h=190,
             pointers={'i': 'blue', 'j': 'pink'}),
        dict(type='text', fn=_groups, size=24, h=60),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('cnt', 'cnt', 'orange'), ('res', 'res', 'green')],
    skip=['n = len', 'm = len', 'fa = [x for', 'cnt = 0', 'res = 0'],
    max_steps=90,
    captions={
        'if strs[i][index] != strs[j][index]': lambda S, B, r: (
            f'第 {S.index} 位：`{S.strs[S.i][S.index]}` vs `{S.strs[S.j][S.index]}` → ' + ('==不同==' if S.strs[S.i][S.index] != S.strs[S.j][S.index] else '相同')),
        'cnt += 1': '又发现一处不同：`cnt` = =={cnt}==',
        'if cnt > 2': lambda S, B, r: (f'`cnt = {S.cnt} > 2`：不同位置太多，肯定不相似，==提前 break==' if S.cnt > 2 else f'`cnt = {S.cnt} ≤ 2`：还有可能相似，继续比'),
        'if cnt <= 2': lambda S, B, r: (f'`cnt = {S.cnt} ≤ 2`：都是异位词，最多两处不同 → ==相似==，合并' if S.cnt <= 2
                                          else f'`cnt = {S.cnt} > 2`：不相似，跳过'),
        'fa_i = self.find': '找 `{i}` 所在集合的祖先',
        'fa_j = self.find': '找 `{j}` 所在集合的祖先',
        'if fa_i < fa_j': lambda S, B, r: f'祖先 `{S.fa_i}` 与 `{S.fa_j}`：' + ('相同则无变化，较小者作新祖先' if S.fa_i == S.fa_j else '不同，较小的做新祖先'),
        'fa[fa_j] = fa_i': '`fa[{fa_j}] = {fa_i}`：把大祖先挂到小祖先下',
        'fa[fa_i] = fa_j': '`fa[{fa_i}] = {fa_j}`：把大祖先挂到小祖先下（相等时不变）',
        'if self.find(index, fa) == index': lambda S, B, r: f'`{S.index}` 的祖先是自己吗？' + ('是 → 它是一组的代表' if S.fa[S.index] == S.index else '不是 → 已被并入别的组'),
        'res += 1': '数到一个代表：`res` = =={res}==',
        'return res': '代表元个数就是组数 → =={res}==',
        'tmp = self.find': '递归找祖先',
        'fa[now] = tmp': '路径压缩：`fa[{now}] = {tmp}`',
    },
    cards=dict(
        one_liner='都是异位词，不同位置 ≤ 2 就相似：两两比，并查集合并',
        complexity='时间 `O(n² m)`，空间 `O(n)`',
        problem=['若交换字符串 `X` 的两个字母能得到 `Y`（或 `X == Y`），二者相似',
                 '相似关系可传递，连起来的一堆算一组，问共有几组',
                 '本视频：`["tars","rats","star"]` → `2`'],
        quote='所有字符串都是字母异位词。这意味着若两个字符串中有不超过两个位置上的字符不同，那么这两个字符串就是相似的。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据范围小：直接两两枚举，数不同位置 `cnt`',
              '`cnt <= 2` 就把两者所在集合合并，`cnt > 2` 立刻 `break`',
              '最后数有多少字符串的祖先是自己，就是组数'],
        summary=['时间 `O(n² m)`，空间 `O(n)`',
                 '题目保证是异位词，所以 `cnt` 只会是 0 或 2 或更大，不用再检查能否交换',
                 '合并时要先 `find` 祖先再挂接，不能直接改下标',
                 '原文是 Python 2 风格，在 Python 3 下无需改动'],
    ),
)
