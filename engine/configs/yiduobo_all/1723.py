JOBS = [5, 3, 4]


def _vals(S, x):
    c = S['jobs']
    return '{' + ','.join(str(c[i]) for i in range(len(c)) if x >> i & 1) + '}'


def _col(S, i, v):
    st, sub = S.get('state'), S.get('sub_state')
    if st is None or S.get('_line', 0) < 22 or 'index' not in S:
        return None
    if sub and (sub >> i & 1):
        return 'pink'
    if st >> i & 1:
        return 'blue'
    return None


def _txt(S):
    st = S.get('state')
    if st is None or S.get('_line', 0) < 22 or 'index' not in S:
        return '`f[state]`：把 state 里的工作分给前几个工人，工作时间最长的工人的最小耗时；`cnt`：工作个数；`max_job`：最长的单个工作'
    sub = S.get('sub_state')
    n = len(S['jobs'])
    if sub:
        return (f'`state={st:0{n}b}` = =={_vals(S, st)}==，最后一个工人做 `sub_state={sub:0{n}b}` = =={_vals(S, sub)}==（耗时 {S["cost"][sub]}），'
                f'其余 `{st ^ sub:0{n}b}` 给前面的工人')
    return f'`state={st:0{n}b}` = =={_vals(S, st)}==，共 `{S["cnt"][st]}` 个工作，已有 `{S["index"] + 1}` 个工人'


def _c_cnt(S, B, ret):
    st, ix = S.state, S.index
    if S.cnt[st] <= ix + 1:
        return f'`cnt[{st}] = {S.cnt[st]} <= {ix + 1}` 个工人：每人最多一个工作 → 剪枝，直接 `f = max_job = {S.max_job[st]}`'
    return f'`cnt[{st}] = {S.cnt[st]} > {ix + 1}` 个工人：工作比工人多，必须枚举子集'


def _c_upd(S, B, ret):
    st, sub = S.state, S.sub_state
    a, b = S.f[st ^ sub], S.cost[sub]
    new = S.f[st]
    old = B.f[st]
    return (f'最后一个工人做 `{sub}`：`max(f[{st ^ sub}], cost[{sub}]) = max({a}, {b}) = {max(a, b)}`；'
            + (f'比 `f[{st}] = {old}` 小 → ==更新== 为 `{new}`' if new != old else f'不比 `f[{st}] = {old}` 小 → 不更新'))


CONFIG = dict(
    num=1723, title='完成所有工作的最短时间', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状压 DP · 工作少于工人时剪枝',
    tags=['灵神题单·动态规划', '灵神题单·数学算法'],
    code='''
class Solution(object):
    def minimumTimeRequired(self, jobs, k):

        n = len(jobs)
        max_state = 1 << n
        cost = [0] * max_state
        cnt = [0] * max_state
        max_job = [0] * max_state
        for state in range(1, max_state):
            for job in range(n):
                if state & (1 << job):
                    cost[state] = cost[state ^ (1 << job)] + jobs[job]
                    cnt[state] = cnt[state ^ (1 << job)] + 1
                    max_job[state] = max(max_job[state ^ (1 << job)], jobs[job])
                    break

        f = cost[:]
        for index in range(1, k):
            for state in range(max_state - 1, 0, -1):
                if cnt[state] <= index + 1:
                    f[state] = max_job[state]
                else:
                    sub_state = state
                    while sub_state:
                        f[state] = min(f[state], max(f[state ^ sub_state], cost[sub_state]))
                        sub_state = (sub_state - 1) & state
        
        return f[-1]
''',
    call=f'Solution().minimumTimeRequired({JOBS}, 2)',
    expect=7,
    skip=['n = len(jobs)', 'max_state = 1 << n', 'cost = [0]', 'cnt = [0]', 'max_job = [0]', 'for state in range(1, max_state)',
          'for job in range(n)', 'while sub_state', 'cnt[state] = cnt', 'max_job[state] = max(', 'break', 'if state & (1 << job)'],
    max_steps=40,
    views=[
        dict(type='array', var='jobs', label='jobs（粉 = 最后一个工人做的 sub_state，蓝 = 其余）', h=170, cell=90, color=_col),
        dict(type='text', fn=_txt, size=22, h=90),
        dict(type='array', var='cost', label='cost[state]：state 里工作的总耗时', h=200, cell=70, pointers={'state': 'blue', 'sub_state': 'pink'}),
        dict(type='array', var='f', label='f[state]：目前最小的最长工作时间', h=220, cell=70, pointers={'state': 'blue'}),
    ],
    watch=[('index', 'index', 'cyan'), ('state', 'state', 'blue'), ('sub_state', 'sub_state', 'pink')],
    captions={
        'cost[state] = cost': '`cost[{state}] = cost[{state ^ (1 << job)}] + jobs[{job}]` = =={cost[state]}==：去掉最低位工作 {job}，再加上它（同时在算工作个数 `cnt` 和最长单个工作 `max_job`）',
        'f = cost[:]': '预处理完成：`cost` 总耗时、`cnt` 工作个数、`max_job` 最长单个工作。只有 1 个工人时全归他：`f = cost`',
        'for index in range(1, k)': lambda S, B, r: ('工人都加完了' if 'index' in B and B.get('index') == S.get('index') else
                                                      f'加入第 `{S.index + 1}` 个工人；`f` 只依赖上一轮，所以 state 要==从大到小==算'),
        'for state in range(max_state - 1': lambda S, B, r: ('这一轮所有 state 都算完了' if S.state == 1 and B.get('state') == 1 else
                                                            f'枚举工作集合 `state = {S.state}`（二进制 `{S.state:03b}`）'),
        'if cnt[state] <= index + 1': _c_cnt,
        'f[state] = max_job[state]': '工人够多：每人一个工作，最长的就是 `max_job[{state}]` = =={f[state]}==',
        'sub_state = state': '`sub_state = state`：从「全给最后一个工人」开始枚举子状态',
        'f[state] = min': _c_upd,
        'sub_state = (sub_state - 1) & state': '`sub_state = (sub_state - 1) & state` → `{sub_state}`：下一个子状态（0 表示枚举完）',
        'return f[-1]': '`f[-1] = f[{max_state - 1}]`：全部工作分完的最小最长耗时 = =={ret}==',
    },
    cards=dict(
        one_liner='f[i][state] 枚举最后一个工人的子状态；工作少于工人时直接剪枝',
        complexity='时间 `O(k·3^n)`，空间 `O(2^n)`',
        problem=['`jobs[i]` 是第 `i` 个工作的耗时，分给 `k` 个工人，一个工作只能给一个人',
                 '工人的工作时间 = 分到的耗时之和，求最长工作时间的最小值',
                 '本视频：`[5,3,4], k=2` → `7`（`[5]` 和 `[3,4]`）'],
        quote='理论上来说上面的做法时间复杂度应该是O(n * 3^n)，在这里还是比较吃紧的，需要做一些剪枝。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i][state]`：state 里的工作分给前 i 个工人，最长工作时间的最小值',
              '枚举 state 的子状态 `sub_state` 交给最后新来的人：`max(f[state ^ sub], cost[sub])`',
              '剪枝：工作个数 `<=` 工人个数时，每人一个，答案就是最长的单个工作 `max_job`',
              '滚动数组省掉 i 这一维，所以 state 从大到小算'],
        summary=['时间 `O(k·3^n)`，空间 `O(2^n)`；剪枝让很多状态不用枚举子集',
                 '==剪枝条件用 `index + 1`==：此时已有 `index + 1` 个工人',
                 '省掉 i 维后必须 state 从大到小，保证 `f[state ^ sub]` 是上一轮的值',
                 '原文已是 Python 3 可运行，没有改动；与灵神做法相比，灵神预处理子集，yiduobo 靠剪枝'],
    ),
)
