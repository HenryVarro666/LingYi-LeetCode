CONFIG = dict(
    num=3980, title='变换二进制字符串的最少操作次数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='从左往右贪心 · 每次看 p 和 p+1',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1846'],
    code='''
class Solution(object):
    def minOperations(self, s1, s2):
        
        p = 0
        res = 0
        while p < len(s1):
            if s1[p] == s2[p]:
                p += 1
                continue
            if s1[p] == '0':
                res += 1
                p += 1
            else:
                if p + 1 < len(s1):
                    if s1[p + 1] == s2[p + 1]:
                        res += 2
                    elif s1[p + 1] == '0':
                        res += 3
                    else:
                        res += 1
                    p += 2
                    
                elif p > 0:
                    res += 2
                    p += 1
                else:
                    return -1
        
        return res
''',
    call="Solution().minOperations('0110100', '1001011')",
    expect=7,
    views=[
        dict(type='string', var='s1', label='s1（要变的串）', h=200, cell=80, pointers={'p': 'blue'},
             color=lambda S, k, v: ('green' if 'p' in S and k < S['p'] else ('yellow' if 'p' in S and k == S['p'] + 1 and S.get('_line') in (14, 15, 16, 17, 18, 19) else None))),
        dict(type='string', var='s2', label='s2（目标）', h=200, cell=80, pointers={'p': 'blue'}),
        dict(type='text', h=70, size=26, fn=lambda S: (
            f"`s1[{S['p']}] = {S['s1'][S['p']]}`，`s2[{S['p']}] = {S['s2'][S['p']]}`") if 'p' in S and S['p'] < len(S['s1']) else 'p 之前（绿色）都已经对齐'),
    ],
    watch=[('p', 'p', 'blue'), ('res', 'res', 'green')],
    captions={
        'p = 0': '`p` 是当前要对齐的位置，从最左边开始',
        'res = 0': '`res` 累计操作次数',
        'while p < len': lambda S, B, r: (f'`p = {S.p}`，还没走完' if S.p < len(S.s1) else f'`p = {S.p}` 已越过末尾 → 全部对齐，结束'),
        'if s1[p] == s2[p]': lambda S, B, r: (f'`s1[{S.p}] = s2[{S.p}] = {S.s1[S.p]}`：本来就相同 → ==不用操作==' if S.s1[S.p] == S.s2[S.p]
                                              else f'`s1[{S.p}] = {S.s1[S.p]}` ≠ `s2[{S.p}] = {S.s2[S.p]}` → 要想办法改'),
        'p += 1': '`p` → {p}',
        "if s1[p] == '0'": lambda S, B, r: ('`s1[p]` 是 0，`s2[p]` 是 1 → 直接 0 变 1，==1 次=='
                                            if S.s1[S.p] == '0' else '`s1[p]` 是 1、要变 0 → 得靠「11 变 00」，看右边一位'),
        'res += 1': '`res = {res}`',
        'if p + 1 < len': lambda S, B, r: (f'`p + 1 = {S.p + 1}` 存在 → 看 `s1[p+1]` 的情况' if S.p + 1 < len(S.s1)
                                           else '`p` 已是最后一位，右边没有了'),
        'if s1[p + 1] == s2[p + 1]': lambda S, B, r: (f'`s1[p+1] = s2[p+1] = {S.s1[S.p + 1]}`：右边本来就对 → 「11变00」再补一次，共 ==2 次==' if S.s1[S.p + 1] == S.s2[S.p + 1]
                                                       else f'`s1[p+1] = {S.s1[S.p + 1]}` ≠ `s2[p+1] = {S.s2[S.p + 1]}`：右边也要改'),
        "elif s1[p + 1] == '0'": lambda S, B, r: ('右边 `s1[p+1] = 0`、目标 1：`10 → 01` 要走 `10→11→00→01`，==3 次==' if S.s1[S.p + 1] == '0'
                                                 else '右边 `s1[p+1] = 1`、目标 0：`11` 直接变 `00`，==1 次=='),
        'res += 2': '`res = {res}`：共 2 次',
        'res += 3': '`res = {res}`：共 3 次（p、p+1 两位一起归位）',
        'p += 2': 'p、p+1 都归位了，`p` 一次跳 2 位 → {p}',
        'elif p > 0': '没有右边了，借已归位的左边：先造 11 再清零，共 2 次',
        'return -1': '只有 1 位，无处可借 → 无解，返回 -1',
        'return res': '最少操作次数 =={ret}==',
    },
    cards=dict(
        one_liner='操作代价都是 1，不铺垫小操作：从左往右，按位直接贪心',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['两个等长二进制串 `s1`、`s2`',
                 '可以把任意 `0` 变 `1`，或把相邻 `11` 同时变 `00`',
                 '求 `s1` 变成 `s2` 的最少操作次数，不可能则 -1',
                 '本视频：`0110100` → `1001011`'],
        quote='由于本题中操作的代价都一样，因此不会有通过先铺垫小操作，然后执行一次大操作达到剩操作数的目的。',
        quote_src='—— yiduobo 题解原文',
        idea=['`s1[p] = s2[p]`：不动；`0 → 1`：加 1 次，p 后移 1 位',
              '`1 → 0`：看右边一位，分三种情况，一次处理 p 和 p+1 两位',
              '没有右边：借左边（已归位），共 2 次；单个 1 变 0 则无解'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`1 → 0` 时右边情况：右边已对 +2，右边是 `0→1` 要 +3，右边是 `1→0` 只要 +1',
                 '这三种情况处理完 p 和 p+1，所以 `p += 2`',
                 '原文就是 Python 2 风格，本题没有整数除法，代码未改动',
                 '对比灵神：灵神把改动记在 s[i+1] 上，每轮只看一位；yiduobo 一次吃掉两位'],
    ),
)
