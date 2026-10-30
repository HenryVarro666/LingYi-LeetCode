NUMS = [4, 4, 2]


def _txt(S):
    ln = S.get('_line', 0)
    if 'res' in S and 'rev_state' in S:
        st, rv = S['state'], S['rev_state']
        k = S['one'][st]
        return (f'`state = {st:02b}`（{k} 个 1，{"奇数 → +" if k % 2 else "偶数 → −"}），`rev_state = {rv:02b}`：'
                f'被它包含的数有 `{S["f"][rv]}` 个，`2^{S["f"][rv]}` = {S["p2"][S["f"][rv]]}')
    if 'one' in S:
        return '`one[state]`：state 里 1 的个数（奇偶决定容斥的符号）'
    if 'index' in S and 'max_state' in S and ln >= 33:
        return f'SOS：外层枚举位 `{S["index"]}`，`f[state] += f[state ^ (1<<{S["index"]})]`，f[s] = 被 s 包含的数的个数'
    if 'zero' in S and 'max_state' not in S:
        return f'`o = {S["o"]:b}`：为 0 的位是 `{S["zero"]}`，所有数这些位上都是 0，可以删掉'
    return '先把 or 里为 0 的位删掉；再对「被谁包含」做 SOS，用容斥数方案'


CONFIG = dict(
    num=3757, title='有效子序列的数量', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='删无用位 + 容斥 + 子集和',
    tags=['数学算法', '难度分 2519'],
    code='''
class Solution(object):
    def countEffective(self, nums):
        
        o = 0
        for v in nums:
            o |= v
        
        m = len(bin(o)[2:])
        zero = []
        for d in range(m - 1, -1, -1):
            if o & (1 << d) == 0:
                zero.append(d)

        for d in zero:
            for index, v in enumerate(nums):
                nums[index] = (v >> (1 + d) << d) | (v & ((1 << d) - 1))

        m = len(bin(max(nums))[2:])
        max_state = (1 << m) - 1
        f = [0] * (max_state + 1)
        p2 = [1]
        mod = 10 ** 9 + 7
        for v in nums:
            f[v] += 1
            p2.append(p2[-1] + p2[-1])
            if p2[-1] >= mod:
                p2[-1] -= mod
        
        mod = 10 ** 9 + 7
        for index in range(m):
            for state in range(1, max_state + 1):
                if state & (1 << index) == (1 << index):
                    f[state] += f[state ^ (1 << index)]
                    if f[state] >= mod:
                        f[state] -= mod
        
        one = [None] * (max_state + 1)
        one[0] = 0
        for state in range(1, max_state + 1):
            lowbit = state & -state
            one[state] = one[state ^ lowbit] + 1

        res = 0
        n = len(nums)
        for state in range(1, max_state + 1):
            rev_state = max_state - state
            if one[state] % 2 == 1:
                delta = 1
            else:
                delta = -1

            res = res + p2[f[rev_state]] * delta
            if res < 0:
                res += mod
            if res >= mod:
                res -= mod
        
        return res
''',
    call=f'Solution().countEffective({NUMS})',
    expect=5,
    skip=['for v in nums:', 'for d in zero', 'for index, v in enumerate', 'for d in range', 'for index in range', 'for state in range',
          'p2.append', 'if p2[-1] >= mod', 'p2[-1] -= mod', 'if f[state] >= mod', 'f[state] -= mod', 'mod = 10', 'if res < 0', 'res += mod',
          'if res >= mod', 'res -= mod', 'if o & (1 << d)', 'zero.append', 'o |= v', 'f = [0]', 'one[0]', 'n = len', 'lowbit ='],
    views=[
        dict(type='array', var='nums', label='nums', h=170, cell=90),
        dict(type='array', var='f', label='f（先是各数出现次数；SOS 后 = 被 state 包含的数的个数）', h=250, cell=100,
             pointers={'state': 'blue', 'rev_state': 'pink'}),
        dict(type='text', fn=_txt, size=28, h=120),
    ],
    watch=[('o', 'o', 'orange'), ('m', 'm'), ('state', 'state', 'blue'), ('rev_state', 'rev_state', 'pink'), ('delta', 'delta'), ('res', 'res', 'green')],
    captions={
        'o = 0': '`o` 记录所有数按位或的结果',
        'm = len(bin(o)[2:])': '`o = {o:b}`，一共 `m = {m}` 位',
        'zero = []': '`zero` 收集 `o` 里==为 0 的位==：所有数这些位上都是 0',
        'nums[index] = ': '删掉第 `{d}` 位：高位右移再左移拼回低位 → `nums[{index}] = {nums[index]}`',
        'm = len(bin(max(nums))': '删完无用位后位数变成 `m = {m}`，对应 `[1, 1, ...]` 这类小问题',
        'max_state = ': '`max_state = {max_state}`：m 位全 1',
        'p2 = [1]': '`p2` 存 2 的幂（取模）',
        'f[v] += 1': '数 `{v}` 出现：`f[{v}] = {f[v]}`',
        'if state & (1 << index)': lambda S, B, r: (f'`state = {S.state}`（{S.state:02b}）含第 {S.index} 位 → 可以转移' if S.state & (1 << S.index) else f'`state = {S.state}`（{S.state:02b}）不含第 {S.index} 位，跳过'),
        'f[state] += f[state ^ (1 << index)]': '`f[{state}] += f[{state ^ (1 << index)}]` → =={f[state]}==：把少一位的子集并进来（==外层必须是位==，才不会重复）',
        'one = [None]': '`one[state]` 记 state 里 1 的个数',
        'one[state] = ': '`one[{state}] = one[{state ^ lowbit}] + 1 = {one[state]}`：去掉最低位的 1 再加一',
        'res = 0': '`res` 累计容斥结果',
        'rev_state = ': '`rev_state = {max_state} − {state} = {rev_state}`：state 的补集，f[补集] = 与 state 的 AND 为 0 的数的个数',
        'if one[state] % 2 == 1': lambda S, B, r: (f'`state` 有 {S.one[S.state]} 个 1（奇数）→ 容斥取 ==+==' if S.one[S.state] % 2
                                                   else f'`state` 有 {S.one[S.state]} 个 1（偶数）→ 容斥取 ==−=='),
        'delta = 1': '`delta = 1`',
        'delta = -1': '`delta = -1`',
        'res = res + p2[f[rev_state]]': '`res += 2^{f[rev_state]} × {delta}` → =={res}==：留下的数只能在补集里，其余数任选',
        'return res': '容斥完成，有效子序列共 `{res}` 个',
    },
    max_steps=80,
    cards=dict(
        one_liner='要让 or 变小，就得有一位从 1 变 0：对这些位做容斥',
        complexity='时间 `O(n + U log U)`，空间 `O(U)`',
        problem=['数组的强度 = 所有元素按位或；移除一个子序列后，剩余数组的强度==严格减少==，就是有效子序列',
                 '求有效子序列的个数，对 `10^9 + 7` 取模',
                 '本视频：`nums = [4,4,2]`（删掉无用位后相当于 `[2,2,1]`）→ `5`'],
        quote='要让强度减少，就必须让最终按位或结果中的至少一位从1变成0。……在这里就需要用到容斥原理了。',
        quote_src='—— yiduobo 题解原文',
        idea=['先删掉 or 里为 0 的位（所有数这些位都是 0）；`[4,4,2]` 删后变 `[2,2,1]`',
              '指定一批「要变 0 的位」state：含这些位的数必须全移走，其余数留不留都行 → `2^(n − f[state])`',
              '重复计数用容斥：state 里有奇数个 1 加，偶数个 1 减；`f` 用子集和（SOS）求'],
        summary=['时间 `O(n + U log U)`，空间 `O(U)`',
                 '删位要从高位到低位，否则低位先删会让高位偏移',
                 'SOS 必须==外层枚举位、内层枚举 state==，否则会重复计算',
                 '原文在 Python 3 下可直接运行，没有改动；原文会就地修改 `nums`',
                 '对比灵神：灵神用「小于 or 的子序列 = 2^n − 恰好等于 or」，只在 or 的子集上容斥；yiduobo 对「变 0 的位集合」容斥'],
    ),
)
