CONFIG = dict(
    num=3794, title='反转字符串前缀', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='切片反转',
    tags=['灵神题单·滑动窗口与双指针', '单序列双指针'],
    code='''
class Solution:
    def reversePrefix(self, s: str, k: int) -> str:
        return s[:k][::-1] + s[k:]
''',
    call='Solution().reversePrefix("abcdefg", 4)',
    expect='dcbaefg',
    views=[
        dict(type='string', var='s', h=200, label='s（蓝色 = 前 k 个字符）', window=('0', 'k - 1'),
             color=lambda S, i, v: 'blue' if i < S['k'] else None),
        dict(type='text', fn=lambda S: f"前缀 `s[:{S['k']}]` = `{S['s'][:S['k']]}`，反转后 `{S['s'][:S['k']][::-1]}`" ),
        dict(type='text', fn=lambda S: f"后缀 `s[{S['k']}:]` = `{S['s'][S['k']:]}` 原样保留 → 拼接得 =={S['s'][:S['k']][::-1] + S['s'][S['k']:]}=="),
    ],
    watch=['s', ('k', 'k', 'blue')],
    captions={
        'return': '`s[:{k}]` 取出前 {k} 个字符，`[::-1]` 把它倒过来，再拼上原样的 `s[{k}:]`，得到 ==`{ret}`==',
    },
    cards=dict(
        one_liner='切出前缀，倒过来，再接上后缀',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给定字符串 `s` 和整数 `k`，反转 `s` 的前 `k` 个字符',
                 '示例：`s="abcd", k=2` → `"bacd"`',
                 '演示用 `s="abcdefg", k=4` → `"dcbaefg"`'],
        quote='时间复杂度：O(n) 或 O(k)，取决于能否原地修改字符串。',
        quote_src='—— 灵茶山艾府题解',
        idea=['本题放在「单序列双指针 · 反转字符串」里：本质是反转一段区间',
              'Python 的字符串不可变，直接用切片最省事',
              '`s[:k][::-1]` 是反转后的前缀，`s[k:]` 是不动的后缀'],
        after=[dict(heading='三个边界例子', lines=['`"abcd", k=2` → `"bacd"`：前两个互换', '`"xyz", k=3` → `"zyx"`：整串反转，后缀为空', '`"hey", k=1` → `"hey"`：只有一个字符，反转后不变', '共同点：始终是「前缀倒序 + 后缀原样」']),
               dict(heading='原地写法（其他语言）', lines=['左指针 `l = 0`，右指针 `r = k - 1`', '交换 `s[l]` 与 `s[r]`，然后 `l++`、`r--`', '直到 `l >= r`：这就是「反转字符串」那一题', '时间 `O(k)`，额外空间 `O(1)`'])],
        summary=['切片会新建字符串，空间 `O(n)`；能原地改的语言用左右指针交换，只需 `O(1)` 额外空间',
                 '`k = len(s)` 时后缀为空，等价于整体反转',
                 '`k = 1` 时前缀只有一个字符，结果不变'],
    ),
)
