def _bits(S):
    if 'state' not in S:
        return None
    return [(S['state'] >> i) & 1 for i in range(S['n'])]


def _head(S):
    if 'state' not in S:
        return ''
    st, n = S['state'], S['n']
    return f'枚举 `state = {st}`（二进制 `{format(st, "0%db" % n)}`），当前成本 `cost = {S.get("cost", 0)}`，上限 `k = {S["k"]}`'


def _if(S, B, ret):
    i, st = S.index, S.state
    if (st >> i) & 1:
        return f'`state` 的第 `{i}` 位是 1 → 放 `1`，成本加上下标 `{i}`' + ('（放之前要先查相邻）' if S.s else '')
    return f'`state` 的第 `{i}` 位是 0 → 放 `0`，不花成本，`s` = `{"".join(S.s)}0`'


def _adj(S, B, ret):
    if S.s and S.s[-1] == '1':
        return f'`s` 末尾已经是 `1`，这一位又是 `1` → ==相邻的 11==，非法'
    return '`s` 为空或末尾是 `0` → 不相邻，可以放 `1`'


CONFIG = dict(
    num=3955, title='成本限制的有效二进制字符串', difficulty='Medium', category='链表、二叉树与回溯',
    author='yiduobo', technique='暴力枚举二进制状态',
    tags=['灵神核心路线', '灵神题单·链表树与回溯', '难度分 1429'],
    code='''
class Solution(object):
    def generateValidStrings(self, n, k):

        res = []
        for state in range(1 << n):
            cost = 0
            s = []
            for index in range(n):
                if (state & (1 << index)) == (1 << index):
                    cost += index
                    if s and s[-1] == '1':
                        cost = k + 1
                        break

                    s.append('1')
                else:
                    s.append('0')

            if cost <= k:
                res.append(''.join(s))

        return res
''',
    call='Solution().generateValidStrings(3, 1)',
    expect=['000', '100', '010'],
    views=[
        dict(type='text', h=70, fn=_head, size=26),
        dict(type='array', var=_bits, label='state 的各比特（下标 0 = 最低位，对应字符串第 0 位）', h=170, cell=84,
             pointers={'index': 'pink'}, color=lambda S, i, v: 'green' if v == 1 else None),
        dict(type='array', var=lambda S: S['s'] if 's' in S else None, label='s（正在拼的字符串）', h=170, cell=84),
        dict(type='stack', var=lambda S: S['res'] if 'res' in S else None, label='res', h=110, fmt=lambda v: repr(v)),
    ],
    watch=[('state', 'state', 'blue'), ('index', 'index', 'pink'), ('cost', 'cost', 'yellow'), ('k', 'k', 'green')],
    skip=['res = []', 'cost = 0', 's = []', 'for index in range(n)', 'cost += index', "s.append('1')", "s.append('0')"],
    captions={
        'for state in range(1 << n)': '`n` 很小（≤ 12）→ 直接暴力：枚举 `0 ~ 2^n - 1` 每个 `state`，一个数就对应一个二进制串',
        'if (state & (1 << index))': _if,
        "if s and s[-1] == '1'": _adj,
        'cost = k + 1': '发现连续 11：把 `cost` 设成 `k + 1 = {cost}`，故意让它超过上限 → 后面会被过滤',
        'break': '这个 `state` 已经非法，不用再看后面的位',
        'if cost <= k': lambda S, B, r: (f'`cost = {S.cost} <= k = {S.k}` → ==有效==，收进答案' if S.cost <= S.k
                                         else f'`cost = {S.cost} > k = {S.k}` → 非法或成本太高，丢弃'),
        'res.append': '`res` 加入 `"{"".join(s)}"`',
        'return res': '8 个 `state` 都枚举完：返回 `{ret}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='n 很小，直接枚举所有二进制串，逐位检查再算成本',
        complexity='时间 `O(n·2^n)`，空间 `O(n)`（不计返回值）',
        problem=['长为 `n` 的二进制串，成本 = 所有 `1` 的下标之和',
                 '有效：==没有连续的 1== 且成本 `≤ k`；返回全部有效串',
                 '本视频：`n = 3, k = 1` → `["000","100","010"]`'],
        quote='题目中n的规模较小，在这里可以直接暴力枚举所有长度为n的进制字符串，然后遍历这个字符串，检测是否存在相邻的1，同时计算其成本。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n ≤ 12`，只有 `4096` 个串，不用任何技巧',
              '用整数 `state` 表示串：第 `index` 位是 1 就放 `1`、成本加 `index`',
              '碰到相邻 `11` 就把成本改成 `k+1` 并 `break`，最后统一用 `cost <= k` 过滤'],
        summary=['时间 `O(n·2^n)`，空间 `O(n)`',
                 '`cost = k + 1` 是个小技巧：不用额外的标志变量，非法串直接被 `cost <= k` 挡掉',
                 '字符串第 0 位对应 `state` 最低位，所以 `state = 1` 得到 `"100"`',
                 '对比灵神：灵神先预处理 `cost[x]` 再 `x & (x>>1)` 判相邻，这里是逐位检查']
    ),
)
