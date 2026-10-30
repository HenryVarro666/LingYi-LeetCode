def _col(S, i, v):
    ma, mi = S.get('ma'), S.get('mi')
    if ma is None:
        return None
    if v == mi:
        return 'green'
    if v == ma:
        return 'orange'
    return None


def _txt(S):
    if 'ma' not in S:
        return '先排除无解和已有序，再找最大、最小字符'
    s = S['s']
    return f"最小 `mi={S['mi']}`，最大 `ma={S['ma']}`；首 `{s[0]}`，尾 `{s[-1]}`"


CONFIG = dict(
    num=3863, title='将一个字符串排序的最小操作次数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='分三类 · 特殊情形要 3 次',
    tags=['灵神题单', '思维题', '难度分 1860'],
    code='''
class Solution(object):
    def minOperations(self, s):
        
        if len(s) == 2 and s[0] > s[-1]:
            return -1
        
        flag = True
        for index in range(1, len(s)):
            if s[index] < s[index - 1]:
                flag = False
                break

        if flag:
            return 0
        
        ma, mi = s[0], s[0]
        for c in s[1:]:
            if c > ma:
                ma = c
            if c < mi:
                mi = c
        
        if s[0] == mi or s[-1] == ma:
            return 1
        
        if s[0] == ma and s[-1] == mi:
            for c in s[1: len(s) - 1]:
                if c == ma or c == mi:
                    return 2
            return 3
        
        return 2
''',
    call='Solution().minOperations("dbca")',
    expect=3,
    skip=['ma, mi = s[0]'],
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='string', var='s', label='s（绿 = 最小字符，橙 = 最大字符）', cell=110, color=_col,
             pointers={'index': 'blue'}, h=260),
    ],
    watch=[('flag', 'flag', 'cyan'), ('mi', 'mi', 'green'), ('ma', 'ma', 'orange')],
    captions={
        'if len(s) == 2 and': '`len(s) = {len(s)}`：长度不是 2，不会因为动不了而无解',
        'flag = True': '假设 `s` 已经有序，下面逐位验证',
        'if s[index] < s[index - 1]': lambda S, B, r: (f'`{S.s[S.index]} < {S.s[S.index-1]}`：==出现逆序==，不是有序的' if S.s[S.index] < S.s[S.index-1]
                                                       else f'`{S.s[S.index]} ≥ {S.s[S.index-1]}`：这一对没问题'),
        'flag = False': '`flag = False`：没法 0 次，跳出循环',
        'if flag': '`flag = {flag}`：有逆序，不是 0 次，继续',
        'if c > ma': '`{c}` 和当前最大 `{ma}` 比：{"更大 → 更新" if c > ma else "不更大"}',
        'ma = c': '最大字符更新为 `{ma}`',
        'if c < mi': '`{c}` 和当前最小 `{mi}` 比：{"更小 → 更新" if c < mi else "不更小"}',
        'mi = c': '最小字符更新为 `{mi}`',
        'if s[0] == mi or s[-1] == ma': '首位 `{s[0]}` 是最小？`{s[0] == mi}`；末位 `{s[-1]}` 是最大？`{s[-1] == ma}` → 都没归位，不是 1 次',
        'if s[0] == ma and s[-1] == mi': '首位是最大且末位是最小？`{s[0] == ma and s[-1] == mi}` → ==就是那个特殊情形==，看中间有没有最值',
        'for c in s[1:': '扫描中间的字符，看有没有最大或最小',
        'if c == ma or c == mi': '`{c}` 是最值吗？{"是 → 可先挪一次，答案 2" if c == ma or c == mi else "不是，继续看下一个"}',
        'return 3': '中间没有最大也没有最小：最值必须先挪进中间，再归位，再排剩余 → ==3 次==',
    },
    cards=dict(
        one_liner='首尾已归位一次，没归位两次，只有一种特殊情形三次',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['选一个==不是整个串==的子串按字母升序排序，求让 `s` 升序的最少次数',
                 '做不到返回 `-1`；示例：`"dog"` → `1`，`"gf"` → `-1`',
                 '本视频：`"dbca"` → `3`'],
        quote='若s[0]是最大的字符，s[-1]是最小的字符，且s[1: len(s) - 1]中没有s中最小以及最大的字符，那么答案就是3，否则答案就是2。',
        quote_src='—— yiduobo 题解原文',
        idea=['无解只有一种：长度为 2 且 `s[0] > s[-1]`，一次操作都做不了',
              '已有序 0 次；`s[0]` 最小或 `s[-1]` 最大，排另一段即可 1 次',
              '其余理想情况 2 次；特殊情形最值无法一步归位，先挪到中间，共 3 次'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：长为 2 时要判断 `s[0] > s[-1]`，否则已有序应返回 0',
                 '最后一行 `return 2` 覆盖「首不是最小、尾不是最大，且不是特殊情形」',
                 '原文为 Python 2 写法，本题代码无需改动即可在 Python 3 运行',
                 '对比灵神：灵神先判有序再判长度，用 `min/max` 内置函数'],
    ),
)
