def _sq(x):
    return sum(int(c) ** 2 for c in str(x))


def _seq(n0):
    out, seen = [n0], {n0}
    while out[-1] != 1:
        nx = _sq(out[-1])
        out.append(nx)
        if nx in seen:
            break
        seen.add(nx)
    return out


SEQS = {19: _seq(19), 4: _seq(4)}  # 19 → 82 → 68 → 100 → 1；4 → 16 → … → 20 → 4


def _run(S):
    ns = S.get('num_set')
    if not ns:
        return None
    return SEQS[19] if 19 in ns else SEQS[4]


def _visited(S):
    seq = _run(S)
    return seq[:len(S['num_set'])] if seq else []


def _chain(S):
    vis = _visited(S)
    if not vis:
        return None
    out = list(vis)
    if S.get('now') == 0 and 'n' in S and S['n'] != vis[-1]:
        out.append(S['n'])
    return out


def _chain_color(S, i, v):
    vis = _visited(S)
    if v == 1:
        return 'green'
    if i == len(vis):  # 刚算出来、还没放进 set 的数
        return 'red' if v in S['num_set'] else 'yellow'
    ch = _chain(S)
    if len(ch) > len(vis) and ch[-1] in S['num_set'] and v == ch[-1]:  # 重复出现的那个数
        return 'red'
    return None


def _formula(S):
    vis = _visited(S)
    if not vis or 'now' not in S:
        return '每次把 `n` 换成==各位数字的平方和=='
    start = vis[-1]
    if S['now'] == 0 and S['n'] == start:
        return f'`n = {start}`'
    expr = ' + '.join(f'{c}²' for c in str(start))
    return f'`{start}` → {expr} = =={_sq(start)}==　（已累加 `n = {S["n"]}`，剩下 `now = {S["now"]}`）'


def _while_cap(S, B, ret):
    if B.n != 1:
        if len(B.num_set) == 1:
            return f'`n = {B.n}` 还不是 1 → 计算各位数字的平方和'
        return f'`n = {B.n}` 还不是 1 → 继续变换'
    return '`n = 1` → ==是快乐数=='


def _div_cap(S, B, ret):
    s = f'`now //= 10`：去掉末位 → `now = {S.now}`'
    if S.num_set == {19} and B.now == 19:
        s += '（原文 Python 2 写 `/=`，已改为 `//=`）'
    return s


def _in_cap(S, B, ret):
    if S.n in B.num_set:
        return f'`{S.n}` ==出现过了== → 进入了循环，永远变不成 1'
    return f'`{S.n}` 没出现过 → 记下来，继续'


CODE = '''
class Solution(object):
    def isHappy(self, n):
        num_set = set()
        num_set.add(n)
        while n != 1:
            now = n
            n = 0
            while now:
                n += (now % 10) ** 2
                now //= 10
            if n in num_set:
                return False
            num_set.add(n)

        return True
'''
_LINES = CODE.strip('\n').split('\n')
RET_FALSE = next(i + 1 for i, l in enumerate(_LINES) if 'return False' in l)

CONFIG = dict(
    num=202, title='快乐数', difficulty='Easy', category='哈希',
    author='yiduobo', technique='模拟 + set 判重',
    tags=['字节30天', '面试经典150'],
    code=CODE,
    call='''a = Solution().isHappy(19)
b = Solution().isHappy(4)
(a, b)''',
    expect=(True, False),
    views=[
        dict(type='text', fn=lambda S: ('第 1 次调用：`isHappy(19)`' if 19 in (S.get('num_set') or ())
                                        else '第 2 次调用：`isHappy(4)`（不快乐的数）'), size=26, h=56),
        dict(type='array', var=_chain, label='变换链（黄 = 刚算出的数，红 = 重复出现，绿 = 1）', cell=96, h=190,
             color=_chain_color),
        dict(type='text', fn=_formula, size=27, h=80),
        dict(type='set', var='num_set', label='num_set（出现过的数）', h=120),
        dict(type='text', fn=lambda S: '`k` 位数的下一个数 ≤ `k×9×9`：数不会越变越大，最终==要么到 1，要么进入循环==',
             size=23, h=90, lines=2),
    ],
    watch=[('n', 'n', 'green'), ('now', 'now', 'blue')],
    skip=['now = n', 'n = 0', 'while now'],
    captions={
        'num_set = set()': '用 set 记录==算出来过的数==：一旦重复，说明进入了循环',
        4: '先把 `n = {n}` 自己放进去',
        'while n != 1': _while_cap,
        'n += (now % 10) ** 2': '末位 `{B.now} % 10 = {B.now % 10}`，平方后累加：`n` = {B.n} + {(B.now % 10) ** 2} = {n}',
        'now //= 10': _div_cap,
        'if n in num_set': _in_cap,
        'return False': '返回 ==False==：不是快乐数',
        13: '`num_set` 加入 `{n}`',
        'return True': '变成了 1 → 返回 ==True==',
    },
    max_steps=56,
    cards=dict(
        one_liner='一直算各位平方和，用 set 记录算过的数：到 1 就快乐，重复就不快乐',
        complexity='时间 `O(log n)`（之后都在三位数以内打转），空间同',
        problem=['把正整数 `n` 替换为它==每个位置上数字的平方和==，重复这个过程',
                 '最终能变成 `1` 就是快乐数，返回 `true`；否则会==无限循环==，返回 `false`',
                 '示例：`19 → 82 → 68 → 100 → 1`，返回 `true`；`n = 2` 返回 `false`'],
        quote='一个k位的数其下一个变换后得到的数最大为k * 9 * 9……于是==可以放心地开一个set记录过去算出来的结果==，然后继续迭代直到变成1或者在set里出现过。',
        quote_src='—— yiduobo 题解原文',
        idea=['数位越多，平方和相对越小：`999` 的下一个才 `243`',
              '所以序列很快落到三位数以内，要么到 1，要么==循环==',
              'set 存下算过的数：新算出的数出现过 → 循环 → `False`'],
        summary=['易错：取各位数字用 `now % 10` 和 `now //= 10`',
                 '原文为 Python 2 写法：`now /= 10` 已改为 `now //= 10`，并删去文档字符串',
                 '不快乐的数最终都会进入 `4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4`',
                 '进阶：快慢指针判环（同 141 题）可做到 `O(1)` 空间'],
    ),
)
