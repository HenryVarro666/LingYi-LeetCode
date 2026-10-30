def _seg(S):
    """当前这一段 [last, index-1]"""
    if 'index' not in S:
        return (0, -1)
    return (S['last'], S['index'] - 1) if S['index'] > S['last'] else (0, -1)


CONFIG = dict(
    num=1869, title='哪种连续子字符串更长', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='一趟遍历 · 记录段首 last',
    tags=['分组循环', '难度分 1205'],
    code='''
class Solution(object):
    def checkZeroOnes(self, s):

        last = 0
        max_zero = max_one = 0
        res = 0
        for index, char in enumerate(s):
            if index == 0:
                last = 0
            elif char != s[index - 1]:
                if char == '1':
                    max_zero = max(max_zero, index - last)
                else:
                    max_one = max(max_one, index - last)
                last = index
        
        if s[-1] == '1':
            max_one = max(max_one, len(s) - last)
        else:
            max_zero = max(max_zero, len(s) - last)
        
        return max_one > max_zero
''',
    call="Solution().checkZeroOnes('1100011')",
    expect=False,
    views=[
        dict(type='string', var='s', label='s（箭头 index = 当前字符，青框 = 上一段 [last, index)，绿色箭头 last = 段首）', h=210,
             pointers={'index': 'blue', 'last': 'green'},
             window=(lambda S: _seg(S)[0], lambda S: _seg(S)[1])),
        dict(type='text', fn=lambda S: f"最长连续 `0` = =={S.get('max_zero')}==，最长连续 `1` = =={S.get('max_one')}==" if 'max_zero' in S else ''),
    ],
    watch=[('index', 'index', 'blue'), ('last', 'last', 'green'), ('max_zero', 'max_zero', 'orange'), ('max_one', 'max_one', 'pink')],
    captions={
        'max_zero = max_one': '`max_zero`、`max_one` 分别记录最长连续 0 / 1',
        'for index, char': '看第 `{index}` 个字符 `char = {char}`',
        'if index == 0': lambda S, B, r: '第一个字符前面没有字符，它自己开一段：`last = 0`' if S.index == 0 else '不是第一个字符，看下一个分支',
        4: '`last` 记录当前连续段的开头位置，先设为 0',
        9: '第一个字符前面没有字符，它自己开一段：`last = 0`',
        'elif char != s[index - 1]': lambda S, B, r: (f"`'{S.char}' != '{S.s[S.index-1]}'` → ==上一段结束了==，长度是 `index - last = {S.index - S.last}`"
                                                      if S.char != S.s[S.index - 1] else f"`'{S.char}' == '{S.s[S.index-1]}'` → 还在同一段，什么也不用做"),
        "if char == '1'": lambda S, B, r: (f"当前是 `1` → 刚结束的那段是 ==0 段=="if S.char == '1' else "当前是 `0` → 刚结束的那段是 ==1 段=="),
        'max_zero = max(max_zero, index - last)': '用上一段（0）的长度更新：`max_zero = max({B.max_zero}, {index - last}) = {max_zero}`',
        'max_one = max(max_one, index - last)': '用上一段（1）的长度更新：`max_one = max({B.max_one}, {index - last}) = {max_one}`',
        'last = index': '新的一段从 `index` 开始：`last = {last}`',
        'if s[-1] == ': '==最后一段没遇到不同字符，还没算过==：看它是 `{s[-1]}` 段',
        'max_one = max(max_one, len(s) - last)': '最后一段（1）长 `len(s) - last = {len(s) - last}` → `max_one = {max_one}`',
        'max_zero = max(max_zero, len(s) - last)': '最后一段（0）长 `len(s) - last = {len(s) - last}` → `max_zero = {max_zero}`',
        'return': lambda S, B, r: f'`max_one = {S.max_one}`，`max_zero = {S.max_zero}`：1 的最长段 ==严格大于== 0 的才为真 → {r}',
    },
    cards=dict(
        one_liner='用 last 记段首，字符一变就结算上一段，最后别忘收尾',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制字符串 `s`，比较「最长连续 1」与「最长连续 0」的长度',
                 '1 的最长段==严格长于== 0 的最长段，返回 `true`，否则 `false`',
                 '示例：`"110100010"` → `false`（1 最长 2，0 最长 3）；本视频：`"1100011"` → `false`'],
        quote='使用一个变量last记录当前连续子字符串的开端位置。对于当前字符，若其不等于前一个字符，说明上一段连续子字符串已经结束了，因此可以使用当前下标index与last，以及上一个字符是0还是1来更新最长连续0的长度或者最长连续1的长度。',
        quote_src='—— yiduobo 题解原文',
        idea=['`last` 是当前段的开头，字符变化时上一段长度 = `index - last`',
              '当前字符是 `1`，说明刚结束的是 0 段，反之亦然',
              '遍历结束时最后一段没有被结算，要单独算：`len(s) - last`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：最后一段必须在循环外单独结算，否则 `"1100011"` 末尾的 11 会丢',
                 '判断当前字符时别搞反：当前是 1，结算的是上一段 0',
                 '返回 `max_one > max_zero`，相等时为 false',
                 '原文变量 `res` 没有用到，保留原样'],
    ),
)
