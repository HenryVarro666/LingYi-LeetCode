def _par(S, i, v):
    return 'blue' if v % 2 == 0 else 'pink'


def _cnt(S):
    d = S.get('digit_list')
    if d is None:
        return ''
    ev = sum(1 for x in d if x % 2 == 0)
    od = len(d) - ev
    return f'偶数位 `{ev}` 个（蓝），奇数位 `{od}` 个（粉）；要的是两边相等'


CONFIG = dict(
    num=2417, title='最近的公平整数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='按奇偶位数差构造 · 进位调整',
    tags=[],
    code='''
class Solution(object):
    def closestFair(self, n):

        digit_list = [int(x) for x in list(str(n))]
        diff = 0
        for digit in digit_list:
            if int(digit) % 2 == 0:
                diff += 1
            else:
                diff -= 1
            
        if diff == 0:
            return n
        
        def generate(length):
            res = 1
            for index in range(length // 2):
                res = res * 10
            
            for index in range(length // 2 - 1):
                res = res * 10 + 1
            
            return res

        if abs(diff) % 2 == 1:
            res = generate(len(digit_list) + 1)
            return res
        
        need_change = abs(diff) // 2
        odd = 0
        even = 0
        p = len(digit_list) - 1
        while True:
            if digit_list[p] % 2 == 0:
                odd += 1
            else:
                even += 1
            
            if (diff > 0 and odd == need_change) or (diff < 0 and even == need_change):
                break
            p -= 1
        
        if diff > 0:
            digit_list[p] += 1
            p += 1
            while p < len(digit_list):
                digit_list[p] = 1
                p += 1
            
            res = 0
            for digit in digit_list:
                res = res * 10 + digit
            
            return res

        while p >= 0 and digit_list[p] >= 8:
            p -= 1
        
        if p == -1:
            res = generate(len(digit_list) + 2)
            return res
        
        if digit_list[p] % 2 == 1:
            digit_list[p] += 1
        else:
            digit_list[p] += 2

        diff = 0
        for index in range(p, -1, -1):
            if digit_list[index] % 2 == 0:
                diff += 1
            else:
                diff -= 1

        r = len(digit_list) - (p + 1)

        zero_cnt = (r - diff) // 2
        for index in range(zero_cnt):
            p += 1
            digit_list[p] = 0
        
        p += 1
        while p < len(digit_list):
            digit_list[p] = 1
            p += 1
        
        res = 0
        for digit in digit_list:
            res = res * 10 + digit
        
        return res
''',
    call='Solution().closestFair(1397)',
    expect=1401,
    views=[
        dict(type='array', var='digit_list', label='digit_list（蓝 = 偶数位，粉 = 奇数位）', pointers={'p': 'yellow'}, cell=110, h=210,
             color=_par),
        dict(type='text', h=90, size=28, fn=_cnt),
        dict(type='text', h=80, size=28,
             fn=lambda S: (f"`diff` = 偶数位 − 奇数位 = =={S['diff']}==" if 'diff' in S else '')),
    ],
    watch=[('diff', 'diff', 'orange'), ('need_change', 'need_change'), ('p', 'p', 'yellow'), ('res', 'res', 'green')],
    skip=['res = res * 10 + digit', 'digit_list = [int(x)'],
    captions={
        5: '`diff` = 偶数位个数 − 奇数位个数；公平数要求 `diff == 0`',
        6: lambda S, B, ret: (f'看下一位 `{S.digit}`' if 'digit' in S and B.get('diff', 0) == S.diff and False else (f'看下一位 `{S.digit}`' if S.get('_inner', {}).get('digit') is not None and S.diff != sum(1 if x % 2 == 0 else -1 for x in S.digit_list) else '每一位都数过了')),
        31: '`even` 统计奇数位个数（原文变量名与含义是反的）',
        30: '`odd` 统计偶数位个数',
        32: '`p` 从最低位出发：`p = {p}`',
        33: '一直往高位走，直到数够 `need_change` 个',
        40: '数够了，`p` 停在这一位',
        41: '`p` 左移到 `{p}`',
        57: '`p` 左移到 `{p}`，继续往高位找可用的位',
        68: '重新统计：从 `p` 到最高位这些已定下来的数位里，偶数位比奇数位多几个',
        78: lambda S, B, ret: ('先填 `{}` 个 0（偶数位，且最小）'.format(S.zero_cnt) if S.digit_list.count(0) < S.zero_cnt else '0 填完了'),
        88: lambda S, B, ret: ('拼完了' if S.res == int(''.join(map(str, S.digit_list))) else '接着拼 `{}`：`res = {}`'.format(S.digit, S.res)),
        'if int(digit) % 2 == 0': lambda S, B, ret: (f'`{S.digit}` 是偶数位 → `diff` 加一' if S.digit % 2 == 0 else f'`{S.digit}` 是奇数位 → `diff` 减一'),
        'diff += 1': '`diff` = `{diff}`',
        'diff -= 1': '`diff` = `{diff}`',
        'if diff == 0': lambda S, B, ret: ('`diff = 0`：本来就公平，直接返回 `n`' if S.diff == 0 else f'`diff = {S.diff}`：奇偶位不等，要调整'),
        'if abs(diff) % 2 == 1': lambda S, B, ret: (
            f'`diff` 是奇数 → 位数是奇数，调整数位凑不成公平数 → 只能进到更长的 `{len(S.digit_list) + 1}` 位' if abs(S.diff) % 2 == 1
            else f'`diff = {S.diff}` 是偶数 → 位数是偶数，可以在本位数内调整'),
        'need_change = abs(diff) // 2': '要把 `{need_change}` 个多出来的位改成另一种奇偶',
        'odd = 0': '从最低位往高位数，找要改的那一位',
        'p = len(digit_list) - 1': '`p` 从最低位出发：`p = {p}`',
        'if digit_list[p] % 2 == 0': lambda S, B, ret: (f'`digit_list[{S.p}] = {S.digit_list[S.p]}` 是偶数位，`odd` 计数' if S.digit_list[S.p] % 2 == 0 else f'`digit_list[{S.p}] = {S.digit_list[S.p]}` 是奇数位，`even` 计数'),
        'if (diff > 0 and odd': lambda S, B, ret: (
            f'`diff < 0`（奇数位多）：数到第 `{S.need_change}` 个奇数位就停 → `even = {S.even}`' + ('，==够了，p 就是它==' if S.even == S.need_change else '，还不够，继续往高位走')
            if S.diff < 0 else
            f'`diff > 0`（偶数位多）：数到第 `{S.need_change}` 个偶数位就停 → `odd = {S.odd}`' + ('，==够了，p 就是它==' if S.odd == S.need_change else '，还不够，继续往高位走')),
        'if diff > 0': lambda S, B, ret: ('偶数位多：把这一位加一变成奇数，后面全填 1' if S.diff > 0 else '奇数位多：这一位要加一或加二变成更大的偶数，要小心 9'),
        'digit_list[p] += 1': '这一位加一 → `{digit_list[p]}`',
        'while p >= 0 and digit_list[p] >= 8': lambda S, B, ret: (
            f'`digit_list[{S.p}] = {S.digit_list[S.p]} ≥ 8`：加 1 或 2 会进位 → ==继续往高位找==' if S.p >= 0 and S.digit_list[S.p] >= 8
            else (f'`digit_list[{S.p}] = {S.digit_list[S.p]} < 8`：加 1 或 2 不进位，可以用' if S.p >= 0 else '一直找到最高位也没有可用位')),
        'if p == -1': lambda S, B, ret: ('没有可调整的位 → 只能进到更长一档（位数 + 2）' if S.p == -1 else f'找到可调整的位 `p = {S.p}`'),
        'if digit_list[p] % 2 == 1': lambda S, B, ret: (f'这位是 `{S.digit_list[S.p]}`：奇数 → 加 1 变成偶数' if S.digit_list[S.p] % 2 == 1 else f'这位是 `{S.digit_list[S.p]}`：偶数 → 加 2 变成更大的偶数（加 1 会变奇数）'),
        'digit_list[p] += 2': '这一位加二 → `{digit_list[p]}`',
        'if digit_list[index] % 2 == 0': lambda S, B, ret: (f'`digit_list[{S.index}] = {S.digit_list[S.index]}` 偶数位 → `diff` 加一' if S.digit_list[S.index] % 2 == 0 else f'`digit_list[{S.index}] = {S.digit_list[S.index]}` 奇数位 → `diff` 减一'),
        'r = len(digit_list) - (p + 1)': '`p` 后面还剩 `r = {r}` 位可以随便填',
        'zero_cnt = (r - diff) // 2': '已定的高位里偶数位比奇数位多 `{diff}` 个；后 `{r}` 位里偶数位要有 `(r − diff) / 2` = `{zero_cnt}` 个（填 0），其余填 1',
        'for index in range(zero_cnt)': lambda S, B, ret: (f'先填 `{S.zero_cnt}` 个 0（偶数位，且最小）' if S.zero_cnt > 0 else '不用填 0'),
        'digit_list[p] = 0': '`digit_list[{p}] = 0`',
        'digit_list[p] = 1': '`digit_list[{p}] = 1`（奇数位里最小的是 1）',
        'while p < len(digit_list)': lambda S, B, ret: (f'剩下的位都填 1' if S.p < len(S.digit_list) else '填完了'),
        'res = 0': '`res` 从 0 开始，逐位拼回整数',
        'return res': '返回 `{res}`',
        'while True': '一直往高位走，直到数够 `need_change` 个',
        'return n': '返回 `{n}`',
    },
    cards=dict(
        one_liner='先看奇偶位数之差，再找一位进位，后面补最小的 0 和 1',
        complexity='时间 `O(len)`，空间 `O(len)`',
        problem=['公平整数：偶数位个数 == 奇数位个数。给 `n`，求 `≥ n` 的最小公平整数',
                 '本视频：`n = 1397` → `1401`',
                 '（1397 里奇数位 4 个、偶数位 0 个，不公平）'],
        quote='首先，若n的长度len为奇数，那么就不可能通过调整n的数字组成达到奇数位和偶数位相同，只能构造一个长度为len + 1的数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`diff` = 偶数位 − 奇数位。`diff` 是奇数 ==等价于位数是奇数==，只能进到更长一档',
              '`diff > 0`：把倒数第 `diff/2` 个偶数位加一，后面全填 1',
              '`diff < 0`：先找倒数第 `|diff|/2` 个奇数位，遇到 ≥ 8 就往高位找 < 8 的位，加一或加二',
              '再用 `(r − diff)/2` 个 0 加若干 1 补全后面的位'],
        summary=['时间 `O(len)`，空间 `O(len)`',
                 '易错：9 加一会进位，所以要找 `< 8` 的位',
                 '找不到可调整的位时，答案是 `100…011…1`，位数比原来多 2',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '代码里变量 `odd` 统计的是偶数位、`even` 统计的是奇数位，名字是反的，看代码时留意'],
    ),
)
