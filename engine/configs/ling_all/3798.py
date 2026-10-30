def _tail(s):
    return len(s) - len(s.rstrip('1'))


CONFIG = dict(
    num=3798, title='最大的偶数', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='去掉尾部的 1',
    tags=[],
    code='''
class Solution:
    def largestEven(self, s: str) -> str:
        return s.rstrip('1')
''',
    call="Solution().largestEven('1221211')",
    expect='12212',
    views=[
        dict(type='text', size=34, fn=lambda S: f"尾部连续的 `1` 有 =={_tail(S['s'])}== 个，删掉后以 `2` 结尾" if 's' in S else ''),
        dict(type='string', var='s', h=300, cell=96,
             color=lambda S, i, v: 'red' if i >= len(S['s']) - _tail(S['s']) else 'green',
             label='s（红 = 尾部的 1，绿 = 保留）'),
        dict(type='text', size=34, fn=lambda S: f"答案 = `{S['s'].rstrip(chr(49))}`" if 's' in S else ''),
    ],
    watch=[('s', 's'), ('尾部 1 的个数', '_tail(s)', 'red'), ('s.rstrip', 's.rstrip("1")', 'green')],
    captions={
        'return s.rstrip': '偶数必须以 `2` 结尾，所以尾部的 `1` 一个都不能留；`rstrip` 去掉 =={len(s) - len(s.rstrip("1"))}== 个 `1`，剩下 `{s.rstrip("1")}`',
    },
    cards=dict(
        before=[dict(heading='先想想：哪些字符串是偶数', lines=['一个数是偶数 ⇔ ==个位是偶数==', '这里只有 `1` 和 `2`，所以结果必须以 `2` 结尾', '位数越多数越大：能多留就多留'])],
        after=[dict(heading='为什么不用再删', lines=['删掉尾部 `1` 后，剩下的字符串已经以 `2` 结尾', '再删任何字符，位数变少，数只会变小', '所以「删尾部 1」既合法又最优'])],
        one_liner='末尾不能是 1，删掉尾部所有 1，剩下的就最大',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计入）',
        problem=['`s` 只含 `1` 和 `2`，可以任意删字符（保持顺序）',
                 '求能表示偶数的最大结果字符串，没有就返回空串',
                 '示例：`221` → `22`；`1` → 空串'],
        quote='答案的末尾不能是 1（这是奇数），所以要移除所有的尾 1。移除后，s 变成偶数且最大，无需继续删除。',
        quote_src='—— 灵茶山艾府题解',
        idea=['偶数的个位只能是 `2`，所以末尾的 `1` 必须删',
              '删完后 `s` 以 `2` 结尾，已经是偶数；再删只会让位数变少、数变小',
              '一行 `rstrip(\'1\')` 搞定：全是 1 时得到空串'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：不要只删最后一个 `1`，是删==所有==尾部连续的 `1`',
                 '全是 `1` 时没有偶数，`rstrip` 自然返回空串',
                 '同类思路：先想「合法结果的形状」，再让它尽量长'],
    ),
)
