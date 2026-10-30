def _mirror(S):
    if 'index' not in S:
        return ''
    n = len(S['s'])
    i = S['index']
    return f'中心位置 `(n-1)/2 = {(n - 1) / 2:g}`：`index = {i}` 的对称位置是 `len(s) - index - 1 = {n - i - 1}`'


ORIG = ["H", "a", "n", "n", "a", "h", "!", "?"]  # 本例每对对称字符都不同，变了就说明交换过


def _color(S, i, v):
    return 'green' if v != ORIG[i] else None


def _for(S, B, ret):
    n = len(S['s'])
    if B.get('index') == S['index']:
        return f'`range({n} // 2)` 遍历完：左半边每个位置都和对称位置换过了 → ==反转完成=='
    return f'`index = {S["index"]}`：只需要遍历==左半边== `0 .. {n // 2 - 1}`，右半边由对称位置负责'


CONFIG = dict(
    num=344, title='反转字符串', difficulty='Easy', category='双指针',
    author='yiduobo', technique='按中心位置交换两侧',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def reverseString(self, s):
        for index in range(len(s) // 2):
            s[index], s[len(s) - index - 1] = s[len(s) - index - 1], s[index]
''',
    call='''s = ["H", "a", "n", "n", "a", "h", "!", "?"]
Solution().reverseString(s)
s''',
    expect=["?", "!", "h", "a", "n", "n", "a", "H"],
    views=[
        dict(type='text', fn=_mirror, h=60),
        dict(type='string', var='s', label='s（绿 = 已和对称位置交换过）', cell=96, h=300,
             pointers={'index': 'blue', 'len(s) - index - 1': 'pink'},
             pointer_labels={'len(s) - index - 1': 'len(s)-index-1'},
             color=_color),
    ],
    watch=[('index', 'index', 'blue'), ('对称位置', 'len(s) - index - 1', 'pink'), ('len(s) // 2', 'len(s) // 2')],
    captions={
        'for index in range': _for,
        's[index], s[len(s)': '交换 `s[{index}]` 和对称位置 `s[{len(s) - index - 1}]`：`{B.s[index]}` ↔ `{B.s[len(s) - index - 1]}`',
    },
    cards=dict(
        one_liner='按中心位置，把两侧对称的字符一对一对交换',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['输入字符串以字符数组 `s` 给出，把它反转过来',
                 '必须==原地修改==输入数组，只用 `O(1)` 额外空间',
                 '示例：`["H","a","n","n","a","h"]` → `["h","a","n","n","a","H"]`',
                 '本视频：`Hannah!?`（n = 8，偶数）'],
        quote='比较基础的题目，==直接按中心位置交换两侧字符即可==。',
        quote_src='—— yiduobo 知乎题解',
        idea=['位置 `index` 和 `len(s) - index - 1` 关于中心对称',
              '只遍历前一半：`index` 从 0 到 `len(s) // 2 - 1`，每次交换一对',
              'n 为奇数时，正中间的字符==自己就是自己的对称位置==，不用动'],
        summary=['时间 `O(n)`，空间 `O(1)`，原地修改',
                 '循环次数是 `len(s) // 2`：多循环一半会把字符==换回原位==',
                 '原文为 Python 2 写法：`len(s) / 2` 已改为整除 `len(s) // 2`，并删去文档字符串',
                 '等价写法：相向双指针 `left`、`right` 往中间走'],
    ),
)
