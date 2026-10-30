S0 = '103301'
N = len(S0)


def _phase(S):
    ln = S.get('_line', 0)
    if 'mid_pos' in S and ln >= 34:
        return 3
    if 'right_one' in S and ln >= 24:
        return 2
    return 1


def _lrow(S):
    ph = _phase(S)
    lt = S.get('left_two')
    if lt is None:
        return None
    if ph == 3:
        r = S['mid_pos'] - 1
    elif ph == 2:
        r = N - 1
    else:
        r = S.get('index', 0)
        if r >= N:
            r = N - 1
    return {f'{k // 10}{k % 10}': v for k, v in enumerate(lt[r]) if v}


def _rrow(S):
    ph = _phase(S)
    rt = S.get('right_two')
    if rt is None or ph == 1:
        return {}
    r = S['mid_pos'] + 1 if ph == 3 else S.get('index', N - 1)
    return {f'{k // 10}{k % 10}': v for k, v in enumerate(rt[r]) if v}


def _ptr(S):
    ph = _phase(S)
    if ph == 3:
        return S['mid_pos']
    return S.get('index')


def _lab_l(S):
    return None


def _dot(S, p):
    return sum(a * b for a, b in zip(S['left_two'][p - 1], S['right_two'][p + 1]))


def _hdr1(S, B, ret):
    if sum(S.left_one) >= N:
        return '从左到右扫完，`left_two[i]` 记下了每个前缀能凑出的两位数个数'
    return f'扫到 `s[{S.index}] = {int(S.s[S.index])}`：`left_two[{S.index}]` 先抄上一行（==不用它==），再考虑用它'


def _hdr2(S, B, ret):
    if sum(S.right_one) >= N:
        return '从右到左也扫完了，`right_two` 同理'
    return f'反向扫到 `s[{S.index}] = {int(S.s[S.index])}`：先抄右边一行，再考虑用它'


def _mid(S, B, ret):
    if B.get('mid_pos') == S.mid_pos:
        return '所有中心都枚举完了'
    p = S.mid_pos
    tot = _dot(S, p)
    return (f'中心 `{p}`（`s[{p}] = {S.s[p]}`）：`left_two[{p - 1}]` 与 `right_two[{p + 1}]` 对应位置相乘再求和 = =={tot}=='
            f'（下面 100 次累加省略，`res` 取模后加上它）')


CONFIG = dict(
    num=2484, title='统计回文子序列数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='枚举中心 · 左右两位子序列计数',
    tags=['灵神题单·动态规划', '难度分 2223'],
    code='''
class Solution(object):
    def countPalindromes(self, s):

        n = len(s)
        mod = 10 ** 9 + 7

        left_one = [0] * 10
        left_two = [[0] * 100 for _ in range(n)]

        right_one = [0] * 10
        right_two = [[0] * 100 for _ in range(n)]


        for index in range(n):
            digit = int(s[index])
            if index > 0:
                left_two[index] = left_two[index - 1][:]
            for high_digit in range(10):
                num = high_digit * 10 + digit
                left_two[index][num] += left_one[high_digit]

            left_one[digit] += 1

        for index in range(n - 1, -1, -1):
            digit = int(s[index])
            if index < n - 1:
                right_two[index] = right_two[index + 1][:]
            for high_digit in range(10):
                num = high_digit * 10 + digit
                right_two[index][num] += right_one[high_digit]
            right_one[digit] += 1

        res = 0
        for mid_pos in range(2, n - 2):
            for num in range(100):
                res += left_two[mid_pos - 1][num] * right_two[mid_pos + 1][num]
                res %= mod

        return res
''',
    call=f'Solution().countPalindromes({S0!r})',
    expect=2,
    skip=['for high_digit', 'num = high_digit', '+= left_one[high_digit]', '+= right_one[high_digit]',
          'for num in range(100)', 'digit = int', 'if index > 0', 'if index < n - 1', 'res += left_two', 'res %= mod'],
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前下标 / 中心）', h=200, cell=84, color=lambda S, i, v: 'blue' if i == _ptr(S) else None, pointers={'mid_pos if _line >= 34 else index': 'blue'}, pointer_labels={'mid_pos if _line >= 34 else index': '当前'}),
        dict(type='array', var='left_one', label='left_one[a]：左边数字 a 的个数', h=140, cell=64),
        dict(type='array', var='right_one', label='right_one[a]：右边数字 a 的个数', h=140, cell=64),
        dict(type='map', var=_lrow, label='left_two 当前行（≠0 的两位数 ab: 个数）', h=110, font=22),
        dict(type='map', var=_rrow, label='right_two 当前行（≠0 的两位数: 个数）', h=110, font=22),
    ],
    watch=['index', 'digit', 'mid_pos', ('res', 'res', 'green')],
    captions={
        'n = len(s)': '`n = {n}`',
        'left_one = ': '`left_one[a]`：前缀里数字 `a` 的个数',
        'left_two = ': '`left_two[i][ab]`：前 `i+1` 个字符凑成两位数 `ab` 的子序列个数；每个 `i` 一行，==后面枚举中心要用，不能滚动掉==',
        'right_one = ': '`right_one`：后缀版本',
        'right_two = ': '`right_two[i][ab]`：从 `i` 到末尾能凑成 `ab`（按从右往左读）的个数',
        'for index in range(n):': _hdr1,
        'for index in range(n - 1': _hdr2,
        'left_two[index] = left_two[index - 1][:]': '情况 1：不用第 `{index}` 个字符，直接继承上一行（复制，别共用同一个列表）',
        'right_two[index] = right_two[index + 1][:]': '不用第 `{index}` 个字符，继承右边一行',
        'left_one[digit] += 1': lambda S, B, r: f'情况 2：`{S.digit}` 当低位，接在每个已有高位后：`left_two[i][high*10+digit] += left_one[high]`；`left_one[{S.digit}]` → {S.left_one[S.digit]}',
        'right_one[digit] += 1': lambda S, B, r: f'同样处理右侧后，`right_one[{S.digit}]` → {S.right_one[S.digit]}',
        'res = 0': '开始枚举回文中心',
        'for mid_pos': _mid,
        'return res': '`res = {res}`：每个中心都累加过 `left × right`，已按 `mod` 取模',
    },
    cards=dict(
        one_liner='枚举中心位置，前缀两位数与后缀两位数一一配对相乘',
        complexity='时间 `O(n·100)`，空间 `O(n·100)`',
        problem=['数字串 `s`，数长度为 5 的==回文子序列==个数，结果对 `10^9+7` 取模',
                 '示例：`"103301"` → `2`',
                 '本视频用 `s = "103301"`（n = 6）'],
        quote='枚举回文子序列的中心位置p，那么问题就被拆解成了前缀中能形成每种两位数的子序列数目，以及后缀中反向能形成每种两位数的子序列数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['定长回文 → 老办法：枚举中心，左右各算前缀/后缀',
              '`left_two[i][j]`：前 `i` 个字符凑成两位数 `j` 的个数，用 `left_one` 辅助递推',
              '右侧反过来遍历，照搬同样做法；中心 `p` 的贡献 = 对 100 种两位数 `left_two[p-1][j] × right_two[p+1][j]` 求和'],
        summary=['时间 `O(100n)`，空间 `O(100n)`（`left_two` 每行都要保留）',
                 '中心只需枚举 `2..n-3`，两侧至少各要有 2 个字符',
                 '复制上一行用 `[:]`，直接赋值会让所有行共用一个列表',
                 '对比灵神：灵神一边扫一边撤销 `suf2`，只用 `O(100)` 空间；yiduobo 把每行都存下来'],
    ),
)
