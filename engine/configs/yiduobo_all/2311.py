def _col(S, i, v):
    if 'p' not in S:
        return None
    p, ln = S['p'], S['_line']
    if ln >= 29:       # 数前缀里的 0
        if i < p and v == '0' and 'index' in S and (i < S['index'] or (i == S['index'] and ln >= 31)):
            return 'green'
        if i == S.get('index') and i < p:
            return 'pink'
        return 'blue' if i >= p else None
    if i >= p:
        if 'index' in S and 17 <= ln <= 22 and i == S['index'] + p:
            return 'pink'
        return 'blue'
    return None


def _txt(S):
    if 'binary_k' not in S or not S['binary_k']:
        return f"先把 `k = {S.get('k')}` 转成二进制，再比较 `s` 的末尾"
    if 'p' not in S:
        return f"`binary_k = {''.join(map(str, S['binary_k']))}`（`k` 的二进制，高位在前）"
    n, p = len(S['binary_k']), S['p']
    bk = ''.join(map(str, S['binary_k']))
    return f"`s` 最后 `n = {n}` 位 `{S['s'][p:]}` 对比 `binary_k = {bk}`，前面 `p = {p}` 位是前缀"


CONFIG = dict(
    num=2311, title='小于等于 K 的最长二进制子序列', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='贪心 · 逐位比较末尾 n 位',
    tags=['灵神题单', '贪心与思维', '难度分 1840'],
    code='''
class Solution(object):
    def longestSubsequence(self, s, k):

        m = len(s)
        binary_k = []
        while k:
            binary_k.append(k % 2)
            k //= 2
        
        n = len(binary_k)
        binary_k.reverse()
        if m < n:
            return m
        
        p = m - n
        flag = False
        for index, num in enumerate(binary_k):
            if str(num) < s[index + p]:
                flag = True
                break
            elif str(num) > s[index + p]:
                break
        
        if flag:
            res = n - 1
        else:
            res = n

        for index in range(p):
            if s[index] == '0':
                res += 1
        
        return res
''',
    call="Solution().longestSubsequence('1001010', 5)",
    expect=5,
    views=[
        dict(type='text', fn=_txt, h=90),
        dict(type='string', var='s', h=230, label='s（蓝 = 末尾 n 位，粉 = 正在比较的一位，绿 = 前缀里的 0）', color=_col),
        dict(type='array', var='binary_k', h=200, label='binary_k（k 的二进制，高位在前）',
             pointers={'index': 'pink'}),
    ],
    watch=['m', 'n', 'p', ('flag', 'flag', 'orange'), ('res', 'res', 'green')],
    captions={
        'm = len': '`m = len(s) = {m}`',
        'while k': '`k = {k}`：{"不为 0，继续取最低位" if k else "变成 0 了，二进制取完"}',
        'binary_k.append': '`k % 2 = {k % 2}`，取到 k 的最低位',
        'k //= 2': '`k` 右移一位 → {k}',
        'n = len': '`k` 的二进制有 `n = {n}` 位',
        'binary_k.reverse': '先收集的是低位，`reverse` 之后高位在前：`binary_k = {binary_k}`，方便和 `s` 对齐比较',
        'if m < n': lambda S, B, r: ('`m = %d < n = %d`：`s` 比 `binary_k` 短 → 一定小于 k，全选' % (S.m, S.n)) if S.m < S.n else ('`m = %d >= n = %d`：不能直接全选' % (S.m, S.n)),
        'return m': '`s` 比 `k` 短，全部选上，答案 `m`',
        'p = m - n': '`p = {p}`：前 `p` 位是前缀，最后 `n` 位和 `binary_k` 对齐',
        'flag = False': '`flag` 记录末尾 n 位是否比 `binary_k` ==大==',
        'for index, num in': '逐位从高到低比较：`binary_k[{index}] = {num}` 对 `s[{index + p}] = {s[index + p]}`',
        'if str(num) < s[index + p]': lambda S, B, r: ('`k` 这位 `%s` < `s` 这位 `%s` → 末尾 n 位比 `binary_k` ==大==' % (S.num, S.s[S.index + S.p])) if str(S.num) < S.s[S.index + S.p] else ('`k` 这位 `%s` 不小于 `s` 这位 `%s` → 还没有定胜负' % (S.num, S.s[S.index + S.p])),
        'flag = True': '末尾 n 位 > `binary_k`，==flag = True==，最后一位没法全留',
        'elif str(num) > s[index + p]': lambda S, B, r: ('`k` 这位 `%s` > `s` 这位 `%s` → 末尾 n 位比 `binary_k` ==小==，可以整段选' % (S.num, S.s[S.index + S.p])) if str(S.num) > S.s[S.index + S.p] else ('两位都是 `%s` → 相等，继续看下一位' % S.num),
        'break': '已经分出大小，不用再比',
        'res = n - 1': '末尾 n 位太大 → 只取其中任意 `n-1` 位：`res = {res}`',
        'res = n': '末尾 n 位 `<= binary_k` → 整段保留：`res = {res}`',
        'for index in range(p)': '再数前缀里的 0，每个都能当前导零',
        'res += 1': '`s[{index}] = 0` → 前导零 +1：`res = {res}`',
        'return res': '最长子序列长度 ==res = {res}==',
    },
    cards=dict(
        one_liner='取 s 的末尾 n 位（n = k 的二进制位数），再配上前面所有的 0',
        complexity='时间 `O(m)`，空间 `O(log k)`',
        problem=['二进制串 `s` 和正整数 `k`，求数值 `<= k` 的最长子序列长度',
                 '子序列允许前导 0，空串视为 0',
                 '本视频：`s = "1001010", k = 5` → `5`'],
        quote='最理想的情况就是s的最后n位小于等于binary_k，然后取这n位配合上前面所有的0。',
        quote_src='—— yiduobo 题解原文',
        idea=['先算出 `binary_k`（`k` 的二进制，`n` 位），`s` 更短就全选',
              '否则从高位到低位比较 `s` 的末尾 `n` 位：大了答案是 `n-1`，否则是 `n`',
              '再加上前面 `p = m - n` 位里 0 的个数，1 不能要'],
        summary=['时间 `O(m)`，空间 `O(log k)`',
                 '比较的是 `s` 的==末尾 n 位==与 `binary_k`，逐位比较直到分出大小',
                 '`str(num) < s[...]` 是在比字符，`0 < 1`',
                 '原文为 Python 2 写法，`k /= 2` 已改为 `k //= 2`',
                 '对比灵神：灵神用 `bit_length` 和 `int(s[-m:], 2)` 一步比较；这里手动转二进制再逐位比'],
    ),
)
