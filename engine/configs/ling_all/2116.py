S0, L0 = '))()))', '010100'
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


def _range(S):
    if 'mn' not in S:
        return '未匹配左括号数 `c` 的取值范围：只维护最小值 `mn` 和最大值 `mx`'
    mn, mx = S['mn'], S['mx']
    vals = list(range(mn, mx + 1, 2)) if mn <= mx else []
    return f'`c` 可能取 =={{{", ".join(map(str, vals)) or "空"}}}==（`mn = {mn}`，`mx = {mx}`，间隔 2）'


def _col(S, i, v):
    return 'purple' if S['locked'][i] == '0' else None


CONFIG = dict(
    num=2116, title='判断一个括号字符串是否有效', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='维护未匹配左括号数的取值范围 [mn, mx]',
    tags=['栈', '合法括号字符串', '难度分 2038'],
    code='''
class Solution:
    def canBeValid(self, s: str, locked: str) -> bool:
        if len(s) % 2:
            return False
        mn = mx = 0
        for b, lock in zip(s, locked):
            if lock == '1':  # 不能改
                d = 1 if b == '(' else -1
                mx += d
                if mx < 0:  # c 不能为负
                    return False
                mn += d
            else:  # 可以改
                mx += 1  # 改成左括号，c 加一
                mn -= 1  # 改成右括号，c 减一
            if mn < 0:  # c 不能为负
                mn = 1  # 此时 c 的取值范围都是奇数，最小的正奇数是 1
        return mn == 0  # 说明最终 c 能是 0
''',
    setup=SETUP,
    call=f'Solution().canBeValid(_S({S0!r}), {L0!r})',
    expect=True,
    views=[
        dict(type='text', fn=_range, size=28, h=110),
        dict(type='string', var='s', label='s（紫 = 可改的 ?，蓝框 = 当前字符）', pointers={'s.k': 'blue'}, pointer_labels={'s.k': 'b'},
             color=_col, window=('s.k', 's.k'), cell=90, h=230),
        dict(type='string', var='locked', label='locked（0 = 可改，1 = 不能改）', cell=90, h=200,
             pointers={'s.k': 'blue'}, pointer_labels={'s.k': 'lock'}, window=('s.k', 's.k'), color=_col),
    ],
    watch=[('b', 'b', 'blue'), ('lock', 'lock', 'purple'), ('mn', 'mn', 'cyan'), ('mx', 'mx', 'orange')],
    captions={
        'len(s) % 2': '长度是奇数就一定有个括号落单 → 直接 `False`；这里长度 `{len(s)}`，继续',
        'mn = mx = 0': '`c` = 未匹配的左括号数；开始时只能是 0，所以 `mn = mx = 0`',
        'for b, lock': lambda S, B, ret: ('字符串遍历完毕' if S.s.done else f"取 `b = '{S.b}'`，`lock = '{S.lock}'`"),
        "if lock == '1'": lambda S, B, ret: ("`lock = '1'`：不能改，括号固定" if S.lock == '1' else "`lock = '0'`：可以改，是个 `?`，两种情况都要考虑"),
        'd = 1 if': '`b = {b!r}` → `d = {d}`：左括号 +1，右括号 −1',
        'mx += d': '所有可能的 `c` 都变化 `d`：`mx` → {mx}',
        'if mx < 0': lambda S, B, ret: (f'`mx = {S.mx} < 0`：连最大的 `c` 都为负，==没有合法方案== → `False`' if S.mx < 0 else f'`mx = {S.mx} ≥ 0`，还有可能'),
        'mn += d': '`mn` 同样 {B.mn} → {mn}',
        'mx += 1': '改成左括号：`c` 最大的情况 +1 → `mx = {mx}`',
        'mn -= 1': '改成右括号：`c` 最小的情况 −1 → `mn = {mn}`',
        'if mn < 0': lambda S, B, ret: (f'`mn = {S.mn} < 0`：负数不合法，要去掉' if S.mn < 0 else f'`mn = {S.mn} ≥ 0`，范围没问题'),
        'mn = 1': '去掉负数后，剩下的 `c` 都是奇数（如 0、2、4 减一再去负数 → 1、3）→ ==最小是 1==，`mn = 1`',
        'return mn == 0': '`mn = {mn}`：最终 `c` ==能==取到 0 吗？结果 =={ret}==',
    },
    cards=dict(
        one_liner='未匹配左括号数 c 的取值范围，只用最小值和最大值就能刻画',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`s` 由括号组成，`locked[i] = 0` 的位置可以改成 `(` 或 `)`',
                 '问能否改成有效括号串',
                 '示例：`s = "))()))"`，`locked = "010100"` → `true`'],
        quote='在遍历 s 的过程中，维护 c 的取值范围。如果最终 c 的取值范围不为空，且包含 0，那么可以把 s 变成有效括号字符串。',
        quote_src='—— 灵茶山艾府题解',
        idea=['有效括号串的任意前缀，左括号数 ≥ 右括号数；`c` 是未匹配的左括号数',
              '`?` 可以让 `c` 加一，也可以减一 → `c` 是一个集合；集合里的数同奇偶、连续',
              '所以只记 `mn`、`mx`：`mx < 0` 无解；`mn < 0` 时置为 1；最后看 `mn == 0`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`mn < 0` 要置为 ==1==，不是 0（剩下的数都是奇数）',
                 '易错：长度为奇数直接 `False`，这能保证最后奇偶性对得上',
                 '进阶：方案数见 CF1709C；视频里 `s` 套了只记下标的字符串子类，仅用于画指针'],
    ),
)
