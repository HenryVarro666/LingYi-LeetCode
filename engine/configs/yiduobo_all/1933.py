CONFIG = dict(
    num=1933, title='判断字符串是否可分解为值均等的子串', difficulty='Medium', category='字符串',
    author='yiduobo', technique='一趟扫描 · 长度 3 为主、仅一个 2',
    code='''
class Solution(object):
    def isDecomposable(self, s):

        n = len(s)
        if n % 3 != 2:
            return False
        
        p = 0
        flag = True
        while p < n:
            if p + 2 < n and s[p] == s[p + 1] == s[p + 2]:
                p += 3
            elif s[p] == s[p + 1] and flag:
                flag = False
                p += 2
            else:
                return False
        
        return True
''',
    call='Solution().isDecomposable("00011111222")',
    expect=True,
    views=[
        dict(type='string', var='s', h=260, pointers={'p': 'blue'},
             color=lambda S, i, v: ('green' if i < S['p'] else None) if 'p' in S else None),
        dict(type='text', fn=lambda S: ('已确认的部分变绿；`flag = True` 表示还没用掉那一个长度 2 的块' if 'flag' in S else ''), size=26),
    ],
    watch=['n', ('p', 'p', 'blue'), ('flag', 'flag', 'orange')],
    captions={
        'n = len': '`n = {n}`',
        'if n % 3 != 2': lambda S, B, r: f'`{S.n} % 3 = {S.n % 3}`' + ('，余数不是 2 → 不可能分解' if S.n % 3 != 2 else '，余数是 2：3 个一组加唯一的 2 个，长度才对得上'),
        'p = 0': '`p` 指向当前块的开头',
        'flag = True': '`flag = True`：长度 2 的块还没用过（只允许一个）',
        'while p < n': lambda S, B, r: (f'`p = {S.p} < n = {S.n}`，继续' if S.p < S.n else f'`p = {S.p}`，整串扫完'),
        'if p + 2 < n and': lambda S, B, r: ('三个字符 `' + S.s[S.p:S.p + 3] + '` 相同 → 能切出长度 3 的块' if S.p + 2 < S.n and S.s[S.p] == S.s[S.p + 1] == S.s[S.p + 2] else f'没有三个连续相同字符（`p={S.p}`）→ 看能不能用长度 2'),
        'p += 3': '切走长度 3：`p` → {p}',
        'elif s[p] == s[p + 1] and flag': lambda S, B, r: (f'`{S.s[S.p]}` 与下一个字符相同，且 `flag = True` → 用掉唯一的长度 2 的块' if S.s[S.p] == S.s[S.p + 1] and S.flag else ('相邻两个相同但长度 2 的名额已用过 → 失败' if S.s[S.p] == S.s[S.p + 1] else f'`{S.s[S.p]}` 与下一个字符不同 → 落单')),
        'flag = False': '`flag = False`：长度 2 的名额用完',
        'p += 2': '切走长度 2：`p` → {p}',
        'return False': lambda S, B, r: '余数不对，直接返回 `False`' if S.n % 3 != 2 else '出现落单字符或第二个长度 2 的块 → `False`',
        'return True': '整串切完，恰好一个长度 2、其余长度 3 → `True`',
    },
    cards=dict(
        one_liner='相同字符连续段只能是 3k 个或 3k+2 个，且 3k+2 的至多一段',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把字符串切成若干个「值均等」的子串（每段字符全相同）',
                 '要求恰好一段长度为 2，其余都是长度 3；能做到返回 `true`',
                 '本视频：`s = "00011111222"` → `true`（`000 | 11 | 111 | 222`）'],
        quote='如果可以成功分解，那么字符串的长度必然是模3余2的。另一方面，对于所有由相同字符构成的连续子串，其要么是某个字符重复了3k次，要么是某个字符重复了3k + 2次，且这个重复3k + 2次的情况只能出现一次。',
        quote_src='—— yiduobo 题解原文',
        idea=['先看长度：不是 `3k+2` 直接 `False`',
              '指针 `p` 从头走：三个相同切 3，否则尝试用掉唯一的 2',
              '落单字符，或第二次需要长度 2，都失败'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`flag` 记录长度 2 的名额，用过就不能再用',
                 '先判长度 `n % 3 == 2`，保证 `s[p + 1]` 不会越界',
                 '本题为会员题，题面按 yiduobo 文章与 LeetCode 原题整理',
                 '原文为 Python 2 写法，仅删去类型说明文档字符串，其余原样'],
    ),
)
