def _line(S):
    if 'self.left_part' not in S:
        return '编辑器还没创建'
    left, right = ''.join(S['self.left_part']), ''.join(reversed(S['self.right_part']))
    return f'文本 `{left}|{right}`　竖线 | 是光标'


def _loop(side, other, word):
    def f(S, B, ret):
        if S['k'] and S['self.' + side]:
            return f'`k = {S["k"]}` 且{word}还有字符 → 再挪一个'
        return f'`k = {S["k"]}` 或{word}空了 → 光标到头或挪完，停止'
    return f


CONFIG = dict(
    num=2296, title='设计一个文本编辑器', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='左右两个栈分别维护光标两侧',
    tags=['栈', '难度分 1912'],
    code='''
class TextEditor(object):

    def __init__(self):
        self.left_part = []
        self.right_part = []

    def addText(self, text):
        for char in text:
            self.left_part.append(char)

    def deleteText(self, k):
        cnt = 0
        while k and self.left_part:
            self.left_part.pop()
            k -= 1
            cnt += 1

        return cnt

    def cursorLeft(self, k):
        while k and self.left_part:
            self.right_part.append(self.left_part.pop())
            k -= 1

        if len(self.left_part) >= 10:
            return ''.join(self.left_part[-10:])
        else:
            return ''.join(self.left_part)

    def cursorRight(self, k):
        while k and self.right_part:
            self.left_part.append(self.right_part.pop())
            k -= 1

        if len(self.left_part) >= 10:
            return ''.join(self.left_part[-10:])
        else:
            return ''.join(self.left_part)
''',
    call='''t = TextEditor()
res = []
t.addText("hello")
res.append(t.cursorLeft(2))
res.append(t.deleteText(1))
t.addText("p")
res.append(t.cursorRight(9))
res.append(t.deleteText(9))
res''',
    expect=['hel', 1, 'heplo', 5],
    views=[
        dict(type='text', fn=_line, size=34, h=60),
        dict(type='stack', var='self.left_part', label='left_part（光标左侧，栈顶靠近光标）', fmt=lambda x: str(x), h=230),
        dict(type='stack', var='self.right_part', label='right_part（光标右侧，栈顶靠近光标）', fmt=lambda x: str(x), h=230),
    ],
    watch=['k', ('left 大小', 'len(self.left_part)', 'blue'), ('right 大小', 'len(self.right_part)', 'pink'), 'cnt'],
    captions={
        'self.left_part = []': '`left_part`：光标==左侧==所有字符，后进先出',
        'self.right_part = []': '`right_part`：光标==右侧==所有字符，同样当栈用',
        'for char in text': '逐个字符加到光标左侧',
        'self.left_part.append(char)': '`{char}` 压入 `left_part`，光标跟着停在它右边',
        'cnt = 0': '`cnt` 记录实际删掉几个',
        'while k and self.left_part': _loop('left_part', 'right_part', '左侧'),
        14: '回退一个字符：左侧栈顶 `{B["self.left_part"][-1]}` 出栈',
        'cnt += 1': '实际删除数 `cnt` = {cnt}（`left_part` 空了就删不动，所以可能小于 k）',
        'return cnt': '返回实际删除的个数 ==`{cnt}`==',
        'self.right_part.append(self.left_part.pop())': '光标左移一格：左侧栈顶 `{self.right_part[-1]}` 挪到右侧栈',
        'while k and self.right_part': _loop('right_part', 'left_part', '右侧'),
        'self.left_part.append(self.right_part.pop())': '光标右移一格：右侧栈顶 `{self.left_part[-1]}` 回到左侧栈（顺序先出后进，刚好还原）',
        'if len(self.left_part) >= 10': lambda S, B, r: (f'左侧有 `{len(S["self.left_part"])}` 个字符，≥ 10 → 只取最后 10 个' if len(S['self.left_part']) >= 10 else f'左侧只有 `{len(S["self.left_part"])}` 个字符，< 10 → 全部返回'),
        "return ''.join(self.left_part[-10:])": '返回光标左边的最后 10 个字符：`"{ret}"`',
        "return ''.join(self.left_part)": '不足 10 个，返回光标左边全部：`"{ret}"`',
    },
    cards=dict(
        one_liner='光标左右各一个栈，增删在左栈，移动就是两栈互倒',
        complexity='`addText` `O(|text|)`，其余 `O(k)`，空间 `O(n)`',
        problem=['编辑器有光标：添加、回退删除（只删光标左边）、左右移动光标',
                 '`deleteText` 返回实际删除数；移动后返回光标左边最后 10 个字符',
                 '本视频：`hello` → 左移 2 → 删 1 → 加 `p` → 右移 9 → 删 9'],
        quote='操作1和操作2都是对光标左侧的数据进行操作，而操作3则是在调整光标左侧和右侧的数据构成，因此一个自然的想法就是分别维护当前光标左右两侧的数据。',
        quote_src='—— yiduobo 题解原文',
        idea=['增、删都在光标左侧，后进先出 → 左侧用一个栈',
              '光标左移 = 左栈顶出栈、加入右侧；右移时又要按先出后进的顺序放回',
              '所以右侧也必须满足后进先出 → 右侧也用栈'],
        summary=['移动、删除都要先判断栈是否为空，否则 pop 会报错',
                 '返回值只看左栈最后 10 个：`[-10:]`，不足 10 个就全返回',
                 '带区间操作的题常用块状链表或伸展树，这里操作简单，两个栈就够了',
                 '原文已是 Python 3 可运行写法，未做修改'],
    ),
)
