CONFIG = dict(
    num=2000, title='反转单词前缀', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='一趟扫描 · 边记录边找 ch',
    tags=['难度分 1199'],
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
    call='Solution().reversePrefix("abcdefd", "d")',
    expect='dcbaefd',
    views=[
        dict(type='string', var='word', label='word（蓝 = 当前扫描的位置）', cell=84, pointers={'index': 'blue'},
             color=lambda S, i, v: 'green' if S.get('p') == i else None),
        dict(type='array', var=lambda S: list(S['res']) if 'res' in S else None,
             label='res（边扫描边记录的字符；反转后变成答案前缀）', cell=84),
        dict(type='text', fn=lambda S: (f"`p = {S['p']}`：ch 第一次出现的位置" if S.get('p') is not None
                                        else '还没找到 `ch`，继续记录'), size=26),
    ],
    watch=[('index', 'index', 'blue'), ('ch', 'ch', 'pink'), ('p', 'p', 'green')],
    captions={
        'p = None': '`p` 记录 ch 第一次出现的下标，`None` 表示还没找到',
        'res = []': '`res` 用来记录扫过的字符',
        'for index': '扫描 word：`index = {index}`',
        'res.append': '把 `word[{index}] = {word[index]!r}` 记入 `res` → `{res}`',
        'if word[index] == ch': lambda S, B, r: (f"`{S.word[S.index]!r} == {S.ch!r}` → ==找到了=="
                                                 if S.word[S.index] == S.ch else
                                                 f"`{S.word[S.index]!r} != {S.ch!r}` → 不是 ch，继续往后"),
        'p = index': '记下位置 `p = {p}`',
        'break': '第一次出现就够了，==直接退出==扫描，后面的 ch 不用管',
        'if p is None': '`p = {p}`，说明中途 break 过 → 需要反转',
        'return word': '没找到 ch，原样返回',
        'res.reverse()': '把 `res` 原地反转 → `{res}`',
        'return ''.join': lambda S, B, ret: f"反转后的前缀 + 没扫过的 `word[{S.p + 1}:]` = `{ret}`",
    },
    cards=dict(
        one_liner='扫到第一个 ch 就停，把记录的前缀反转后接上剩余部分',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['找到 `ch` 第一次出现的下标 `i`，反转 `word[0..i]`',
                 '`ch` 不存在则不操作',
                 '示例：`"abcdefd"`, `ch = d` → `"dcbaefd"`'],
        quote='一趟扫描，将当前遍历到的字符记录在一个list中，直到当前遍历到的字符等于ch或者到达word的末尾为止。',
        quote_src='—— yiduobo 题解原文',
        idea=['边扫描边把字符放进 `res`，遇到 `ch` 就记下 `p` 并 `break`',
              '`p` 仍是 `None` → 整串里没有 ch，直接返回 `word`',
              '否则 `res` 反转后拼上没扫过的 `word[p+1:]`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：只反转到==第一次==出现的 ch，要 `break`',
                 '易错：拼接的后半段是 `word[p + 1:]`，不要重复 p 位置',
                 '原文就是 Python 3 可运行的写法，未做修改'],
    ),
)
