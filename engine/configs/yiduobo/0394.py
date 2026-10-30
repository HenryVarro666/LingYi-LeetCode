TRACK = '''
class Tracked(str):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k, ch in enumerate(str.__iter__(self)):
            self.k = k
            yield ch
        self.k = None
'''


def _cur(S):
    s = S.get('s')
    k = getattr(s, 'k', None)
    return k if isinstance(k, int) and k >= 0 else None


def _read(S, i):
    s = S.get('s')
    k = getattr(s, 'k', -1)
    if k is None:
        return True
    return i < k


def _digit_cap(S, B, ret):
    c = S.char
    if 48 <= ord(c) <= 57:
        return f"`ord('{c}') = {ord(c)}` 落在 48~57 → ==是数字=="
    return f"`ord('{c}') = {ord(c)}` 不在 48~57 → 不是数字"


CONFIG = dict(
    num=394, title='字符串解码', difficulty='Medium', category='栈',
    author='yiduobo', technique='栈 · 一趟扫描',
    code='''
class Solution(object):
    def decodeString(self, s):
        stack = []
        res = ''
        multi = 0
        for char in s:
            if ord(char) >= 48 and ord(char) <= 57:
                multi = multi * 10 + int(char)
            elif char == '[':
                stack.append([res, multi])
                res = ''
                multi = 0
            elif char == ']':
                prev_res, prev_multi = stack.pop()
                res = prev_res + res * prev_multi
            else:
                res += char

        return res
''',
    setup=TRACK,
    call='Solution().decodeString(Tracked("a2[b2[c]]"))',
    expect='abccbcc',
    views=[
        dict(type='string', var=lambda S: str(S['s']), label='s（灰色 = 已扫描）', h=190, cell=96,
             pointers={_cur: 'cyan'}, pointer_labels={_cur: 'char'},
             dim=lambda S, i, v: _read(S, i)),
        dict(type='stack', var='stack', label='stack：每项是 [括号前的 res, 倍数 multi]',
             fmt=lambda x: f"['{x[0]}', {x[1]}]", h=140),
        dict(type='text', fn=lambda S: (f"当前统计：`res = '{S['res']}'`　`multi = {S['multi']}`"
                                        if 'multi' in S else ''), size=30),
        dict(type='text', fn=lambda S: '遇到 `]` 时结算：`res = prev_res + res * prev_multi`', size=26),
    ],
    watch=[('char', 'char', 'cyan'), ('multi', 'multi', 'purple'), ('res', 'res', 'green'), ('len(stack)', 'len(stack)')],
    captions={
        'stack = []': '栈：遇到 `[` 时保存“括号外面”的现场',
        "res = ''": lambda S, B, ret: ('当前字符串 `res` 初始为空' if not S.get('stack')
                                       else '进入括号：`res` 重置为空串，从头统计括号里的内容'),
        'multi = 0': lambda S, B, ret: ('倍数 `multi` 初始为 0' if not S.get('stack')
                                        else '`multi` 也重置为 0，留给括号里的数字'),
        'for char in s': lambda S, B, ret: (f'扫描下一个字符 `char = {S.char}`' if getattr(S.s, 'k', None) is not None
                                            else '扫描结束'),
        'if ord(char)': _digit_cap,
        'multi = multi * 10': '情况 1：数字 → 更新倍数 `multi = {B.multi} × 10 + {char} = {multi}`',
        "elif char == '['": lambda S, B, ret: ('情况 3：左括号' if S.char == '[' else f'`{S.char}` 不是 `[`'),
        'stack.append([res, multi])': "把 `['{B.res}', {B.multi}]` ==压入栈==：括号结束后还要回到这里",
        "elif char == ']'": lambda S, B, ret: ('情况 4：右括号 → 要结算这一对括号' if S.char == ']' else f'`{S.char}` 不是 `]`'),
        'prev_res, prev_multi = stack.pop()': "弹出栈顶：括号前的 `prev_res = '{prev_res}'`，倍数 `prev_multi = {prev_multi}`",
        'res = prev_res + res * prev_multi': "栈顶的 multi 修饰的是==当前 res==：`'{prev_res}' + '{B.res}' × {prev_multi}` = =={res!r}==",
        'res += char': "情况 2：字母 → 直接接到当前字符串：`res = '{res}'`",
        'return res': '扫描结束，返回 =={ret!r}==',
    },
    cards=dict(
        one_liner='数字记倍数，[ 压栈保存现场，] 弹栈结算',
        complexity='时间、空间都与输出串长度同阶',
        problem=['编码规则 `k[encoded_string]`：方括号内的字符串重复 `k` 次，可以嵌套',
                 '示例：`"3[a]2[bc]"` → `"aaabcbc"`',
                 '示例：`"3[a2[c]]"` → `"accaccacc"`'],
        quote='需要注意的是，==栈顶的multi是用来修饰当前res的==，因此最终的字符串res应该为 res = prev_res + prev_multi * res',
        quote_src='—— yiduobo 题解',
        idea=['从左往右一趟扫描，当前字符分四种情况：',
              '数字 → 更新 `multi`；字母 → 更新 `res`',
              '`[` → `[res, multi]` 压栈并重置；`]` → 弹栈结算'],
        result='`"a2[b2[c]]"` 解码为 `"abccbcc"` ✓',
        summary=['一趟扫描，栈的深度 = 括号嵌套层数',
                 '易错：压栈的 multi 修饰的是==括号里的== res，不是 prev_res',
                 '易错：压栈后 `res`、`multi` 都要重置；多位数要 `multi * 10` 累加',
                 '`ord` 判断 48~57 等价于 `char.isdigit()`',
                 '原文为 Python 2 写法：仅删去文档字符串，逻辑未改'],
    ),
)
