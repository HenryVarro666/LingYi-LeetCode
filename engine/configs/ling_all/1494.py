def _b(x, n=4):
    return format(x, f'0{n}b')


def _set(x, n=4):
    s = [str(j + 1) for j in range(n) if x >> j & 1]
    return '{' + ','.join(s) + '}' if s else '{}'


def _fmt(S):
    if 'i' not in S or 'u' not in S:
        return '`f[i]` = 学完集合 `i` 里的课，最少要几个学期（二进制从低位起：第 1 位是课程 1）'
    i = S['i']
    if 'i1' in S and S['_line'] >= 15:
        return f'`i = {_b(i)}` 待学 {_set(i)}，现在能学 `i1 = {_b(S["i1"])}` {_set(S["i1"])}'
    return f'`i = {_b(i)}`：还剩 {_set(i)} 没学，补集 {_set(S["u"] ^ i)} 已经学完'


def _color(S, k, v):
    if 'i' not in S or 'u' not in S:
        return None
    if k == S['i']:
        return 'yellow'
    if S['_line'] >= 21 and 'i1' in S and 'j' in S and k == S['i'] ^ S['j']:
        return 'blue'
    if S['_line'] in (17,) and 'i1' in S and k == S['i'] ^ S['i1']:
        return 'blue'
    if v != float('inf') and k < S['i']:
        return 'green'
    return None


def _if1(S, B, ret):
    c = S.i1.bit_count()
    if c <= S.k:
        return f'`i = {_b(S.i)}`，能学 `i1` = {_set(S.i1)}，{c} 门 ≤ {S.k} → ==全学掉=='
    return f'`i = {_b(S.i)}`，能学 `i1` = {_set(S.i1)}，{c} 门 > {S.k} → ==要挑 k 门，枚举子集=='


CONFIG = dict(
    num=1494, title='并行课程 II', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='子集状压 DP · 枚举 i1 的子集',
    tags=['灵神题单'],
    code='''
class Solution:
    def minNumberOfSemesters(self, n: int, relations: List[List[int]], k: int) -> int:
        pre1 = [0] * n
        for x, y in relations:
            pre1[y - 1] |= 1 << (x - 1)  # y 的先修课程集合，下标改从 0 开始

        u = (1 << n) - 1
        f = [inf] * (1 << n)
        f[0] = 0
        for i in range(1, 1 << n):
            ci = u ^ i  # i 的补集
            i1 = 0
            for j, p in enumerate(pre1):
                if i >> j & 1 and p | ci == ci:  # p 在 i 的补集中，可以学（否则这学期一定不能学）
                    i1 |= 1 << j
            if i1.bit_count() <= k:  # 如果个数小于 k，则可以全部学习，不再枚举子集
                f[i] = f[i ^ i1] + 1
                continue
            j = i1
            while j:  # 枚举 i1 的子集 j
                if j.bit_count() == k:
                    f[i] = min(f[i], f[i ^ j] + 1)
                j = (j - 1) & i1
        return f[u]
''',
    call='Solution().minNumberOfSemesters(4, [[1,4],[2,4]], 2)',
    expect=2,
    skip=['for j, p in enumerate', 'i1 = 0', 'ci = u ^ i', 'j = (j - 1)', 'for x, y in', 'while j:', 'for i in range', 'if i >> j & 1', 'i1 |= 1 << j', 'continue'],
    max_steps=120,
    views=[
        dict(type='text', fn=_fmt, size=24, h=70),
        dict(type='array', var='f', label='f[i]（下标 = 剩余课程集合 i；黄 = 当前，蓝 = 依赖，绿 = 已算）', h=200, cell=70,
             pointers={'i': 'blue'}, color=_color),
        dict(type='array', var='pre1', label='pre1[y]：课程 y+1 的先修课集合（位掩码）', h=220, cell=90),
    ],
    watch=[('i', 'i', 'blue'), ('i1', 'i1', 'green'), ('j', 'j', 'pink'), ('k', 'k', 'yellow')],
    captions={
        'pre1[y - 1] |=': '课程 `{y}` 的先修课加入 `{x}`：`pre1[{y-1}] = {pre1[y-1]}`（位掩码）',
        'u = (1 << n) - 1': '全集 `u = {u}`：{n} 门课都在里面',
        'f = [inf]': '`f[i]` 初始为无穷：状态 `i` 还不知道要几个学期',
        'f[0] = 0': '边界：没有课要学，需要 0 个学期',
        'if i1.bit_count()': _if1,
        'f[i] = f[i ^ i1] + 1': '一学期学完：`f[{i}] = f[{i ^ i1}] + 1` = =={f[i]}==',
        'if j.bit_count() == k': lambda S, B, r: (f'子集 `j = {_b(S.j)}` {_set(S.j)}：恰好 {S.k} 门 → ==试=='
                                                  if S.j.bit_count() == S.k else f'子集 `j = {_b(S.j)}` {_set(S.j)}：{S.j.bit_count()} 门 → 跳过'),
        'f[i] = min(': '学 `j`：`f[{i ^ j}] + 1`，`f[{i}]` → =={f[i]}==',
        'return f[u]': '全集的答案 `f[{u}]` = =={ret}== 个学期',
    },
    cards=dict(
        one_liner='f[i] = 学完集合 i 的课，最少几个学期；每学期挑 k 门可学的课',
        complexity='时间 `O(3^n)`，空间 `O(2^n)`',
        problem=['`n` 门课，`relations` 给出先修关系，一学期最多上 `k` 门，且先修课必须在之前的学期上完',
                 '求上完所有课最少要几个学期',
                 '示例：`n=4, relations=[[2,1],[3,1],[1,4]], k=2` → `3`',
                 '本视频：`n=4, relations=[[1,4],[2,4]], k=2` → `2`'],
        quote='如果 i 中存在一门课程 x，它的先修课不在 i 的补集中，那么 j 一定不能包含 x。……此外，如果 |i1| > k，可以枚举大小恰好为 k 的子集（多学一点是一点）。',
        quote_src='—— 灵茶山艾府题解（枚举优化）',
        idea=['`dfs(i)`：上完集合 `i` 的课最少几个学期，补集里的课已经学完',
              '只有先修课在补集里的课才能学，这些课组成 `i1`，只枚举 `i1` 的子集',
              '记忆化搜索 1:1 翻译成递推 `f[i]`，初始 `f[0] = 0`，答案 `f[u]`'],
        summary=['时间 `O(3^n)`：每个集合枚举它的子集，二项式定理得 `3^n`',
                 '易错：同一学期不能同时学课程和它的先修课，所以要用补集判断',
                 '`|i1| ≤ k` 时直接全学，不必枚举；否则只枚举恰好 k 门的子集',
                 '本题视频演示递推版；同题解的记忆化搜索写法逻辑相同'],
    ),
)
