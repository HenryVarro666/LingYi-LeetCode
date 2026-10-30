LET = 'abcdefghijklmnopqrstuvwxyz'


def _o(S):
    o = S.get('order')
    return o if isinstance(o, int) else None


def _txt(S):
    o = _o(S)
    if o is None:
        return '`f[i]`：以第 `i` 小的字母结尾的最长理想子序列长度'
    l, r = S.get('left'), S.get('right')
    if l is None or S.get('_line', 0) < 9:
        return f'当前字符 ==`{LET[o]}`==，order = {o}'
    return f'`{LET[o]}` 的上一个字符范围 ==[`{LET[l]}`, `{LET[r]}`]=='


CONFIG = dict(
    num=2370, title='最长理想子序列', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='按字母序号离散状态',
    tags=['灵神题单', '动态规划', '难度分 1835'],
    code='''
class Solution(object):
    def longestIdealString(self, s, k):

        f = [0] * 26

        for char in s:
            order = ord(char) - 97
            left = max(0, order - k)
            right = min(25, order + k)
            ma = 0
            for last_order in range(left, right + 1):
                ma = max(ma, f[last_order])
            
            f[order] = ma + 1
        
        return max(f)
''',
    call='Solution().longestIdealString("abcbd", 1)',
    expect=4,
    max_steps=80,
    views=[
        dict(type='string', var='s', label='s', h=130, cell=80),
        dict(type='text', fn=_txt, size=26, h=60),
        dict(type='array', var='f', label='f[i]：下标 0~25 = a~z，黄框 = [left, right]', h=240, cell=36,
             window=(lambda S: S.get('left') if S.get('_line', 0) >= 9 else None,
                     lambda S: S.get('right') if S.get('_line', 0) >= 9 else None),
             pointers={'order': 'pink'},
             dim=lambda S, i, v: False),
    ],
    watch=[('order', 'order', 'pink'), ('left', 'left', 'blue'), ('right', 'right', 'blue'),
           ('ma', 'ma', 'yellow'), ('最大长度', 'max(f)', 'green')],
    captions={
        'f = [0] * 26': '`f[0]` 是以 `a` 结尾的长度，`f[1]` 是以 `b` 结尾的……全部初始化为 0',
        'for char in s': '一趟遍历，依次处理每个字符',
        'order = ord': '`ord(char) - 97`：`{char}` 是第 `{order}` 小的字母',
        'left = max': '上一个字符最小可以是 `{LET[left]}`（不能小于 `a`）',
        'right = min': '上一个字符最大可以是 `{LET[right]}`（不能大于 `z`）',
        'ma = 0': '`ma` 记录范围 `[{left}, {right}]` 内最长的前驱，先设为 0',
        'for last_order': '枚举上一个字符 `last_order`',
        'ma = max': lambda S, B, r: f'`f[{S.last_order}] = {S.f[S.last_order]}`，`ma = max({B.ma}, {S.f[S.last_order]})` = =={S.ma}==',
        'f[order] = ma + 1': '`{char}` 接在最长的前驱后面：`f[{order}] = {ma} + 1` = =={f[order]}==',
        'return max(f)': '`f` 中的最大值就是答案 =={ret}==',
    },
    cards=dict(
        one_liner='要的是子序列不是子串，用「结尾字母」当离散状态',
        complexity='时间 `O(nk)`，空间 `O(1)`（长 26 的数组）',
        problem=['`s` 的子序列，相邻字母位次差 `≤ k`，称为理想字符串',
                 '返回最长理想字符串的长度，`a` 和 `z` 差 25',
                 '示例：`s = "acfgbd", k = 2` → `4`；本视频：`"abcbd", k = 1` → `4`'],
        quote='我在这里使用的是f[i]表示以第i小的字符结尾的最长理想子序列的长度，也就是f[0]表示以\'a\'结尾的最长子序列的长度，f[1]表示以\'b\'结尾……',
        quote_src='—— yiduobo 题解原文',
        idea=['题目找的是子序列，不是子串 → 用相对离散的状态：按==结尾字母==分 26 格',
              '遍历到某字符，算出它是第 `order` 小，上一个字符在 `[left, right]`',
              '手写循环取这段的最大值 `ma`，再 `f[order] = ma + 1`'],
        summary=['时间 `O(nk)`，空间 `O(26)`',
                 '`left`、`right` 要截断到 `[0, 25]`',
                 '原文是 Python 2 写法的类，在 Python 3 下无需修改，直接运行',
                 '对比灵神：灵神用切片 `max(f[...])` 一行取最大，yiduobo 手写循环'],
    ),
)
