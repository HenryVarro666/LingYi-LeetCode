CONFIG = dict(
    num=2810, title='故障键盘', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='直接模拟 · 双指针翻转',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def finalString(self, s):

        res = []
        for char in s:
            if char == 'i':
                left = 0
                right = len(res) - 1
                while left < right:
                    res[left], res[right] = res[right], res[left]
                    left += 1
                    right -= 1
            else:
                res.append(char)
        
        return ''.join(res)
''',
    call="Solution().finalString('string')",
    expect='rtsng',
    views=[
        dict(type='string', var='s', h=130, label='输入 s'),
        dict(type='array', var='res', pointers={'left': 'blue', 'right': 'pink'}, label='屏幕上的文本 res', h=200, cell=70),
    ],
    watch=['char', ('left', 'left', 'blue'), ('right', 'right', 'pink')],
    captions={
        'res = []': '`res` 就是屏幕上的文本',
        'for char in s': '敲下字符 `{char}`',
        "if char == 'i'": lambda S, B, r: ('是 `i`：把 `res` 翻转过来' if S.char == 'i' else '`{}` 是普通字符'.format(S.char)),
        'left = 0': '翻转用双指针：`left` 从头开始',
        'right = len(res) - 1': '`right = len(res) - 1 = {right}`，从尾开始',
        'while left < right': lambda S, B, r: ('`left = {} < right = {}`：还没碰头，继续交换'.format(S.left, S.right) if S.left < S.right
                                                else '`left = {} >= right = {}`：翻转完成'.format(S.left, S.right)),
        'res[left], res[right]': '交换 `res[{left}]` 和 `res[{right}]`',
        'left += 1': '`left` → {left}',
        'right -= 1': '`right` → {right}',
        'res.append(char)': '`{char}` 接到末尾：`{"".join(res)}`',
        'return': '最终屏幕上是 `{ret}`',
    },
    cards=dict(
        one_liner='数据规模很小，遇到 i 就老老实实把 res 翻转',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['键盘故障：输入 `i` 时把已写的字符串==反转==，其他字符正常输入',
                 '返回最终屏幕上的字符串',
                 '示例：`s = "string"` → `"rtsng"`'],
        quote='题目的数据规模很小，完全可以直接一趟遍历进行模拟。当遇到字符i时将当前已有的字符串翻转过来就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历，普通字符 `append`，`i` 就原地翻转 `res`',
              '翻转用相向双指针：交换 `res[left]` 与 `res[right]`，直到相遇',
              '作者也提到：可以改成切换插入位置，用双端队列做到 `O(n)`，但这里选了暴力'],
        summary=['时间最坏 `O(n^2)`（每个 `i` 翻转 `O(n)`），`n <= 100` 够用',
                 '易错：`right = len(res) - 1`，不是 `len(res)`',
                 '翻转条件是 `left < right`，中间元素不用动',
                 '原文为 Python 2 写法，只删去了类型说明文档字符串；对比灵神：用方向标记 + 双端队列 `O(n)`'],
    ),
)
