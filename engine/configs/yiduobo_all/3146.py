CONFIG = dict(
    num=3146, title='两个字符串的排列差', difficulty='Easy', category='字符串',
    author='yiduobo', technique='哈希表 · 两趟遍历',
    code='''
class Solution(object):
    def findPermutationDifference(self, s, t):

        pos = {}
        for index, char in enumerate(s):
            pos[char] = index
        
        res = 0
        for index, char in enumerate(t):
            res += abs(index - pos[char])
        return res
''',
    call="Solution().findPermutationDifference('abcde', 'edbac')",
    expect=12,
    views=[
        dict(type='string', var='s', label='s', cell=96, h=130, pointers={'index': 'blue'}, dim=lambda S, i, v: S['_line'] >= 8),
        dict(type='string', var='t', label='t', cell=96, h=130, pointers={'index': 'blue'}, dim=lambda S, i, v: S['_line'] < 8),
        dict(type='map', var='pos', label='pos（字符 → 下标）', fmt=lambda k, v: f"'{k}': {v}", h=150, font=32),
        dict(type='text', h=70, size=30, fn=lambda S: f"累计差 `res = {S['res']}`" if 'res' in S else ''),
    ],
    watch=[('index', 'index', 'blue'), ('char', 'char'), ('res', 'res', 'green')],
    captions={
        'pos = {}': '`pos` 用来记 `s` 中每个字符出现的下标',
        'pos[char] = index': '`pos[{char!r}] = {index}`：字符 {char!r} 在 `s` 的下标是 {index}',
        'res = 0': '`res` 累加答案，从 0 开始',
        'res += abs': '`{char!r}` 在 `t` 下标 {index}，在 `s` 下标 {pos[char]}：`|{index} − {pos[char]}| = {abs(index - pos[char])}`，`res` → =={res}==',
        'return res': '`t` 遍历完，排列差为 ==`{res}`==',
    },
    cards=dict(
        one_liner='第一趟记 s 的下标，第二趟查表算差',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`s`、`t` 内字符各不相同，`t` 是 `s` 的一个排列',
                 '求每个字符在两串下标之差的绝对值之和',
                 '示例：`s = "abcde", t = "edbac"` → `12`'],
        quote='先对s进行一趟遍历，使用哈希表记录其中每个字符出现的下标，接下来再对t进行一趟遍历，计算当前字符在哈希表中对应的值与当前下标之差的绝对值，累加到答案中即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`s` 里字符不重复，哈希表能唯一记住每个字符的下标',
              '遍历 `t`：当前下标减去表里的值，取绝对值，累加进 `res`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：别忘了取绝对值 `abs`',
                 '对比灵神：灵神把两趟写成推导式一行；yiduobo 用两个显式循环，步骤更直观',
                 '原文已是 Python 3 可运行写法，无需修改'],
    ),
)
