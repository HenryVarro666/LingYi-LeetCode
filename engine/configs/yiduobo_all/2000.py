CONFIG = dict(
    num=2000, title='反转单词前缀', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='一趟扫描 + 列表反转',
    tags=['滑动窗口与双指针', '难度分 1199'],
    code='''
class Solution(object):
    def reversePrefix(self, word, ch):
        p = None
        res = []
        for index in range(len(word)):
            res.append(word[index])
            if word[index] == ch:
                p = index
                break

        if p is None:
            return word
        else:
            res.reverse()
            return ''.join(res) + word[p + 1:]
''',
    call="Solution().reversePrefix('abcdefd', 'd')",
    expect='dcbaefd',
    views=[
        dict(type='string', var='word', label='word（蓝 = 当前扫描位置）', h=170, cell=80, pointers={'index': 'blue'},
             color=lambda S, k, x: 'green' if S.get('p') is not None and k <= S['p'] else None),
        dict(type='array', var='res', label='res（已经扫过的字符，按顺序放入）', h=220, cell=70),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'pink'), ('ch', 'ch', 'yellow')],
    captions={
        'p = None': '`p` 记录 `ch` 出现的位置，`None` 表示还没找到',
        'res = []': '`res` 按顺序收集扫过的字符',
        'for index in range': '扫描第 `{index}` 个字符 `{word[index]}`',
        'res.append(word[index])': '先把 `{word[index]}` 放进 `res`：`{res}`',
        'if word[index] == ch': lambda S, B, r: (f'`{S.word[S.index]}` == `{S.ch}`：找到了第一个 `ch`' if S.word[S.index] == S.ch else f'`{S.word[S.index]}` ≠ `{S.ch}`：继续往后扫'),
        'p = index': '记下位置 `p = {p}`，前缀就是 `word[0..{p}]`',
        'break': '第一个 `ch` 已找到，不用再扫，退出',
        'if p is None': lambda S, B, r: ('`p` 是 `None`：整串都没有 `ch` → 原样返回' if S.p is None else f'`p = {S.p}`：有 `ch`，要反转前缀'),
        'res.reverse()': '`res` 里正好是前缀 `word[0..{p}]`，反转它：`{res}`',
        "return ''.join(res)": "反转后的前缀 `{''.join(res)}` + 没扫过的 `word[{p + 1}:]` = =={ret}==",
        'return word': '原样返回 `{word}`',
    },
    cards=dict(
        one_liner='边扫边存，碰到 ch 就停，把存下的前缀反转再拼回去',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给你字符串 `word` 和字符 `ch`',
                 '找到 `ch` 第一次出现的位置，把从开头到它的这段==反转==；没有就不动',
                 '示例：`word = "abcdefd"`，`ch = "d"` → `"dcbaefd"`'],
        quote='一趟扫描，将当前遍历到的字符记录在一个list中，直到当前遍历到的字符等于ch或者到达word的末尾为止。',
        quote_src='—— yiduobo 题解原文',
        idea=['扫描时把字符依次存进 `res`，遇到 `ch` 就记下 `p` 并停下',
              '此时 `res` 正好是前缀，反转后再接上没扫过的 `word[p+1:]`',
              '一直没遇到 `ch`（`p is None`）就直接返回 `word`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：只反转到第一个 `ch`，之后的 `ch` 不管；别忘了拼上 `word[p + 1:]`',
                 '原文为 Python 2 风格写法，在 Python 3 下无需改动，只删去了空行',
                 '对比灵神：灵神原地用双指针交换，yiduobo 用 `reverse()` 一次反转'],
    ),
)
