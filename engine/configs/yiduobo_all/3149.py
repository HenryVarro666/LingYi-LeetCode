A0 = [0, 3, 2, 1]
N = len(A0)


def _ft(S):
    f = S.get('f')
    if f is None:
        return [['·'] * N for _ in range(1 << N)]
    return [['·' if v is None else v for v in row] for row in f]


def _nx(S):
    g = S.get('nxt')
    if g is None:
        return [['·'] * N for _ in range(1 << N)]
    return [['·' if v is None else v for v in row] for row in g]


def _col(S, r, c, v):
    I = S['_inner']
    if 'state' not in I:
        return None
    if r == I['state'] and c == I['last']:
        return 'yellow'
    idx = I.get('index')
    if idx is not None and S.get('_line') in (16, 17, 18, 19) and not I['state'] >> idx & 1 and r == (I['state'] | 1 << idx) and c == idx:
        return 'blue'
    return None


def _K(S):
    return S['_inner'].get('index')


def _L(S):
    return S['_inner'].get('last')


def _txt(S):
    I = S['_inner']
    if 'state' not in I:
        return '`f[state][last]`：已填 state、最后一个是 last 时，填完剩余的最小分数；`nxt` 记下最优的下一个'
    st, last = I['state'], I['last']
    t = f'`state = {st:0{N}b}`，`last = {last}`'
    if I.get('index') is not None and 'v' in I:
        t += f'，试填 `index = {I["index"]}`'
    return t


CONFIG = dict(
    num=3149, title='找出分数最低的排列', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状压 DP · 记忆化搜索 + nxt 记录方案',
    tags=['状压 DP', '输出具体方案', '难度分 2642'],
    code='''
class Solution(object):
    def findPermutation(self, nums):

        n = len(nums)
        max_state = (1 << n) - 1
        f = [[None] * n for _ in range(max_state + 1)]
        nxt = [[None] * n for _ in range(max_state + 1)]

        def calc(state, last):
            if f[state][last] is None:
                if state == max_state:
                    f[state][last] = abs(last - nums[0])
                else:
                    for index in range(n):
                        if (state & (1 << index)) == 0:
                            v = calc(state | (1 << index), index) + abs(last - nums[index])
                            if f[state][last] is None or v < f[state][last]:
                                f[state][last] = v
                                nxt[state][last] = index
            
            return f[state][last]
        
        calc(1, 0)
        res = [0]
        state = 1
        last = 0
        while nxt[state][last] is not None:
            res.append(nxt[state][last])
            nxt_state = state | (1 << nxt[state][last])
            last = nxt[state][last]
            state = nxt_state
        
        return res
''',
    call=f'Solution().findPermutation({A0})',
    expect=[0, 2, 3, 1],
    skip=['n = len(nums)', 'max_state = (1', 'nxt = [[None]', 'for index in range(n)', 'return f[state][last]'],
    views=[
        dict(type='array', var='nums', label='nums', cell=60, h=130, pointers={_K: 'pink', _L: 'blue'}, pointer_labels={_K: 'index', _L: 'last'}),
        dict(type='text', fn=_txt, size=22, h=64),
        dict(type='table', var=_ft, label='f[state][last]：行 = state（二进制，最低位是数字 0），列 = last；· 还没算', h=450, cell=60,
             rows=lambda S: [format(x, f'0{N}b') for x in range(1 << N)], cols=lambda S: [str(x) for x in range(N)], color=_col),
        dict(type='array', var='res', label='res', cell=56, h=96),
    ],
    watch=[('state', lambda S: format(S['_inner']['state'], f'0{N}b') if 'state' in S['_inner'] else '', 'cyan'),
           ('last', lambda S: S['_inner'].get('last'), 'blue'), ('index', lambda S: S['_inner'].get('index'), 'pink'), ('v', lambda S: S['_inner'].get('v'), 'green')],
    captions={
        'f = [[None]': '`f[state][last]` 初始是 `None`，表示还没算过；`nxt` 之后记录最优的下一个元素',
        'if state == max_state': lambda S, B, r: ('`state` 已经是全集：只差首尾相接 `abs(last - nums[0])`' if S.state == S.max_state
                                                  else '还有数没填：从 0 到 n-1 枚举下一个填的元素 `index`（从小到大，保证字典序小）'),
        'f[state][last] = abs': lambda S, B, r: f'`f[{S.state:0{N}b}][{S.last}] = |{S.last} − nums[0]| = {S.f[S.state][S.last]}`',
        'if (state & (1 << index)) == 0': lambda S, B, r: (f'`index = {S.index}` 还没用过 → 可以填' if S.state & (1 << S.index) == 0 else f'`index = {S.index}` 已用过 → 跳过'),
        'v = calc': '填 `index = {B.index}`：先递归得到剩余部分的最小分数，再加 `|{B.last} − nums[{B.index}]| = {abs(B.last - nums[B.index])}`',
        'if f[state][last] is None or v': lambda S, B, r: (f'`v = {S.v}`' + ('，`f` 还是空 → 直接采用' if S.f[S.state][S.last] is None
                                                                             else (f' < `f = {S.f[S.state][S.last]}` → 更新' if S.v < S.f[S.state][S.last] else f' 不小于 `f = {S.f[S.state][S.last]}` → 不更新（同分保留更小的 index）'))),
        'if f[state][last] is None': lambda S, B, r: ('这个状态还没算过 → 开始计算' if S.f[S.state][S.last] is None else '已经算过 → 直接返回（记忆化）'),
        'f[state][last] = v': lambda S, B, r: f'`f[{S.state:0{N}b}][{S.last}]` = =={S.v}==',
        'nxt[state][last] = index': lambda S, B, r: f'`nxt[{S.state:0{N}b}][{S.last}] = {S.index}`：记下这个状态最优的下一个元素',
        'calc(1, 0)': '入口：`state = 1`（只填了 0），`last = 0`',
        'res = [0]': '算完了。答案必以 0 开头；顺着 `nxt` 还原',
        'while nxt[state][last]': lambda S, B, r: ('`nxt` 为空：已经填完 → 结束' if S.nxt[S.state][S.last] is None else f'`nxt[{S.state:0{N}b}][{S.last}] = {S.nxt[S.state][S.last]}` → 继续'),
        'res.append': '加入 `{res[-1]}` → `res = {res}`',
        'nxt_state = state': '新状态 `nxt_state = {nxt_state:0{N}b}`',
        'return res': '分数最低且字典序最小：`{ret}`',
    },
    max_steps=66,
    cards=dict(
        one_liner='先把 0 放到队首，再从后往前推「剩下的最小分数」',
        complexity='时间 `O(n^2 2^n)`，空间 `O(n 2^n)`',
        problem=['`nums` 是 `0..n-1` 的排列，排列 `perm` 的分数是循环相邻的 `|perm[i] - nums[perm[i+1]]|` 之和',
                 '求分数最小的 `perm`，同分取字典序最小',
                 '本视频：`nums = [0,3,2,1]` → `[0,2,3,1]`'],
        quote='对于一个排列perm，其元素循环位移后得到的新排列得分与perm完全相同。……最终答案必然是以0开头的一个排列。',
        quote_src='—— yiduobo 题解原文',
        idea=['分数是个环，循环位移不变 → 通过位移把 0 放到开头，答案一定以 0 开头',
              '`f[state][last]`：已用集合 state、最后是 last，==填完剩下的==最小分数；`nxt` 记下下一个填谁',
              '从 0 到 n-1 枚举 index：先定后面的、再定前面的，像基数排序，字典序自然最小'],
        summary=['时间 `O(n^2 2^n)`，空间 `O(n 2^n)`',
                 '`state == max_state` 时要把首尾相接的最后一项 `abs(last - nums[0])` 加进去',
                 '`v < f[state][last]` 用严格小于，同分时保留 index 更小的方案',
                 '对比灵神：灵神把 s 设成 f[s][j] 从大到小递推；yiduobo 用记忆化 + 同样的 f/nxt 还原方案。原文已是 Python 3 可运行的写法'],
    ),
)
