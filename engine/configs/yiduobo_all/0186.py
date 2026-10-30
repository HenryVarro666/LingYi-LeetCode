CONFIG = dict(
    num=186, title='反转字符串中的单词 II', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='整体反转 + 逐词反转',
    code='''
class Solution(object):
    def reverseWords(self, s):

        def reverse_part(left, right):
            while left < right:
                s[left], s[right] = s[right], s[left]
                left += 1
                right -= 1
        
        reverse_part(0, len(s) - 1)
        
        p = 0
        for index in range(1, len(s)):
            if s[index] == ' ':
                reverse_part(p, index - 1)
                p = index + 1
        
        reverse_part(p, len(s) - 1)
''',
    setup="s0 = list('ab cde f')\nsol = Solution()",
    call='sol.reverseWords(s0)\n"".join(s0)',
    expect='f cde ab',
    views=[
        dict(type='array', var='s', pointers={'left': 'blue', 'right': 'pink', 'p': 'green', 'index': 'orange'}, h=330),
        dict(type='text', fn=lambda S: '字符数组 `s`（空格也占一格），原地修改，不用额外空间', size=26),
    ],
    watch=['left', 'right', ('p', 'p', 'green'), ('index', 'index', 'orange')],
    captions={
        'def reverse_part': '先定义辅助函数：反转 `s[left..right]`，相向双指针交换',
        'while left < right': lambda S, B, r: (f"`left = {S.left} < right = {S.right}` → 继续交换" if S.left < S.right else f"`left = {S.left} >= right = {S.right}` → 这一段反转完了"),
        's[left], s[right] =': '交换 `s[{left}]` 与 `s[{right}]`',
        'left += 1': '`left` → {left}',
        'right -= 1': '`right` → {right}',
        'reverse_part(0, len(s) - 1)': '第一步：整体反转。单词顺序对了，但每个单词自己也倒过来了',
        'p = 0': '`p` 记录当前单词的起点',
        'for index in range': lambda S, B, r: (f'`index` = {S.index}，往后扫描找单词的结尾' if B.get('index') != S.index else '`index` 扫到末尾，循环结束'),
        'if s[index] == ': lambda S, B, r: (f"`s[{S.index}]` 是空格 → 单词 `[{S.p}, {S.index - 1}]` 结束了" if S.s[S.index] == ' ' else f"`s[{S.index}] = '{S.s[S.index]}'` 不是空格 → 还在单词里"),
        'reverse_part(p, index - 1)': '把这个单词再反转一次，负负得正，字母顺序恢复',
        'p = index + 1': '下一个单词从空格后面开始：`p` = =={p}==',
        'reverse_part(p, len(s) - 1)': '最后一个单词后面没有空格，循环里碰不到，要在循环外单独反转 `[{p}, {len(s) - 1}]`',
    },
    cards=dict(
        one_liner='先整体反转，再把每个单词反转回来',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s` 是字符数组，单词之间用单个空格隔开',
                 '要求原地把单词的顺序反转，单词本身不变，不能用额外空间',
                 '示例：`"ab cde f"` → `"f cde ab"`'],
        quote='反转整个数组，但是这样一来每个单词自身就被反转了，此时只需一趟遍历，将每个单词自身再进行一次反转就可以抵消掉反转整个数组带来的影响了。',
        quote_src='—— yiduobo 题解原文',
        idea=['整体反转 = 单词顺序倒过来 + 每个单词内部也倒过来',
              '再对每个单词各反转一次，内部顺序就恢复了',
              '用 `p` 记单词起点，遇到空格就反转 `[p, index-1]`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：最后一个单词后面没有空格，必须在循环后再反转一次',
                 '`reverse_part` 修改的是外层的 `s`，所以函数本身没有返回值',
                 '为方便展示，调用后用 `"".join(s0)` 取出结果；原文已是 Python 3 可运行写法'],
    ),
)
