CK = [8, 15, 10]


def _vals(S, x):
    c = S['cookies']
    return '{' + ','.join(str(c[i]) for i in range(len(c)) if x >> i & 1) + '}'


def _pj(S):
    return S.get('j') if S.get('_line', 0) >= 12 else None


def _ps(S):
    return S.get('s') if S.get('_line', 0) >= 14 else None


def _col(S, i, v):
    j, s = S.get('j'), S.get('s')
    if j is None or s is None or not (S.get('j', 0) > 0):
        return None
    if s >> i & 1:
        return 'pink'
    if j >> i & 1:
        return 'blue'
    return None


def _txt(S):
    j, s = S.get('j'), S.get('s')
    if j is None or s is None or 'f' not in S or 'SUM' not in S or 'm' not in S or j <= 0 or j >= S['m']:
        return '`f[j]`：已把集合 j 的饼干分给若干孩子时的最小不公平程度；`SUM[s]`：集合 s 的饼干总数'
    return (f'集合 `j={j:b}` = =={_vals(S, j)}==，新孩子拿 `s={s:b}` = =={_vals(S, s)}==，'
            f'其余 `j^s={j ^ s:b}` = =={_vals(S, j ^ s)}== 给前面的孩子')


def _c_v(S, B, ret):
    return (f'新孩子拿 {_vals(S, S.s)}（和 `{S.SUM[S.s]}`），前面的孩子分剩下的 {_vals(S, S.j ^ S.s)}：`v = f[{S.j ^ S.s}]` = =={S.v}==')


def _c_cmp(S, B, ret):
    if S.SUM[S.s] > B.v:
        return f'`SUM[s] = {S.SUM[S.s]} > v = {B.v}`：新孩子拿得更多 → 不公平程度变成他的 `{S.v}`'
    return f'`SUM[s] = {S.SUM[S.s]} <= v = {B.v}`：新孩子没有比前面多 → 不公平程度不变，仍是 `{S.v}`'


def _c_upd(S, B, ret):
    if S.v < B.f[S.j]:
        return f'`v = {S.v} < f[{S.j}] = {B.f[S.j]}`：这种分法更公平 → ==更新== `f[{S.j}] = {S.v}`'
    return f'`v = {S.v} >= f[{S.j}] = {B.f[S.j]}`：不比已有方案好，不更新'


CONFIG = dict(
    num=2305, title='公平分发饼干', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='子集状压 DP · 枚举子集',
    tags=['灵神题单·动态规划', '难度分 1887'],
    code='''
class Solution:
    def distributeCookies(self, cookies: List[int], k: int) -> int:
        m = 1 << len(cookies)
        SUM = [0] * m
        for i, v in enumerate(cookies):
            bit = 1 << i
            for j in range(bit):
                SUM[bit | j] = SUM[j] + v

        f = SUM.copy()
        for _ in range(1, k):
            for j in range(m - 1, 0, -1):
                s = j
                while s:
                    v = f[j ^ s]
                    if SUM[s] > v: v = SUM[s]  # 不要用 max 和 min，那样会有额外的函数调用开销
                    if v < f[j]: f[j] = v
                    s = (s - 1) & j
        return f[-1]
''',
    call=f'Solution().distributeCookies({CK}, 2)',
    expect=18,
    skip=['for j in range(bit)', 'for i, v in enumerate', 'bit = 1 << i', 'while s:'],
    max_steps=52,
    views=[
        dict(type='array', var='cookies', label='cookies（粉 = 新孩子拿的 s，蓝 = 前面孩子拿的 j^s）', h=170, cell=90, color=_col),
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='array', var='SUM', label='SUM[s]：下标 s 是饼干集合的二进制编码', h=200, cell=70, pointers={'s': 'pink'}),
        dict(type='array', var='f', label='f[j]：集合 j 分给已有孩子时的最小不公平程度', h=220, cell=70, pointers={'j': 'blue'}),
    ],
    watch=[('j', 'j', 'blue'), ('s', 's', 'pink'), 'v', ('f[j]', 'f[j]', 'green')],
    captions={
        'm = 1 << len': '`n = {len(cookies)}` 块饼干 → `{m}` 个子集；下标的第 `i` 位为 1 表示选了第 `i` 块',
        'SUM[bit | j] = SUM[j] + v': '集合 `{bit | j}` = 集合 `{j}` 再加第 `{i}` 块（{v}）→ `SUM[{bit | j}] = {SUM[bit | j]}`',
        'f = SUM.copy()': '只有 1 个孩子时，所有饼干都归他：`f[j] = SUM[j]`',
        'for _ in range': lambda S, B, r: ('孩子都加完了（共 `k` 个），结束' if '_' in B else
                                           f'加入第 `{S.get("_") + 1}` 个孩子；倒序枚举 `j`，这样 `f[j ^ s]` 还是前 `{S.get("_")}` 个孩子的旧值'),
        'for j in range(m - 1': '枚举已分配的饼干集合 `j = {j}` = {_vals(S, j)}',
        's = j': '从 `s = j`（全给新孩子）开始枚举 j 的所有非空子集 s',
        'v = f[j ^ s]': _c_v,
        'if SUM[s] > v': _c_cmp,
        'if v < f[j]': _c_upd,
        's = (s - 1) & j': '`s = (s-1) & j` → `{s}`：枚举下一个子集（0 表示枚举完）',
        'return f[-1]': '全部饼干都分出去：`f[-1] = f[{m - 1}]` = =={ret}==',
    },
    cards=dict(
        one_liner='f[j] = min over 子集 s 的 max(f[j\\s], sum[s])：最后一个孩子拿 s',
        complexity='时间 `O(k·3^n)`，空间 `O(2^n)`',
        problem=['`cookies[i]` 是第 `i` 包饼干数，分给 `k` 个孩子，==一包不能拆开==',
                 '不公平程度 = 单个孩子拿到的最大总数，求其最小值',
                 '示例：`[8,15,10,20,8], k=2` → `31`；本视频用 `[8,15,10], k=2` → `18`'],
        quote='定义 f[i][j] 表示前 i 个孩子分配的饼干集合为 j 时，前 i 个孩子的不公平程度的最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['给第 i 个孩子的集合设为 `s`，他前面的孩子拿的是 `j\\s`',
              '新孩子拿多了，程度变成 `sum[s]`；没拿多，保持 `f[j\\s]` → 取 ==max==',
              '枚举 j 的所有子集 s 取 ==min==；倒序枚举 j，第一维可以省掉'],
        summary=['时间 `O(k·3^n)`：每个集合枚举它的子集，总数 `3^n`；空间 `O(2^n)`',
                 '==倒序枚举 j==：`f[j^s]` 必须是上一轮的值，所以滚动数组要从大到小',
                 '`s = (s-1) & j` 枚举子集；`s = 0` 时停止，不含空集',
                 '灵神注释：手写 max/min 比函数调用快；本题与 1723 相同'],
    ),
)
