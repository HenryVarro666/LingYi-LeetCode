CONFIG = dict(
    num=2716, title='最小化字符串长度', difficulty='Easy', category='字符串',
    author='yiduobo', technique='集合去重',
    tags=[],
    code='''
class Solution(object):
    def minimizedStringLength(self, s):
        return len(set(s))
''',
    call='Solution().minimizedStringLength("dddaaa")',
    expect=2,
    views=[
        dict(type='string', var='s', label='s（颜色 = 同一种字母）', cell=90, h=220,
             color=lambda S, i, v: {'d': 'blue', 'a': 'pink'}.get(v)),
        dict(type='text', fn=lambda S: '`set(s)` 把重复字母合并，剩下 ==每种一个==', size=28, h=60),
        dict(type='set', var=lambda S: set(S['s']), label='set(s)', h=200),
    ],
    watch=[('len(set(s))', 'len(set(s))', 'green')],
    captions={
        'return len(set(s))': '`set(s) = {sorted(set(s))}`，不同字符共 `{len(set(s))}` 种 → 返回 ==`{ret}`==',
    },
    cards=dict(
        one_liner='重复的字符都能删到只剩一个，答案就是不同字符数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['选下标 `i`，删掉它左右两侧各一个最近的同字符，可重复任意次',
                 '求最小化后的字符串长度',
                 '示例：`"dddaaa"` → `2`'],
        quote='按照题目中的删除方式，可以将每种重复出现的字符删除到只剩下一个为止，因此最终答案就是字符串中不同字符的数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['每次操作只会删掉重复的字符，不会让一种字符彻底消失',
              '所以每种字符最后都留一个，长度就是字符种类数',
              '`set(s)` 正好去重，一行搞定'],
        before=[dict(heading='先看一次操作', lines=[
            '`"dddaaa"` 选下标 1 的 `d`：删掉左边的 `d` 和右边的 `d` → `"daaa"`',
            '再选下标 2 的 `a`：删掉左右各一个 `a` → `"da"`',
            '每次操作都是删掉==重复==的字符，所以每种字符至少留 1 个'])],
        after=[dict(heading='为什么能删到只剩一个', lines=[
            '某种字符出现 ≥ 2 次：选其中一个，必有同字符在左或右，可以继续删',
            '只剩 1 个时，左右都没有同字符，删不动了',
            '所以最终长度 = ==不同字符数==，与删除顺序无关'])],
        summary=['时间 `O(n)`，空间 `O(1)`（字符集固定为小写字母）',
                 '易错：答案不是 `len(s)` 减去操作次数，不用模拟删除',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
