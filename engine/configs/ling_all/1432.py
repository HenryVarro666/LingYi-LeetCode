def _top(S):
    if 's' not in S:
        return ''
    s = S['s']
    mx, mn = S.get('mx'), S.get('mn')
    parts = [f'`s = "{s}"`']
    if mx is not None and S['_line'] >= 8:
        parts.append(f'最大值 `mx = {mx}`')
    if mn is not None and S['_line'] >= 13:
        parts.append(f'最小值 `mn = {mn}`')
    return '　'.join(parts)


def _bottom(S):
    if 'mx' in S and 'mn' in S and S['_line'] >= 20:
        return f'差值 `{S["mx"]} − {S["mn"]}` = =={S["mx"] - S["mn"]}=='
    return ''


CONFIG = dict(
    num=1432, title='改变一个整数能得到的最大差值', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='分别求替换后的最大/最小值',
    tags=['灵神题单', '难度分 1427'],
    code='''
class Solution:
    def maxDiff(self, num: int) -> int:
        s = str(num)

        mx = num
        for d in s:
            if d != '9':
                mx = int(s.replace(d, '9'))
                break

        mn = num
        if s[0] != '1':
            mn = int(s.replace(s[0], '1'))
        else:
            for d in s:
                if d > '1':  # 不是 0 也不是 1
                    mn = int(s.replace(d, '0'))
                    break

        return mx - mn
''',
    call='''Solution().maxDiff(9288)
Solution().maxDiff(123456)''',
    expect=820000,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='s', label='s（粉 = 这一轮选中的数字 d 出现的位置）', cell=84,
             color=lambda S, i, v: 'pink' if 'd' in S and S['d'] == v else None),
        dict(type='text', fn=lambda S: (f'当前要替换的数字 `d = {S["d"]}`' if 'd' in S else ''), size=26),
        dict(type='text', fn=_bottom, size=30),
    ],
    watch=['num', ('d', 'd', 'pink'), ('mx', 'mx', 'green'), ('mn', 'mn', 'blue')],
    captions={
        's = str(num)': '`s = "{s}"`：按字符串处理，要让数大/小 = 让字典序大/小，==替换高位更好==',
        'mx = num': '`mx = num`：先假设不替换（全是 9 时无需替换）',
        "for d in s": lambda S, B, r: f"从高位向低位：`d = '{S.d}'`",
        "if d != '9'": lambda S, B, r: (f"`'{S.d}' != '9'` → 成立：这是==最高的非 9 数字==" if S.d != '9'
                                        else "`d = '9'` 已经最大，不用换，看下一位"),
        "mx = int(s.replace(d, '9'))": '把所有 `{d}` 换成 9 → `mx = {mx}`',
        'break': '只换最高的那一种数字，跳出循环',
        'mn = num': '`mn = num`：先假设不替换（比如只含 0 和 1 时换不了）',
        "if s[0] != '1'": lambda S, B, r: (f"`s[0] = '{S.s[0]}'` 不是 1 → 把首位换成 1，不能换成 0（会有前导零）" if S.s[0] != '1'
                                           else "`s[0] = '1'` 首位已经最小，不能再换；去后面找可换成 0 的数字"),
        "mn = int(s.replace(s[0], '1'))": '把所有 `{s[0]}` 换成 1 → `mn = {mn}`',
        'for d in s': lambda S, B, r: f"从高位向低位：`d = '{S.d}'`",
        "if d > '1'": lambda S, B, r: (f"`'{S.d}' > '1'` → 成立：不是 0 也不是 1，可以换成 0" if S.d > '1'
                                       else f"`'{S.d}' > '1'` 不成立：1 不能换成 0（首位会变 0，有前导零），0 本来就最小"),
        "mn = int(s.replace(d, '0'))": '把所有 `{d}` 换成 0 → `mn = {mn}`',
        'return mx - mn': '答案 = 最大值 − 最小值 = `{mx} − {mn}` = =={ret}==',
    },
    cards=dict(
        one_liner='一个换成最大、一个换成最小，差值自然最大',
        complexity='时间 `O(log num)`，空间 `O(log num)`',
        problem=['对整数 `num` 做两次「把所有数字 `x` 换成 `y`」，结果 `a`、`b` 不能有前导 0 且不为 0',
                 '求 `a` 和 `b` 的最大差值',
                 '示例：`9288` → `8700`；`123456` → `820000`'],
        quote='要让替换后的数尽量大，等价于让 s 的字典序尽量大，替换前面的数（高位）相比替换后面的数更好。',
        quote_src='—— 灵茶山艾府题解',
        idea=['答案 = 替换后的最大值 `mx` − 最小值 `mn`',
              '最大值：把最高的非 9 数字全换成 9',
              '最小值：首位不是 1 就把它全换成 1；否则找第一个大于 1 的数字换成 0'],
        summary=['时间 `O(log num)`，空间 `O(log num)`',
                 '易错：最小值不能把首位换成 0（前导零）',
                 '首位是 1 时，找的是 `d > \'1\'`，不是 `d > \'0\'`，否则会把首位的 1 换成 0',
                 '必须整个数字一起替换，`10010` 不能只换一部分 1',
                 'num 到 10^9 时最大值会超过 32 位，要用 64 位整数'],
    ),
)
