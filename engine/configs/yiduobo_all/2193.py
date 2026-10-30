CONFIG = dict(
    num=2193, title='得到回文串的最少操作次数', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='贪心 · 两侧向中心配对',
    tags=['常用数据结构'],
    code='''
class Solution(object):
    def minMovesToMakePalindrome(self, s):
        n = len(s)
        s_list = list(s)
        l = 0
        r = n - 1
        res = 0
        while l < r:
            p = r
            while p > l and s_list[p] != s_list[l]:
                p -= 1
            if p == l:
                res += n // 2 - l
                l += 1
            else:
                for index in range(p, r):
                    s_list[index], s_list[index + 1] = s_list[index + 1], s_list[index]
                    res += 1
                l += 1
                r -= 1
        
        return res
''',
    call="Solution().minMovesToMakePalindrome('letelt')",
    expect=2,
    skip=['n = len(s)', 's_list = list(s)', 'l = 0', 'r = n - 1', 'res = 0'],
    max_steps=90,
    views=[
        dict(type='text', fn=lambda S: (f"已就位：左 {S['l']} 个、右 {len(S['s_list']) - 1 - S['r']} 个；累计交换 `{S['res']}` 次" if 'r' in S else ''), h=50),
        dict(type='string', var='s_list', pointers={'l': 'blue', 'r': 'pink', 'p': 'yellow'}, window=('l', 'r'), h=260,
             color=lambda S, i, v: ('blue' if i == S['l'] else 'pink' if i == S['r'] else None) if 'r' in S else None,
             dim=lambda S, i, v: 'r' in S and not (S['l'] <= i <= S['r'])),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), 'p', ('res', 'res', 'green')],
    captions={
        'while l < r': lambda S, B, r_: (f'`l = {S.l} < r = {S.r}`：还有没配对的两侧字符' if S.l < S.r else f'`l = {S.l} >= r = {S.r}`：两指针相遇，全部配好'),
        'p = r': '给左边的 `{s_list[l]}` 找搭档：从最右端 `r` 开始往左找第一个相同字符',
        'while p > l': lambda S, B, r_: (f'`s_list[{S.p}] = {S.s_list[S.p]}` 和 `s_list[{S.l}] = {S.s_list[S.l]}` 不同，且 p > l → 继续往左' if S.p > S.l and S.s_list[S.p] != S.s_list[S.l] else f'停在 `p = {S.p}`：' + ('一路没找到相同字符（p 回到 l）' if S.p == S.l else f'`s_list[{S.p}]` 就是左边字符的搭档')),
        'p -= 1': '这个字符不是搭档 → `p` 左移到 {p}',
        'if p == l': lambda S, B, r_: (f'`p == l`：`{S.s_list[S.l]}` 没有搭档，它是==落单的中间字符==' if S.p == S.l else f'`p = {S.p} != l`：找到搭档，把它换到右端 `r = {S.r}`'),
        'res += n // 2 - l': '落单字符到中间 `n // 2` 的距离 `{n // 2} − {l}` 先记上，==但先不移动它==，等其他字符就位（避免多余的反向交换）。`res = {res}`',
        'l += 1': lambda S, B, r_: ('`l` 右移，换下一个字符' ),
        'for index in range(p, r)': lambda S, B, r_: (f'`s_list[{S.p}]` 已经一步步换到 `r = {S.r}`，这一对站好了' if B.get('index') is not None and B.get('index') == S.index and S.index == S.r - 1 else f'把 `s_list[{S.p}]` 一步步向右交换到 `r = {S.r}`：共 `{S.r - S.p}` 次，每次 +1'),
        's_list[index], s_list[index + 1]': '交换相邻 `s_list[{index}]` 和 `s_list[{index + 1}]`，`res = {res}`',
        'res += 1': '这次交换计 1 次操作：`res = {res}`',
        'r -= 1': '这一对 `{s_list[l - 1]}` 已经站好两端 → `l = {l}`，`r` 左移到 {r}',
        'return res': '最少操作次数 `{res}`',
    },
    cards=dict(
        one_liner='相同字符不互换：左边字符找最右的搭档，一步步换到对称位',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['给一个字符串 `s`，每次可交换==相邻==两个字符',
                 '求把它变成回文串的最少交换次数（保证能变成回文）',
                 '示例：`letelt` → `2`（`lettel` 或 `ltetel`）'],
        quote='两个相同的字符之间是不应该发生交换的，相当于浪费了一次操作。从这个节点可以引申出每个字符对应的匹配字符从一开始就固定好了，可以按从两侧向中心的方式寻找到每个字符的匹配字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['匹配关系是固定的：对左边 `s[l]`，选==最右边==的同字符作搭档',
              '搭档换到对称位置 `r`，两端就位，再处理里面',
              '从外往里做，后面的操作不会破坏已就位的字符',
              '落单的中间字符最后才动：不能提前移动'],
        summary=['时间 `O(n^2)`，本题数据规模足够；更大规模可用树状数组',
                 '易错点：落单字符只记距离 `n // 2 − l`，不立刻交换',
                 '原文为 Python 2 写法，整数除法 `n / 2` 已改为 `n // 2`',
                 '搭档必须取最右侧的相同字符'],
    ),
)
