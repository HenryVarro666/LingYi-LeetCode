CK = [8, 15, 10]
INF = 8 * 100000


def _vals(S, x):
    c = S['cookies']
    return '{' + ','.join(str(c[i]) for i in range(len(c)) if x >> i & 1) + '}'


def _show(a):
    return lambda S: [('∞' if v >= INF else v) for v in S[a]] if a in S else None


def _col(S, i, v):
    st, ls = S.get('state'), S.get('last_state')
    if st is None or ls is None or 'g' not in S:
        return None
    if (st ^ ls) >> i & 1 and ls & st == ls:
        return 'pink'
    if ls >> i & 1 and ls & st == ls:
        return 'blue'
    return None


def _txt(S):
    st, ls = S.get('state'), S.get('last_state')
    if st is None or ls is None or 'g' not in S:
        return '`f[state]`：分走饼干集合 state 时的最小不公平程度；`base[state]`：state 的饼干总和'
    if ls & st != ls:
        return f'`state={st:03b}` 与 `last_state={ls:03b}`：last 不是 state 的子集，跳过'
    return (f'`state={st:03b}` = =={_vals(S, st)}==：前面的孩子拿 `{ls:03b}` = =={_vals(S, ls)}==，'
            f'新孩子拿 `{st ^ ls:03b}` = =={_vals(S, st ^ ls)}== = {S["base"][st ^ ls]}')


def _c_if(S, B, ret):
    st, ls = S.state, S.last_state
    if st & ls == ls:
        return f'`{st:03b} & {ls:03b} = {ls:03b}`：last_state 是 state 的子集 → 新孩子拿 {_vals(S, st ^ ls)}'
    return f'`{st:03b} & {ls:03b} = {st & ls:03b} ≠ {ls:03b}`：不是子集，跳过'


def _c_upd(S, B, ret):
    st, ls = S.state, S.last_state
    a, b = S.g[ls], S.base[st ^ ls]
    old = B.f[st]
    return (f'`max(g[{ls}], base[{st ^ ls}]) = max({a}, {b}) = {max(a, b)}`，'
            + (f'比 `f[{st}] = {"∞" if old >= INF else old}` 小 → ==更新== 为 `{S.f[st]}`' if S.f[st] != old
               else f'不比 `f[{st}] = {old}` 小 → 不更新'))


CONFIG = dict(
    num=2305, title='公平分发饼干', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='状态压缩 DP · 枚举上一轮状态',
    tags=['灵神题单·动态规划', '难度分 1887'],
    code='''
class Solution(object):
    def distributeCookies(self, cookies, k):

        n = len(cookies)
        value_dict = {}
        for index, c in enumerate(cookies):
            value_dict[1 << index] = c

        max_state = (1 << n)
        base = [0] * max_state
        for state in range(1, max_state):
            tmp = state & -state
            base[state] = base[state ^ tmp] + value_dict[tmp]
        
        f = base[:]
        for i in range(1, k):
            g = f[:]
            f = [8 * 100000] * max_state
            for state in range(1, max_state):
                for last_state in range(state):
                    if state & last_state == last_state:
                        f[state] = min(f[state], max(g[last_state], base[state ^ last_state]))
            
        return f[-1]
''',
    call=f'Solution().distributeCookies({CK}, 2)',
    expect=18,
    skip=['for index, c in', 'for state in range(1, max_state)', 'for last_state', 'tmp = state'],
    max_steps=42,
    views=[
        dict(type='array', var='cookies', label='cookies（粉 = 新孩子拿的，蓝 = 前面孩子拿的）', h=200, cell=90, color=_col),
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='array', var='g', label='g = 上一轮的 f（前 i 个孩子）', h=260, cell=70, pointers={'last_state': 'blue'}),
        dict(type='array', var=_show('f'), label='f[state]：当前轮（∞ = 还没算出）', h=260, cell=70, pointers={'state': 'pink'}),
    ],
    watch=[('state', 'state', 'pink'), ('last_state', 'last_state', 'blue'), ('i', 'i', 'cyan')],
    captions={
        'n = len(cookies)': '`n = {n}` 包饼干，状态 `state` 的第 `p` 位为 1 表示第 `p` 包在集合里',
        'value_dict[1 << index] = c': '`value_dict[{1 << index}] = {c}`：单个 bit 对应的饼干数',
        'max_state = (1 << n)': '一共 `{max_state}` 个状态（0 ~ {max_state - 1}）',
        'base[state] = base': '`base[{state}] = base[{state ^ tmp}] + value_dict[{tmp}]` = =={base[state]}==：去掉最低位 `tmp={tmp}` 再加上它',
        'f = base[:]': '`i = 0`：只有 1 个孩子，集合 state 全归他：`f[state] = base[state]`',
        'for i in range(1, k)': lambda S, B, r: ('孩子都加完了' if 'i' in B else
                                                  f'加入第 `{S.i + 1}` 个孩子；f 只依赖上一轮 → 用 `g` 保存旧的 f'),
        'g = f[:]': '`g` 备份上一轮：前 `{i}` 个孩子的结果',
        'f = [8 * 100000]': '`f` 重置为很大的数（题目上限 `8×10^5`），等着取 min',
        'if state & last_state': _c_if,
        'f[state] = min': _c_upd,
        'return f[-1]': '`f[-1]` 就是 `f[{max_state - 1}]`：所有饼干都分完的最小不公平程度 = =={ret}==',
    },
    cards=dict(
        one_liner='f[i][state]：枚举上一轮的子状态，新孩子拿剩下的',
        complexity='时间 `O(k·4^n)`（朴素枚举），空间 `O(2^n)`',
        problem=['`cookies[i]` 是第 `i` 包饼干数，分给 `k` 个孩子，一包不能拆开',
                 '不公平程度 = 单个孩子拿到的最大总数，求最小值',
                 '本视频：`[8,15,10], k=2` → `18`（`[15]` 和 `[8,10]`）'],
        quote='每个小朋友分到的饼干数目不确定，不再适合网络流和匹配相关的算法，只能老老实实用状态压缩动态规划。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][state]`：第 0 到第 i 个孩子分走了集合 `state` 的最小不公平程度',
              '`i=0`：全给一个孩子，`f = base[state]`',
              '`i>0`：枚举上一轮 `last_state`，要求 `state & last_state == last_state`',
              '新孩子拿 `state ^ last_state`：`min(f, max(g[last], base[新孩子拿的]))`'],
        summary=['朴素写法枚举所有 `last_state < state` 再判断子集，`O(k·4^n)`；n ≤ 8 够用',
                 'yiduobo 提到：可以用 `sub = (sub-1) & state` 枚举子集，降到 `O(k·3^n)`',
                 '滚动数组：每轮用 `g` 保存上一轮，`f` 重置为大数',
                 '`f[-1]` 就是全集 `(1<<n)-1` 的答案'],
    ),
)
