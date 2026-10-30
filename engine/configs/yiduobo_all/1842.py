CONFIG = dict(
    num=1842, title='下个由相同数字构成的回文串', difficulty='Hard', category='贪心与思维',
    author='yiduobo', technique='前半部分的下一个排列',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def nextPalindrome(self, num):

        n = len(num) // 2

        if len(num) % 2 == 1:
            mid = num[n]
        else:
            mid = ''
        
        num_list = list(num[:n])
        p = n - 1
        while p > 0 and num_list[p] <= num_list[p - 1]:
            p -= 1
        
        if p <= 0:
            return ""
        
        p -= 1
        q = n - 1
        while num_list[q] <= num_list[p]:
            q -= 1

        num_list[p], num_list[q] = num_list[q], num_list[p]
        left = p + 1
        right = n - 1
        while left < right:
            num_list[left], num_list[right] = num_list[right], num_list[left]
            left += 1
            right -= 1
        
        res = ''.join(num_list) + mid
        num_list.reverse()
        return res + ''.join(num_list)
''',
    call='Solution().nextPalindrome("134252431")',
    expect='142353241',
    views=[
        dict(type='string', var='num', label='num（前半 | 正中间 | 后半）', cell=70,
             color=lambda S, i, v: 'green' if i < len(S['num']) // 2 else ('yellow' if i == len(S['num']) // 2 and len(S['num']) % 2 else None)),
        dict(type='array', var='num_list', label='num_list：前半部分（求它的下一个排列）', cell=90,
             pointers={'p': 'pink', 'q': 'blue', 'left': 'cyan', 'right': 'orange'},
             color=lambda S, i, v: 'pink' if i == S.get('p') and S['_line'] >= 21 else None),
        dict(type='text', fn=lambda S: f"`mid = '{S['mid']}'`（长度为奇数时的正中间字符）" if 'mid' in S else '', size=26),
    ],
    watch=['n', 'mid', 'p', 'q', 'left', 'right', ('res', 'res', 'green')],
    captions={
        'n = len': '半区长度 `n = {n}`：回文串前后两半的字符组成相同，只需处理前半',
        'mid = num[n]': '长度为奇数，先记下正中间字符 `mid = {mid}`',
        "mid = ''": '长度为偶数，没有中间字符',
        'num_list = list': '前半部分 `num_list = {num_list}`：现在要求它的==下一个排列==',
        'p = n - 1': '`p` 从最后一位开始，找“降序后缀”的前一位',
        'while p > 0 and': lambda S, B, r: (f"`num_list[{S.p}] = {S.num_list[S.p]} <= num_list[{S.p-1}] = {S.num_list[S.p-1]}` → 仍是降序，`p` 左移"
                                           if S.p > 0 and S.num_list[S.p] <= S.num_list[S.p - 1]
                                           else f"`p = {S.p}`：降序后缀结束（或已到头）"),
        'p -= 1': '`p` 再左移一位：==`num_list[{p}] = {num_list[p]}`== 是要被换大的那一位',
        'if p <= 0': lambda S, B, r: ('`p <= 0`：整个前半已是最大排列 → 没有下一个，返回空串' if S.p <= 0 else '`p > 0`：存在下一个排列'),
        'q = n - 1': '`q` 从末尾往左，找第一个比 `num_list[p]` 大的数',
        'while num_list[q] <= num_list[p]': '`num_list[{q}] = {num_list[q]}` 与 `num_list[p] = {num_list[p]}` 比较：不大于则 `q` 左移',
        'num_list[p], num_list[q]': '交换 `p`、`q` 处的数：前半变成 `{num_list}`，高位变大了',
        'left = p + 1': '后缀要变成最小：把它==反转==（原本是降序）',
        'while left < right': '`left = {left}`，`right = {right}`：还没交错就继续反转',
        'num_list[left], num_list[right]': '交换 `left`、`right`：`{num_list}`',
        'left += 1': '`left` → {left}',
        'right -= 1': '`right` → {right}',
        'res = ': "新的前半 + 中间字符：`res = '{res}'`",
        'num_list.reverse': '把新前半倒转，得到后半部分 `{num_list}`',
        'return res': '前半 + 中间 + 倒转的前半 = =={ret}==',
    },
    cards=dict(
        one_liner='回文串的下一个，就是前半部分的下一个排列',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给定回文数字串 `num`，用==相同的数字==重排，求比它大的最小回文串',
                 '不存在则返回空串',
                 '示例：`"1221"` → `"2112"`'],
        quote='由于半区的数字不会产生变化，那么实际上就是要求找出前半部分的下一个排列。对于这个问题，直接照搬之前31题的算法就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['回文串前后两半字符组成相同，只看前半部分',
              '前半求==下一个排列==：找降序后缀前一位 `p`，与后缀里刚好更大的 `q` 交换，再反转后缀',
              '长度为奇数时记下中间字符，最后拼 `前半 + mid + 倒转前半`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：奇数长度要先保存正中间字符，否则拼出来少一位',
                 '前半已是最大排列（`p <= 0`）就返回空串',
                 '原文为 Python 2 写法，`len(num) / 2` 已改为 `//`',
                 '算法就是第 31 题「下一个排列」'],
    ),
)
