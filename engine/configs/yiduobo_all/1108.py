CONFIG = dict(
    num=1108, title='IP 地址无效化', difficulty='Easy', category='字符串',
    author='yiduobo', technique='字符串 replace',
    code='''
class Solution(object):
    def defangIPaddr(self, address):

        return address.replace('.', '[.]')
''',
    call="Solution().defangIPaddr('192.168.1.1')",
    expect='192[.]168[.]1[.]1',
    views=[
        dict(type='string', var='address', label='address（原地址）', h=200),
        dict(type='text', size=34, fn=lambda S: '把每个 `.` 换成 `[.]`'),
    ],
    watch=['address'],
    captions={
        'return': "`replace('.', '[.]')` 把所有 `.` 换成 `[.]` → `{ret}`",
    },
    cards=dict(
        one_liner='利好 Python：一句 replace 搞定',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给一个有效的 IPv4 地址 `address`，返回它的「无效化」版本',
                 '无效化：把每个 `.` 替换成 `[.]`',
                 '示例：`1.1.1.1` → `1[.]1[.]1[.]1`；本视频：`192.168.1.1`'],
        quote='利好python的题目，直接利用语言特性replace一下即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`str.replace(old, new)` 会替换字符串里的全部匹配',
              '`.` 在 replace 里是普通字符，不是正则，不用转义',
              '一行代码，一次扫描'],
        summary=['时间 `O(n)`，空间 `O(n)`（字符串不可变，会生成新串）',
                 '易错点：`replace` 返回新字符串，不会修改原串',
                 '其他语言可以遍历字符拼接：遇到 `.` 追加 `[.]`',
                 '原文已是 Python 3 可运行写法，未作修改'],
        after=[dict(heading='换成别的语言怎么做', lines=['遍历每个字符，不是 `.` 就原样追加', '是 `.` 就追加 `[.]` 三个字符', '结果长度 = 原长度 + 2 × 点的个数（IPv4 有 3 个点，所以多 6）'])],
    ),
)
