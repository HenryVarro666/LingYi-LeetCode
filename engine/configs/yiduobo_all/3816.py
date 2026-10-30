CODE = '''
class Solution(object):
    def lexSmallestAfterDeletion(self, s):
        
        cnt = {}
        for c in s:
            cnt[c] = cnt.get(c, 0) + 1
        
        stack = []
        for c in s:
            while stack and c < stack[-1] and cnt[stack[-1]] > 1:
                cnt[stack.pop()] -= 1
            stack.append(c)
        
        while stack and cnt[stack[-1]] > 1:
            cnt[stack.pop()] -= 1
        
        return ''.join(stack)
'''
_L = CODE.strip('\n').split('\n')
LN_APP = [i for i, l in enumerate(_L, 1) if 'stack.append(c)' in l][0]
LN_TAIL = [i for i, l in enumerate(_L, 1) if l.strip().startswith('while stack and cnt[stack[-1]] > 1')][0]


def _idx(S):
    """已处理个数 = 栈里的 + 已删掉的（cnt 总和每删一个少 1）"""
    if 'stack' not in S or 'c' not in S or S['_line'] >= LN_TAIL:
        return None
    done = len(S['stack']) + len(S['s']) - sum(S['cnt'].values())
    i = done if S['_line'] < LN_APP else done - 1
    return i if 0 <= i < len(S['s']) else None


def _show(S):
    if 'stack' not in S:
        return '`cnt[x]` = x 现在的总个数；大于 1 的才不算「落单」'
    t = ''.join(S['stack'])
    if S['_line'] >= LN_TAIL:
        if S['stack']:
            x = S['stack'][-1]
            return f'清尾　栈 `"{t}"`　栈顶 `{x}` 共 ==`{S["cnt"][x]}`== 个'
        return '栈空了'
    if _idx(S) is not None and S['stack'] and S['_line'] < LN_APP:
        x = S['stack'][-1]
        return f'当前 `{S["c"]}`　栈顶 `{x}`（`cnt = {S["cnt"][x]}`）'
    return f'栈 `"{t}"`'


def _while(S, B, ret):
    c, st, cnt = S.c, S.stack, S.cnt
    if not st:
        return '栈空了，停止弹栈'
    x = st[-1]
    if c < x and cnt[x] > 1:
        return f'栈顶 `{x}` > `{c}`，且 `{x}` 不落单（共 {cnt[x]} 个）→ ==弹掉栈顶，让小字符靠前=='
    if c < x:
        return f'栈顶 `{x}` > `{c}`，但 `{x}` ==落单==，不能删，停止'
    return f'栈顶 `{x}` ≤ `{c}`，删了不会更优 → 停止'


def _tail(S, B, ret):
    if not S.stack:
        return '栈空了，结束'
    x = S.stack[-1]
    if S.cnt[x] > 1:
        return f'末尾 `{x}` 重复出现（共 {S.cnt[x]} 个）→ ==删掉，字符串更短==，字典序更小'
    return f'末尾 `{x}` 落单，必须保留 → 停止'


CONFIG = dict(
    num=3816, title='删除重复字符后的字典序最小字符串', difficulty='Hard', category='单调栈',
    author='yiduobo', technique='贪心 · 栈 + 落单判断',
    tags=['最小字典序', '难度分 2377'],
    code=CODE,
    call='Solution().lexSmallestAfterDeletion("cbaabcb")',
    expect='aabc',
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前字符 c，灰 = 已处理）', cell=96, h=215,
             pointers={_idx: 'blue'}, pointer_labels={_idx: 'c'},
             dim=lambda S, i, v: _idx(S) is not None and i < _idx(S),
             color=lambda S, i, v: 'blue' if i == _idx(S) else None),
        dict(type='stack', var='stack', label='stack（栈，栈顶在右）', h=150, font=34),
        dict(type='map', var='cnt', label='cnt（每个字符现在的总个数）', fmt=lambda k, v: f"'{k}': {v}", h=160, font=30),
        dict(type='text', fn=_show, size=28, h=90),
    ],
    watch=[('c', 'c', 'blue'), ('stack', "''.join(stack)", 'green')],
    captions={
        'cnt = {}': '先准备哈希表 `cnt`，统计每种字符的个数',
        'cnt[c] = cnt.get': lambda S, B, ret: f'`{S.c}` 目前共 `{S.cnt[S.c]}` 个',
        'stack = []': '`stack` 记录留下来的字符',
        'for c in s': lambda S, B, ret: (f'扫描第 `{_idx(S)}` 个字符 `{S.c}`' if _idx(S) is not None
                                         else ('扫描结束，去清理末尾' if 'stack' in S else ('统计完毕' if sum(S.cnt.values()) == len(S.s) else f'数一数：`{S.c}`'))),
        'while stack and c <': _while,
        'cnt[stack.pop()] -= 1': lambda S, B, ret: (f'弹出 `{B.stack[-1]}`，它的总个数变成 `{S.cnt[B.stack[-1]]}`' if B.stack else '弹出栈顶'),
        'stack.append(c)': lambda S, B, ret: f'`{S.c}` 压栈 → `stack = "{"".join(S.stack)}"`',
        'while stack and cnt[stack[-1]] > 1': _tail,
        'return': '栈里剩下的字符就是答案 `"{ret}"`',
    },
    cards=dict(
        one_liner='删字符前先看：它不落单，且后面紧跟更小的字符',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每次选一个==至少出现两次==的字母，删掉其中一次',
                 '求最终字典序最小的字符串',
                 '示例：`"aaccb"` → `"aacb"`；本视频：`"cbaabcb"` → `"aabc"`'],
        quote='删除某个字符除了应该满足非落单的条件之外，还需要满足的一点是其与字典序更小的字符是相邻的，否则删除当前字符并不会使得答案更优。',
        quote_src='—— yiduobo 题解原文',
        idea=['从 `a` 开始想：删首个 `a` 左边的重复字符？反例 `"bcab"`：删第一个 `b` 会让落单的 `c` 顶到前面',
              '所以删字符要同时满足：不落单、紧挨着更小的字符',
              '只比较栈顶与当前字符，就能实现；最后再清掉末尾重复的字符'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：最后一定要清理末尾重复字符，保证前缀最小后再最短',
                 '易错：弹栈时 `cnt` 也要减一，否则「落单」判断会错',
                 '原文本来就是 Python 3 可运行的写法，代码未改动',
                 '对比灵神：灵神直接类比 316 题；yiduobo 从「首个 a 左边怎么删」推出相邻条件'],
    ),
)
