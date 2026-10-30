CONFIG = dict(
    num=3271, title='哈希分割字符串', difficulty='Medium', category='字符串',
    author='yiduobo', technique='模拟 · 步长遍历起点',
    tags=[],
    code='''
class Solution(object):
    def stringHash(self, s, k):

        res = []
        for index in range(0, len(s), k):
            h = sum([ord(c) - 97 for c in s[index : index + k]]) % 26
            res.append(chr(h + 97))
        
        return ''.join(res)
''',
    call='Solution().stringHash("abcxyzmno", 3)',
    expect='dun',
    views=[
        dict(type='text', fn=lambda S: (f"子串 `s[{S['index']}:{S['index']+S['k']}]` = =={S['s'][S['index']:S['index']+S['k']]}==" + (f"，`h = {S['h']}`" if 'h' in S and S['_line'] >= 7 else '')) if 'index' in S else '', size=28),
        dict(type='string', var='s', label='s（以 k 为步长取子串）', cell=84,
             color=lambda S, idx, v: ('blue' if S['index'] <= idx < S['index'] + S['k'] else None) if 'index' in S else None,
             dim=lambda S, idx, v: 'index' in S and idx < S['index']),
        dict(type='array', var='res', label='res', cell=84),
    ],
    watch=[('index', 'index', 'blue'), ('k', 'k'), ('h', 'h', 'yellow'), ('res', 'res', 'green')],
    captions={
        'for index': lambda S, B, ret: ('起点已超出 `len(s)`，循环结束' if 'index' in B and S.index == B.index else f'以 `k = {S.k}` 为步长，这块的起点是 `index = {S.index}`'),
        'h = sum': '每个字符的顺序 = ASCII 码 − 97（`a` 的码），累加后对 26 取模：`h = {h}`',
        'res.append': '字母表第 `h` 个字符的码 = `h + 97`：`chr({h} + 97)` = ==`{chr(h + 97)}`==',
        'return': '所有子串处理完，拼起来得到 `"{ret}"`',
    },
    cards=dict(
        one_liner='先以 k 为步长找起点，再累加 k 个字符的顺序',
        complexity='时间 `O(n)`，空间 `O(n // k)`',
        problem=['`s` 仅含小写字母，长度 `n` 是 `k` 的倍数',
                 '分成 `n // k` 个长 `k` 的子串，逐个求和取模 26，转成字母',
                 '示例：`s = "mxz"`，`k = 3` → `"i"`'],
        quote='直接按照题目要求模拟即可。先以k为步长遍历所有子串的起点，然后对于每个起点，往后遍历k个字符，计算这些字符在字母表中的顺序之和。',
        quote_src='—— yiduobo 题解',
        idea=['字符顺序 = 字符 ASCII 码 − `a` 的 ASCII 码（97）',
              '字母表第 `h` 个字符的码 = `h + 97`，用 `chr` 转回来',
              '子串起点用 `range(0, len(s), k)` 一次枚举完'],
        summary=['时间 `O(n)`，结果串长 `n // k`',
                 '易错：求和后要对 26 取模，再加 97 转字符',
                 '切片 `s[index : index + k]` 刚好取 `k` 个字符'],
    ),
)
