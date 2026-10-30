TRACK = '''
class Tracked(str):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k, ch in enumerate(str.__iter__(self)):
            self.k = k
            yield ch
        self.k = None
'''

K0 = {'1432219': 3, '1023': 2}


def _cur(S):
    k = getattr(S.get('num'), 'k', None)
    return k if isinstance(k, int) else None


def _ids(S):
    """模拟同样的过程，求出当前栈里每个字符在 num 中的下标、已被删掉的下标"""
    num = S.get('num')
    if num is None or 'stack' not in S:
        return [], set()
    num = str(num)
    k, st, gone = K0[num], [], set()
    cur = _cur(S)
    target = (len(S['stack']), S['k'])
    end = len(num) if cur is None else cur + 1
    for i in range(end):
        if i == cur and (len(st), k) == target:
            return st, gone
        while st and k > 0 and num[st[-1]] > num[i]:
            gone.add(st.pop())
            k -= 1
            if i == cur and (len(st), k) == target:
                return st, gone
        st.append(i)
        if i == cur and (len(st), k) == target:
            return st, gone
    while len(st) > target[0]:
        gone.add(st.pop())
    return st, gone


def _color(S, i, v):
    st, gone = _ids(S)
    if i == _cur(S):
        return 'blue'
    if i in st:
        return 'green'
    if i in gone:
        return 'red'
    return None


def _dim(S, i, v):
    cur = _cur(S)
    return 'stack' in S and cur is not None and i > cur


def _text(S):
    if 'stack' not in S:
        return ''
    num = str(S['num'])
    used = K0[num] - S['k']
    return f'要删 `{K0[num]}` 位：已删 `{used}` 位，还能删 =={S["k"]}== 位；栈 = `"{"".join(S["stack"])}"`'


def _while_cap(S, B, ret):
    st, k, now = B.stack, B.k, S.now
    if not st:
        return f'栈空 → `{now}` 直接入栈'
    if k <= 0:
        return f'`k = 0`：已经删够了 → 不再删，`{now}` 直接入栈'
    if st[-1] > now:
        return f'栈顶 `{st[-1]}` > `{now}`：高位比低位大 → ==删掉高位==，数会更小'
    return f'栈顶 `{st[-1]}` ≤ `{now}` → 保留，不删'


def _tail_cap(S, B, ret):
    if B.k > 0:
        return f'遍历完还要删 `{B.k}` 位：栈是==单调递增==的 → 删栈顶（最大的低位）'
    return '删够了'


CODE = '''
class Solution(object):
    def removeKdigits(self, num, k):
        stack = []
        for now in num:
            while stack and k > 0 and stack[-1] > now:
                stack.pop()
                k -= 1
            stack.append(now)

        while k > 0:
            stack.pop()
            k -= 1

        if not stack:
            return '0'

        return str(int(''.join(stack)))
'''

CONFIG = dict(
    num=402, title='移掉K位数字', difficulty='Medium', category='栈',
    author='yiduobo', technique='贪心 + 单调栈',
    tags=['热题173'],
    code=CODE,
    setup=TRACK,
    call='''a = Solution().removeKdigits(Tracked("1432219"), 3)
b = Solution().removeKdigits(Tracked("1023"), 2)
(a, b)''',
    expect=('1219', '2'),
    views=[
        dict(type='text', fn=lambda S: (f'调用：`removeKdigits("{S["num"]}", {K0[str(S["num"])]})`' if 'num' in S else ''),
             size=26, h=56),
        dict(type='string', var=lambda S: str(S['num']), label='num（蓝 = 当前位，绿 = 在栈中，红 = 已删）', cell=100, h=220,
             pointers={_cur: 'blue'}, pointer_labels={_cur: 'now'}, color=_color, dim=_dim),
        dict(type='stack', var='stack', label='stack（单调不减）', h=120),
        dict(type='text', fn=_text, size=27, h=70),
    ],
    watch=[('now', 'now', 'blue'), ('k', 'k', 'orange')],
    captions={
        'stack = []': '维护一个栈，从高位到低位遍历',
        'for now in num': lambda S, B, ret: (f'看下一位 `now = {S.now}`' if _cur(S) is not None else '遍历完 num'),
        'while stack and k > 0': _while_cap,
        6: '弹出 `{B.stack[-1]}`（删掉它）',
        7: lambda S, B, ret: (f'还能删 `k = {S.k}` 位；继续看新的栈顶' if S.k else '`k = 0`：删够了'),
        'stack.append(now)': '`{now}` 入栈 → `"{"".join(stack)}"`',
        'while k > 0': _tail_cap,
        11: '删掉栈顶 `{B.stack[-1]}`',
        12: '还能删 `k = {k}` 位',
        'if not stack': lambda S, B, ret: ('栈空了 → 返回 `"0"`' if not S.stack else f'栈非空：`"{"".join(S.stack)}"`'),
        'return str(int': '`int()` 去掉前导零：`"{"".join(stack)}"` → =={ret}==',
    },
    max_steps=60,
    cards=dict(
        one_liner='从高位往低位看：前一位比后一位大，就删掉前一位',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['字符串 `num` 表示非负整数，移除其中 `k` 位，使剩下的数==最小==',
                 '示例：`num = "1432219", k = 3` → `"1219"`',
                 '`"10200", k = 1` → `"200"`（去掉前导零）；`"10", k = 2` → `"0"`'],
        quote='从高位开始往低位看，==若存在相邻的两位满足高位大于低位，那么此时就应该删去高位==，同时继续往前验证。',
        quote_src='—— yiduobo 题解原文',
        idea=['维护一个栈，从高位到低位遍历',
              '当前数字比栈顶小且还没删够 → 弹栈，直到栈顶 ≤ 当前或删够了',
              '遍历完还没删够：栈单调递增 → ==删栈顶的 k 个=='],
        summary=['时间 `O(n)`：每位最多入栈、出栈各一次',
                 '易错：遍历完 `k` 可能还 `> 0`，要从栈顶继续删',
                 '易错：结果去掉前导零；全删光要返回 `"0"`',
                 '原文为 Python 2 风格：只删去了类型说明文档字符串，代码未改'],
    ),
)
