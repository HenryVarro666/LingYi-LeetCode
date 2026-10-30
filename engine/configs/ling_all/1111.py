SEQ = '(()(()))'


def _depth(seq, i):
    """第 i 个括号的深度（左括号：左侧未闭合左括号数；右括号：含自己所配的那个）"""
    d = 0
    for k in range(i):
        d += 1 if seq[k] == '(' else -1
    return d if seq[i] == '(' else d - 1


def _info(S):
    if 'i' not in S:
        return '把括号序列拆成 A、B 两组，让最大嵌套深度最小'
    seq, i = S['seq'], S['i']
    dp = _depth(seq, i)
    kind = '左括号' if seq[i] == '(' else '右括号'
    return f'`seq[{i}]` 是{kind}，深度 =={dp}== → 深度 {dp} 的奇偶性 `{dp % 2}`（0 → A，1 → B）'


def _col(S, i, v):
    if 'ans' not in S:
        return None
    if i == S.get('i', -1):
        return 'yellow'
    if i < S.get('i', -1):
        return 'cyan' if S['ans'][i] == 0 else 'orange'
    return None


CONFIG = dict(
    num=1111, title='有效括号的嵌套深度', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='按深度奇偶性拆分',
    tags=['栈', '合法括号字符串', '难度分 1749'],
    code='''
class Solution:
    def maxDepthAfterSplit(self, seq: str) -> List[int]:
        ans = [0] * len(seq)
        for i, ch in enumerate(seq):
            ans[i] = (i + ord(ch)) % 2
        return ans
''',
    call=f'Solution().maxDepthAfterSplit({SEQ!r})',
    expect=[0, 1, 1, 1, 0, 0, 1, 0],
    views=[
        dict(type='text', fn=_info, size=26, h=90),
        dict(type='string', var='seq', label='seq（黄 = 当前括号，青 = 分到 A，橙 = 分到 B）', pointers={'i': 'blue'}, color=_col, cell=90, h=200),
        dict(type='array', var='ans', label='ans（0 = A，1 = B）', cell=90, h=200,
             color=lambda S, i, v: 'yellow' if i == S.get('i', -1) else None),
        dict(type='text', fn=lambda S: ('`(i + ord(ch)) % 2`：`i` 的奇偶 + 括号 ASCII 的奇偶；`(` = 40 偶，`)` = 41 奇' if 'i' in S else ''), size=24, h=80),
    ],
    watch=[('i', 'i', 'blue'), ('ch', 'ch', 'yellow'), ('ord(ch)', 'ord(ch)', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = [0]': '先造一个全 0 的结果数组，长度和 `seq` 一样',
        'for i, ch': lambda S, B, ret: ('所有字符都分配完了，循环结束' if 'i' in B and B.i == S.i else f'枚举第 `{S.i}` 个字符 `{S.ch}`，它的深度是 =={_depth(S.seq, S.i)}=='),
        'ans[i] =': '`ans[{i}] = ({i} + {ord(ch)}) % 2` = =={ans[i]}==：深度奇偶 = 下标与括号 ASCII 的奇偶之和，==免去维护 depth==',
        'return ans': '偶数深度进 A、奇数深度进 B，返回 `{ret}`',
    },
    cards=dict(
        one_liner='把括号的深度按奇偶性分到 A、B，两边深度各减半',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计）',
        problem=['把有效括号序列拆成两个子序列 A、B，使两者都是有效括号串',
                 '要让 `max(depth(A), depth(B))` 最小，返回每个位置属于 A(0) 还是 B(1)',
                 '示例：`"(()())"` → `[0,1,1,1,1,0]`'],
        quote='更好的做法是按照深度的奇偶性拆分，偶数深度分到 A 中，奇数深度分到 B 中，这样只需一次遍历。',
        quote_src='—— 灵茶山艾府题解',
        idea=['套娃类比：均分最好，把偶数层分一组、奇数层分另一组',
              '左括号深度 `= i - 2R`，奇偶性和 `i` 相同；右括号深度奇偶性和 `i+1` 相同',
              '`(` 的 ASCII 是 40（偶）、`)` 是 41（奇），所以答案就是 `(i + ord(ch)) % 2`'],
        result='返回 `[0,1,1,1,0,0,1,0]`：A = `(())`，B = `()()`，深度 2 和 1，比原来的 3 小',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '写法一维护 `depth` 变量；写法二用 `i` 的奇偶推出深度奇偶',
                 '写法三（本视频）：再用 ASCII 的奇偶合并左右括号的两种情况',
                 '易错：右括号的深度要把它自己算上，所以先 `depth -= 1` 再取模'],
    ),
)
