# 灵神原文：预处理表长 1 << 12（题目 n ≤ 12）；演示只把表长改成 1 << 3（示例 n = 3），其余逐字照搬。
# 为了让引擎追踪到类外的预处理，call 里用 '<solution>' 文件名重新执行一遍这段代码。
CODE = '''
cost = [0] * (1 << 3)
for x in range(1, len(cost)):
    if x & (x >> 1):  # 有两个连续的 1
        cost[x] = inf  # 不合法
    else:
        # 去掉 x 中的一个比特位（最低位还是最高位都可以），计算 DP
        i = x.bit_length() - 1
        cost[x] = cost[x ^ (1 << i)] + i

class Solution:
    def generateValidStrings(self, n: int, k: int) -> List[str]:
        ans = []
        s = [''] * n
        for x in range(1 << n):
            if cost[x] > k:
                continue
            for j in range(n):  # 注意左边是低位，右边是高位
                s[j] = str(x & 1)
                x >>= 1
            ans.append(''.join(s))
        return ans
'''.strip('\n')

_N, _K = 3, 1
_L = CODE.split('\n')
_LN = lambda sub: next(i + 1 for i, t in enumerate(_L) if sub in t)
L_SHIFT, L_BODY, L_FORJ, L_FORX, L_IF, L_CONT, L_APP = (
    _LN('x >>= 1'), _LN('s[j] = str'), _LN('for j in range(n)'), _LN('for x in range(1 << n)'),
    _LN('if cost[x] > k'), _LN('continue'), _LN('ans.append'))

COST = [0] * 8
for _x in range(1, 8):
    COST[_x] = float('inf') if _x & (_x >> 1) else COST[_x ^ (1 << (_x.bit_length() - 1))] + _x.bit_length() - 1


def _cost(S):
    return S['cost'] if 'cost' in S else COST


def _orig(S):
    """主循环里 x 会被不断右移，这里还原出这一轮枚举的原始 x"""
    if 'n' not in S:
        return None
    ln = S['_line']
    if ln in (L_FORX, L_IF, L_CONT):
        return S['x']
    if ln == L_APP:
        sh = S['n']
    elif ln == L_SHIFT:
        sh = S['j'] + 1
    else:
        sh = S['j']
    return (S['x'] << sh) | sum(int(S['s'][t]) << t for t in range(sh))


def _ptr(S):
    return S['x'] if 'cost' in S and 'n' not in S else _orig(S)


def _ccolor(S, i, v):
    p = _ptr(S)
    if p == i:
        return 'green' if v != float('inf') else 'red'
    if 'cost' in S and 'i' in S and 'n' not in S and i == (S['x'] ^ (1 << S['i'])):
        return 'blue'
    return None


def _fm(v):
    return '∞' if v == float('inf') else str(v)


def _bin(x, w=3):
    return format(x, '0%db' % w)


def _line(S):
    if 'n' not in S:
        if 'x' not in S:
            return '`cost[x]`：二进制数 x 的成本 = 值为 1 的比特位的位置之和'
        x = S['x']
        if x & (x >> 1):
            return f'`x = {_bin(x)}`，`x & (x>>1) = {_bin(x & (x >> 1))}` 不为 0 → 有相邻 `11`，==不合法=='
        return f'`x = {_bin(x)}`：去掉最高位 `{S.get("i", x.bit_length() - 1)}`，成本 = `cost[{x ^ (1 << (x.bit_length() - 1))}]` + `{x.bit_length() - 1}`'
    o = _orig(S)
    if o is None:
        return ''
    c = COST[o]
    return f'枚举 `x = {_bin(o)}`（`cost[x] = {_fm(c)}`，`k = {S["k"]}`）'


def _cap_if(S, B, ret):
    x, k = S.x, S.k
    return (f'`cost[{x}] = {_fm(COST[x])}` > `k = {k}` → ==成本太高/不合法==，跳过' if COST[x] > k
            else f'`cost[{x}] = {_fm(COST[x])}` ≤ `k = {k}` → 有效，开始把 x 还原成字符串')


def _cap_prune(S, B, ret):
    return '`x & (x >> 1)` ' + ('非 0：相邻两位都是 1 → `cost[x] = inf`' if S.x & (S.x >> 1) else '为 0：没有连续的 1，计算成本')


def _cap_body(S, B, ret):
    return f'取出 x 的最低位 `{S.s[S.j]}` 放到 `s[{S.j}]`（==左边是低位==，从低到高逐位还原）'


CONFIG = dict(
    num=3955, title='成本限制的有效二进制字符串', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='预处理成本 + 二进制枚举',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1429'],
    code=CODE,
    setup=f'CODE = {CODE!r}',
    call=f"exec(compile(CODE, '<solution>', 'exec'), globals())\nSolution().generateValidStrings({_N}, {_K})",
    expect=['000', '100', '010'],
    views=[
        dict(type='text', h=70, fn=_line, size=26),
        dict(type='array', var=_cost, label='cost[x]（x 的二进制：低位在右；红 = 含 11 不合法）', h=200, cell=84,
             color=_ccolor, pointers={_ptr: 'blue'}, pointer_labels={_ptr: 'x'}),
        dict(type='array', var=lambda S: S['s'] if 's' in S else None, label='s（下标 0 是 x 的最低位）', h=170, cell=84,
             pointers={'j': 'pink'}),
        dict(type='stack', var=lambda S: S['ans'] if 'ans' in S else None, label='ans', h=110, fmt=lambda v: repr(v)),
    ],
    watch=[('x', _ptr, 'blue'), ('k', 'k', 'yellow'), ('j', 'j', 'pink')],
    skip=['ans = []', 's = [\'\'] * n', 'continue', 'for j in range(n)', 'i = x.bit_length()'],
    captions={
        'cost = [0]': '`cost[x]` 表示整数 x 的二进制所对应的成本；演示表长取 `1 << 3`（原文 `1 << 12`）',
        'for x in range(1, len(cost))': lambda S, B, r: (f'预处理：从小到大算 `cost[{S.x}]`' if S.x < 8 else ''),
        'if x & (x >> 1)': _cap_prune,
        'cost[x] = inf': '`cost[{x}] = inf`：含相邻的 1，永远不会是有效字符串',
        'cost[x] = cost[x ^': '最高位是 `{i}`：`cost[{x}] = cost[{x ^ (1 << i)}] + {i}` = =={cost[x]}==（去掉最高位，是规模更小的子问题）',
        'for x in range(1 << n)': '枚举所有长度为 `n` 的二进制数 `x`（下面再翻译成字符串）',
        'if cost[x] > k': _cap_if,
        's[j] = str': _cap_body,
        'x >>= 1': '`x` 右移一位，下一轮取下一位',
        'ans.append': lambda S, B, r: f'`s` 拼成 `"{"".join(S.s)}"`，加入答案',
        'return ans': '全部枚举完：返回 `{ans}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='先 DP 预处理每个 x 的成本，再枚举 x 还原成字符串',
        complexity='时间 `O(n·2^n)`（不计预处理），空间 `O(n)`',
        problem=['长为 `n` 的二进制串，成本 = 所有 `1` 的下标之和',
                 '有效 = ==没有相邻的 11== 且成本 `≤ k`，返回所有有效串',
                 '示例：`n = 3, k = 1` → `["000","010","100"]`'],
        quote='所有相邻的 11 变成 1，其余变成 0。x 不含 11，等价于 x & (x >> 1) 等于 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x & (x>>1)` 把每对相邻比特做 `&`，非 0 就说明有 `11`',
              '成本：去掉最高位 `i`，剩下的是子问题，`cost[x] = cost[x去掉最高位] + i`',
              '预处理一次，之后枚举 `x`，查表过滤，再逐位还原成字符串'],
        result='找到 3 个有效字符串 ✓',
        summary=['预处理 `O(2^12)`，每次查询 `O(n·2^n)`，空间 `O(n)`（不计返回值）',
                 '易错：字符串==左边是 x 的低位==，所以下标 `j` 从 0 开始取低位',
                 '原文预处理表长是 `1 << 12`，演示缩成 `1 << 3`，其余逐字照搬',
                 '原文还给了库函数写法：`bin(x)[2:].zfill(n)[::-1]`，一行完成还原',
                 '同类题：78. 子集（位运算枚举子集）'],
    ),
)
