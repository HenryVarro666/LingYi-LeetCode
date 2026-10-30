def _bits(S):
    n = S.get('n')
    return bin(n)[2:][::-1] if isinstance(n, int) else ''


CONFIG = dict(
    num=868, title='二进制间距', difficulty='Easy', category='位运算',
    author='yiduobo', technique='pow2 逐位扫描',
    tags=['灵神题单', '位运算', '难度分 1307'],
    code='''
class Solution(object):
    def binaryGap(self, n):

        now = 1
        pos = 0
        while n & now == 0:
            pos += 1
            now <<= 1
        
        last = pos
        pos += 1
        now <<= 1
        res = 0
        while now <= n:
            while now <= n and n & now == 0:
                pos += 1
                now <<= 1
            res = max(res, pos - last)
            last = pos
            pos += 1
            now <<= 1
        
        return res
''',
    call='Solution().binaryGap(22)',
    expect=2,
    views=[
        dict(type='string', var=_bits, label='n = 22 的二进制（第 0 位在左，低位 → 高位）', h=330,
             pointers={'pos': 'blue', 'last': 'pink'},
             color=lambda S, i, v: 'green' if v == '1' else None,
             dim=lambda S, i, v: v == '0'),
        dict(type='text', fn=lambda S: (f"`now = {S['now']}`（第 {S['now'].bit_length() - 1} 位），`n & now = {S['n'] & S['now']}`" if 'now' in S else ''), h=70),
    ],
    watch=[('pos', 'pos', 'blue'), ('last', 'last', 'pink'), ('now', 'now', 'cyan'), ('res', 'res', 'green')],
    captions={
        'while n & now == 0': lambda S, B, r: (f'`n & now = {S.n & S.now}`，这一位是 0 → 继续往高位找' if S.n & S.now == 0
                                               else f'`n & now = {S.n & S.now} ≠ 0`：第 {S.pos} 位是 ==1== → 找到最低位的 1'),
        'pos += 1': '`pos` 前进到第 {pos} 位',
        'now <<= 1': '`now` 左移一位，检测下一位：`now = {now}`',
        'last = pos': '记录这个 1 的位置：`last = {last}`（用来和下一个 1 算距离）',
        'while now <= n:': lambda S, B, r: (f'`now = {S.now} <= n = {S.n}`：还有更高位 → 继续' if S.now <= S.n
                                            else f'`now = {S.now} > n = {S.n}`：已超过最高位 → 结束'),
        'while now <= n and': lambda S, B, r: (f'`n & now = {S.n & S.now}`，这一位是 0 → 跳过' if S.now <= S.n and S.n & S.now == 0
                                               else '这一位是 1（或已越过最高位）→ 退出内层循环'),
        'res = max': '当前 1 在 `pos = {pos}`，上一个 1 在 `last = {last}`：距离 `{pos - last}`，`res = max({B.res}, {pos - last}) = {res}`',
        'return res': '最大间距 `{res}`',
    },
    cards=dict(
        one_liner='先找到所有 1 的位置，相邻位置相减取最大',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['求 `n` 的二进制里，==相邻两个 1 之间的最大距离==，没有相邻的 1 就返回 0',
                 '例：`22 = 10110` → `2`；`8 = 1000` → `0`',
                 '本视频：`n = 22`'],
        quote='可以使用n与2的幂次进行与运算来确定当前位置上是否为1。于是现在可以维护一个变量pow2，不断将其左移同时判断当前位上是否为1，并根据这些位置来更新答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`now` 从 1 开始不断左移，`n & now` 不为 0 就说明这一位是 1',
              '`pos` 是当前位下标，`last` 是上一个 1 的下标',
              '先跳过低位的 0 找到第一个 1，再每遇到一个 1 就用 `pos - last` 更新答案'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '先单独找第一个 1，之后才开始算距离',
                 '内层循环要写 `now <= n`，避免越过最高位后死循环',
                 '对比灵神：灵神用 lowbit 一次跳过一段 0，只循环 1 的个数次'],
    ),
)
