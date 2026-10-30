REQ = ["java", "nodejs", "reactjs"]
PEOPLE = [["java"], ["nodejs"], ["nodejs", "reactjs"], ["java", "reactjs"]]


def _row(name):
    def g(S):
        v = S.get(name)
        if v is None:
            return [[]]
        return [['-' if x is None else x for x in v]]
    return g


def _color(S, r, c, v):
    st, ns = S.get('state'), S.get('new_state')
    if st is None or ns is None or S.get('_line', 0) < 20:
        return None
    if c == st:
        return 'yellow'
    if c == ns:
        return 'green'
    return None


def _info(S):
    p = S.get('p')
    if not p:
        return '技能 `java=0, nodejs=1, reactjs=2`，每个人压成二进制数'
    ms = '  '.join(f'人{k}==`{m:03b}`==' for k, m in enumerate(p))
    st, ns, i = S.get('state'), S.get('new_state'), S.get('i')
    if st is not None and ns is not None and i is not None and S.get('_line', 0) >= 20:
        return f'`{st:03b}` | 人{i}`{p[i]:03b}` = `{ns:03b}`'
    if 'res' in S:
        return f'倒推：`now = {S["now"]:03b}`，结果 `{S["res"]}`'
    return ms


def _cap_cmp(S, B, ret):
    f, st, ns, i = S.f, S.state, S.new_state, S.i
    if f[ns] is None:
        return f'`f[{ns}]` 还没凑出过 → 人{i}加入后第一次凑出，==更新=='
    if f[ns] > f[st] + 1:
        return f'`f[{ns}] = {f[ns]}` > `f[{st}] + 1 = {f[st] + 1}` → 人数更少，==更新=='
    return f'`f[{ns}] = {f[ns]}` ≤ `f[{st}] + 1 = {f[st] + 1}` → 不用更新'


CONFIG = dict(
    num=1125, title='最小的必要团队', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状压 DP + 记录转移来源倒推',
    tags=['灵神题单', '动态规划', '难度分 2251'],
    code='''
class Solution(object):
    def smallestSufficientTeam(self, req_skills, people):

        n = len(req_skills)
        skill_dict = {}
        for index, skill in enumerate(req_skills):
            skill_dict[skill] = index
        
        p = []
        for skill_list in people:
            tmp = 0
            for skill in skill_list:
                tmp |= (1 << skill_dict[skill])
            p.append(tmp)
        
        f = [None] * (1 << n)
        f[0] = 0
        fa = [None] * (1 << n)
        use = [None] * (1 << n)
        for i in range(len(p)):
            for state in range(1 << n):
                if f[state] is not None:
                    new_state = state | p[i]
                    if f[new_state] is None or f[new_state] > f[state] + 1:
                        f[new_state] = f[state] + 1
                        fa[new_state] = state
                        use[new_state] = i
            
        res = []
        now = (1 << n) - 1
        while now != 0:
            res.append(use[now])
            now = fa[now]
        
        return res
''',
    call=f'Solution().smallestSufficientTeam({REQ!r}, {PEOPLE!r})',
    expect=[2, 0],
    skip=['for index, skill in enumerate', 'for skill_list in people', 'for skill in skill_list', 'tmp = 0',
          'p.append', 'for i in range(len(p))', 'for state in range', 'fa = [None]', 'use = [None]', 'skill_dict = {}', 'skill_dict[skill] = index', 'if f[state] is not None',
          'f[new_state] = f[state] + 1', 'fa[new_state] = state'],
    max_steps=60,
    views=[
        dict(type='text', fn=_info, size=24, h=60),
        dict(type='table', var=_row('f'), label='f[state]：凑出 state 最少几个人（黄 = state，绿 = new_state）', h=180, cell=90,
             rows=['f'], cols=[f'{k}' for k in range(8)], color=_color),
        dict(type='table', var=_row('fa'), label='fa[state]：从哪个状态转移来', h=160, cell=90,
             rows=['fa'], cols=[f'{k}' for k in range(8)]),
        dict(type='table', var=_row('use'), label='use[state]：这一步加入了哪个人', h=160, cell=90,
             rows=['use'], cols=[f'{k}' for k in range(8)]),
        dict(type='array', var='p', label='p[i]：第 i 个人的技能位掩码', h=140, cell=80, pointers={'i': 'blue'}),
    ],
    watch=[('i', 'i', 'blue'), ('state', 'state', 'yellow'), ('new_state', 'new_state', 'green'), ('res', 'res', 'cyan')],
    captions={
        'n = len(req_skills)': '技能最多 16 种 → 用 `n = {n}` 位二进制表示「已拥有哪些技能」',
        'skill_dict[skill] = index': '技能名映射成下标',
        'tmp |= ': '把技能 `{skill}` 的第 `{skill_dict[skill]}` 位置 1 → `tmp = {tmp}`',
        'f = [None]': '`f[state]`：拥有 state 中技能最少要几个人；`None` = 凑不出',
        'f[0] = 0': '`f[0] = 0`：什么技能都不要，0 个人',
        'if f[state] is not None': lambda S, B, r: (f'`f[{S.state}] = {S.f[S.state]}`：这个技能集合能凑出，可以再加人{S.i}' if S.f[S.state] is not None
                                                   else f'`f[{S.state}]` 是 None：凑不出，不能转移，跳过'),
        'new_state = state | p[i]': '加入人{i}：`{state} | {p[i]}` = `new_state = {new_state}`（二进制 `{new_state:03b}`）',
        'if f[new_state] is None or': _cap_cmp,
        'use[new_state] = i': '`f[{new_state}] = {f[new_state]}`，记下来源 `fa[{new_state}] = {state}`，加入的人 `use[{new_state}] = {i}`',
        'res = []': '倒推：从全集 `{(1 << n) - 1}` 出发，一路沿 `fa` 回到 0，收集 `use`',
        'now = (1 << n) - 1': '`now = {now}`：全部技能',
        'while now != 0': lambda S, B, r: (f'`now = {S.now}` ≠ 0，继续倒推' if S.now != 0 else '`now = 0`：回到起点，结束'),
        'res.append(use[now])': '`use[{now}] = {use[now]}`：凑出 {now} 时加入了人{use[now]} → `res = {res}`',
        'now = fa[now]': '回到上一个状态：`now = fa[...] = {now}`',
        'return res': '最小团队：==`{ret}`==',
    },
    cards=dict(
        one_liner='技能只有 16 种，二进制表示拥有的技能，记录来源倒推方案',
        complexity='时间 `O(n·2^m)`，空间 `O(2^m)`',
        problem=['需求技能清单 `req_skills`，每个备选人员掌握若干技能',
                 '选出==人数最少==的团队，覆盖所有技能，返回人员编号',
                 '本视频：3 项技能、4 个人'],
        quote='由于这里的skill最多只有16种，因此很容易想到使用状态压缩动态规划来解决问题。令f[i][state]表示前i个员工，拥有state中的技能时最少需要的员工数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['转移：`new_state = state | p[i]`，`f[new_state] = min(…, f[state] + 1)`',
              '转移是按位或，正序枚举 state 不会重复叠加 → 可以去掉 `i` 这一维',
              '要具体名单：每个 `new_state` 额外记 `fa`（从哪来）和 `use`（加了谁）'],
        summary=['时间 `O(n·2^m)`，空间 `O(2^m)`',
                 '`f[state] is None` 表示凑不出，必须跳过',
                 '最后从全集倒推：`use[now]` 收集人员，`now = fa[now]`',
                 '对比灵神：灵神把人员集合也存成位掩码 `ids`，yiduobo 用 `fa`/`use` 链倒推'],
    ),
)
