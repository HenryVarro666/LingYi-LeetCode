def _top(S):
    if 'left' not in S:
        return ''
    if 'right' in S:
        return f'替换区间 `s[{S["left"]}:{S["right"]}]`（左闭右开）：中间这段每个字符减一'
    return f'最高位的非 a 字符在 `left = {S["left"]}`，从它开始替换'


def _win(S):
    if 'right' in S and S['right'] > S['left']:
        return ('left', 'right-1')
    return None


CONFIG = dict(
    num=2734, title='执行子串操作后的字典序最小字符串', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='找最高位非 a · 区间替换',
    tags=['灵神题单', '难度分 1405'],
    code='''
class Solution(object):
    def smallestString(self, s):
        left = 0
        while left < len(s) and s[left] == 'a':
            left += 1

        if left == len(s):
            return s[:len(s) - 1] + 'z'

        right = left + 1
        while right < len(s) and s[right] != 'a':
            right += 1

        return s[:left] + ''.join([chr(ord(ch) - 1) for ch in s[left : right]]) + s[right:]
''',
    call='''Solution().smallestString("abcab")
Solution().smallestString("aa")''',
    expect='az',
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='s', label='s（蓝 = left，粉 = right；蓝框 = 被替换的区间）', cell=84,
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right - 1'),
             color=lambda S, i, v: 'green' if 'right' in S and S['left'] <= i < S['right'] else None),
        dict(type='text', fn=lambda S: f'`left = {S["left"]}`，`right = {S["right"]}`：替换 `{S["s"][S["left"]:S["right"]]}` → `{"".join(chr(ord(c) - 1) for c in S["s"][S["left"]:S["right"]])}`' if 'right' in S else '', size=26),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink')],
    captions={
        'left = 0': '`left` 从最高位出发，找第一个非 a 的字符',
        "while left < len(s) and s[left] == 'a'": lambda S, B, r: (
            f"`left = {S.left} == len(s)`：整串都是 a" if S.left >= len(S.s)
            else (f"`s[{S.left}] = 'a'` → 把 a 减一是负收益，跳过" if S.s[S.left] == 'a'
                  else f"`s[{S.left}] = '{S.s[S.left]}'` 不是 a → 找到最高位的非 a 字符")),
        'left += 1': '`left` → {left}',
        'if left == len(s)': lambda S, B, r: ('`left == len(s)`：整个字符串都是 a，但必须操作一次' if S.left == len(S.s)
                                             else f'`left = {S.left} < len(s)`：存在非 a 字符，走一般情况'),
        'return s[:len(s) - 1]': '全是 a：替换最低位的 a 损失最小 → `{ret}`',
        'right = left + 1': '`right` 从 `left` 的下一位开始，找替换区间的右端',
        'while right < len(s)': lambda S, B, r: (f"`s[{S.right}] = '{S.s[S.right]}'` 不是 a → 区间继续延伸" if S.right < len(S.s) and S.s[S.right] != 'a'
                                                else (f"`s[{S.right}] = 'a'` → 遇到 a，区间到此为止" if S.right < len(S.s)
                                                      else '到达字符串末尾，区间到此为止')),
        'right += 1': '`right` → {right}',
        'return s[:left]': '`s[:{left}]` 不动 + 中间 `s[{left}:{right}]` 各减一 + `s[{right}:]` 不动 → `{ret}`',
    },
    cards=dict(
        one_liner='找最高位非 a 的字符，往后替换到下一个 a 之前',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['选 `s` 的任一非空子串，每个字符换成字母表前一个字符（`a` 换成 `z`），恰好操作一次',
                 '求操作后字典序最小的字符串',
                 '本视频依次跑：`"abcab"` → `"aabab"`；`"aa"` → `"az"`'],
        quote='题目中的替换操作，对于除a之外的字符都是正收益，而替换a则是负收益。为了使得替换后的字符串字典序最小，那么就应该找到最高位的非a字符，从这个字符开始进行替换。',
        quote_src='—— yiduobo 题解原文',
        idea=['`left` 跳过前导的 a，停在最高位非 a 字符',
              '`right` 从 `left + 1` 往后走，直到末尾或下一个 a',
              '区间 `s[left:right]` 逐字符减一，前后两段原样拼接'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '特殊情况：整个串都是 a，替换最低位（最后一个）a 为 z',
                 '区间是左闭右开：`s[left : right]`，`right` 停在 a 或末尾',
                 '原文代码已是 Python 3 可运行写法，未做修改',
                 '对比灵神：灵神用列表原地改；这里用双指针找区间再切片拼接'],
    ),
)
