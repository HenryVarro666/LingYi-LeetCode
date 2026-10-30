def _fmt(lst):
    return ' '.join(f'{c}×{n}' for c, n in lst) if lst else '（空）'


def _top(S):
    if 'name_list' not in S:
        return ''
    t = f"name 收缩：`{_fmt(S['name_list'])}`"
    if 'typed_list' in S:
        t += f"　　typed 收缩：`{_fmt(S['typed_list'])}`"
    return t


def _cmp(S):
    if 'index' not in S or 'typed_list' not in S:
        return ''
    i = S['index']
    a, b = S['name_list'][i], S['typed_list'][i]
    return f"第 {i} 组：name `{a[0]}×{a[1]}` 对 typed `{b[0]}×{b[1]}`"


def _done(S, i, which):
    if 'name_list' not in S:
        return None
    if which == 'name':
        k = len(S['name']) if 'typed_list' in S else sum(c for _, c in S['name_list']) + S['now_cnt']
    else:
        if 'typed_list' not in S:
            return None
        k = sum(c for _, c in S['typed_list']) + S['now_cnt']
    return 'green' if i < k else None


CONFIG = dict(
    num=925, title='长按键入', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='连续字符收缩 + 计数比较',
    tags=['滑动窗口与双指针'],
    code='''
class Solution(object):
    def isLongPressedName(self, name, typed):

        now_char = None
        now_cnt = 0
        name_list = []
        for char in name:
            if char == now_char:
                now_cnt += 1
            else:
                if now_char is not None:
                    name_list.append([now_char, now_cnt])
                now_char = char
                now_cnt = 1

        name_list.append([now_char, now_cnt])

        now_char = None
        now_cnt = 0
        typed_list = []
        for char in typed:
            if char == now_char:
                now_cnt += 1
            else:
                if now_char is not None:
                    typed_list.append([now_char, now_cnt])
                now_char = char
                now_cnt = 1
        
        typed_list.append([now_char, now_cnt])

        if len(name_list) != len(typed_list):
            return False

        for index in range(len(name_list)):
            if name_list[index][0] != typed_list[index][0]:
                return False
            if name_list[index][1] > typed_list[index][1]:
                return False
        
        return True
''',
    call="Solution().isLongPressedName('saeed', 'ssaaedd')",
    expect=False,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='name', label='name', h=190, cell=70, color=lambda S, i, v: _done(S, i, 'name')),
        dict(type='string', var='typed', label='typed', h=190, cell=70, color=lambda S, i, v: _done(S, i, 'typed')),
        dict(type='text', fn=_cmp, size=28),
    ],
    watch=['char', 'now_char', 'now_cnt', 'index'],
    captions={
        'now_char = None': '`now_char` 记录当前这一段的字符，`None` 表示还没开始',
        'now_cnt = 0': '`now_cnt` 记录当前这一段已经连续出现几次',
        'name_list = []': '`name_list` 收集 name 的 ==[字符, 连续次数]==',
        'typed_list = []': '`typed_list` 收集 typed 的 ==[字符, 连续次数]==',
        'for char in name': lambda S, B, r: ('name 的字符都看完了' if sum(c for _, c in S.name_list) + S.now_cnt == len(S.name) else f'看 name 的下一个字符 `{S.char}`'),
        'for char in typed': lambda S, B, r: ('typed 的字符都看完了' if sum(c for _, c in S.typed_list) + S.now_cnt == len(S.typed) else f'看 typed 的下一个字符 `{S.char}`'),
        'if char == now_char': lambda S, B, r: (f"`'{S.char}' == '{S.now_char}'`：和上一个相同，属于同一段" if S.char == S.now_char
                                                else f"`'{S.char}' != '{S.now_char}'`：换了字符，上一段结束"),
        'now_cnt += 1': '同一段 +1：`now_cnt` = {now_cnt}',
        'if now_char is not None': lambda S, B, r: ('`now_char` 不是 None：说明上一段有内容，要收进列表' if S.now_char is not None
                                                    else '`now_char` 是 None：这是第一个字符，没有上一段'),
        'name_list.append([now_char, now_cnt])': lambda S, B, r: (f'循环结束，最后一段还没收进去，补上 `{S.now_char}×{S.now_cnt}`' if S._line == 16 else f'把上一段收进列表：`{B.now_char}×{B.now_cnt}`'),
        'typed_list.append([now_char, now_cnt])': lambda S, B, r: (f'循环结束，补上 typed 的最后一段 `{S.now_char}×{S.now_cnt}`' if S._line == 30 else f'把上一段收进列表：`{B.now_char}×{B.now_cnt}`'),
        'now_char = char': '开始新的一段：`now_char = {now_char}`',
        'now_cnt = 1': '这一段先出现 1 次',
        'if len(name_list) != len': lambda S, B, r: (f'段数 `{len(S.name_list)}` 和 `{len(S.typed_list)}` 不同：收缩后字符串不一致 → 不可能' if len(S.name_list) != len(S.typed_list)
                                                      else f'段数都是 `{len(S.name_list)}`：收缩后长度一致，再逐段比'),
        'for index in range': '比较第 `{index}` 段',
        'if name_list[index][0] != ': lambda S, B, r: (f"字符 `{S.name_list[S.index][0]}` != `{S.typed_list[S.index][0]}` → 收缩后字符串不同" if S.name_list[S.index][0] != S.typed_list[S.index][0]
                                                         else f"字符都是 `{S.name_list[S.index][0]}`，一致"),
        'if name_list[index][1] > ': lambda S, B, r: (f"name 要连按 `{S.name_list[S.index][1]}` 次，typed 只按了 `{S.typed_list[S.index][1]}` 次：==typed 次数不够，不可能== → False" if S.name_list[S.index][1] > S.typed_list[S.index][1]
                                                       else f"name `{S.name_list[S.index][1]}` 次 <= typed `{S.typed_list[S.index][1]}` 次：长按可以多，没问题"),
        'return False': '不满足条件，返回 `False`',
        'return True': '每一段都满足 → `True`',
    },
    cards=dict(
        one_liner='把连续重复字符收缩成「字符×次数」，再逐段比较',
        complexity='时间 `O(n+m)`，空间 `O(n+m)`',
        problem=['键盘输入 `name`，某些字符可能被长按而重复多次得到 `typed`',
                 '判断 `typed` 是否可能是 `name` 的键入结果',
                 '本视频：`name = saeed`、`typed = ssaaedd` → `False`'],
        quote='我们可以将name和typed的连续重复字符进行收缩，并统计其出现的次数。那么如果typed可以与name对应，那么二者收缩后的字符串必然完全一致，同时对于每个字符而言，typed中的出现次数必然要大于等于name中出现的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['先各自收缩成 `[字符, 次数]` 的列表',
              '条件一：两个列表的 ==字符序列完全一致==（段数相同、字符相同）',
              '条件二：每一段 `typed` 的次数 ==不小于== `name` 的次数'],
        summary=['时间、空间都是 `O(n+m)`',
                 '循环结束要补上最后一段，不然漏掉末尾字符',
                 '本例 `saeed` 的 `ee` 要 2 次，typed 里只有 1 次 `e`，所以 False',
                 '次数只能多不能少；字符和顺序必须一致',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
