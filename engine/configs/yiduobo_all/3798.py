CONFIG = dict(
    num=3798, title='最大的偶数', difficulty='Easy', category='字符串',
    author='yiduobo', technique='从后往前找最后一个 2',
    tags=[],
    code='''
class Solution(object):
    def largestEven(self, s):
        
        p = len(s) - 1
        while p >= 0 and s[p] == '1':
            p -= 1
        return s[:p + 1]
''',
    call="Solution().largestEven('1221211')",
    expect='12212',
    views=[
        dict(type='text', size=34, fn=lambda S: (f"`p = {S['p']}`：`s[{S['p']}] = {S['s'][S['p']]}`" if 'p' in S and S['p'] >= 0 else '`p = -1`：没有 2') if 'p' in S else ''),
        dict(type='string', var='s', h=300, cell=96, pointers={'p': 'pink'},
             color=lambda S, i, v: ('red' if i > S['p'] else 'green') if 'p' in S else None,
             label='s（红 = 被删掉的尾部 1）'),
        dict(type='text', size=34, fn=lambda S: f"答案 = `s[:{S['p'] + 1}]` = `{S['s'][:S['p'] + 1]}`" if 'p' in S else ''),
    ],
    watch=[('s', 's'), ('p', 'p', 'pink')],
    captions={
        'p = len(s) - 1': '`p` 从最后一个下标 `{p}` 开始往前找',
        'while p >= 0': lambda S, B, r: (f'`p = {S.p}`，`s[{S.p}] = 1` 是奇数结尾 → 继续删' if S.p >= 0 and S.s[S.p] == '1'
                                         else (f'`s[{S.p}] = 2`，找到最后一个 `2`，停下' if S.p >= 0 else '`p < 0`：全是 `1`，没有偶数')),
        'p -= 1': '末尾的 `1` 不能要，删掉它：`p` → {p}',
        'return s[:p + 1]': '保留 `s[:{p + 1}]` = `{s[:p + 1]}`；以 `2` 结尾且尽量长，所以最大',
    },
    cards=dict(
        after=[dict(heading='为什么只删尾部', lines=['中间的 `1` 不用删：删了位数变少，数变小', '只有尾部的 `1` 挡住了「以 2 结尾」', '所以从后往前扫到第一个 `2` 就够了'])],
        one_liner='结尾必须是 2，又要尽量少删：删掉末尾连续的 1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s` 只含 `1` 和 `2`，可以删字符，剩余顺序不变',
                 '求能得到的最大偶数；不存在则返回空串',
                 '本视频：`1221211` → `12212`'],
        quote='为了使得最终结果为偶数，必须保证最后一个字符为\'2\'。另一方面，为了使得结果最大，因此应该尽量少删字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['两个条件合起来：结果以 `2` 结尾 + 删得最少',
              '所以只删末尾连续的 `1`，找到最后一个 `2` 的下标 `p`',
              '答案就是 `s[:p + 1]`；没有 `2` 时 `p = -1`，得到空串'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`while` 里先判 `p >= 0` 再访问 `s[p]`，避免越界',
                 '原文为 Python 2 风格 `class Solution(object)`，代码无需改动',
                 '对比灵神：灵神用一行 `rstrip(\'1\')`，这里手写了同样的从后往前扫描'],
    ),
)
