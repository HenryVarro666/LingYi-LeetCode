def _now(S):
    if 't' not in S or 'i' not in S:
        return '把小时和分钟拆开算：答案 = 小时个数 × 分钟个数'
    t, i = S['t'], S['i']
    a = '?' if t[0] == '?' else t[0]
    return f"枚举 `i = {i:02d}`：十位 `{i // 10}` 对 `{t[0]}`，个位 `{i % 10}` 对 `{t[1]}`，目前 `ans = {S.get('ans', 0)}`"


CONFIG = dict(
    num=2437, title='有效时间的数目', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='分开枚举 · 乘法原理',
    tags=[],
    code='''
def count(t: str, period: int) -> int:
    ans = 0
    for i in range(period):
        if (t[0] == '?' or i // 10 == int(t[0])) and \\
           (t[1] == '?' or i % 10 == int(t[1])):
            ans += 1
    return ans

class Solution:
    def countTime(self, time: str) -> int:
        return count(time[:2], 24) * count(time[3:], 60)
''',
    call='Solution().countTime("?5:4?")',
    expect=20,
    views=[
        dict(type='text', fn=_now, size=26),
        dict(type='string', var='t', label='当前这段（小时 / 分钟）', cell=110),
        dict(type='text', fn=lambda S: (f"这个 `i` 的两位都能和 `t` 对上 → 合法" if S.get('_line') == 6 else ''), size=26),
    ],
    skip=[5],
    max_steps=40,
    watch=[('period', 'period'), ('i', 'i', 'blue'), ('ans', 'ans', 'green')],
    captions={
        2: '分别数小时、分钟各有几种合法填法，`ans` 从 0 开始',
        3: '枚举 `[0, {period})` 里的每个整数 `i`，看它能不能是 `t` 填完 `?` 后的样子',
        4: lambda S, B, r: (f"十位：`t[0] = '{S.t[0]}'` {'是 ?，随便' if S.t[0] == '?' else '要等于 ' + str(S.i // 10)}；个位：`t[1] = '{S.t[1]}'` {'是 ?，随便' if S.t[1] == '?' else '要等于 ' + str(S.i % 10)} → "
                                      + ('==匹配==' if (S.t[0] == '?' or S.i // 10 == int(S.t[0])) and (S.t[1] == '?' or S.i % 10 == int(S.t[1])) else '不匹配')),
        6: '`i = {i}` 是一种合法填法，`ans` → {ans}',
        7: '这一段共有 `{ans}` 种有效填法',
        11: '小时和分钟互不影响，乘法原理：`{ret}` 种',
    },
    cards=dict(
        one_liner='小时、分钟互不影响，各数各的再相乘',
        complexity='时间 `O(24+60)=O(1)`，空间 `O(1)`',
        problem=['`"hh:mm"` 里有若干 `?`，每个可以填 0 到 9，求能得到多少个有效时间（00:00 到 23:59）',
                 '示例：`"?5:00"` → `2`；`"??:??"` → `1440`',
                 '本视频：`"?5:4?"` → 小时 2 种 × 分钟 10 种 = `20`'],
        quote='分别计算小时和分钟的有效个数，根据乘法原理，答案为这两个个数的乘积。',
        quote_src='—— 灵茶山艾府题解',
        idea=['小时枚举 `[0,23]`，分钟枚举 `[0,59]`，每个 `i` 拆成十位和个位',
              '十位是 `?` 或等于 `i` 的十位，个位同理，两个条件都满足才算一种',
              '两个判断写进同一个函数 `count(t, period)`，传入 24 或 60'],
        result='小时 `"?5"` 有 05、15 两种，分钟 `"4?"` 有 10 种 → `2 × 10 = 20` ✓',
        summary=['时间 `O(1)`：最多枚举 24 + 60 个数',
                 '`i < 10` 时十位是 0：`i // 10 == 0`，所以 `"0?"` 也能匹配',
                 '易错：小时上限 24、分钟上限 60 别写反，`range` 不含上界',
                 '字符串 `time[:2]` 与 `time[3:]` 跳过了冒号'],
    ),
)
