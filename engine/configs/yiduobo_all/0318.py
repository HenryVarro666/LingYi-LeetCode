def _letters(m):
    return ''.join(chr(97 + b) for b in range(26) if m >> b & 1)


def _info(S):
    if 'len_list' not in S or 'res' not in S or 'j' not in S:
        return ''
    i, j = S['i'], S['j']
    a, b = S['len_list'][i][0], S['len_list'][j][0]
    return (f"mask[{i}] = `{_letters(a)}`，mask[{j}] = `{_letters(b)}`，`&` = ==`{_letters(a & b) or '空'}`==")


CONFIG = dict(
    num=318, title='最大单词长度乘积', difficulty='Medium', category='位运算',
    author='yiduobo', technique='位掩码 + 两重循环',
    tags=[],
    code='''
class Solution(object):
    def maxProduct(self, words):

        len_list = []
        for word in words:
            tmp = 0
            for char in word:
                tmp |= 1 << (ord(char) - 97)
            len_list.append([tmp, len(word)])

        res = 0
        for i in range(len(len_list) - 1):
            for j in range(i + 1, len(len_list)):
                if len_list[i][0] & len_list[j][0] == 0 and len_list[i][1] * len_list[j][1] > res:
                    res = len_list[i][1] * len_list[j][1]

        return res
''',
    call='Solution().maxProduct(["abcw", "baz", "foo", "xtfn"])',
    expect=16,
    views=[
        dict(type='array', var='words', label='words', cell=104, h=150,
             color=lambda S, k, v: 'blue' if S.get('i') == k and 'j' in S else ('pink' if S.get('j') == k else None)),
        dict(type='array', var=lambda S: [_letters(m) for m, l in S['len_list']] if 'len_list' in S else None,
             label='len_list：掩码里的字母（长度见 words）', pointers={'i': 'blue', 'j': 'pink'}, cell=104, h=250),
        dict(type='text', h=90, size=28, fn=_info),
        dict(type='text', h=70, size=30, fn=lambda S: (f"当前最大乘积 `res = {S['res']}`" if 'res' in S else '')),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('tmp', 'tmp', 'cyan'), ('res', 'res', 'green')],
    skip=['len_list = []', 'for char in word'],
    max_steps=100,
    captions={
        'for word in words': '处理单词 `{word}`：只关心出现过哪些字母',
        'tmp = 0': '`tmp = 0`：26 位二进制，从没有任何字母开始',
        'for char in word': '字母 `{char}`',
        'tmp |= 1 << (ord(char) - 97)': '`{char}` 是第 `{ord(char) - 97}` 个字母 → 把 `tmp` 的第 {ord(char) - 97} 位置 1，`tmp` = {tmp}',
        'len_list.append': '`{word}` 的掩码 `{tmp}`（字母 `{"".join(chr(97 + b) for b in range(26) if tmp >> b & 1)}`），长度 `{len(word)}`',
        'res = 0': '`res` 记录最大乘积',
        'for i in range': '第一个单词 `words[{i}]` = `{words[i]}`',
        'for j in range': '第二个单词 `words[{j}]` = `{words[j]}`（只配后面的，避免重复）',
        'if len_list[i][0] & len_list[j][0] == 0': lambda S, B, r: (
            f"掩码相与 = {S.len_list[S.i][0] & S.len_list[S.j][0]}"
            + ("，==没有公共字母==，" + (f"乘积 `{S.len_list[S.i][1]} × {S.len_list[S.j][1]}` = {S.len_list[S.i][1] * S.len_list[S.j][1]} "
               + (f"> res {S.res} → 更新" if S.len_list[S.i][1] * S.len_list[S.j][1] > S.res else f"≤ res {S.res} → 不更新"))
               if S.len_list[S.i][0] & S.len_list[S.j][0] == 0 else "，有公共字母 → 这对不行")),
        'res = len_list[i][1]': '更新 `res = {len_list[i][1]} × {len_list[j][1]}` = =={res}==',
        'return res': '最大乘积 `{res}`',
    },
    cards=dict(
        one_liner='用一个整数的 26 个二进制位表示单词里有哪些字母',
        complexity='时间 `O(L + n²)`（L 为总字符数），空间 `O(n)`',
        problem=['找两个==没有公共字母==的单词，使长度乘积最大，没有就返回 0',
                 '单词只含小写字母',
                 '示例：`["abcw","baz","foo","xtfn"]` → `abcw` × `xtfn` = `16`'],
        quote='对于一个字符串，我们实际上只关心某个字符是否出现过，而不关心其出现的次数，又由于题目保证了所有的字符都是小写的，因此可以利用一个长度为26的二进制串来表示每个单词中字母出现的情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['`1 << (ord(char) - 97)`：第 k 个字母对应第 k 位',
              '两个掩码按位与 `& == 0` ⇔ 没有公共字母',
              '预处理一次，再两重循环 `i < j` 枚举所有单词对'],
        summary=['时间 `O(L + n²)`，空间 `O(n)`',
                 '2^26 小于 2^31，一个整数就够存',
                 'Python 里 `&` 优先级高于 `==`，所以 `a & b == 0` 不用加括号（C 语言则要）',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码无需其他改动'],
    ),
)
