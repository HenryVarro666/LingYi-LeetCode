def _sw_color(S, i, v):
    if 'right' not in S:
        return None
    l, r = S['left'], S['right']
    if i < l or i > r:
        return 'green'  # 已经交换到位
    return None


def _status(S):
    if 'right' not in S:
        return ''
    l, r = S['left'], S['right']
    n = len(S['s'])
    if l >= r:
        return f'`left = {l} >= right = {r}`：==所有字符都交换完毕=='
    return f'`left + right = {l} + {r} = {n - 1}` ==恒等于 n − 1==：下一对要交换 `s[{l}]` 和 `s[{r}]`'


def _while(S, B, ret):
    l, r = B['left'], B['right']
    if l < r:
        return f'`left = {l} < right = {r}`：中间还有没交换的字符'
    if l == r:
        return f'`left = right = {l}`：n 是奇数，==正中间的字符不用动== → 退出'
    return f'`left = {l} > right = {r}`：n 是偶数，两指针交错 → 全部交换完，退出'


CONFIG = dict(
    num=344, title='反转字符串', difficulty='Easy', category='双指针',
    author='灵茶山艾府', technique='相向双指针（首尾交换）',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def reverseString(self, s: List[str]) -> None:
        left = 0
        right = len(s) - 1
        while left < right:
            s[left], s[right] = s[right], s[left]
            left += 1
            right -= 1
''',
    call='''s = ["s", "t", "r", "e", "a", "m", "s"]
Solution().reverseString(s)
s''',
    expect=["s", "m", "a", "e", "r", "t", "s"],
    views=[
        dict(type='text', fn=_status, h=60),
        dict(type='string', var='s', label='s（绿 = 已交换到最终位置）', cell=96, h=300,
             pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'), color=_sw_color),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('n', 'len(s)')],
    captions={
        'left = 0': '`left = 0` 指向第一个要交换的位置',
        'right = len(s) - 1': '`right = n - 1 = {right}` 指向最后一个位置：==s[0] 要和 s[n-1] 交换==',
        'while left < right': _while,
        's[left], s[right] =': '交换 `s[{B.left}]` 和 `s[{B.right}]`：`{B.s[B.left]}` ↔ `{B.s[B.right]}`，==这两个位置就此定型==',
        'left += 1': '交换后向中间靠拢：`left` → {left}',
        'right -= 1': '`right` → {right}，始终保持 `left + right = n - 1`',
    },
    cards=dict(
        one_liner='反转 = 交换 s[0] 与 s[n-1]、s[1] 与 s[n-2]……首尾两两交换',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['输入字符串以字符数组 `s` 给出，把它反转过来',
                 '必须==原地修改==输入数组，只用 `O(1)` 额外空间',
                 '示例：`["h","e","l","l","o"]` → `["o","l","l","e","h"]`',
                 '本视频：`streams` → `smaerts`（n = 7，奇数）'],
        quote='反转可以看成是==交换 s[0] 和 s[n-1]，交换 s[1] 和 s[n-2]==，交换 s[2] 和 s[n-3]，依此类推。当 left ≥ right 时，所有字符交换完毕，退出循环。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`left = 0`、`right = n-1` 表示要交换的位置，每次交换后各向中间走一步',
              'n 奇数：最后 `left = right = floor(n/2)`，中间那个==无需交换==',
              'n 偶数：最后一次交换后两指针交错，`left > right`，同样退出'],
        summary=['时间 `O(n)`，空间 `O(1)`，原地修改',
                 '循环条件是 `left < right`：写成 `<=` 也对，但中间会自己和自己交换一次',
                 '单指针写法：`left + right = n-1` 恒成立，`for i in range(n // 2)` 交换 `s[i]` 和 `s[-i-1]`',
                 '库函数：`s.reverse()`；不能写 `s = s[::-1]`：==形参重新赋值影响不到外部=='],
    ),
)
