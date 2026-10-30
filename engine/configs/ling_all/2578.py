CONFIG = dict(
    num=2578, title='最小和分割', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='排序后奇偶下标分组',
    tags=['灵神题单', '难度分 1351'],
    code='''
class Solution:
    def splitNum(self, num: int) -> int:
        s = ''.join(sorted(str(num)))
        return int(s[::2]) + int(s[1::2])
''',
    call='Solution().splitNum(4325)',
    expect=59,
    views=[
        dict(type='string', var='s', label='s：排序后的数字（蓝 = 偶数下标 → num1，粉 = 奇数下标 → num2）', cell=110,
             color=lambda S, i, v: 'blue' if i % 2 == 0 else 'pink'),
        dict(type='text', fn=lambda S: f"`s[::2] = {S['s'][::2]}`　`s[1::2] = {S['s'][1::2]}`" if 's' in S else '', size=34),
        dict(type='text', fn=lambda S: f"`{int(S['s'][::2])} + {int(S['s'][1::2])}` = =={int(S['s'][::2]) + int(S['s'][1::2])}==" if 's' in S else '', size=34),
    ],
    watch=['num', 's'],
    captions={
        "s = ''.join": '数字从小到大排序：`s = "{s}"`。小的在前，接下来分给高位',
        'return': '偶数下标 `{s[::2]}` 为一组，奇数下标 `{s[1::2]}` 为另一组：`{int(s[::2])} + {int(s[1::2])}` = =={ret}==',
    },
    cards=dict(
        one_liner='尽量均匀分，小的数字放高位：排序后按奇偶下标分组',
        complexity='时间 `O(m log m)`，空间 `O(m)`，`m` 为位数',
        problem=['把 `num` 的所有数位分给 `num1`、`num2`（可有前导 0），求两数之和的==最小值==',
                 '示例：`4325` → `59`（`24 + 35`）',
                 '`687` → `75`（`68 + 7`）'],
        quote='如果分成 432 和 5 这两组，不如分成 32 和 45，因为 4 在 432 中是 400，在 45 中是 40。这启发我们要尽量均匀分。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先问：`4325` 怎么分？高位数字别叠在同一个数里，==均匀分==',
              '每组内部，`23` 比 `32` 好：==小的数字排在高位，大的排在低位==',
              '合起来：排序后按奇偶下标分组，两组各是一个数'],
        after=[dict(heading='用 687 验证', lines=[
            '排序得 `s = "678"`，偶数下标 `6, 8` → `68`，奇数下标 `7` → `7`',
            '`68 + 7 = 75`，正是示例答案',
            '若改成 `6 + 78 = 84` 或 `687 + 0`，高位数字被放大，更差'])],
        summary=['时间 `O(m log m)`，空间 `O(m)`',
                 '位数为奇数时，多出的那个数字放哪一组都可以',
                 '`s[::2]` 是偶数下标，`s[1::2]` 是奇数下标，别写反成相邻切分',
                 '对比 yiduobo：他是遍历时交替拼接，本质相同'],
    ),
)
