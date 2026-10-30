def _sim(s):
    r = []
    for ch in s:
        if ch == '*':
            if r:
                r.pop()
        elif ch == '#':
            r = r + r
        elif ch == '%':
            r = r[::-1]
        else:
            r.append(ch)
    return r


_UNDO = (21, 24, 25, 27, 31)


def _res(S):
    c = S.get('c')
    s = S['s']
    if c is None or c not in s:
        return ['·']
    idx = s.index(c)
    if S['_line'] >= 19 and S['_line'] in _UNDO:
        r = _sim(s[:idx])
    else:
        r = _sim(s[:idx + 1])
    return r or ['·']


def _kptr(S):
    if S['_line'] >= 16 and S.get('k') is not None and 0 <= S['k'] < len(_res(S)):
        return S['k']
    return None


def _top(S):
    if S['_line'] <= 14:
        return f"正向只算长度：`length = {S.get('length', 0)}`，不真的拼出 result"
    return f"倒推：要找的下标 `k = {S['k']}`，当前长度 `length = {S['length']}`"


CONFIG = dict(
    num=3614, title='用特殊操作处理字符串 II', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='先算长度 · 倒推第 k 个字符',
    tags=['灵神题单·贪心与思维', '灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def processStr(self, s, k):
        
        length = 0
        for c in s:
            if c == '*':
                if length > 0:
                    length -= 1
            elif c == '#':
                length += length
            elif c == '%':
                continue
            else:
                length += 1
        
        if k >= length:
            return '.'
        
        for c in s[::-1]:
            if c == '*':
                length += 1
            elif c == '#':
                if k >= length // 2:
                    k -= length // 2
                length //= 2
            elif c == '%':
                k = length - k - 1
            elif k == length - 1:
                return c
            else:
                length -= 1
''',
    call='Solution().processStr("ab#%*c", 1)',
    expect='a',
    views=[
        dict(type='text', fn=_top, size=26, h=70),
        dict(type='string', var='s', label='s（蓝 = 当前处理的字符）', cell=84, h=210,
             pointers={'s.index(c)': 'blue'}, pointer_labels={'s.index(c)': 'c'}),
        dict(type='string', var=_res, label='result（示意：代码本身并不构造它；粉色箭头 = k）', cell=84, h=260,
             pointers={_kptr: 'pink'}, pointer_labels={_kptr: 'k'}),
    ],
    watch=[('c', 'c', 'blue'), ('length', 'length', 'orange'), ('k', 'k', 'pink')],
    captions={
        4: '`length` 记录当前 result 的长度，只算长度、不造字符串',
        5: lambda S, B, r: f"从左到右扫描：`{S.c}`" if S.c != B.get('c') or 'c' not in B else '长度算完了',
        8: '遇到 `*`：长度大于 0 才能删，`length` = {length}',
        10: '遇到 `#`：result 复制一份接在后面，长度翻倍：`length` = =={length}==',
        12: '遇到 `%`：反转不改变长度，直接跳过',
        14: '遇到字母：长度加一，`length` = {length}',
        16: lambda S, B, r: (f'`k = {S.k} >= length = {S.length}` → 越界，返回 `.`' if S.k >= S.length
                             else f'`k = {S.k} < length = {S.length}`：下标合法，从 s 的最后一个字符往回推'),
        17: '越界，返回 `.`',
        19: lambda S, B, r: f"==倒推==：撤销 `{S.c}` 这一步，此时 result 长度 `length = {S.length}`",
        21: '上一步删过一个字符，撤销它 → `length` = {length}（空串情况前缀可整个丢掉，不影响 k）',
        23: lambda S, B, r: (f'`k = {S.k} >= {S.length // 2}`：k 在复制出的后半段，要去前半段找' if S.k >= S.length // 2
                             else f'`k = {S.k} < {S.length // 2}`：k 在前半段，后面那份复制可以直接丢掉'),
        24: '后半段第 k 个 = 前半段第 `k - length // 2` 个，`k` = =={k}==',
        25: '撤销复制：长度减半，`length` = {length}',
        27: '撤销反转：现在第 k 个是反转前的第 `length - k - 1` 个，`k` = =={k}==',
        28: lambda S, B, r: (f'`k = {S.k} == length - 1 = {S.length - 1}`：k 正好是刚添加的最后一个字符' if S.k == S.length - 1
                             else f'`k = {S.k} != length - 1 = {S.length - 1}`：刚添加的字符不是要找的'),
        29: '就是它：答案 `{c}`',
        31: '把这个字符撤销掉：`length` = {length}，继续往前推',
    },
    cards=dict(
        one_liner='不造字符串：先算最终长度，再从最后一步倒推 k',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s` 里字母追加、`*` 删末位、`#` 复制追加、`%` 反转',
                 '求最终 `result` 的第 `k` 个字符，越界返回 `.`',
                 '`k` 最大 `10^15`，示例：`"ab#%*c"`，`k = 1` → `a`'],
        quote='如果不完整模拟出整个字符，而是计算其最终的长度，则只需对s进行一趟遍历。……就是先通过s的最后一个字符，推测出最终result中的第k个字符，在倒数第二步完成时是result中的第几个字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一趟只累计长度：`*` 减一、`#` 翻倍、`%` 不变、字母加一',
              '`k >= length` 直接 `.`；否则倒着扫 s，一步步把 k 换成上一步的下标',
              '`#` 看 k 在前后哪半段；`%` 换成 `length - k - 1`；字母若恰好是末位就是答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`*` 倒推只需 `length += 1`：空串时的删除可以连同前缀整个忽略',
                 '`#` 先判断 k 再减半长度，顺序反了会错',
                 '原文本来就是 Python 3 可运行的写法，代码未改动',
                 '对比灵神：灵神先把 `sz` 减半再比较 k；yiduobo 先比较 `length // 2` 再减半，效果相同'],
    ),
)
