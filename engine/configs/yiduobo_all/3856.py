CONFIG = dict(
    num=3856, title='移除尾部元音字母', difficulty='Easy', category='字符串',
    author='yiduobo', technique='转 list · 末尾 pop',
    code='''
class Solution(object):
    def trimTrailingVowels(self, s):
        
        vowel = set(['a', 'e', 'i', 'o', 'u'])
        res = list(s)
        while res and res[-1] in vowel:
            res.pop()
        
        return ''.join(res)
''',
    call='Solution().trimTrailingVowels("beautifulidea")',
    expect='beautifulid',
    views=[
        dict(type='set', var='vowel', h=130, fmt=lambda x: x),
        dict(type='array', var='res', h=260, cell=60,
             color=lambda S, i, v: 'blue' if i == len(S['res']) - 1 else None),
    ],
    watch=['res'],
    captions={
        'vowel = set': '元音集合 `vowel`，用 set 判断成员是 `O(1)`',
        'res = list(s)': '字符串不能改，转成 list `res`，方便从末尾 pop',
        'while res and': lambda S, B, r: (f"`res` 不空，末尾 `'{S.res[-1]}'` 是元音 → 删掉" if S.res and S.res[-1] in S.vowel
                                         else (f"末尾 `'{S.res[-1]}'` 不是元音 → 停止" if S.res else '`res` 已空 → 停止')),
        'res.pop()': '删掉末尾元音，剩下 `{len(res)}` 个字符',
        "return ''.join": '拼回字符串 `"{\'\'.join(res)}"`',
    },
    cards=dict(
        one_liner='末尾是元音就 pop，直到不是为止',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['去掉字符串 `s` 末尾的所有元音字母（`a e i o u`）',
                 '示例：`"idea"` → `"id"`，`"aeiou"` → `""`',
                 '本视频：`"beautifulidea"` → `"beautifulid"`'],
        quote='将s转化为list，然后不断检测其最后一个元素是否为元音字母，如果是，则将其pop掉。重复此过程直到list为空，或者最后一个元素不是元音字母为止。',
        quote_src='—— yiduobo 题解原文',
        idea=['`list(s)` 变成可修改的列表', '循环条件两个：列表非空、末尾是元音；任一不满足就停',
              '最后 `join` 回字符串'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`while` 里先判 `res` 非空，再看 `res[-1]`，顺序不能反（否则空列表越界）',
                 '原文代码在 Python 3 下可直接运行，未作改动'],
    ),
)
