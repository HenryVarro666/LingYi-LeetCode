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


_UNDO = (17, 21, 23)


def _res(S):
    c = S.get('c')
    s = S['s']
    if c is None or c not in s:
        return ['·']
    idx = s.index(c)
    back = S['_line'] >= 15
    if back and S['_line'] in _UNDO:
        r = _sim(s[:idx])
    else:
        r = _sim(s[:idx + 1])
    return r or ['·']


def _kptr(S):
    if S['_line'] >= 12 and S.get('k') is not None and 0 <= S['k'] < len(_res(S)):
        return S['k']
    return None


def _top(S):
    if S['_line'] <= 10:
        return f"正向只算长度：`sz = {S.get('sz', 0)}`，不真的拼出 result（太长会爆内存）"
    return f"倒着还原：要找的下标 `k = {S['k']}`，当前长度 `sz = {S['sz']}`"


CONFIG = dict(
    num=3614, title='用特殊操作处理字符串 II', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='逆向思维 · 先算长度再倒推下标',
    tags=['灵神题单·贪心与思维', '灵神题单·链表树与回溯'],
    code='''
class Solution:
    def processStr(self, s: str, k: int) -> str:
        sz = 0
        for c in s:
            if c == '*':
                sz = max(sz - 1, 0)
            elif c == '#':
                sz *= 2
            elif c != '%':
                sz += 1

        if k >= sz:
            return '.'

        for c in reversed(s):
            if c == '*':
                sz += 1
            elif c == '#':
                sz //= 2
                if k >= sz:
                    k -= sz
            elif c == '%':
                k = sz - 1 - k
            else:
                sz -= 1
                if k == sz:
                    return c
''',
    call='Solution().processStr("cd%#*x", 2)',
    expect='d',
    views=[
        dict(type='text', fn=_top, size=26, h=70),
        dict(type='string', var='s', label='s（蓝 = 当前处理的字符）', cell=84, h=210,
             pointers={'s.index(c)': 'blue'}, pointer_labels={'s.index(c)': 'c'}),
        dict(type='string', var=_res, label='result（示意：代码本身并不构造它；粉色箭头 = k）', cell=84, h=260,
             pointers={_kptr: 'pink'}, pointer_labels={_kptr: 'k'}),
    ],
    watch=[('c', 'c', 'blue'), ('sz', 'sz', 'orange'), ('k', 'k', 'pink')],
    captions={
        'sz = 0': '`sz` 记录处理到当前字符后 result 的长度',
        'for c in s': lambda S, B, r: f"正着扫一遍，处理 `{S.c}`" if S.c != B.get('c') or 'c' not in B else '长度算完了',
        'sz = max': '`*` 删一个字符，长度不会小于 0：`sz` = {sz}',
        'sz *= 2': '`#` 复制，长度翻倍：`sz` = =={sz}==',
        'sz += 1': lambda S, B, r: (f'字母加一个字符：`sz` = {S.sz}' if S['_line'] < 11 else f'撤销 `*`：它删掉的那个字符回来了，`sz` = {S.sz}'),
        'if k >= sz': lambda S, B, r: ((f'`k = {S.k} >= sz = {S.sz}` → 下标越界，答案是 `.`' if S.k >= S.sz else f'`k = {S.k} < 总长 {S.sz}`：没越界，答案一定存在，开始倒推') if S['_line'] < 15 else
                                       (f'`k = {S.k} >= 半长 {S.sz}`：k 在复制出的右半边 → 对应左半边下标 `k - sz`' if S.k >= S.sz else f'`k = {S.k} < 半长 {S.sz}`：k 在左半边，复制对它没影响')),
        "return '.'": '越界，返回 `.`',
        'for c in reversed': lambda S, B, r: f"==倒着==撤销最后一步操作：`{S.c}`，此时 result 长度 `sz = {S.sz}`",
        'sz //= 2': '撤销复制：长度减半，`sz` = {sz}',
        'k -= sz': '`k` 在右半边，对应的字母在前半边的下标 `k - sz` = =={k}==',
        'k = sz - 1 - k': '撤销反转：现在的第 `k` 个，原来是第 `sz-1-k` 个 → `k` = =={k}==',
        'sz -= 1': '撤销添加字母：长度减一，`sz` = {sz}（它就是这个字母的下标）',
        'if k == sz': lambda S, B, r: (f"`k = {S.k} == sz = {S.sz}`：这个字母就是最后一位，==找到答案==" if S.k == S.sz else f'`k = {S.k} != sz = {S.sz}`：答案在更前面，继续倒推'),
        'return c': '答案是 `{c}`',
    },
    cards=dict(
        one_liner='正着会爆内存，倒着想最后一步：先算长度，再倒推 k',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['按 `s` 从左到右操作 `result`：字母追加，`*` 删末位，`#` 复制追加，`%` 反转',
                 '返回最终 `result[k]`，越界返回 `.`',
                 '`k` 最大 `10^15`，示例：`"cd%#*x"`，`k = 2` → `d`'],
        quote='生成的 result 字符串太长，超出内存限制，不行。倒着做可以吗？想清楚最后一步怎么做，就想清楚了每一步怎么做。',
        quote_src='—— 灵茶山艾府题解',
        idea=['第一遍只维护长度 `sz`，`k >= sz` 直接返回 `.`',
              '第二遍倒着撤销每一步：`#` 看 k 在哪半边，`%` 把 k 镜像，`*` 只需把长度加回',
              '遇到字母且 `k == sz-1`，这个字母就是答案'],
        after=[dict(heading='另一种写法：优化前', lines=[
            '题解先写了开 `size` 数组的版本，每步存下长度，空间 `O(n)`',
            '优化后用倒推还原 `sz`，只要一个变量，空间 `O(1)`'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`*` 倒推直接 `sz += 1`：已提前判断越界，k 合法就不会撞上空串',
                 '`#` 先减半再比较：`k >= sz` 才要 `k -= sz`',
                 '`%` 之后 `k = sz - 1 - k`，长度不变',
                 '同类题：3307、880、1545'],
    ),
)
