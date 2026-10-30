def _top(S):
    if 'max_one' not in S:
        return ''
    return f"最长连续 `1`：==`{S['max_one']}`==　　最长连续 `0`：==`{S['max_zero']}`=="


def _col(S, i, v):
    if 'last' in S and 'index' in S and S['last'] <= i < S['index']:
        return 'green' if v == '1' else 'orange'
    return None


CONFIG = dict(
    num=1869, title='哪种连续子字符串更长', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='一趟遍历 · last 记段起点',
    tags=['灵神题单·滑动窗口与双指针', '难度分 1205'],
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
    call='Solution().checkZeroOnes("110100010")',
    expect=False,
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='string', var='s', label='s（last 是当前这段的开头，index 是正在看的字符）', cell=84,
             pointers={'last': 'blue', 'index': 'pink'}, color=_col),
        dict(type='text', fn=lambda S: (f"刚结束的上一段：`{S['s'][S['index'] - 1]}` × {S['index'] - S['last']}"
                                         if 'index' in S and 'last' in S and S['index'] > 0 and S['index'] < len(S['s'])
                                         and S['s'][S['index']] != S['s'][S['index'] - 1] else ''), size=26),
    ],
    watch=[('index', 'index', 'pink'), ('last', 'last', 'blue'), ('max_one', 'max_one', 'green'), ('max_zero', 'max_zero', 'orange')],
    skip=['res = 0'],
    captions={
        9: '第一个字符：第一段从下标 `0` 开始，`last = 0`',
        4: '`last` 记录当前连续段的==开头==下标',
        'max_zero = max_one = 0': '`max_zero`、`max_one` 分别是最长连续 0、连续 1 的长度',
        'for index, char in enumerate(s)': lambda S, B, r: (f'看 `s[{S.index}] = {S.char!r}`' if 'char' not in B or B.get('index') != S.index
                                                              else '遍历结束，但最后一段还没统计'),
        'if index == 0': lambda S, B, r: ('`index == 0`：第一个字符，没有「前一个」可比' if S.index == 0 else '`index != 0`，可以和前一个字符比较'),
        'elif char != s[index - 1]': lambda S, B, r: (
            f'`{S.char!r}` ≠ 前一个 `{S.s[S.index - 1]!r}` → 上一段在 `{S.index - 1}` 结束，可以结算了'
            if S.char != S.s[S.index - 1] else f'`{S.char!r}` == 前一个字符 → 还在同一段，什么都不用做'),
        "if char == '1'": lambda S, B, r: (
            f'当前是 `1`，说明刚结束的那段是 ==0==，长度 `{S.index - S.last}`' if S.char == '1'
            else f'当前是 `0`，说明刚结束的那段是 ==1==，长度 `{S.index - S.last}`'),
        'max_zero = max(max_zero, index - last)': '`max_zero = max({B.max_zero}, {index - last}) = {max_zero}`',
        'max_one = max(max_one, index - last)': '`max_one = max({B.max_one}, {index - last}) = {max_one}`',
        'last = index': '新的一段从 `index = {index}` 开始：`last` → {last}',
        "if s[-1] == '1'": lambda S, B, r: (
            f'循环结束，最后一段没人结算：它是 `{S.s[-1]}`，长度 `len(s) - last = {len(S.s) - S.last}`'),
        'max_one = max(max_one, len(s) - last)': '`max_one = max({B.max_one}, {len(s) - last}) = {max_one}`（补上最后一段）',
        'max_zero = max(max_zero, len(s) - last)': '`max_zero = max({B.max_zero}, {len(s) - last}) = {max_zero}`（补上最后一段）',
        'return max_one > max_zero': '`max_one = {max_one}`，`max_zero = {max_zero}`：1 要==严格更长== → `{max_one > max_zero}`',
    },
    cards=dict(
        one_liner='一趟遍历，遇到字符变化就结算上一段',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制字符串 `s`，比较最长连续 1 与最长连续 0 的长度',
                 '1 的更长（严格）返回 `true`，否则 `false`',
                 '示例：`"110100010"` → 1 最长 2，0 最长 3 → `false`'],
        quote='需要注意在遍历完成后，最后一个连续子字符串由于没有遇到不同的字符，因此其的长度是没有被计算过的，需要单独拿出来计算。',
        quote_src='—— yiduobo 题解原文',
        idea=['用 `last` 记当前连续段的开头；字符和前一个不同，说明上一段结束了',
              '上一段的长度是 `index - last`，上一段是什么字符看当前字符取反',
              '最后一段后面没有「不同的字符」，循环后要==补算一次=='],
        result='最长 1 是 2，最长 0 是 3 → `2 > 3` 不成立 → `False` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：忘了循环后补算最后一段，`"111"` 这种全是同一字符的串会得到 0',
                 '`if char == \'1\'` 更新的是 `max_zero`：因为结束的是==上一段==',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，其余未改',
                 '对比灵神：灵神用内层 while 一口气走完一段；yiduobo 逐字符比较前一个字符'],
    ),
)
