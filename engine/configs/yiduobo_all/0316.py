CODE = '''
class Solution(object):
    def removeDuplicateLetters(self, s):

        char_counts = {}
        for char in s:
            char_counts[char] = char_counts.get(char, 0) + 1

        res = []
        in_stack = set()

        for char in s:
            if char not in in_stack:
                while res and char_counts[res[-1]] > 0 and res[-1] > char:
                    in_stack.remove(res.pop())
                res.append(char)
                in_stack.add(char)
            char_counts[char] -= 1

        return ''.join(res)
'''
_L = CODE.strip('\n').split('\n')
LN_FOR2 = [i for i, l in enumerate(_L, 1) if l.strip() == 'for char in s:'][1]
LN_DEC = [i for i, l in enumerate(_L, 1) if '-= 1' in l][0]


def _idx(S):
    """当前处理第几个字符（计数在循环末尾才减，所以 -= 1 之前 done=i，之后 done=i+1）"""
    if 'in_stack' not in S or S['_line'] < LN_FOR2 or 'char' not in S:
        return None
    done = len(S['s']) - sum(S['char_counts'].values())
    i = done if S['_line'] < LN_DEC else done - 1
    return i if 0 <= i < len(S['s']) else None


def _show(S):
    if 'res' not in S or 'in_stack' not in S:
        return '先数每个字母出现几次，再用栈挑字符'
    i = _idx(S)
    r = ''.join(S['res'])
    if i is None:
        return f'栈 `res = "{r}"`'
    c = S['char']
    if S['res'] and c not in S['in_stack'] and S['_line'] < LN_DEC:
        t = S['res'][-1]
        return f'当前 `{c}`　栈顶 `{t}`　`{t}` 后面还剩 ==`{S["char_counts"][t]}`== 个'
    return f'当前 `{c}`　栈 `"{r}"`'


def _while(S, B, ret):
    r, c, cc = S.res, S.char, S.char_counts
    if not r:
        return '栈空了 → 不再弹，准备压入当前字符'
    t = r[-1]
    if t > c and cc[t] > 0:
        return f'栈顶 `{t}` > 当前 `{c}`，且它后面还剩 `{cc[t]}` 个 → ==弹掉它，后面还能补回来=='
    if t > c:
        return f'栈顶 `{t}` > 当前 `{c}`，但它后面没有了 → ==落单不能弹==，停止'
    return f'栈顶 `{t}` < 当前 `{c}`，栈已经递增 → 停止'


CONFIG = dict(
    num=316, title='去除重复字母', difficulty='Medium', category='单调栈',
    author='yiduobo', technique='贪心 · 栈 + 剩余次数',
    tags=['最小字典序', '难度分 2185'],
    code=CODE,
    call='Solution().removeDuplicateLetters("bdabcdb")',
    expect='abcd',
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前字符，灰 = 已处理）', cell=96, h=215,
             pointers={_idx: 'blue'}, pointer_labels={_idx: 'char'},
             dim=lambda S, i, v: _idx(S) is not None and i < _idx(S),
             color=lambda S, i, v: 'blue' if i == _idx(S) else None),
        dict(type='stack', var='res', label='res（栈，栈顶在右）', h=150, font=34),
        dict(type='map', var='char_counts', label='char_counts（后面还剩几个，处理完才减）', fmt=lambda k, v: f"'{k}': {v}", h=160, font=30),
        dict(type='text', fn=_show, size=28, h=90),
    ],
    watch=[('char', 'char', 'blue'), ('res', "''.join(res)", 'green'), ('in_stack', 'sorted(in_stack)', 'cyan')],
    captions={
        'char_counts = {}': '先准备一个哈希表，统计每个字符出现的次数',
        'char_counts[char] = char_counts.get': lambda S, B, ret: f'统计：`{S.char}` 出现 `{S.char_counts[S.char]}` 次',
        'res = []': '`res` 当栈用，从左往右挑字符',
        'in_stack = set()': '`in_stack` 记录哪些字符已在栈里',
        'for char in s': lambda S, B, ret: (f'扫描 `{S.char}`' if _idx(S) is not None else ('扫描结束' if 'in_stack' in S else '统计完毕' if sum(S.char_counts.values()) == len(S.s) else f'数一遍：`{S.char}`')),
        'if char not in in_stack': lambda S, B, ret: (f'`{S.char}` 不在栈中 → 要考虑放进去' if S.char not in S.in_stack
                                                       else f'`{S.char}` 已经在栈里了 → 跳过，只减计数'),
        'while res': _while,
        'in_stack.remove': '弹出 `{B.res[-1]}` 并标记不在栈里：后面还有它，之后会重新放回',
        'res.append(char)': lambda S, B, ret: f'`{S.char}` 压栈 → `res = "{"".join(S.res)}"`',
        'in_stack.add(char)': '标记 `{char}` 已在栈中',
        'char_counts[char] -= 1': lambda S, B, ret: f'`{S.char}` 处理完了，它后面还剩 `{S.char_counts[S.char]}` 个',
        'return': '栈里每个字符各一个，字典序最小：`"{ret}"`',
    },
    cards=dict(
        one_liner='前面的字符比后面的大，且后面还有 → 前面的必须删',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`',
        problem=['去掉重复字符，==每种只留一个==，结果字典序最小',
                 '不能打乱其余字符的相对顺序',
                 '示例：`"cbacdcbc"` → `"acdb"`；本视频：`"bdabcdb"` → `"abcd"`'],
        quote='若其中某个字符p的左边一位字符q满足q > p，且q在p右侧再次出现过，那么此时p左侧的q必然是要删除的。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想什么时候必须删：左边的 `q` 比 `p` 大，右边还会再出现 `q`',
              '从左往右扫，用栈维护：当前字符小于栈顶且栈顶还有剩余 → 弹栈',
              '压栈前保证栈里没有它；这样每个字符各一个且字典序最小'],
        summary=['时间 `O(n)`，空间 `O(|Σ|)`',
                 '`char_counts` 表示当前位置之后还剩几个，处理完才减一',
                 '易错：已在栈中的字符直接跳过，但仍要把计数减一',
                 '原文本来就是 Python 3 可运行的写法，代码未改动',
                 '对比灵神：灵神一进循环先减 left；yiduobo 在循环末尾才减'],
    ),
)
