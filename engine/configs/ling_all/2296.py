def _line(S):
    if 'self.left' not in S:
        return '编辑器还没创建'
    left, right = ''.join(S['self.left']), ''.join(reversed(S['self.right']))
    return f'文本 `{left}|{right}`　竖线 | 是光标'


CONFIG = dict(
    num=2296, title='设计一个文本编辑器', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='对顶栈',
    tags=['栈', '难度分 1912'],
    code='''
class TextEditor:
    def __init__(self):
        self.left = []  # 光标左侧字符
        self.right = []  # 光标右侧字符

    def addText(self, text: str) -> None:
        self.left.extend(text)  # 入栈

    def deleteText(self, k: int) -> int:
        pre = len(self.left)  # 删除之前的栈大小
        del self.left[-k:]  # 出栈
        return pre - len(self.left)  # 减去删除之后的栈大小

    def text(self) -> str:
        return ''.join(self.left[-10:])  # 光标左边至多 10 个字符

    def cursorLeft(self, k: int) -> str:
        while k and self.left:
            self.right.append(self.left.pop())  # 左手倒右手
            k -= 1
        return self.text()

    def cursorRight(self, k: int) -> str:
        while k and self.right:
            self.left.append(self.right.pop())  # 右手倒左手
            k -= 1
        return self.text()
''',
    call='''t = TextEditor()
res = []
t.addText("abcde")
res.append(t.deleteText(2))
t.addText("xy")
res.append(t.cursorLeft(3))
res.append(t.cursorRight(1))
res.append(t.deleteText(9))
res''',
    expect=[2, 'ab', 'abc', 3],
    views=[
        dict(type='text', fn=_line, size=34, h=60),
        dict(type='stack', var='self.left', label='左栈（光标左边，栈顶 = 光标处）', fmt=lambda x: str(x), h=230),
        dict(type='stack', var='self.right', label='右栈（光标右边，栈顶 = 光标处）', fmt=lambda x: str(x), h=230),
    ],
    watch=['k', ('左栈大小', 'len(self.left)', 'blue'), ('右栈大小', 'len(self.right)', 'pink')],
    captions={
        'self.left = []': '左栈：存==光标左边==的字符，栈顶就是光标位置',
        'self.right = []': '右栈：存==光标右边==的字符，两个栈==栈顶对栈顶==',
        'self.left.extend': '添加文本 = 在左栈上==入栈==：光标始终在新文本右边，左栈 `{self.left}`',
        'pre = len': '先记下删除前左栈大小 `{pre}`',
        'del self.left': '删除光标左边 `k={k}` 个字符 = 左栈==出栈==；不够就全删（切片越界不报错）',
        'return pre - len': '实际删除 = `{pre} − {len(self.left)}` = =={ret}==',
        'while k and self.left': lambda S, B, r: (f'`k = {S.k}` 且左栈非空 → 光标还能再左移一格' if S.k and S['self.left'] else '`k` 用完或左栈空了（光标到头）→ 停止'),
        'self.right.append(self.left.pop())': '光标左移一格：==左手倒右手==，`{self.right[-1]}` 从左栈顶移到右栈顶',
        'while k and self.right': lambda S, B, r: (f'`k = {S.k}` 且右栈非空 → 光标还能再右移一格' if S.k and S['self.right'] else '`k` 用完或右栈空了（光标到头）→ 停止'),
        'self.left.append(self.right.pop())': '光标右移一格：==右手倒左手==，`{self.left[-1]}` 回到左栈顶',
        'k -= 1': '剩余移动次数 `k = {k}`',
        'return self.text()': '移动完毕，调用 `text()` 取光标左边至多 10 个字符作为返回值',
        "''.join(self.left[-10:])": '取左栈最后 10 个拼成字符串：`"{ret}"`（只看光标左边）',
    },
    cards=dict(
        one_liner='两个栈头对头，光标移动就是左右手来回倒数据',
        complexity='`addText` `O(|text|)`，其余 `O(k)`，空间 `O(n)`',
        problem=['带光标的编辑器：`addText` 在光标处添加，`deleteText(k)` 删光标左边 k 个',
                 '`cursorLeft/Right(k)` 移动光标，返回光标左边至多 10 个字符',
                 '本视频：`abcde` → 删 2 → 加 `xy` → 左移 3 → 右移 1 → 删 9'],
        quote='创建左右两个栈，头对头（栈顶对栈顶），光标的左右移动就相当于两个栈中的数据来回倒（左手倒右手，右手倒左手）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['增删只发生在光标左边 → 直接对==左栈==入栈、出栈',
              '光标左移：左栈顶弹出，压进右栈；右移则反过来',
              '两栈头对头，保证倒过去再倒回来顺序不变'],
        summary=['`deleteText` 用切片 `del left[-k:]`，k 超过长度也不会报错，返回差值即实际删除数',
                 '`k` 很大时移动是 `O(k)`；进阶可用 ==Splay== 做到与 k 无关（原文选读）',
                 '易错：移动要判断栈是否为空，否则光标会跑出文本',
                 '同类：HDU 4699 Editor（对顶栈）'],
    ),
)
