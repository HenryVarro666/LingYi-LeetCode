# 输入字符串用 _Str 包一层：遍历时每个字母带上自己的下标 .i，视图靠它画“当前读到哪”和“哪些还在栈里”
SETUP = '''
class _Ch(str):
    pass


class _Str(str):
    def __iter__(self):
        for k, ch in enumerate(str.__iter__(self)):
            c = _Ch(ch)
            c.i = k
            yield c
'''
TEXT = "acbzay"


def _sim(s):
    """复现算法，得到 {下标: 与它一起被消掉的栈顶下标}（只用于画图）"""
    st, pair = [], {}
    for k, ch in enumerate(s):
        if st and abs(ord(ch) - ord(s[st[-1]])) in (1, 25):
            pair[k] = st.pop()
        else:
            st.append(k)
    return pair


PAIR = _sim(TEXT)


def _state(S):
    c = S.get('b')
    if c is None:
        return None
    ln = S['_line']
    cur = c.i
    kept = {x.i for x in S['st']}
    top = S['st'][-1].i if S['st'] else None
    return cur, kept, top, ln


def _color(S, i, v):
    r = _state(S)
    if r is None:
        return None
    cur, kept, top, ln = r
    if ln == 11 and i in (cur, PAIR.get(cur)):
        return 'red'
    if ln in (3, 4, 10) and top is not None and i == top and i != cur:
        return 'yellow'
    if ln >= 14:
        return 'green' if i in kept else None
    if i == cur:
        return 'green' if (ln == 13 and i in kept) else 'blue'
    if i < cur and i in kept:
        return 'green'
    return None


def _dim(S, i, v):
    r = _state(S)
    if r is None:
        return False
    cur, kept, top, ln = r
    if i in kept:
        return False
    if ln == 11 and i == PAIR.get(cur):
        return False
    return i < cur or ln >= 14


def _msg(S, B):
    c = S.get('b')
    if c is None:
        return '栈 `st` 按顺序记录“还没被消掉”的字母'
    ln = S['_line']
    st = S['st']
    if ln == 9:
        return f'读到 `{c}`；栈顶 `{st[-1] if st else "（空）"}`'
    if ln == 10:
        return (f'栈顶 `{st[-1]}` 和当前 `{c}`：字母表里连续吗？' if st else '栈是空的，没有字母可比')
    if ln in (3, 4):
        x, y = S['x'], S['y']
        return f"`|ord('{x}') − ord('{y}')| = |{ord(x)} − {ord(y)}|` = =={abs(ord(x) - ord(y))}=="
    if ln == 11:
        return f'`{B["st"][-1]}{c}` 连续，立刻消掉；栈里剩 `{"".join(st) or "空"}`'
    if ln == 13:
        return f'`{c}` 入栈，栈里 `{"".join(st)}`'
    return f'栈里从底到顶：`{"".join(st)}`'


CONFIG = dict(
    num=3561, title='移除相邻字符', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='栈 · 从左到右立刻消除连续字母',
    tags=['灵神核心路线', '灵神题单·常用数据结构', '难度分 1397'],
    code='''
# 更快的写法见【Python3 写法二】
def is_consecutive(x: str, y: str) -> bool:
    d = abs(ord(x) - ord(y))
    return d == 1 or d == 25

class Solution:
    def resultingString(self, s: str) -> str:
        st = []
        for b in s:
            if st and is_consecutive(b, st[-1]):
                st.pop()
            else:
                st.append(b)
        return ''.join(st)
''',
    setup=SETUP,
    call=f'Solution().resultingString(_Str("{TEXT}"))',
    expect='ay',
    views=[
        dict(type='text', fn=_msg, size=28, h=70),
        dict(type='string', var='s', label='s（蓝 = 当前字母，黄 = 正比较的栈顶，绿 = 还在栈里，红 = 正被消掉，灰 = 已消）',
             cell=84, pointers={'b.i': 'blue'}, pointer_labels={'b.i': 'b'}, color=_color, dim=_dim, h=190),
        dict(type='stack', var='st', label='st（还没被消掉的字母）', fmt=lambda x: str(x), font=34, h=130),
    ],
    watch=[('b', 'b', 'blue'), ('栈顶', 'st[-1] if st else None', 'purple'), ('d', 'd', 'yellow'), ('len(st)', 'len(st)', 'green')],
    captions={
        'st = []': '栈 `st` 按顺序记录==还没被消掉==的字母',
        'for b in s': lambda S, B, ret: (f'从左到右读第 `{S.b.i}` 个字母 `b = {S.b}`' if 'b' not in B or B.b.i != S.b.i
                                         else '字母都读完了，栈里剩下的就是答案'),
        'if st and': lambda S, B, ret: (
            f'栈是空的，没有字母可以比 → `{S.b}` 直接入栈' if not S.st else
            f'拿 `b = {S.b}` 和栈顶 `{S.st[-1]}` 比：字母表里连续吗？调用 `is_consecutive` 判断'),
        'd = abs': lambda S, B, ret: (f"`d = |ord('{S.x}') − ord('{S.y}')| = |{ord(S.x)} − {ord(S.y)}|` = =={S.d}==，"
                                      '字母表上隔了多远'),
        'return d == 1': lambda S, B, ret: (
            f'`d = {S.d}`：' + ('==d 等于 1，字母表里相邻==' if S.d == 1 else
                              '==d 等于 25，a 和 z 首尾相接，循环字母表里也相邻==' if S.d == 25 else
                              f'既不是 1 也不是 25（`d = 0` 是相同字母，也不算）') + f' → 返回 `{ret}`'),
        'st.pop()': lambda S, B, ret: (f'连续就立刻消除（题目要消最左边的一对）：弹出栈顶 `{B.st[-1]}`，`{S.b}` 也不入栈。'
                                       + (f'新栈顶是 `{S.st[-1]}`，成了后面字母的左邻居' if S.st else '栈空了')),
        'st.append(b)': '不连续，`{b}` 入栈，等后面的字母来配 → 栈 `{"".join(st)}`',
        "return ''.join": '栈里从底到顶拼起来：`{ret}`',
    },
    cards=dict(
        one_liner='每次消最左边一对 → 从左到右扫，连续就立刻弹栈',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['小写字母串 `s`，只要还有两个相邻字符在字母表里==连续==（`a`与`b`、`b`与`a`，`a`与`z` 也算），就移除==最左边==的一对',
                 '剩下的字符向左靠拢，反复进行，返回最终字符串',
                 '示例：`"abc"` → `"c"`；`"adcb"` → `""`；`"zadb"` → `"db"`',
                 '本视频用 `"acbzay"` → `"ay"`：消掉 `cb` 后 `a`、`z` 才碰到一起'],
        quote='由于每次都是消除最左边的字符，我们从左到右遍历 s，同时用栈记录字符：如果栈不为空，且 s[i] 与栈顶是「连续」的，那么立刻消除，弹出栈顶。否则把 s[i] 入栈。',
        quote_src='—— 灵茶山艾府题解',
        idea=['注意：消除后原本不相邻的字符会变相邻，可以继续消除 → 栈顶就是新的左邻居',
              '「连续」：`|ord(x) − ord(y)|` 等于 `1`，或者等于 `25`（`a` 和 `z` 首尾相接）',
              '每次消最左边的一对，等价于从左往右扫，一出现连续就立刻消'],
        result='栈里从底到顶是 `a`、`y`，返回 `"ay"` ✓',
        summary=['时间 `O(n)`，空间 `O(n)`（灵神说 C++ 原地做法可以 `O(1)`）',
                 '易错：别漏掉 `d == 25`；也别把相同字母（`d = 0`）当成连续',
                 '灵神写法二：预处理 `mp[b] = lc[i-1] + lc[(i+1)%26]`（`b` 左右两个邻居），判断变成 `st[-1] in mp[b]`，更快',
                 '同类题：第 1047、2696 题，见题单 §3.3 邻项消除'],
    ),
)
