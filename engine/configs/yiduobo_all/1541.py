S0 = '(()))(('
SETUP = '''
class _S(str):
    k = None
    done = False
    def __iter__(self):
        for j, c in enumerate(str.__iter__(self)):
            self.k = j
            yield c
        self.done = True
'''


def _info(S):
    if 'char' not in S:
        return '用 `left`、`right` 表示当前合法串形如 `(((…(` 或 `(((…()`'
    return f'已有 `left = {S["left"]}` 个左括号，末尾 `right = {S["right"]}` 个右括号（0 或 1），已插入 `res = {S["res"]}`'


CONFIG = dict(
    num=1541, title='平衡括号字符串的最少插入次数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='维护合法串形态 · left / right 计数',
    tags=['栈', '合法括号字符串', '难度分 1759'],
    code='''
class Solution(object):
    def minInsertions(self, s):

        left = right = 0
        res = 0
        for char in s:
            if char == '(':
                if right == 1:
                    if left > 0:
                        left -= 1
                        res += 1
                    else:
                        res += 2
                
                left += 1
                right = 0
            else:
                if right == 1:
                    if left > 0:
                        left -= 1
                    else:
                        res += 1
                    right = 0
                else:
                    right += 1
        
        if right == 1:
            res += 1
            if left > 0:
                left -= 1
            else:
                res += 1
        
        res += left * 2
        return res
''',
    setup=SETUP,
    call=f'Solution().minInsertions(_S({S0!r}))',
    expect=5,
    views=[
        dict(type='text', fn=_info, size=26, h=100),
        dict(type='string', var='s', label='s（蓝框 = 当前字符）', pointers={'s.k': 'blue'}, pointer_labels={'s.k': 'char'}, cell=90, h=240,
             window=('s.k', 's.k')),
        dict(type='text', fn=lambda S: (('合法串末尾状态：' + ('`((…()`，挂着一个右括号' if S.get('right') == 1 else '`((…(`，只有左括号')) if 'right' in S else ''), size=26, h=80),
    ],
    watch=[('left', 'left', 'pink'), ('right', 'right', 'orange'), ('res', 'res', 'green')],
    captions={
        'left = right = 0': '`left` 数合法串里的左括号，`right`（0 或 1）数末尾挂着的右括号',
        'res = 0': '`res` 累计要插入的括号个数',
        'for char in s': lambda S, B, ret: ('字符串扫描完了，还要处理末尾残留' if S.s.done else f"取下一个字符 `char = '{S.char}'`"),
        "if char == '('": lambda S, B, ret: (f"`'('`：左括号，先看前面有没有挂着一个单独的 `)`" if S.char == '(' else "`')'`：右括号，看看末尾有没有挂着等它的 `)`"),
        8: lambda S, B, ret: ('`right = 1`：末尾挂着一个落单的 `)`，新来的 `(` 到了，必须==补一个 `)`== 凑成 `))`' if S.right == 1 else '`right = 0`：末尾没挂着右括号，直接把 `(` 加进去'),
        10: '`(` 前面有 `{B.left}` 个左括号：补的那个 `)` 配上其中一个 → `left = {left}`',
        11: '补了一个 `)`：`res = {res}`',
        'res += 2': '没有左括号可配：补 `(` 和 `)` 各一个 → `res = {res}`',
        18: lambda S, B, ret: ('`right = 1`：末尾已挂着一个 `)`，这个 `)` 和它凑成 `))`' if S.right == 1 else '`right = 0`：这是第一个 `)`，先挂起来等下一个'),
        19: lambda S, B, ret: (f'`left = {S.left} > 0`：有左括号配这对 `))`' if S.left > 0 else '`left = 0`：没有左括号可配，只能==补一个 `(`=='),
        20: '`))` 配掉一个左括号：`left = {left}`',
        22: '没有左括号：补一个 `(`，`res = {res}`',
        25: '先挂一个 `)`（`right = 1`），等下一个字符决定：是 `)` 就凑成 `))`',
        27: lambda S, B, ret: ('`right = 1`：末尾还挂着一个 `)`，要补一个 `)` 凑成 `))`' if S.right == 1 else '`right = 0`：末尾没有残留'),
        'left += 1': '当前左括号加入合法串：`left = {left}`',
        'right = 0': '`right = 0`：末尾没有挂着的右括号',
        'res += left * 2': '剩下 `{left}` 个左括号，每个补 2 个 `)`：`res` → =={res}==',
        'return res': '一共插入 =={ret}== 个括号',
    },
    cards=dict(
        one_liner='合法串只会是 `((…(` 或 `((…()`：数左括号，再看挂没挂右括号',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['一个 `(` 必须配两个连续的 `))`，求让 `s` 平衡的最少插入次数',
                 '示例：`"(()))"` → `1`（末尾补一个 `)`）',
                 '本视频：`"(()))(("` → `5`'],
        quote='任意时刻可能出现，且合法的情况必然是形如 ((((..( 或者 ((((..() ，其中，左括号可以由任意多个，而右括号的数量只能是0或者1。',
        quote_src='—— yiduobo 题解原文',
        idea=['只记两个数：`left` 个左括号，末尾 `right` 个右括号（0 或 1）',
              '来了 `(` 而末尾挂着 `)`：补一个 `)` 凑成 `))`，有左括号可配就 `res += 1`，否则补 `()` 要 `res += 2`',
              '来了 `)` 而末尾挂着 `)`：凑成 `))`，有左括号就配对，没有就补一个 `(`；扫完再处理残留'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`right == 1` 时来了 `(`，要先处理这个落单的 `)`，再加入新的左括号',
                 '易错：结尾还要处理一次 `right == 1`，最后每个剩余 `(` 补 `))`',
                 '对比灵神：灵神用下标 `i` 跳两格，yiduobo 用 `right` 状态位逐字符处理',
                 '视频里 `s` 套了个只记下标的字符串子类，仅用于画指针，不影响题解逻辑'],
    ),
)
