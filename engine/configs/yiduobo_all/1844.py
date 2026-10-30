CONFIG = dict(
    num=1844, title='将所有数字用字符替换', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟扫描 · ASCII 偏移',
    code='''
class Solution(object):
    def replaceDigits(self, s):

        res = []
        for index in range(0, len(s), 2):
            char = s[index]
            res.append(char)
            if index + 1 < len(s):
                offset = int(s[index + 1])
                res.append(chr(ord(char) + offset))
        
        return ''.join(res)
''',
    call="Solution().replaceDigits('a1b2c3d')",
    expect='abbdcfd',
    views=[
        dict(type='string', var='s', pointers={'index': 'blue'}, h=200,
             color=lambda S, i, v: 'pink' if 'index' in S and i == S['index'] + 1 else None),
        dict(type='array', var='res', label='res', h=170, color=lambda S, i, v: 'green'),
    ],
    watch=['index', 'char', 'offset', ('res', 'res', 'green')],
    captions={
        'res = []': '`res` 收集结果字符',
        'for index in range': lambda S, B, r: (f'步长为 2，`index = {S.index}` 指向一个字母（偶数位字母，奇数位数字）' if B.get('index') != S.index else '下标走完，循环结束'),
        'char = s[index]': '当前字母 `char = {char!r}`',
        'res.append(char)': '字母原样放进结果',
        'if index + 1 < len(s)': lambda S, B, r: (f'`{S.index + 1} < {len(S.s)}`：后面还有数字 → 需要替换' if S.index + 1 < len(S.s)
                                                  else f'`{S.index + 1} < {len(S.s)}` 不成立：末尾字母后没有数字，不用替换'),
        'offset = int': '后面的数字是偏移量 `offset = {offset}`',
        'res.append(chr': '`ord({char!r}) + {offset}` 再转回字符：{char!r} 往后移 {offset} 位 → =={res[-1]!r}==',
        'return': '拼成字符串：`{ret!r}`',
    },
    cards=dict(
        one_liner='字母后面的数字，是它往后移的位数；用 ASCII 码算',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['字符串 `s` 偶数下标是小写字母，奇数下标是数字', '把每个数字 `s[i]` 替换为 `shift(s[i-1], s[i])`，即字母往后移 `s[i]` 位',
                 '示例：`"a1b2c3d"` → `"abbdcfd"`'],
        quote='比较基础的题目，一趟扫描，利用ascii码来完成题目替换的要求即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['步长 2 遍历，每次处理一个「字母 + 数字」对', '`ord` 取字母码，加偏移后 `chr` 转回字符',
              '字符串长度可能是奇数，末尾字母后没有数字，要判断 `index + 1 < len(s)`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：奇数长度时末尾字母后无数字，要判边界',
                 '用列表收集再 `join`，比字符串反复拼接高效',
                 '题目保证移位不会超过 `z`'],
    ),
)
