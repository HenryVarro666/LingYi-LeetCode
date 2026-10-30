CONFIG = dict(
    num=2914, title='使二进制字符串变美丽的最少修改次数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='等价转化 · 相邻两两相等',
    tags=['灵神题单', '难度分 1480'],
    code='''
class Solution:
    def minChanges(self, s: str) -> int:
        return sum(s[i] != s[i + 1] for i in range(0, len(s), 2))
''',
    call='Solution().minChanges("10110100")',
    expect=2,
    views=[
        dict(type='string', var='s', label='s（每 2 个一组：绿 = 相等，红 = 不等，要改 1 个）', h=260,
             color=lambda S, i, v: 'red' if S['s'][i // 2 * 2] != S['s'][i // 2 * 2 + 1] else 'green'),
        dict(type='text', fn=lambda S: '分组：' + ' | '.join(S['s'][j:j + 2] for j in range(0, len(S['s']), 2)), size=32),
        dict(type='text', fn=lambda S: f"不相等的组数 = `{sum(S['s'][j] != S['s'][j + 1] for j in range(0, len(S['s']), 2))}`", size=32),
    ],
    watch=[('len(s)', 'len(s)', 'blue'), ('组数', 'len(s) // 2', 'orange')],
    captions={
        'return sum': '`i` 取 `0, 2, 4, 6`：逐组比较 `s[i]` 与 `s[i+1]`，==不相等的组各改 1 个字符==，数出来共 =={ret}== 组（`True` 当 1 加）',
    },
    cards=dict(
        one_liner='美丽字符串 = 每两个字符一组，两个字符相等',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制串 `s`（长度为偶数）能切成若干「偶数长度、全 0 或全 1」的子串，就叫美丽的',
                 '每次可以改任一个字符，求让 `s` 变美丽的最少修改次数',
                 '本视频：`s = "10110100"` → `2`'],
        quote='美丽字符串等价于对于所有偶数下标 `i`，有 `s[i] == s[i+1]`。如果不满足上式，修改其中一个字母即可。',
        quote_src='—— 灵茶山艾府题解',
        before=[dict(heading='先看例子', lines=['`"1001"` 改成 `"1100"`，分成 `11|00`，改了 2 次', '`"10"` 改成 `"11"`，改了 1 次', '`"0000"` 本来就美丽，改 0 次']),
                dict(heading='为什么只看两两一组', lines=['任何偶数长度的全相同子串，都能再拆成长为 2 的全相同小段', '所以美丽 ⇔ 每个偶数下标 `i` 满足 `s[i] == s[i+1]`'])],
        idea=['偶数长度的全 0/全 1 子串，都能再拆成长为 2 的全相同小段',
              '所以只要每个 `(s[0],s[1])`、`(s[2],s[3])`…… 内部相等就行',
              '不相等的一组恰好改一个字符；各组互不影响，直接数不相等的组数'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`range(0, len(s), 2)` 步长 2，且 `s[i+1]` 不会越界（长度为偶数）',
                 '`True` 在 `sum` 里当 1 算',
                 '同类思路：先把条件等价成「相邻两两相等」，再逐组统计'],
    ),
)
