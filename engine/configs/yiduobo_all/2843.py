def _cur(S):
    if 'str_x' not in S:
        return '逐个检查 `low` 到 `high` 的整数：前半段数位和 = 后半段数位和？'
    x, s = S['str_x'], S['str_x']
    if len(x) % 2:
        return f'`{x}` 有 {len(x)} 位，奇数位 → ==不可能是对称整数=='
    if 'left' in S and 'right' in S and 's' in S:
        return f'成对相减：`s` = 左边数字 − 右边数字 的累计 = ==`{S["s"]}`==（为 0 才对称）'
    return f'`{x}` 有 {len(x)} 位（偶数），可以检查'


CONFIG = dict(
    num=2843, title='统计对称整数的数目', difficulty='Easy', category='动态规划',
    author='yiduobo', technique='直接枚举 + 首尾双指针配对相减',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def countSymmetricIntegers(self, low, high):

        res = 0
        for x in range(low, high + 1):
            str_x = str(x)
            if len(str_x) % 2 == 0:
                left = 0
                right = len(str_x) - 1
                s = 0
                while left < right:
                    s += int(str_x[left]) - int(str_x[right])
                    left += 1
                    right -= 1
                
                if s == 0:
                    res += 1
        
        return res
''',
    call='Solution().countSymmetricIntegers(97, 102)',
    expect=1,
    skip=['left = 0', 'right = len', 'left += 1', 'for x in range'],
    views=[
        dict(type='text', fn=lambda S: f"当前 `x = {S['x']}`" if 'x' in S else '', size=30, h=60),
        dict(type='string', var='str_x', label='str_x（蓝 = left，粉 = right）', cell=90, h=230,
             pointers={'left': 'blue', 'right': 'pink'},
             color=lambda S, i, v: 'blue' if i == S.get('left') else 'pink' if i == S.get('right') else None),
        dict(type='text', fn=_cur, size=26, h=90),
    ],
    watch=[('x', 'x', 'yellow'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('s', 's', 'cyan'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 统计对称整数的个数，从 0 开始',
        'str_x = str(x)': '把 `x = {x}` 转成字符串，方便取出每一位：`{str_x!r}`',
        'if len(str_x) % 2': lambda S, B, r: (f"长度 `{len(S.str_x)}` 是偶数，才可能前半 = 后半 → 继续检查" if len(S.str_x) % 2 == 0
                                               else f"长度 `{len(S.str_x)}` 是奇数，无法分成相等两半 → ==直接跳过=="),
        'while left < right': lambda S, B, r: (f"`left = {S.left}` < `right = {S.right}`：还有一对没配 → 继续" if S.left < S.right
                                                else f"`left = {S.left}` ≥ `right = {S.right}`：所有数位都配完了"),
        's += int': '首尾一对数位配对：`s += {str_x[left]} − {str_x[right]}` → `s = {s}`。==左边加、右边减，前半和 − 后半和 就累计在 s 里==',
        'right -= 1': '两端各向内一位：`left` = {left}，`right` = {right}',
        's = 0': '`s` 累计「左边数字 − 右边数字」，从 0 开始',
        'if s == 0': lambda S, B, r: (f"`s = {S.s}` ==等于 0== → 前半和 = 后半和，`{S.str_x}` 是对称整数" if S.s == 0
                                       else f"`s = {S.s}` ≠ 0 → 前后半数位和不相等，不是对称整数"),
        'res += 1': '找到一个：`res` → {res}',
        'return res': '`[{low}, {high}]` 内共有 `{res}` 个对称整数',
    },
    cards=dict(
        one_liner='数据只到 10^4，不用数位 DP，直接枚举每个数检查',
        complexity='时间 `O((high−low)·log high)`，空间 `O(log high)`',
        problem=['`2n` 位整数，前 `n` 位数字之和等于后 `n` 位数字之和，称为==对称整数==',
                 '求 `[low, high]` 内对称整数的个数',
                 '本视频：`low=97, high=102` → `1`（只有 99）'],
        quote='看题面应该可以使用数位动态规划求解，不过本题的数据规模非常小，完全可以直接枚举low到high之间的所有整数，将数位分离出来之后检测前半段之和是否等于后半段之和。',
        quote_src='—— yiduobo 题解原文',
        idea=['先看数据范围：`high ≤ 10^4`，枚举就够，不必上数位 DP',
              '偶数位才有可能对称；奇数位直接跳过',
              '用首尾两个指针往中间走，每走一步 `s += 左 − 右`；走完 `s == 0` 就说明前后半和相等'],
        summary=['时间 `O((high−low)·log high)`，空间 `O(log high)`',
                 '先判断长度是偶数，再用首尾指针配对；奇数位的数一定不是对称整数',
                 '`s` 是累计差而不是分别求和，最后判断 `s == 0`',
                 '原文已是 Python 3 可运行的写法，代码未做修改'],
    ),
)
