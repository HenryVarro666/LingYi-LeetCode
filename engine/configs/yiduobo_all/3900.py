def _t(S):
    if 'pre_s' not in S or 'zero' not in S:
        return ''
    return f"前缀和 `pre_s = {S['pre_s']}`：找 `pre_s − 2`（区间和 2，换出一个 1）或 `pre_s + 2`（区间和 −2，换出一个 0）"


CONFIG = dict(
    num=3900, title='一次交换后的最长平衡子串', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和 + first/second 两张哈希表',
    tags=['前缀和与哈希表', '难度分 2135'],
    code='''
class Solution(object):
    def longestBalanced(self, s):
        
        zero, one = 0, 0
        for c in s:
            if c == '0':
                zero += 1
            else:
                one += 1
        
        first = {0: -1}
        second = {}
        pre_s = 0
        res = 0
        for index, c in enumerate(s):
            if c == '0':
                pre_s -= 1
            else:
                pre_s += 1
            
            if pre_s in first:
                res = max(res, index - first[pre_s])
            
            if pre_s - 2 in first and (index - first[pre_s - 2] - 2) // 2 < zero:
                res = max(res, index - first[pre_s - 2])
            if pre_s - 2 in second:
                res = max(res, index - second[pre_s - 2])
            
            if pre_s + 2 in first and (index - first[pre_s + 2] - 2) // 2 < one:
                res = max(res, index - first[pre_s + 2])
            if pre_s + 2 in second:
                res = max(res, index - second[pre_s + 2])
            
            if pre_s not in first:
                first[pre_s] = index
            elif pre_s not in second:
                second[pre_s] = index
        
        return res
''',
    call="Solution().longestBalanced('10001')",
    expect=4,
    views=[
        dict(type='string', var='s', label='s', cell=100, h=230, pointers={'index': 'blue'}),
        dict(type='map', var='first', label='first：前缀和 → 第一次出现的位置', fmt=lambda k, v: f'{k}: {v}', h=140, font=30),
        dict(type='map', var='second', label='second：前缀和 → 第二次出现的位置', fmt=lambda k, v: f'{k}: {v}', h=140, font=30),
        dict(type='text', h=100, size=26, fn=_t),
    ],
    watch=[('index', 'index', 'blue'), ('pre_s', 'pre_s', 'cyan'), ('zero', 'zero', 'orange'), ('one', 'one', 'pink'), ('res', 'res', 'green')],
    captions={
        'zero, one = 0, 0': '先数全串里 0 和 1 的个数，后面判断“区间外还有没有可换的字符”',
        'for c in s:': lambda S, B, r: (f'数一个字符 `{S.c}`' if S.zero + S.one < len(S.s) else '统计完：`zero = {}`，`one = {}`'.format(S.zero, S.one)),
        'zero += 1': '0 的个数 `zero = {zero}`',
        'one += 1': '1 的个数 `one = {one}`',
        'first = {0: -1}': '`first`：每个前缀和第一次出现的位置，空前缀 `0 → -1`',
        'second = {}': '`second`：每个前缀和==第二次==出现的位置',
        'pre_s = 0': '`pre_s`：前缀和，0 记 −1，1 记 +1',
        'res = 0': '`res = 0`',
        'for index, c in enumerate': lambda S, B, r: (f'看下标 `{S.index}` 的字符 `{S.c}`' if 'index' not in B or S.index != B.index else '遍历结束'),
        'pre_s -= 1': '遇到 0：`pre_s = {pre_s}`',
        'pre_s += 1': '遇到 1：`pre_s = {pre_s}`',
        'if pre_s in first:': lambda S, B, r: (f'`pre_s = {S.pre_s}` 之前出现过（位置 {S.first[S.pre_s]}）：中间和为 0，不交换也平衡' if S.pre_s in S.first
                                              else f'`pre_s = {S.pre_s}` 还没出现过，不交换没有候选'),
        'res = max(res, index - first[pre_s])': '不交换：长度 `{index} − ({first[pre_s]}) = {index - first[pre_s]}` → `res = {res}`',
        'if pre_s - 2 in first': lambda S, B, r: (
            (f'`pre_s − 2 = {S.pre_s - 2}` 出现过：区间 1 比 0 多两个；区间内约 {(S.index - S.first[S.pre_s - 2] - 2) // 2} 个 0，'
             + ('< zero，区间外还有 0，可换' if (S.index - S.first[S.pre_s - 2] - 2) // 2 < S.zero else '= zero，区间外没有 0，不能用 first'))
            if S.pre_s - 2 in S.first else f'`pre_s − 2 = {S.pre_s - 2}` 没在 first 里'),
        'res = max(res, index - first[pre_s - 2])': '换出一个 1：长度 `{index} − ({first[pre_s - 2]}) = {index - first[pre_s - 2]}` → `res = {res}`',
        'if pre_s - 2 in second': lambda S, B, r: (f'`pre_s − 2` 在 second 里（位置 {S.second[S.pre_s - 2]}）：区间必含 0 和 1，外面有 0 可换' if S.pre_s - 2 in S.second
                                                  else '`pre_s − 2` 不在 second 里，跳过'),
        'res = max(res, index - second[pre_s - 2])': '用第二次出现的位置：长度 `{index} − {second[pre_s - 2]}` → `res = {res}`',
        'if pre_s + 2 in first': lambda S, B, r: (
            (f'`pre_s + 2 = {S.pre_s + 2}` 出现过：区间 0 比 1 多两个；区间内约 {(S.index - S.first[S.pre_s + 2] - 2) // 2} 个 1，'
             + ('< one，区间外还有 1，可换' if (S.index - S.first[S.pre_s + 2] - 2) // 2 < S.one else '= one，区间外没有 1，不能用 first'))
            if S.pre_s + 2 in S.first else f'`pre_s + 2 = {S.pre_s + 2}` 没在 first 里'),
        'res = max(res, index - first[pre_s + 2])': '换出一个 0：长度 `{index} − ({first[pre_s + 2]}) = {index - first[pre_s + 2]}` → `res = {res}`',
        'if pre_s + 2 in second': lambda S, B, r: (f'`pre_s + 2` 在 second 里（位置 {S.second[S.pre_s + 2]}）：外面有 1 可换' if S.pre_s + 2 in S.second
                                                  else '`pre_s + 2` 不在 second 里，跳过'),
        'res = max(res, index - second[pre_s + 2])': '用第二次出现的位置：长度 `{index} − {second[pre_s + 2]}` → `res = {res}`',
        'if pre_s not in first': lambda S, B, r: ('第一次见到这个前缀和 → 记进 `first`' if S.pre_s not in S.first else '以前见过，看看能不能记进 `second`'),
        'first[pre_s] = index': '`first[{pre_s}] = {index}`',
        'elif pre_s not in second': lambda S, B, r: ('第二次见到 → 记进 `second`' if S.pre_s not in S.second else '已经见过两次，不再记录'),
        'second[pre_s] = index': '`second[{pre_s}] = {index}`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='和为 ±2 的区间，外面有字符可换才算数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二进制串 `s`，最多交换任意两个字符一次，再选一个 0 和 1 个数相等的子串',
                 '求这个平衡子串的最大长度',
                 '示例：`s = "10001"` → `4`'],
        quote='前一种情况中，子区间内部0的数量比1多两个，而后一种情况，子区间内部1的数量比0多两个。再转化为区间和，前一种情况的区间和就是-2，而后一种情况的区间和就是2。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想不交换：0 记 −1、1 记 +1，找最长和为 0 的区间 → 相等前缀和相减',
              '要交换：区间和是 ±2，找 `pre_s ± 2` 第一次出现的位置',
              '区间外没有可换的字符时，用 `second`（第二次出现）退一步'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：区间外是否有可换字符，用 `(index − first − 2) // 2` 与 zero/one 比较',
                 '先查询后更新 first/second，两张表分别记第 1、2 次位置',
                 '原文已是 Python 3 可运行的写法（`//` 本来就是整除），未做修改',
                 '对比灵神：灵神用 `defaultdict(list)` 一张表存前两次；这里拆成 first / second'],
    ),
)
