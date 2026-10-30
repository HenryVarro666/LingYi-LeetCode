def _top(S):
    if 's' not in S:
        return ''
    s, t = S['s'], S.get('t')
    if t is None:
        return f"左半边 `s = \"{s}\"`（从大到小填，每个数字填 `cnt // 2` 个）"
    return f"左半边 `\"{s}\"` + 镜像 `t = \"{t}\"`"


CONFIG = dict(
    num=2384, title='最大回文数字', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='从大到小填左半 · 镜像',
    tags=['灵神题单', '难度分 1636'],
    setup="digits = '0123456789'  # 即 string.digits",
    code='''
class Solution:
    def largestPalindromic(self, num: str) -> str:
        cnt = Counter(num)
        if cnt['0'] == len(num):  # 特判最特殊的情况：num 全是 0
            return "0"

        s = ""
        for d in digits[:0:-1]:
            s += d * (cnt[d] // 2)
        if s:  # 如果填了数字，则可以填 0
            s += '0' * (cnt['0'] // 2)

        t = s[::-1]
        for d in digits[::-1]:
            if cnt[d] % 2:  # 还可以填一个变成奇回文串
                s += d
                break
        return s + t  # 添加镜像部分
''',
    call='Solution().largestPalindromic("444947137")',
    expect='7449447',
    views=[
        dict(type='string', var='num', label='num', cell=70, h=150,
             color=lambda S, i, v: 'yellow' if S.get('d') == v and 'd' in S else None),
        dict(type='map', var='cnt', label='cnt（数字 → 出现次数；每 2 个一对）', fmt=lambda k, v: f"'{k}': {v}", h=170),
        dict(type='text', fn=_top, size=28),
        dict(type='string', var='s', label='s（回文串的左半边 + 中心）', cell=70, h=150),
    ],
    watch=['d', ('s', 's', 'green'), ('t', 't', 'cyan')],
    captions={
        'cnt = Counter': '统计每个数字出现几次：`{dict(cnt)}`，成对的才能放两侧',
        "cnt['0'] == len(num)": lambda S, B, r: (f"`0` 出现 `{S.cnt['0']}` 次 == `len(num)` → 全是 0，只能返回 `\"0\"`" if S.cnt['0'] == len(S.num)
                                                 else f"`0` 出现 `{S.cnt['0']}` 次，`len(num) = {len(S.num)}` → 不全是 0，继续"),
        's = ""': '`s` 存回文串的==左半边==，高位越大越好 → 从 9 到 1 依次填',
        8: lambda S, B, r: ('9 到 1 都枚举完了' if 'd' in B and B.d == S.d
                            else f'枚举数字 `{S.d}`（先不碰 0：0 放最高位会是前导零）'),
        's += d *': '数字 `{d}` 有 `{cnt[d]}` 个，能成 `{cnt[d] // 2}` 对 → 左半边填 `{cnt[d] // 2}` 个 → `s = "{s}"`',
        'if s:': lambda S, B, r: (f'`s = "{S.s}"` 非空 → 最高位不是 0，==可以填 0=='
                                  if S.s else '`s` 为空：1~9 都凑不成对，填 0 会变成前导零 → 不填'),
        "s += '0'": '0 的 `{cnt["0"]}` 个能成 `{cnt["0"] // 2}` 对，接在后面（不会在最高位）→ `s = "{s}"`',
        't = s[::-1]': '右半边就是左半边的镜像：`t = "{t}"`',
        14: '从大到小找出现奇数次的数字，先看 `{d}`',
        'if cnt[d] % 2': lambda S, B, r: (f'`cnt[{S.d}] = {S.cnt[S.d]}` 是奇数 → 有一个落单，可放==中心==' if S.cnt[S.d] % 2
                                          else f'`cnt[{S.d}] = {S.cnt[S.d]}` 不是奇数 → 没有落单，看下一个'),
        's += d': '中心放最大的落单数字 `{d}` → `s = "{s}"`',
        'break': '中心只需要 1 个，找到最大的就停',
        'return s + t': '左半 `{s}` + 镜像 `{t}` = =={ret}==',
    },
    cards=dict(
        one_liner='大数字成对放左右，高位尽量大；落单最大的放中心',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给一串数字 `num`，任意取一些并重排，拼成==最大的回文整数==（字符串）',
                 '不能有前导零，至少用一个数字',
                 '示例：`"444947137"` → `"7449447"`；`"00009"` → `"9"`'],
        quote='特判最特殊的情况：num 全是 0。如果填了数字，则可以填 0。还可以填一个变成奇回文串。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['先数每个数字出现次数；左半边从 9 到 1 依次填 `cnt // 2` 个，==高位越大越好==',
              '左半边非空，才能接着填 0，避免前导零；全是 0 的情况单独返回 `"0"`',
              '右半边 = 左半边的镜像；中心放出现奇数次的==最大==数字'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`digits` 是 `string.digits`（"0123456789"），视频里在 setup 里定义',
                 '易错：只有 0 成对时（如 `"00009"`）不能填 0，否则前导零 → 答案是 `"9"`',
                 '易错：全是 0 要返回 `"0"`；中心数字不一定是 9，要找出现奇数次的最大数字'],
    ),
)
