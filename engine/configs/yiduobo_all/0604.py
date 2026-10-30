def _txt(S):
    if 'self.char_pos' not in S:
        if 'compressedString' in S:
            return f"压缩串 `{S['compressedString']!r}`：读字符，再把后面的数字拼成个数（`p = {S['p']}`）"
        return ''
    cl, cp, k = S['self.char_list'], S['self.char_pos'], S['self.cnt']
    if cp >= len(cl):
        return '`char_pos` 走到末尾：没有字符可用了，`hasNext = False`'
    n = S['self.cnt_list'][cp]
    return f'当前字符 `{cl[cp]}`：已用 =={k}== 个 / 共 {n} 个，还剩 {n - k} 个'


CONFIG = dict(
    num=604, title='迭代压缩字符串', difficulty='Easy', category='设计',
    author='yiduobo', technique='拆成字符数组 + 次数数组 · 两个指针',
    tags=[],
    code='''
class StringIterator(object):

    def __init__(self, compressedString):

        self.char_list = []
        self.cnt_list = []

        p = 0
        while p < len(compressedString):
            self.char_list.append(compressedString[p])
            p += 1
            now = 0
            while p < len(compressedString) and compressedString[p] >= '0' and compressedString[p] <= '9':
                now = now * 10 + int(compressedString[p])
                p += 1
            
            self.cnt_list.append(now)

        self.char_pos = 0
        self.cnt = 0

    def next(self):
        if self.hasNext():
            res = self.char_list[self.char_pos]
            self.cnt += 1
            if self.cnt == self.cnt_list[self.char_pos]:
                self.cnt = 0
                self.char_pos += 1
            
        else:
            res = ' '
        
        return res

    def hasNext(self):

        return self.char_pos != len(self.char_list)
''',
    call="""it = StringIterator('a2b1')
out = []
out.append(it.next())
out.append(it.next())
out.append(it.next())
out.append(it.hasNext())
out.append(it.next())
out""",
    expect=['a', 'a', 'b', False, ' '],
    views=[
        dict(type='array', var='self.char_list', label='char_list（字符）', cell=90, h=200, pointers={'self.char_pos': 'pink'}),
        dict(type='array', var='self.cnt_list', label='cnt_list（每个字符的个数）', cell=90, h=200, pointers={'self.char_pos': 'pink'}),
        dict(type='text', h=90, size=28, fn=_txt),
        dict(type='calls', label='正在执行', h=110),
    ],
    watch=[('p', 'p', 'blue'), ('now', 'now', 'cyan'), ('char_pos', 'self.char_pos', 'pink'), ('cnt', 'self.cnt', 'orange'), ('res', 'res', 'green')],
    skip=['self.cnt_list = []'],
    captions={
        'self.char_list = []': '`char_list` 存字符，`cnt_list` 存每个字符对应的个数',
        'p = 0': '`p` 从头扫描压缩串',
        'while p < len(compressedString):': lambda S, B, r: (f'`p = {S.p}`：还没扫完，读下一段 “字符+数字”' if S.p < len(S.compressedString) else f'`p = {S.p}` 到末尾：解析完毕'),
        'self.char_list.append': '字符 `{compressedString[p]!r}` 放进 `char_list`',
        'p += 1': lambda S, B, r: ('`p` 跳过字符，指向它后面的数字' if S._line == 11 else f'读完一位数字，`p` → {S.p}'),
        'now = 0': '`now` 用来累计这个字符的个数',
        'while p < len(compressedString) and': lambda S, B, r: (f'`{S.compressedString[S.p]!r}` 是数字 → 继续累计（多位数也能处理）' if S.p < len(S.compressedString) and S.compressedString[S.p].isdigit()
                                                                   else f'下一个不是数字（或到末尾）→ 这个字符的个数读完'),
        'now = now * 10': '`now = {B.now} × 10 + {compressedString[p]} = {now}`：按十进制往后拼',
        'self.cnt_list.append(now)': '个数 `{now}` 放进 `cnt_list`：`{self.char_list}` / `{self.cnt_list}`',
        'self.char_pos = 0': '`char_pos`：当前用到第几个字符',
        20: '`cnt`：当前字符已经用了几个，一开始 0 个',
        'if self.hasNext():': lambda S, B, r: ('判断 `hasNext()`：`char_pos = {}` 没到末尾 → 还有字符，进 if'.format(S.self.char_pos) if S.self.char_pos != len(S.self.char_list)
                                              else '判断 `hasNext()`：`char_pos = {}` 已到末尾 → 没有字符，走 else'.format(S.self.char_pos)),
        'res = self.char_list[self.char_pos]': '取出当前字符 `{res!r}`',
        'self.cnt += 1': '这个字符又用掉一个：`cnt = {self.cnt}`',
        'if self.cnt == self.cnt_list[self.char_pos]': lambda S, B, r: (f'`cnt = {S.self.cnt}` 等于它的个数 {S.self.cnt_list[S.self.char_pos]}：这个字符用完了 → 换下一个' if S.self.cnt == S.self.cnt_list[S.self.char_pos]
                                                                        else f'`cnt = {S.self.cnt}` 还没到 {S.self.cnt_list[S.self.char_pos]}：下次继续用同一个字符'),
        27: '`cnt` 重置为 0，给下一个字符用',
        'self.char_pos += 1': '`char_pos` 后移一位 → {self.char_pos}',
        "res = ' '": '没有字符了，按题意返回空格 `\' \'`',
        'return res': '`next()` 返回 `{res!r}`',
        'return self.char_pos != len(self.char_list)': '`char_pos = {self.char_pos}`，`len(char_list) = {len(self.char_list)}`：不相等才有字符 → `{ret}`',
    },
    max_steps=110,
    cards=dict(
        one_liner='把压缩串拆成两个数组，用 char_pos 和 cnt 两个指针边用边数',
        complexity='构造 `O(n)`；`next` / `hasNext` 都是 `O(1)`',
        problem=['压缩串形如 `"L1e2t1C1o1d1e1"`：每个字符后面跟它的重复次数',
                 '设计 `StringIterator`：`next()` 依次返回下一个字符，没有了返回 `\' \'`；`hasNext()` 问是否还有',
                 '本视频：`"a2b1"` → `next=a, a, b`，然后 `hasNext=False`，`next=\' \'`'],
        quote='将压缩字符串中的字符和数量拆开，形成两个数组char_list和cnt_list，并使用两个变量char_pos和cnt分别记录当前使用到的字符的下标以及该字符已经使用了几个。',
        quote_src='—— yiduobo 题解原文',
        idea=['构造时一次扫完：读一个字符，再把后面连续的数字拼成个数（可能是多位数）',
              '`next`：返回 `char_list[char_pos]`，`cnt` 加一；==用够个数就换下一个字符==并把 `cnt` 清零',
              '`hasNext`：只要 `char_pos` 没到 `char_list` 末尾就还有字符'],
        summary=['构造 `O(n)`，之后每次操作 `O(1)`，空间 `O(n)`',
                 '个数可能是多位数：用 `now * 10 + 数字` 累计',
                 '用完个数的那一刻就移动 `char_pos`，所以 `hasNext` 不用再看 `cnt`',
                 '没有字符时 `next` 返回空格，不能抛异常',
                 '原文为 Python 2 风格，本题代码在 Python 3 下可直接运行，未改动'],
    ),
)
