S0 = 'dbcb*b*c*'


def _scolor(S, k, v):
    rm = S.get('remove', set())
    if k in rm and S0[k] != '*':
        return 'red'
    if S.get('index') == k:
        return 'yellow' if S0[k] == '*' else 'blue'
    return None


def _txt(S):
    if S.get('_line', 0) >= 12 and 'asc' in S and 'c' in S and S.get('index') is not None and S0[S['index']] == '*':
        return f'从 `a` 往 `z` 找第一个还有剩余的字母：现在看 `{S["c"]}`'
    return '`pos[字母]` = 这个字母剩余的下标（越靠后越在末尾）；`remove` = 要删掉的下标'


CONFIG = dict(
    num=3170, title='删除星号以后字典序最小的字符串', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='字母 → 下标列表 + 删最靠后的最小字母',
    tags=['常用数据结构', '贪心与思维', '难度分 1772'],
    code='''
class Solution(object):
    def clearStars(self, s):

        pos = {}
        remove = set()
        for index, char in enumerate(s):
            if 'a' <= char <= 'z':
                if char not in pos:
                    pos[char] = []
                pos[char].append(index)
            else:
                for asc in range(97, 123):
                    c = chr(asc)
                    if c in pos and len(pos[c]) > 0:
                        remove.add(pos[c][-1])
                        pos[c].pop()
                        break
            
                remove.add(index)
        
        return ''.join([s[index] if index not in remove else '' for index in range(len(s))])
''',
    call=f'Solution().clearStars({S0!r})',
    expect='dcc',
    skip=['for asc in range'],
    max_steps=90,
    views=[
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='array', var='s', label='s（红 = 已标记删除；黄 = 当前的 *；蓝 = 当前字母）', cell=76, h=190,
             pointers={'index': 'blue'}, color=_scolor) if False else
        dict(type='string', var='s', label='s（红 = 已标记删除；黄 = 当前的 *；蓝 = 当前字母）', cell=76, h=190,
             pointers={'index': 'blue'}, color=_scolor),
        dict(type='map', var='pos', label='pos（字母 → 剩余下标，列表末尾 = 最靠后的）', h=230,
             fmt=lambda k, v: f"{k}: {v}"),
        dict(type='set', var='remove', label='remove（要删除的下标，包括星号自己）', h=150, fmt=lambda x: str(x)),
    ],
    watch=['index', ('char', 'char', 'blue'), ('asc', 'asc', 'cyan'), ('c', 'c', 'pink')],
    captions={
        'pos = {}': '`pos[字母]` 记录这个字母在 `s` 里出现过、还没被删的下标',
        'remove = set()': '`remove` 记录最终要删掉的下标',
        "if 'a' <= char": lambda S, B, r: (f'`{S.char}` 是小写字母 → 记录它的位置' if 'a' <= S.char <= 'z'
                                           else '`*`：要删掉它左边==字典序最小==的字母'),
        'if char not in pos': lambda S, B, r: (f'`{S.char}` 第一次出现，先建一个空列表' if S.char not in S.pos
                                               else f'`{S.char}` 之前出现过，列表已有 `{S.pos[S.char]}`'),
        'pos[char] = []': '`pos["{char}"] = []`',
        'pos[char].append': '下标 `{index}` 加到 `pos["{char}"]` 末尾 → `{pos[char]}`：==越靠后的下标越在末尾=='.replace('==越靠后的下标越在末尾==', '末尾是最靠后的'),
        'c = chr(asc)': lambda S, B, r: ('`*` 要删最小的字母：从 `a` 往 `z` 依次找，第一个还有剩余下标的就是它。' if S.asc == 97 else '') + f'看字母 `{S.c}`',
        'if c in pos': lambda S, B, r: ((f'`{S.c}` 还有下标 `{S.pos[S.c]}` → 它就是最小字母' if S.c in S.pos and len(S.pos[S.c]) > 0
                                        else f'`{S.c}` 没出现过或已删光 → 看下一个字母')),
        'remove.add(pos[c][-1])': lambda S, B, r: (f'最小字母 `{S.c}` 有多个 `{S.pos[S.c]}`：删==下标最靠后==的 `{S.pos[S.c][-1]}`（列表末尾），前面保留更多小字母，字典序更小' if len(S.pos[S.c]) > 1 else f'最小字母 `{S.c}` 只剩一个 `{S.pos[S.c]}`，删掉它'),
        'pos[c].pop()': '把它从 `pos["{c}"]` 末尾弹出 → `{pos[c]}`',
        'break': '已经删掉一个最小字母，不再往后找',
        'remove.add(index)': '`*` 自己（下标 `{index}`）也要删掉',
        'return ': lambda S, B, r: f'没被标记的字母按原顺序连起来 = =={r}=='.replace('{r}', str(r)),
    },
    cards=dict(
        one_liner='最小字母有多个，删下标最靠后的，让小字母尽量留在前面',
        complexity='时间 `O(26n)`，空间 `O(n)`',
        problem=['字符串 `s` 含小写字母和 `*`，从左到右处理每个 `*`',
                 '处理时：删掉这个 `*` 和它左边==字典序最小==的一个字母',
                 '求删完以后字典序最小的字符串',
                 '本视频：`"dbcb*b*c*"` → `"dcc"`'],
        quote='为了使得最终答案的字典序最小，就应该让字典序小的字符尽量靠前，那么在这里就应该删掉字典序最小的字符中==下标最靠后的那个==。',
        quote_src='—— yiduobo 题解原文',
        idea=['`pos[字母]` 记下每种字母出现的下标，新下标追加在末尾，所以末尾就是最靠后的',
              '遇到 `*`：从 `a` 扫到 `z`，第一个有剩余下标的字母最小，删它末尾那个下标',
              '星号自己也加入 `remove`；最后过滤掉 `remove` 里的下标'],
        summary=['时间 `O(26n)`：每个 `*` 最多扫 26 个字母；空间 `O(n)`',
                 '易错：星号自己的下标也要放进 `remove`',
                 '易错：同一字母删最靠后的，不是最靠前的（删前面的会让大字母前移）',
                 '原文是 Python 2 风格的写法，在 Python 3 下无需修改，代码未改',
                 '对比灵神：他用 26 个栈 + `mask & -mask` 在 `O(1)` 找最小字母；这里直接扫 a~z'],
    ),
)
