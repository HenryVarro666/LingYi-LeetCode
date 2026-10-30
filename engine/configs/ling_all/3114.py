CONFIG = dict(
    num=3114, title='替换字符可以得到的最晚时间', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='直接判断 · 逐位贪心', tags=[],
    code='''
class Solution:
    def findLatestTime(self, s: str) -> str:
        s = list(s)
        if s[0] == '?':
            s[0] = '1' if s[1] == '?' or s[1] <= '1' else '0'
        if s[1] == '?':
            s[1] = '1' if s[0] == '1' else '9'
        if s[3] == '?':
            s[3] = '5'
        if s[4] == '?':
            s[4] = '9'
        return ''.join(s)
''',
    call='Solution().findLatestTime("?4:5?")',
    expect='04:59',
    views=[
        dict(type='array', var='s', h=220, cell=100,
             color=lambda S, i, v: 'yellow' if v == '?' else ('green' if i in S.get('_chg', ()) else None)),
        dict(type='text', size=32, fn=lambda S: '时间格式 `HH:MM`，小时 `00–11`，分钟 `00–59`'),
    ],
    watch=[('时间', "''.join(s)", 'green')],
    captions={
        's = list': '字符串不能原地改，先转成列表；`?` 是要填的位',
        "if s[0] == '?'": lambda S, B, r: ("小时十位是 `?`，需要填" if S.s[0] == '?' else f"小时十位已是 `{S.s[0]}`，不用填"),
        "s[0] = '1'": lambda S, B, r: (f"十位：个位 `{S.s[1]}` 是 `?` 或 `<= 1`，10、11 都合法 → 填 ==1==" if S.s[0] == '1'
                                       else f"十位：个位 `{S.s[1]}` 在 2~9，只能配 0（02~09）→ 填 ==0=="),
        "if s[1] == '?'": lambda S, B, r: ("小时个位是 `?`，需要填" if S.s[1] == '?' else f"小时个位已是 `{S.s[1]}`，不用填"),
        "s[1] = '1'": '个位：十位是 1 时最大是 11 → 填 `1`；十位是 0 时可到 09 → 填 `9`；结果 =={s[1]}==',
        "if s[3] == '?'": lambda S, B, r: ("分钟十位是 `?`" if S.s[3] == '?' else f"分钟十位已是 `{S.s[3]}`，不用填"),
        "s[3] = '5'": '分钟十位最大 `5`',
        "if s[4] == '?'": lambda S, B, r: ("分钟个位是 `?`" if S.s[4] == '?' else f"分钟个位已是 `{S.s[4]}`，不用填"),
        "s[4] = '9'": '分钟个位最大 `9`',
        "return ''.join": '拼回字符串：=={r}==',
    },
    cards=dict(
        one_liner='小时看相互约束，分钟直接填 59',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['12 小时制 `HH:MM`，`HH` 在 00–11，`MM` 在 00–59', '把 `?` 替换成数字，得到最晚的有效时间',
                 '示例：`"1?:?4"` → `"11:54"`；本视频：`"?4:5?"` → `"04:59"`'],
        quote='方法二：直接判断。',
        quote_src='—— 灵茶山艾府题解',
        idea=['十位：个位 `<= 1` 或未知时填 1，否则只能填 0', '个位：十位是 1 填 1，否则填 9', '分钟：十位 5、个位 9，互不影响'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错：先填十位再填个位，个位依赖已填好的十位',
                 '灵神另给了方法一：从 11:59 倒着枚举，第一个匹配的就是答案',
                 '同类题：`1736`'],
    ),
)
