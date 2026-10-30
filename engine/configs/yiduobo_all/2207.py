CONFIG = dict(
    num=2207, title='字符串中最多数目的子序列', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='贪心 · 拆成两部分计数',
    tags=[],
    code='''
class Solution(object):
    def maximumSubsequenceCount(self, text, pattern):

        cnt1 = cnt2 = 0
        res = 0
        for char in text:
            if char == pattern[1]:
                res += cnt1
                cnt2 += 1
            if char == pattern[0]:
                cnt1 += 1
        
        return res + max(cnt1, cnt2)
''',
    call='Solution().maximumSubsequenceCount("aabcb", "ab")',
    expect=6,
    views=[
        dict(type='string', var='text', h=150, pointers={},
             color=lambda S, i, v: ('green' if v == S['pattern'][0] else 'pink' if v == S['pattern'][1] else None) if 'pattern' in S else None),
        dict(type='text', h=70, fn=lambda S: (f"pattern = `{S['pattern']}`：绿 = `{S['pattern'][0]}`，粉 = `{S['pattern'][1]}`" if 'pattern' in S else '')),
    ],
    watch=[('cnt1', 'cnt1', 'green'), ('cnt2', 'cnt2', 'pink'), ('res', 'res', 'yellow'), 'char'],
    captions={
        'cnt1 = cnt2 = 0': '`cnt1`：`pattern[0]` 的个数；`cnt2`：`pattern[1]` 的个数',
        'res = 0': '`res` 先统计原串里 pattern 的个数',
        'for char in text': '看 `char = {char}`',
        'if char == pattern[1]': '`{char} == {pattern[1]}`？{"是：以它结尾的 pattern 个数 = 它前面 pattern[0] 的个数" if char == pattern[1] else "不是"}',
        'res += cnt1': '前面有 `{cnt1}` 个 `{pattern[0]}`：`res` {B.res} → =={res}==',
        'cnt2 += 1': '顺便统计 `pattern[1]` 个数：`cnt2` → {cnt2}',
        'if char == pattern[0]': '`{char} == {pattern[0]}`？{"是" if char == pattern[0] else "不是"}',
        'cnt1 += 1': '`cnt1` → {cnt1}（在 res 之后更新，pattern 两字符相同时也不会算错）',
        'return res': '原串有 `{res}` 个；插入带来 `max({cnt1}, {cnt2}) = {max(cnt1, cnt2)}` → =={res + max(cnt1, cnt2)}==',
    },
    cards=dict(
        one_liner='答案 = 原串里的 pattern 数 + 插入带来的 max(cnt1, cnt2)',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['可以在 `text` 里插入一个字符，只能是 `pattern[0]` 或 `pattern[1]`',
                 '求插入后 `pattern` 子序列最多有几个',
                 '本视频：`text = "aabcb"`，`pattern = "ab"` → `6`'],
        quote='最终答案可以分为两个部分，分别是由插入字符带来的等于pattern的子序列数目，再加上原始字符串text中等于pattern的子序列数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['插入 `pattern[0]`：放最前，右边每个 `pattern[1]` 都能配 → 多 `cnt2`',
              '插入 `pattern[1]`：放最后，左边每个 `pattern[0]` 都能配 → 多 `cnt1`',
              '原串部分：遇到 `pattern[1]`，加上前缀里 `pattern[0]` 的个数'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '两部分共用同一次遍历：数原串 pattern 的同时统计 cnt1、cnt2',
                 '易错：`res += cnt1` 要在 `cnt1 += 1` 之前，否则 pattern 两字符相同时会自己配自己'],
    ),
)
