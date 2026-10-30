S_IN, T_IN = 'abca', 'acbac'


def _pos(S):
    """(which string, index) currently being processed, derived from the counts"""
    ln = S.get('_line')
    d = S.get('char_dict')
    if d is None or ln is None:
        return None, None
    tot = sum(d.values())
    if ln == 4:
        return 't', tot
    if ln == 5:
        return 't', tot - 1
    if ln == 6:
        return 's', len(S['t']) - tot
    if ln == 7:
        return 's', len(S['t']) - tot - 1
    return None, None


def _strings(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    which, idx = _pos(S)
    ln = S.get('_line') or 0
    cell = 84
    for r, (nm, txt) in enumerate((('t', S.get('t', T_IN)), ('s', S.get('s', S_IN)))):
        Y = y0 + 20 + r * 150
        cv.text((x0 + 18, Y), f'{nm}（{"计数 +1" if nm == "t" else "计数 −1"}）', 24, T['muted'], bold=True)
        sx = x0 + 120
        for k, ch in enumerate(txt):
            X = sx + k * cell
            if nm == which and k == idx:
                fill, tc = T['blue'], T['bg']
            elif (nm == 't' and (ln >= 6 or (which == 't' and k < idx))) or (nm == 's' and (ln >= 9 or (which == 's' and k < idx))):
                fill, tc = (T['green'] if nm == 't' else T['pink']), T['bg']
            else:
                fill, tc = T['panel2'], T['text']
            if ln >= 9 and S.get('char') == ch and nm == 't':
                fill, tc = T['yellow'], T['bg']
            cv.rect((X + 4, Y + 36, X + cell - 4, Y + 36 + 72), fill=fill, r=10, outline=T['border'])
            cv.text((X + cell / 2, Y + 72), ch, 36, tc, anchor='mm', bold=True, mono=True)
            cv.text((X + cell / 2, Y + 114), k, 18, T['dim'], anchor='mt', mono=True)
            if nm == which and k == idx:
                cv.tri_up(X + cell / 2, Y + 136, 9, T['blue'])


def _note(S):
    ln = S.get('_line')
    d = S.get('char_dict')
    if ln in (9, 10, 11) and S.get('char') is not None:
        c = S['char']
        return f"检查 `char_dict['{c}'] = {d[c]}`" + (' > 0 → ==多出来的就是它==' if d[c] > 0 else '：两边一样多')
    if ln in (6, 7):
        return '第二遍：`s` 里每出现一次就 −1，抵消掉 `t` 里相同的字母'
    if ln in (3, 4, 5):
        return '第一遍：统计 `t` 中每个字母出现的次数'
    return ''


CONFIG = dict(
    num=389, title='找不同', difficulty='Easy', category='哈希',
    author='yiduobo', technique='哈希计数：t 加 s 减',
    tags=['字节30天'],
    code='''
class Solution(object):
    def findTheDifference(self, s, t):
        char_dict = {}
        for char in t:
            char_dict[char] = char_dict.get(char, 0) + 1
        for char in s:
            char_dict[char] -= 1

        for char in char_dict:
            if char_dict[char] > 0:
                return char
''',
    call=f'Solution().findTheDifference({S_IN!r}, {T_IN!r})',
    expect='c',
    views=[
        dict(type='text', fn=_note, h=60),
        dict(type='custom', draw=_strings, h=320),
        dict(type='map', var='char_dict', label='char_dict（字母 → t 比 s 多出现几次）', font=30, h=150,
             fmt=lambda k, v: f"'{k}': {v}"),
    ],
    watch=[('char', 'char', 'blue')],
    captions={
        'char_dict = {}': '`char_dict` 记录每个字母的出现次数',
        'for char in t': lambda S, B, ret: (f"取 `t` 的下一个字母 `'{S.char}'`" if _pos(S)[1] < len(S.t) else '`t` 统计完毕'),
        'char_dict[char] = char_dict.get': "`char_dict['{char}']` = `{B.char_dict.get(char, 0)} + 1` = =={char_dict[char]}==",
        'for char in s': lambda S, B, ret: (f"取 `s` 的下一个字母 `'{S.char}'`" if _pos(S)[1] < len(S.s) else '`s` 抵消完毕'),
        'char_dict[char] -= 1': "`'{char}'` 在 `s` 里也有 → 抵消一次：`char_dict['{char}']` = =={char_dict[char]}==",
        'for char in char_dict': "看字母 `'{char}'`",
        'if char_dict[char] > 0': lambda S, B, ret: (f"`char_dict['{S.char}'] = {S.char_dict[S.char]}` > 0 → 找到了"
                                                     if S.char_dict[S.char] > 0 else f"`char_dict['{S.char}'] = 0`：两边一样多"),
        'return char': "多出来的字母是 =={ret}==",
    },
    cards=dict(
        one_liner='t 中字母计数 +1，s 中字母计数 −1，剩下 1 的就是多出来的',
        complexity='时间 `O(n)`，空间 `O(Σ)`（Σ = 26）',
        problem=['字符串 `t` 由 `s` 随机重排后，再在随机位置添加==一个==字母得到',
                 '找出 `t` 中被添加的那个字母',
                 '示例：`s = "abcd"`，`t = "abcde"` → `"e"`',
                 f'本视频：`s = "{S_IN}"`，`t = "{T_IN}"` → `"c"`（多的字母和已有字母重复）'],
        quote='比较基础的题目，直接统计两个字符串中各个字符出现的次数即可。当然也可以将题目看成两个数字串，找出出现奇数次的那个数字，因此也可以通过异或来解决问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历 `t`：每个字母计数 +1',
              '遍历 `s`：每个字母计数 −1，和 `t` 里相同的字母互相抵消',
              '最后计数 ==大于 0== 的字母就是被添加的那个'],
        summary=['时间 `O(|s| + |t|)`，空间 `O(26)`',
                 '先遍历 `t` 再遍历 `s`：`s` 的字母一定在 `t` 里，`-= 1` 不会出现 KeyError',
                 '多出的字母可能和已有字母相同（如本例的 `c`），所以要比较次数，不能只看「有没有」',
                 '另一种写法：把两个串所有字符异或起来，成对的抵消，剩下的就是答案',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
