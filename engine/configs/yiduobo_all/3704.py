def _digits(S):
    return S.get('digits', [])


def _txt(S):
    if 'state' not in S:
        return '从低位往高位填 `a`，再推出 `b` 的这一位；状态 = 3 位二进制 `(b前导0, a前导0, 借位)`'
    st = S['state']
    br, az, bz = st & 1, (st >> 1) & 1, (st >> 2) & 1
    return f"处理第 {S['index']} 位（从低到高）：`state = {st}` → 借位 {br}，a 前导零 {az}，b 前导零 {bz}"


def _fcol(S, i, v):
    if 'state' in S and i == S['state'] and S.get('_line') not in (None,):
        return 'blue'
    return 'green' if v else None


CONFIG = dict(
    num=3704, title='统计和为 N 的无零数对', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='数位 DP · 3 位状态 + 滚动数组',
    tags=['灵神题单', '难度分 2419'],
    code='''
class Solution(object):
    def countNoZeroPairs(self, n):
        
        digits = []
        tmp = n
        while tmp:
            digits.append(tmp % 10)
            tmp //= 10

        length = len(digits)
        f = [0] * 8
        f[0] = 1

        for index in range(length):
            g = f[:]
            f = [0] * 8
            for state in range(8):
                if state & 1:
                    borrow = True
                else:
                    borrow = False

                if state & 2:
                    a_zero = True
                else:
                    a_zero = False
                
                if state & 4:
                    b_zero = True
                else:
                    b_zero = False

                r = digits[index]
                if borrow:
                    r -= 1

                if index > 0:
                    nxt_state = 2
                    
                    if not b_zero or r == 0:
                        if r < 0:
                            nxt_state |= 1
                        elif r == 0:
                            nxt_state |= 4
                    
                        f[nxt_state] += g[state]

                if not a_zero:
                    nxt_state = 0
                    if r <= 0:
                        nxt_state |= 1
                        if b_zero:
                            if r == -1:
                                f[nxt_state | 4] += g[state]
                        else:
                            f[nxt_state] += g[state] * 8
                            if r == 0:
                                f[nxt_state] += g[state]
                            else:
                                f[nxt_state | 4] += g[state]
                
                    else:
                        if b_zero:
                            f[nxt_state | 4] += g[state]
                        else:
                            f[nxt_state] += g[state] * (r - 1)
                            if index > 0:
                                f[nxt_state | 4] += g[state]
                            f[nxt_state | 1] += g[state] * (9 - r)
        
        return f[0] + f[2] + f[4] + f[6]
''',
    call='Solution().countNoZeroPairs(11)',
    expect=8,
    views=[
        dict(type='text', h=90, size=26, fn=_txt),
        dict(type='array', var='digits', label='digits（n 的各位，下标 0 是最低位）', cell=100, h=190,
             color=lambda S, i, v: 'blue' if i == S.get('index') else None),
        dict(type='array', var='g', label='g：处理前的方案数（下标 = state）', cell=84, h=190,
             color=lambda S, i, v: 'yellow' if i == S.get('state') else ('green' if v else None)),
        dict(type='array', var='f', label='f：处理后的方案数（下标 = nxt_state）', cell=84, h=190,
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=[('index', 'index', 'blue'), ('state', 'state', 'yellow'), ('r', 'r', 'orange'),
           ('nxt_state', 'nxt_state', 'pink')],
    max_steps=58, max_events=40000,
    skip=['borrow = True', 'borrow = False', 'a_zero = True', 'a_zero = False', 'b_zero = True', 'b_zero = False',
          'tmp = n', 'digits = []', 'tmp //= 10', 'while tmp', 'length = len', 'if state & 1', 'if state & 2', 'if state & 4', 'else:', 15, 40, 51, 68, 33, 34, 37, 38, 48, 49, 41, 43, 52, 53, 57, 63, 67, 'f = [0] * 8'],
    captions={
        7: '拆出 `n` 的各位，从最低位开始存入 `digits`：现在是 `{digits}`',
        12: '初始：没借位、没前导零的状态 `f[0] = 1`，其余为 0',
        58: '`r == 0`：`a` 填 1~9，`b = 10 − a` 也是 1~9，都非零 → 再加一种，共 9 种',
        60: '`r == -1`：`a` 填 9 时 `b` 这位刚好是 0 → 进入 b 前导零，加到 `f[{nxt_state | 4}]`',
        14: '填第 `{index}` 位（从最低位往高位）',
        15: '`g` 存上一轮的 `f`，这一轮从 `g` 转移到新的 `f`',
        16: '新的 `f` 清零（滚动数组，只依赖上一位）',
        17: lambda S, B, r: f"状态 `{S.state}` = 借位 {S.state & 1}、a前导零 {(S.state >> 1) & 1}、b前导零 {(S.state >> 2) & 1}；上一轮方案数 `g[{S.state}] = {S.g[S.state]}`",
        33: '`r = digits[{index}] = {r}`：这一位的数字',
        35: '低位借走了 1 → `r` 减 1 变成 `{r}`',
        37: lambda S, B, r: ('不是最低位 → `a` 这一位可以填 0（进入前导零）' if S.index > 0 else '最低位：`a` 不能填 0（否则 a 的个位就是 0 了）'),
        38: '`a` 填 0：新状态带上「a 前导零」位，`b` 这一位 = `r`',
        40: '`b` 的这一位就是 `r`：`b` 已前导零时只能 `r == 0`，否则 `b` 会出现非零后的空洞',
        42: '`r < 0` → `b` 的位要借位：`nxt_state |= 1`',
        44: '`r == 0` → `b` 这位是 0，接下去 b 进入前导零：`nxt_state |= 4`',
        46: '把 `g[{state}]` 累加到 `f[{nxt_state}]`',
        48: lambda S, B, r: ('`a` 没进入前导零 → 这一位可以填 1~9' if not S.a_zero else '`a` 已经是前导零 → 不能再填非零'),
        49: '`a` 填 1~9：先不带前导零，再看是否要借位',
        50: lambda S, B, r: (f'`r = {S.r} ≤ 0`：`a` 填 1~9 一定比 `r` 大 → ==必借位==' if S.r <= 0 else f'`r = {S.r} > 0`：`a` 有三段取值：小于 r、等于 r、大于 r'),
        64: '`b` 的这位变成 0 → b 进入前导零：加到 `f[{nxt_state | 4}]`',
        56: '`a` 填 1~8 时 `b` 这位非零（共 8 种）→ `f[{nxt_state}] += g[{state}] × 8`',
        66: '`a` 填 1 到 r-1（共 `{r - 1}` 种），`b` 这位为正且不借位 → 乘 `{r - 1}`',
        69: '`a` 填 r+1 到 9（共 `{9 - r}` 种）→ 会借位，`b` 为正 → 加到 `f[{nxt_state | 1}]`',
        71: '最后不能再欠借位：只加借位位为 0 的 4 个状态 `f[0]+f[2]+f[4]+f[6]` = ==`{ret}`==',
    },
    cards=dict(
        one_liner='低位到高位逐位填 a，b 由 n 反推；状态记借位和前导零',
        complexity='时间 `O(8·log n)`，空间 `O(8)`（滚动数组）',
        problem=['无零整数：十进制里没有数字 `0` 的正整数',
                 '给定 `n`，数有多少种拆成两个无零整数 `a + b = n` 的方式',
                 '示例：`n = 11` → ==8==（本视频就用它）'],
        quote='因为有进位的存在，因此本题应该从低位开始向高位进行填充，那么大致的过程就是从低到高填充a的数位，然后通过已经填充的数位，计算b对应的数位，同时检测其中是否存在0。',
        quote_src='—— yiduobo 题解原文',
        idea=['`state` 是 3 位二进制：借位、a 前导零、b 前导零',
              '填 `a` 的这一位，`b` 的这一位 = `r`（`n` 的位减去借位）再推出',
              '`a` 或 `b` 一旦进入前导零，之后只能一直填 0',
              '用 `f[index]` 推 `f[index+1]`，滚动数组只留两层'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '末尾只统计借位位为 0 的四个状态：`f[0]+f[2]+f[4]+f[6]`',
                 '最低位 `index == 0` 时 `a` 不能填 0，所以 `if index > 0`',
                 '原文已是 Python 3 可运行写法（整除用 `//`），代码未改',
                 '对比灵神：灵神从低位递归记忆化，yiduobo 用 8 种状态逐位递推'],
    ),
)
