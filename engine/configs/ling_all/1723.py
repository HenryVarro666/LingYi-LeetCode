JOBS = [5, 3, 4]


def _vals(S, x):
    c = S['jobs']
    return '{' + ','.join(str(c[i]) for i in range(len(c)) if x >> i & 1) + '}'


def _col(S, i, v):
    j, s = S.get('j'), S.get('s')
    if j is None or s is None or S.get('_line', 0) < 12 or not (0 < j < (1 << len(S['jobs']))):
        return None
    if s >> i & 1:
        return 'pink'
    if j >> i & 1:
        return 'blue'
    return None


def _txt(S):
    j, s = S.get('j'), S.get('s')
    if j is None or s is None or S.get('_line', 0) < 14 or 'f' not in S:
        return '`f[j]`：把集合 j 的工作分给已有工人时，耗时最长的工人的最小耗时；`SUM[s]`：集合 s 的总耗时'
    w = len(S['jobs'])
    return (f'集合 `j={j:0{w}b}` = =={_vals(S, j)}==，新工人做 `s={s:0{w}b}` = =={_vals(S, s)}==，'
            f'其余 `j^s={j ^ s:0{w}b}` = =={_vals(S, j ^ s)}== 给前面的工人')


def _c_v(S, B, ret):
    return f'新工人做 {_vals(S, S.s)}（耗时 `{S.SUM[S.s]}`），前面的工人做剩下的 {_vals(S, S.j ^ S.s)}：`v = f[{S.j ^ S.s}]` = =={S.v}=='


def _c_cmp(S, B, ret):
    if S.SUM[S.s] > B.v:
        return f'`SUM[s] = {S.SUM[S.s]} > v = {B.v}`：新工人更忙 → 最长耗时变成他的 `{S.v}`'
    return f'`SUM[s] = {S.SUM[S.s]} <= v = {B.v}`：新工人没有更忙 → 最长耗时不变，仍是 `{S.v}`'


def _c_upd(S, B, ret):
    if S.v < B.f[S.j]:
        return f'`v = {S.v} < f[{S.j}] = {B.f[S.j]}`：这种分法更均衡 → ==更新== `f[{S.j}] = {S.v}`'
    return f'`v = {S.v} >= f[{S.j}] = {B.f[S.j]}`：不比已有方案好，不更新'


CONFIG = dict(
    num=1723, title='完成所有工作的最短时间', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='子集状压 DP · 预处理子集',
    tags=['灵神题单·动态规划', '灵神题单·数学算法'],
    setup='''
subsets = [[] for _ in range(1 << 3)]
for i in range(1 << 3):
    s = i
    while s:
        subsets[i].append(s)
        s = (s - 1) & i
''',
    code='''
class Solution:
    def minimumTimeRequired(self, jobs: List[int], k: int) -> int:
        m = 1 << len(jobs)
        SUM = [0] * m
        for i, v in enumerate(jobs):
            bit = 1 << i
            for j in range(bit):
                SUM[bit | j] = SUM[j] + v

        f = SUM.copy()
        for _ in range(1, k):
            for j in range(m - 1, 0, -1):
                for s in subsets[j]:
                    v = f[j ^ s]
                    if SUM[s] > v: v = SUM[s]  # 不要用 max 和 min，那样会有额外的函数调用开销
                    if v < f[j]: f[j] = v
        return f[-1]
''',
    call=f'Solution().minimumTimeRequired({JOBS}, 2)',
    expect=7,
    skip=['for j in range(bit)', 'for i, v in enumerate', 'bit = 1 << i'],
    max_steps=47,
    views=[
        dict(type='array', var='jobs', label='jobs（粉 = 新工人做的 s，蓝 = 前面工人做的 j^s）', h=170, cell=90, color=_col),
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='array', var='SUM', label='SUM[s]：下标 s 是工作集合的二进制编码', h=200, cell=70, pointers={'s': 'pink'}),
        dict(type='array', var='f', label='f[j]：集合 j 分给已有工人时的最小「最长耗时」', h=220, cell=70, pointers={'j': 'blue'}),
    ],
    watch=[('j', 'j', 'blue'), ('s', 's', 'pink'), 'v', ('f[j]', 'f[j]', 'green')],
    captions={
        'm = 1 << len': '`n = {len(jobs)}` 个工作 → `{m}` 个子集；下标第 `i` 位为 1 表示包含第 `i` 个工作',
        'SUM[bit | j] = SUM[j] + v': '集合 `{bit | j}` = 集合 `{j}` 加上工作 `{i}`（{v}）→ `SUM[{bit | j}] = {SUM[bit | j]}`',
        'f = SUM.copy()': '只有 1 个工人时，所有工作都归他：`f[j] = SUM[j]`',
        'for _ in range': lambda S, B, r: ('工人都加完了（共 `k` 个），结束' if '_' in B else
                                           f'加入第 `{S.get("_") + 1}` 个工人；倒序枚举 `j`，`f[j ^ s]` 还是前 `{S.get("_")}` 个工人的旧值'),
        'for j in range(m - 1': '枚举要分配的工作集合 `j = {j}` = {_vals(S, j)}',
        'for s in subsets[j]': lambda S, B, r: (f'枚举 j 的非空子集 `s = {S.s}` = {_vals(S, S.s)}（直接取预处理好的 `subsets[j]`）'
                                                if S.get('s') is not None and S.get('s') != B.get('s') or B.get('j') != S.get('j')
                                                else '`subsets[j]` 里的子集枚举完了'),
        'v = f[j ^ s]': _c_v,
        'if SUM[s] > v': _c_cmp,
        'if v < f[j]': _c_upd,
        'return f[-1]': '全部工作都分出去：`f[-1] = f[{m - 1}]` = =={ret}==',
    },
    cards=dict(
        one_liner='最后一个工人做子集 s：f[j] = min(max(f[j\\s], sum[s]))',
        complexity='时间 `O(k·3^n)`，空间 `O(2^n)`',
        problem=['`jobs[i]` 是第 `i` 个工作的耗时，分给 `k` 个工人，一个工作只能给一个人',
                 '工人的工作时间 = 分到的工作耗时之和，求「最长工作时间」的最小值',
                 '示例：`[3,2,3], k=3` → `3`；本视频：`[5,3,4], k=2` → `7`'],
        quote='优化 1：把 min 和 max 拆开，改为手写，避免额外的函数调用开销。优化 2：预处理每个二进制数的子集。',
        quote_src='—— 灵茶山艾府题解',
        idea=['算法同 2305：`f[j]` 取「新工人做 s，前面做 j\\s」的 `max(f[j\\s], sum[s])`，再对 s 取 `min`',
              'Python 直接搬会超时：手写 `max/min`，并把每个 j 的子集提前存进 `subsets[j]`',
              '演示里 `subsets` 在 setup 中预处理（原文为 `1 << 12`，这里缩小为 `1 << 3`）'],
        summary=['时间 `O(k·3^n)`，空间 `O(2^n)`；`subsets` 预处理是 `O(3^n)` 的额外空间',
                 '==倒序枚举 j==：保证 `f[j ^ s]` 是上一轮的值',
                 '`subsets[j]` 不含空集 0，与 `while s:` 的写法等价',
                 '原文预处理 `1 << 12` 覆盖 n ≤ 12，演示缩小到 `1 << 3`；与 2305 是同一道题的 Python 优化版'],
    ),
)
