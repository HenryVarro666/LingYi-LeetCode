CONFIG = dict(
    num=2609, title='最长平衡子字符串', difficulty='Easy', category='模拟',
    author='yiduobo', technique='分离连续的 0 段和 1 段',
    tags=[],
    code='''
class Solution(object):
    def findTheLongestBalancedSubstring(self, s):

        p = 0
        res = 0
        while p < len(s):
            start = p
            while p < len(s) and s[p] == '0':
                p += 1
            zero_cnt = p - start

            start = p
            while p < len(s) and s[p] == '1':
                p += 1
            one_cnt = p - start
            
            res = max(res, min(zero_cnt, one_cnt))
        
        return res + res
''',
    call="Solution().findTheLongestBalancedSubstring('01000111')",
    expect=6,
    views=[
        dict(type='string', var='s', pointers={'p': 'blue', 'start': 'pink'}, h=260,
             color=lambda S, i, v: ('green' if v == '0' else 'cyan') if 'p' in S and i < S['p'] else None),
        dict(type='text', fn=lambda S: (f"0 段长 `zero_cnt = {S['zero_cnt']}`" if 'zero_cnt' in S else '') + (f"，1 段长 `one_cnt = {S['one_cnt']}`" if 'one_cnt' in S and S.get('_line') in (15, 17) else ''), size=32),
    ],
    watch=['p', 'start', 'zero_cnt', 'one_cnt', ('res', 'res', 'green')],
    skip=['p = 0', 'res = 0', 'start = p'],
    max_steps=60,
    captions={
        'while p < len(s):\n': '还没扫完',
        'p += 1': lambda S, B, r: ('`s[{}]` 是 `{}`，继续扩展这一段：`p = {}`'.format(B.p, S.s[B.p], S.p)),
        'zero_cnt = p': '这一段 0 的长度 `zero_cnt = p − start = {p} − {start}` = =={zero_cnt}==',
        'one_cnt = p': '紧接着这一段 1 的长度 `one_cnt = {p} − {start}` = =={one_cnt}==',
        'res = max': '可取后缀 k 个 0 和前缀 k 个 1，k 最大是 `min({zero_cnt}, {one_cnt})` = {min(zero_cnt, one_cnt)}；`res = max({B.res}, {min(zero_cnt, one_cnt)})` = =={res}==',
        'return res + res': '每个 k 对应长度 `2k`：`res + res` = =={ret}==',
    },
    cards=dict(
        one_liner='一段 0 加紧跟的一段 1，取较短的长度 k，平衡串长 2k',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制字符串，平衡子串：所有 0 在 1 之前，且 0 和 1 个数相等',
                 '求最长平衡子串的长度（空串也算，答案可为 0）',
                 '示例：`"01000111"` → `6`（即 `"000111"`）'],
        quote='对于一段连续的0和其后方紧接着的连续的1，就可以从这一段0中选取长度为k的后缀，从这一段1中选组长度为k的前缀，这样一来就组合成了一个长度为2k的平衡子串。',
        quote_src='—— yiduobo 题解原文',
        idea=['字符串由「连续 0」「连续 1」交错组成，每次分离出一对',
              '这一对里 k 最大是两段长度的较小值，整对贡献 `2k`',
              '`res` 只记 k 的最大值，最后返回 `res + res`'],
        summary=['时间 `O(n)`，空间 `O(1)`：指针 `p` 只往右走一遍',
                 '易错点：开头就是 1 时，0 段长度为 0，`min` 自然得 0',
                 '`res` 存的是 k 而不是长度，别忘了最后乘 2',
                 '原文为 Python 2 风格，无需改动，直接运行',
                 '对比灵神：灵神一次循环记 `pre/cur`，这里用两个内层 while 把两段分开数'],
    ),
)
