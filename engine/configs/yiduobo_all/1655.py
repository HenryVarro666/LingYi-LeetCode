def _bits(x, m):
    return format(x, f'0{m}b')


def _info(S):
    if 'state' not in S or 'm' not in S:
        return ''
    m = S['m']
    st = S['state']
    if 'sub_state' in S and S['_line'] in range(0, 99) and S.get('sub_set') is not None and S.get('_inner', {}).get('sub_state') is not None:
        ss = S['sub_state']
        return (f"state=`{_bits(st, m)}` = 子集 `{_bits(ss, m)}` 用前面的数 + 余下 `{_bits(st ^ ss, m)}` 给当前这种数"
                f"（需要 `{S['s'][st] - S['s'][ss]}` 个，有 `{S.get('cnt', '?')}` 个）")
    return f"state=`{_bits(st, m)}`：想满足这些顾客，所需总数 `{S['s'][st]}`"


CONFIG = dict(
    num=1655, title='分配重复整数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状压 DP · 枚举子集',
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
    call='Solution().canDistribute([1,2,2,3,3,3], [3,2])',
    expect=True,
    views=[
        dict(type='array', var='cnt_list', label='cnt_list（每种数字的个数）', h=150, cell=64),
        dict(type='array', var='quantity', label='quantity（顾客订单，第 0、1 位顾客）', h=150, cell=64),
        dict(type='array', var='s', label='s[state]：state 里所有顾客需要的总数（下标 = state）', h=150, cell=64,
             color=lambda S, i, v: 'yellow' if i == S.get('state') else ('cyan' if i == S.get('sub_state') else None)),
        dict(type='array', var='f', label='f[state]：已处理的数字能否满足 state 表示的顾客', h=150, cell=64,
             color=lambda S, i, v: ('yellow' if i == S.get('state') else 'cyan' if i == S.get('sub_state') else 'green' if v is True else None)
             if 'state' in S else ('green' if v is True else None)),
        dict(type='text', size=28, fn=_info),
    ],
    watch=[('cnt', 'cnt', 'orange'), ('state', 'state', 'yellow'), ('sub_state', 'sub_state', 'cyan'),
           ('sub_set', 'sorted(sub_set)', 'purple')],
    captions={
        'cnt_dict[num] =': '数字 `{num}` 的个数记为 `{cnt_dict[num]}`',
        'cnt_list =': '`cnt_list = {cnt_list}`：只关心每种数字有几个，不关心数值本身',
        'm = len': '`m = {m}` 位顾客，每位顾客对应二进制的一位 → 状态 `0 ~ {(1 << m) - 1}`',
        'max_state = ': '一共 `{max_state}` 个状态（顾客的所有子集）',
        'for state in range(1, max_state)': '预处理 `s[state]`：这个顾客子集一共要多少个数字',
        'if state & (1 << index)': '`state` 的第 `{index}` 位是 {1 if state & (1 << index) else 0}',
        's[state] = s[state ^': '取 `state` 的最低位顾客 `{index}`：`s[{state}] = s[{state ^ (1 << index)}] + {quantity[index]}` = =={s[state]}==',
        'f = [False]': '`f[state]`：用已处理的数字，能否满足 `state` 里的所有顾客；先全设 False',
        'if s[state] <= cnt_list[0]': '只用第一种数字（共 `{cnt_list[0]}` 个）：`s[{state}] = {s[state]}` ≤ `{cnt_list[0]}` → {"可以" if s[state] <= cnt_list[0] else "不行"}',
        'f[state] = True': '`f[{state}]` = True：一种数字就能满足这批顾客',
        'for cnt in cnt_list[1:]': '加入下一种数字，它有 `{cnt}` 个：它要么不用，要么分给 `state` 的某个子集',
        'for state in range(max_state - 1': '==state 从大到小==：这样 `f[sub_state]` 还是上一轮的值，省掉一维',
        'if f[state]': lambda S, B, r: ('`f[{}]` 已经是 True（上一轮就能满足），跳过'.format(S.state) if S.f[S.state] else '`f[{}]` 还不行，试试让当前这种数字分担一部分'.format(S.state)),
        'sub_set = set([0])': '`sub_set` 用来装 `state` 的所有子集，先放入空集 0',
        'for index in range(m)': '枚举 `state` 里每位顾客，逐个扩充子集',
        'sub_set.update': '加入顾客 `{index}`：`sub_set` 里每个子集再多一个带 `{index}` 位的版本 → `{sorted(sub_set)}`',
        'for sub_state in sub_set': '枚举子集 `sub_state = {sub_state}`：它由之前的数字满足，其余由这种数字满足',
        'if f[sub_state] and': lambda S, B, r: (
            f'子集 `{S.sub_state}`：`f[{S.sub_state}]` = {S.f[S.sub_state]}，余下顾客要 `{S.s[S.state]} − {S.s[S.sub_state]} = {S.s[S.state] - S.s[S.sub_state]}` 个'
            + (f' ≤ `{S.cnt}` → ==成立==' if S.f[S.sub_state] and S.s[S.state] - S.s[S.sub_state] <= S.cnt else (
                f' 但 `f[{S.sub_state}]` 是 False → 不行' if not S.f[S.sub_state] else f' > `{S.cnt}` → 不够分，换下一个子集'))),
        'f[state] = True': lambda S, B, r: (f'`f[{S.state}] = True`：前面的数字满足 `{S.sub_state}`，当前数字满足 `{S.state ^ S.sub_state}`' if S.get('sub_state') is not None and S.get('_line') == 36 else f'`f[{S.state}] = True`：只用第一种数字就能满足这批顾客'),
        'break': '已经满足 `state`，不用再试别的子集',
        'return f[-1]': '`f[-1]` 就是全部顾客：答案 =={ret}==',
    },
    skip=[5, 9, 12, 13, 29, 14, 15, 16, 18, 21, 26, 30, 31, 34],
    max_steps=110,
    cards=dict(
        one_liner='用二进制记录「已满足哪些顾客」，一种数字一种数字地加进来',
        complexity='时间 `O(n · 3^m)`，空间 `O(2^m)`',
        problem=['`nums` 至多 50 种数字，`quantity[i]` 是第 `i` 位顾客要的个数',
                 '每位顾客拿到的数字必须==全相同==，问能否满足所有顾客',
                 '本视频：`nums=[1,2,2,3,3,3]`，`quantity=[3,2]` → `True`'],
        quote='到了最后还是只能老老实实用状态压缩动态规划来做。',
        quote_src='—— yiduobo 题解原文',
        idea=['先试贪心：优先用个数少的数字，但==分配规则无法确定==，每种都能找到反例',
              '`m ≤ 10`，用二进制 `state` 表示顾客子集；`s[state]` 预处理所需总数',
              '加入一种数字（有 `cnt` 个）：枚举 `state` 的子集，前面的数字满足 `sub_state`，这种数字满足余下的',
              '`state` 从大到小枚举，就能省掉「第几种数字」这一维'],
        summary=['时间 `O(n · 3^m)`，空间 `O(2^m)`，`n` 是不同数字的种类数',
                 '易错：同一个顾客的订单==只能用同一种数字==，所以按「数字」做阶段，按「顾客子集」做状态',
                 '原文为 Python 2 写法，`cnt_dict.values()` 要切片，已改为 `list(cnt_dict.values())`',
                 '本例：订单 3 给数字 3，订单 2 给数字 2，数字 1 用不上'],
    ),
)
