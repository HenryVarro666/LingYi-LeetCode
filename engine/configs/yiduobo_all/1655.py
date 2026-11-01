def _txt(S):
    st, sub, cnt = S.get('state'), S.get('sub_state'), S.get('cnt')
    m = len(S['quantity'])
    s = S.get('s')
    if st is None or s is None or sub is None or cnt is None or S.get('_line', 0) < 31:
        return '`f[state]`：用目前处理过的数字，能否满足顾客集合 state；`s[state]` 是需求总数'
    return (f'sub_state = `{sub:0{m}b}` 已被前面的数字满足：`f[sub]` = {f"{S["f"][sub]}"}；'
            f'剩下 state ^ sub 需要 `s[{st}] − s[{sub}]` = {s[st] - s[sub]}，这种数字有 {cnt} 个')


CONFIG = dict(
    num=1655, title='分配重复整数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状压 DP · 滚动一维',
    tags=['灵神题单·动态规划', '难度分 2307'],
    code='''
class Solution(object):
    def canDistribute(self, nums, quantity):
        cnt_dict = {}
        for num in nums:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1

        cnt_list = list(cnt_dict.values())
        n = len(cnt_list)

        m = len(quantity)
        max_state = 1 << m
        s = [0] * max_state
        for state in range(1, max_state):
            for index in range(m):
                if state & (1 << index):
                    s[state] = s[state ^ (1 << index)] + quantity[index]
                    break

        f = [False] * max_state
        for state in range(max_state):
            if s[state] <= cnt_list[0]:
                f[state] = True

        for cnt in cnt_list[1:]:
            for state in range(max_state - 1, 0, -1):
                if f[state]:
                    continue
                sub_set = set([0])
                for index in range(m):
                    if state & (1 << index):
                        sub_set.update(set([x | (1 << index) for x in sub_set]))

                for sub_state in sub_set:
                    if f[sub_state] and s[state] - s[sub_state] <= cnt:
                        f[state] = True
                        break

        return f[-1]
''',
    call='Solution().canDistribute([1, 1, 1, 2, 2, 3], [2, 2])',
    expect=True,
    views=[
        dict(type='array', var='cnt_list', label='cnt_list：每种数字的个数（蓝 = 当前这种）', cell=70, h=120,
             color=lambda S, k, v: 'blue' if S.get('cnt') == v and S.get('_line', 0) >= 26 else None),
        dict(type='array', var='s', label='s[state]：顾客集合 state 需要的总数', cell=70, h=200, pointers={'state': 'blue', 'sub_state': 'pink'}),
        dict(type='array', var='f', label='f[state]：能否满足（绿 = 能；蓝 = state，粉 = sub_state）', cell=70, h=200,
             pointers={'state': 'blue', 'sub_state': 'pink'},
             color=lambda S, k, v: 'green' if v else None),
        dict(type='set', var='sub_set', label='sub_set：state 的所有子集', h=100, fmt=lambda x: format(x, 'b')),
        dict(type='text', fn=_txt, size=24, h=90),
    ],
    watch=[('cnt', 'cnt', 'orange'), ('state', 'state', 'blue'), ('sub_state', 'sub_state', 'pink'),
           ('max_state', 'max_state', 'cyan')],
    skip=['cnt_dict[num]', 'for num in nums', 'n = len(cnt_list)', 'm = len(quantity)', 'cnt_dict = {}', 27],
    max_steps=80,
    captions={
        'cnt_list = list': '`cnt_dict` 统计出每种数字的个数：`cnt_list` = {cnt_list}',
        'max_state = 1 << m': '`m = {len(quantity)}` 位顾客，状态共 `2^m = {max_state}` 种',
        's = [0] * max_state': '`s[state]`：state 里的顾客一共要多少个数',
        13: lambda S, B, r: (f'`state = {S.state:0{S.m}b}`，算它的需求总数 `s[state]`' if S.get('state') != B.get('state') else '`s` 算完了'),
        14: lambda S, B, r: (f'看第 `{S.index}` 位顾客' if not (S.index == B.get('index') == S.m - 1) else '没有更多位了'),
        15: lambda S, B, r: (f'第 `{S.index}` 位在 state 里 → 找到了最低位' if S.state & (1 << S.index) else f'第 `{S.index}` 位不在 state 里，看下一位'),
        16: '`s[{state}] = s[去掉第 {index} 位] + quantity[{index}]` = =={s[state]}==',
        17: '最低位处理完就 break，其余部分已经算过了',
        'f = [False] * max_state': '`f[state]`：用前面处理过的数字能否满足 state',
        20: lambda S, B, r: (f'先只用第一种数字（{S.cnt_list[0]} 个）初始化：`state = {S.state:0{S.m}b}`' if S.get('state') != B.get('state') else '初始化完成'),
        21: '`s[{state}]` = {s[state]} {"≤" if s[state] <= cnt_list[0] else ">"} {cnt_list[0]}：{"第一种数字就能满足" if s[state] <= cnt_list[0] else "不够"}',
        22: '`f[{state}]` = ==True==',
        24: lambda S, B, r: (f'处理下一种数字：`cnt = {S.cnt}` 个' if S.get('cnt') != B.get('cnt') else '所有数字都处理完'),
        25: lambda S, B, r: ((f'`state = {S.state:0{S.m}b}`：==从大到小==枚举，这样 `f[sub]` 还是上一轮的结果')
                             if not (S.state == B.get('state') == 1) else '这一种数字的所有 state 都更新完'),
        26: lambda S, B, r: ('`f[state]` 已经是 True，不用再算' if S.f[S.state] else '`f[state]` 还是 False，枚举它的子集试试'),
        28: '`sub_set` 从空集开始，逐位加入 state 里的顾客',
        29: lambda S, B, r: (f'看第 `{S.index}` 位顾客' if not (S.index == B.get('index') == S.m - 1) else '位都看完了'),
        30: lambda S, B, r: (f'第 `{S.index}` 位在 state 里：所有已有子集都可以带上它' if S.state & (1 << S.index) else f'第 `{S.index}` 位不在 state 里，跳过'),
        31: '`sub_set` = =={sorted(sub_set)}==（目前得到的子集）',
        33: lambda S, B, r: (f'试 `sub_state = {S.sub_state:0{S.m}b}`：前面的数字满足它，其余给这种数字'
                             if not (S.get('sub_state') == B.get('sub_state') and S.sub_state == list(S.sub_set)[-1]) else '所有子集都试完了'),
        34: lambda S, B, r: (f'`f[{S.sub_state}]` = {S.f[S.sub_state]}，`s[{S.state}] − s[{S.sub_state}]` = {S.s[S.state] - S.s[S.sub_state]} '
                             f'{"≤" if S.s[S.state] - S.s[S.sub_state] <= S.cnt else ">"} cnt = {S.cnt} → '
                             + ('==成立==' if S.f[S.sub_state] and S.s[S.state] - S.s[S.sub_state] <= S.cnt else '不成立')),
        35: '`f[{state}]` = ==True==：前面能满足 sub_state，剩下的由这种数字提供',
        36: '找到一种方案，不用再试了',
        'return f[-1]': '`f[-1]`：所有顾客的集合能否被满足 → =={ret}==',
    },
    cards=dict(
        one_liner='先试贪心无解，只好状压 DP：逐种数字，枚举它负责的顾客子集',
        complexity='时间 `O(n · 3^m)`，空间 `O(2^m)`',
        problem=['`nums` 至多 50 种不同的值，`quantity[i]` 是第 i 位顾客要的个数',
                 '每位顾客拿到的数必须==全相同且恰好 quantity[i] 个==',
                 '本视频：`nums=[1,1,1,2,2,3]`，`quantity=[2,2]` → `true`'],
        quote='到了最后还是只能老老实实用状态压缩动态规划来做。',
        quote_src='—— yiduobo 题解原文',
        idea=['贪心「先用个数少的数字」分配时无法确定该给谁，找得到反例',
              '`f[i][state]`：前 i 种数字能否满足 state 表示的顾客；用 `s[state]` 预存需求总和',
              '枚举 state 的子集 `sub`：前面满足 sub，其余 `s[state] − s[sub] ≤ cnt` 给第 i 种数字',
              'state 从大到小枚举，可以省掉 i 这一维'],
        summary=['时间 `O(n · 3^m)`，空间 `O(2^m)`（滚动掉 i 一维）',
                 '原文为 Python 2 写法，`dict.values()` 要下标/切片，已改为 `list(cnt_dict.values())`，删去了类型说明文档字符串',
                 '易错点：state 必须==从大到小==更新；子集枚举用 `sub_set` 逐位生成',
                 '对比灵神：灵神用二维 `dp[i][j]` 加位运算枚举子集，yiduobo 滚动成一维'],
    ),
)
