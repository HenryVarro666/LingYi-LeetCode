N0 = 91


def _tern(v):
    if v == 0:
        return '0'
    s = ''
    while v:
        s = str(v % 3) + s
        v //= 3
    return s


def _digits(S):
    n = S.get('n')
    if n is None:
        return None
    t = _tern(N0)
    done = len(t) - len(_tern(n)) if n else len(t)
    return list(t), done


def _text(S):
    r = _digits(S)
    if r is None:
        return f'要判断的 `n = {N0}`，三进制写出来是 `{_tern(N0)}`'
    t, done = r
    return f'`{N0}` 的三进制 `{"".join(t)}`：已检查最低 ==`{done}`== 位，剩下 `n = {S["n"]}`'


def _arr(S):
    r = _digits(S)
    return r[0] if r else list(_tern(N0))


def _col(S, i, v):
    r = _digits(S)
    if not r:
        return None
    t, done = r
    pos = len(t) - 1 - i  # 第几位（从低位数起）
    if pos < done:
        return 'red' if v == '2' else 'green'
    return None


CONFIG = dict(
    num=1780, title='判断一个数字是否可以表示成三的幂的和', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='三进制逐位检查',
    tags=['灵神题单', '难度分 1506'],
    code='''
class Solution:
    def checkPowersOfThree(self, n: int) -> bool:
        while n:
            if n % 3 == 2:
                return False
            n //= 3
        return True
''',
    call='Solution().checkPowersOfThree(91)',
    expect=True,
    views=[
        dict(type='text', fn=_text, h=80, lines=2),
        dict(type='array', var=_arr, label='n 的三进制（左高位 → 右低位）', color=_col, h=170),
    ],
    watch=[('n', 'n', 'blue'), ('n % 3', 'n % 3 if n else None', 'orange')],
    captions={
        'while n': lambda S, B, r: (f'`n = {S.n}` 还没取完 → 继续看下一位' if S.n else '`n = 0`：三进制每一位都检查完了，没有出现 2'),
        'n % 3 == 2': lambda S, B, r: (f'末位 `n % 3 = {S.n % 3}`：是 2 → 同一个幂要用两次，==不可能凑出=='
                                       if S.n % 3 == 2 else f'末位 `n % 3 = {S.n % 3}`：不是 2（0 不选，1 选这一位）→ 继续'),
        'n //= 3': '丢掉最低位：`n` → =={n}==',
        'return False': '出现数字 2，返回 `False`',
        'return True': '全是 0 或 1：每个 3 的幂最多用一次 → 返回 `True`',
    },
    cards=dict(
        one_liner='n 的三进制里只要有数字 2，就凑不出',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['每个 3 的幂最多用一次（不同的三的幂），能否加出 `n`',
                 '示例：`12 = 3 + 9` → `true`；`21` → `false`',
                 '本视频：`n = 91 = 1 + 9 + 81` → `true`'],
        quote='如果 n 的三进制表示中有数字 2，那么 n 就无法表示成若干个不同的三的幂之和。否则，n 可以表示成若干个不同的三的幂之和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['必须先分出不超过 `n` 的最大 3 的幂：这正是三进制展开',
              '某一位是 2，等于同一个幂用了两次，继续拆也避不开重复',
              '逐位检查：`n % 3` 取末位，`n //= 3` 丢掉末位'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '判断条件是「某一位 == 2」，不是「余数 != 0」',
                 '写法二：`n, d = divmod(n, 3)`，一次取商和余数',
                 '类似思路：把数字按进制逐位拆开处理'],
    ),
)
