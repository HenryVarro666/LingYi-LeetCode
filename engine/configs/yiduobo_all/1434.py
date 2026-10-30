HATS = [[3, 4], [4, 5]]


def _tbl(name):
    def g(S):
        v = S.get(name)
        return [list(v)] if v is not None else [[]]
    return g


def _color(S, r, c, v):
    st, p = S.get('state'), S.get('p')
    if st is None or p is None or S.get('_line', 0) < 25:
        return None
    if c == st:
        return 'yellow'
    if c == st ^ (1 << p):
        return 'green'
    return None


def _info(S):
    n = len(S['hats'])
    hat = S.get('hat')
    if hat is None:
        return '`g[state]`：帽子考虑到上一顶时，state 里的人都戴上帽子的方案数'
    st, p = S.get('state'), S.get('p')
    if st is not None and p is not None and S.get('_line', 0) >= 25:
        return f'帽子 ==#{hat}== 给人{p}：`{st:0{n}b}` 去掉第 {p} 位 → `{st ^ (1 << p):0{n}b}`'
    return f'正在考虑帽子 ==#{hat}==，可戴的人 `{S["hat_dict"][hat]}`'


CONFIG = dict(
    num=1434, title='每个人戴不同帽子的方案数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状压 DP（按帽子枚举 · 滚动数组）',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def numberWays(self, hats):

        hat_dict = {}
        for index, hat_list in enumerate(hats):
            for hat in hat_list:
                if hat not in hat_dict:
                    hat_dict[hat] = []
                hat_dict[hat].append(index)
        
        n = len(hats)
        max_state = 1 << n

        l = len(hat_dict)

        g = [0] * max_state
        g[0] = 1

        mod = 10 ** 9 + 7

        for hat in hat_dict.keys():
            f = g[:]
            for state in range(1, max_state):
                for p in hat_dict[hat]:
                    if state & (1 << p):
                        f[state] += g[state ^ (1 << p)]
                        f[state] %= mod
        
            g = f[:]
        
        return f[-1]
''',
    call=f'Solution().numberWays({HATS!r})',
    expect=3,
    skip=['for index, hat_list', 'for hat in hat_list', 'if hat not in hat_dict', 'hat_dict[hat] = []', 'l = len(hat_dict)',
          'max_state = 1 << n', 'mod = 10', 'f[state] %= mod', 'for state in range', 'for p in hat_dict', 'f = g[:]'],
    views=[
        dict(type='text', fn=_info, size=24, h=60),
        dict(type='map', var='hat_dict', label='hat_dict：帽子编号 → 喜欢它的人', h=170,
             fmt=lambda k, v: f'帽子{k}: 人{v}'),
        dict(type='table', var=_tbl('g'), label='g[state]：上一顶帽子之后的方案数（黄 = state，绿 = state 去掉人 p）', h=180, cell=100,
             rows=['g'], cols=lambda S: [f'{k:0{len(S["hats"])}b}' for k in range(1 << len(S['hats']))], color=_color),
        dict(type='table', var=_tbl('f'), label='f[state]：加入当前这顶帽子后的方案数', h=180, cell=100,
             rows=['f'], cols=lambda S: [f'{k:0{len(S["hats"])}b}' for k in range(1 << len(S['hats']))],
             color=lambda S, r, c, v: 'yellow' if S.get('state') == c and S.get('_line', 0) >= 25 else None),
    ],
    watch=[('hat', 'hat', 'purple'), ('state', 'state', 'yellow'), ('p', 'p', 'blue'), ('g[0]', 'g[0]', 'green')],
    captions={
        'hat_dict[hat].append(index)': '帽子 `{hat}` 记下可戴它的人：`hat_dict[{hat}] = {hat_dict[hat]}`',
        'n = len(hats)': '`n = {n}` 个人 → 每个人戴没戴帽子用一位二进制表示，共 `2^n` 个状态',
        'g = [0] * max_state': '`g[state]`：已处理的帽子，分给 state 里的人（每人恰好一顶）的方案数',
        'g[0] = 1': '`g[0] = 1`：没有人要戴帽子，只有「什么都不做」这 1 种方案',
        'for hat in hat_dict.keys()': lambda S, B, r: (f'开始处理帽子 `{S.hat}`，可戴它的人 `{S.hat_dict[S.hat]}`' if S.get('hat') != B.get('hat') else '所有帽子都处理完了'),
        'if state & (1 << p)': lambda S, B, r: (f'`state = {S.state:0{S.n}b}` 的第 {S.p} 位是 1 → 人{S.p}要戴帽子 `{S.hat}`，可以转移' if S.state & (1 << S.p)
                                                 else f'`state = {S.state:0{S.n}b}` 的第 {S.p} 位是 0 → 这个状态里人{S.p}不戴帽子，不能用这顶帽子给他'),
        'f[state] += g[': '人{p}戴帽子 {hat}：其余人要由前面的帽子覆盖 → `f[{state}] += g[{state ^ (1 << p)}]` → =={f[state]}==',
        'g = f[:]': '这顶帽子处理完：`g` 更新成 `{g}`（滚动数组，只保留上一轮）',
        'return f[-1]': '全部人都戴上帽子的方案数 `f[-1]` = =={ret}==',
    },
    cards=dict(
        one_liner='人最多 10 个，位表示谁已戴帽，帽子逐顶去分',
        complexity='时间 `O(帽子数 · 2^n · n)`，空间 `O(2^n)`',
        problem=['`n` 个人，每个人有自己喜欢的帽子列表（帽子编号 1~40）',
                 '每人戴一顶喜欢的帽子，且==任意两人帽子不同==，求方案数（对 `10^9+7` 取模）',
                 '本视频：`hats = [[3,4],[4,5]]` → `3`'],
        quote='注意到这里的人数n最多只有10，那么很自然想到使用二进制编码来进行状态压缩。令f[i][state]表示前i + 1顶帽子，给state表示的人来戴有多少种方案。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举帽子，而不是枚举人：人只有 10 个，帽子有 40 顶但每顶帽子至多给一个人',
              '`state` 里第 `p` 位为 1 且帽子可给 p → `f[state] += g[state ^ (1<<p)]`',
              '只依赖上一顶帽子 → 用 `g` / `f` 两个数组滚动'],
        summary=['时间 `O(40 · 2^n · n)`，空间 `O(2^n)`',
                 '易错：`f = g[:]` 先拷贝，「这顶帽子不分给任何人」的方案要保留',
                 '每顶帽子至多给 1 人 → 同一个 `state` 里一顶帽子只会用一次',
                 '答案 `f[-1]` 是全部人都戴上帽子的状态；每次累加后取模'],
    ),
)
