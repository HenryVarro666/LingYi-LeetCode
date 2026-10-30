TRACK = '''
class Tracked(str):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k, ch in enumerate(str.__iter__(self)):
            self.k = k
            yield ch
        self.k = None
'''


def _k(S):
    k = getattr(S.get('s'), 'k', None)
    return k if isinstance(k, int) else None


def _top(S):
    if 'b_flag' not in S:
        return ''
    return '`b_flag = ' + str(S['b_flag']) + '`：' + ('已经见过 b，之后不能再出现 a' if S['b_flag'] else '还没见过 b，a 随便出现')


def _if_a(S, B, ret):
    c = S.char
    if c == 'a' and S.b_flag:
        return f"`char = 'a'` 且 `b_flag` 为真：==这个 a 前面有 b== → 马上返回 False"
    if c == 'a':
        return "`char = 'a'`，但 `b_flag` 为 False：前面还没有 b，没问题"
    return f"`char = '{c}'`，不是 a，不需要检查"


CONFIG = dict(
    num=2124, title='检查是否所有 A 都在 B 之前', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟遍历 · b_flag 标记',
    tags=[],
    code='''
class Solution(object):
    def checkString(self, s):

        b_flag = False
        for char in s:
            if char == 'a' and b_flag:
                return False
            elif char == 'b':
                b_flag = True

        return True
''',
    setup=TRACK,
    call='Solution().checkString(Tracked("aabbab"))',
    expect=False,
    views=[
        dict(type='text', fn=_top, size=28),
        dict(type='string', var='s', label='s（箭头 = 当前字符，粉 = 第一个 b）', cell=90, pointers={'s.k': 'blue'}, pointer_labels={'s.k': 'char'}, h=200,
             color=lambda S, i, v: ('pink' if (S.get('b_flag') and v == 'b' and i == S['s'].index('b') and (_k(S) is None or i <= _k(S)))
                                    else 'blue' if i == _k(S) else None)),
        dict(type='text', fn=lambda S: '目标：所有 `a` 都排在所有 `b` 前面，即 ==出现 b 之后不能再有 a==', size=24),
    ],
    watch=[('b_flag', 'b_flag', 'orange'), ('char', 'char', 'blue')],
    captions={
        'b_flag = False': '`b_flag` 记录：==到目前为止有没有见过 b==，一开始没有',
        'for char in s': lambda S, B, ret: (f"取下一个字符 `char = '{S.char}'`" if _k(S) is not None else '遍历完了，没有遇到“b 之后再出现 a”'),
        "if char == 'a' and b_flag": _if_a,
        'return False': '有 b 出现在这个 a 之前 → 不满足“所有 a 在所有 b 之前”，返回 `False`',
        "elif char == 'b'": lambda S, B, ret: ("`char = 'b'` → 成立" if S.char == 'b' else f"`char = '{S.char}'` 不是 b → 不成立，什么都不做"),
        'b_flag = True': '遇到 b：`b_flag = True`，从现在起不允许再出现 a',
        'return True': '整个字符串遍历完都没有 a 跟在 b 后面 → 返回 `True`',
    },
    cards=dict(
        one_liner='用一个标记记住“见过 b 没有”，见过 b 之后再遇到 a 就失败',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串 `s` 只含 `a` 和 `b`，判断是否==每个 a 都在每个 b 之前==',
                 '示例：`"aaabbb"` → `true`；`"abab"` → `false`；`"bbb"` → `true`（没有 a）',
                 '本视频：`"aabbab"` → `false`'],
        quote='使用一个变量b_flag记录当前是否有b出现过，初始化为false，接下来从左向右一趟遍历。若当前字符为a且b_flag为true，那么说明有b出现在当前的a之前，此时直接返回false。',
        quote_src='—— yiduobo 题解原文',
        idea=['从左往右扫，`b_flag` 记录前面有没有 b',
              '遇到 b 就把标记置 True；遇到 a 时若标记已为 True，说明有 b 在它前面',
              '一直没触发就是合格的，返回 True'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '没有 a（如 `"bbb"`）或没有 b 时都返回 True',
                 '等价于：字符串里不能出现子串 `"ba"`',
                 '原文是 Python 2 风格的 `class Solution(object)`，只删去了类型说明文档字符串，代码无其他改动'],
    ),
)
