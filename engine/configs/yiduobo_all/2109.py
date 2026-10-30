CONFIG = dict(
    num=2109, title='向字符串添加空格', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='指针 p 匹配 spaces',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1315'],
    code='''
class Solution(object):
    def addSpaces(self, s, spaces):

        res = []
        p = 0
        for index in range(len(s)):
            if p < len(spaces) and index == spaces[p]:
                res.append(' ')
                p += 1
            res.append(s[index])

        return ''.join(res)
''',
    call='Solution().addSpaces("LeetcodeHelpsMe", [8,13])',
    expect='Leetcode Helps Me',
    views=[
        dict(type='string', var='s', pointers={'index': 'blue'}, label='s', h=240, cell=60),
        dict(type='array', var='spaces', pointers={'p': 'pink'}, label='spaces', h=200),
        dict(type='text', fn=lambda S: ("res = `" + ''.join(S['res']).replace(' ', '␣') + "`" if 'res' in S else ''), size=34),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'pink')],
    captions={
        'res = []': '`res` 数组记录最终答案',
        'p = 0': '`p`：当前匹配到 `spaces` 里的第几个元素',
        'for index': '遍历 `s`：`index = {index}`',
        'if p < len(spaces)': lambda S, B, r: (f'`index = {S.index}` 等于 `spaces[{S.p}] = {S.spaces[S.p]}` → ==这里要加空格==' if (S.p < len(S.spaces) and S.index == S.spaces[S.p])
            else (f'`spaces[{S.p}] = {S.spaces[S.p]}`，和 `index = {S.index}` 不同 → 不加空格' if S.p < len(S.spaces) else '`p` 已走完 `spaces` → 不再加空格')),
        "res.append(' ')": '往 `res` 里加一个空格',
        'p += 1': '匹配下一个位置：`p` → {p}（只增不减，所以均摊 `O(1)`）',
        'res.append(s[index])': '加入字符 `{s[index]}`：`res` = `{"".join(res)}`',
        'return': '拼接得到 `{ret!r}`',
    },
    cards=dict(
        one_liner='spaces 是有序的，用指针 p 记录匹配到哪个，p 只增不减',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['在 `s` 的下标 `spaces[k]` 处的字符之前各插入一个空格',
                 '本视频：`"LeetcodeHelpsMe"`，`[8,13]` → `"Leetcode Helps Me"`'],
        quote='逐个把当前遍历到的字符添加到答案数组当中，若当前下标出现在space中，则在答案数组中添加一个空格。',
        quote_src='—— yiduobo 题解原文',
        idea=['判断下标是否在 `spaces` 中：可以转成哈希表，也可以用单调性',
              '`spaces` 有序，用指针 `p` 记录匹配到哪个元素，`p` 只会变大',
              '均摊 `O(1)` 判断；另一种写法是直接切片再用空格连接'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`p < len(spaces)` 先判断，避免越界',
                 '空格在字符之前加入',
                 '对比灵神：灵神同样双指针，另给了按空格位置切片的写法'],
    ),
)
