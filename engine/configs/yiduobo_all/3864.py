def _len(S):
    return S.get('part_length') or S.get('min_length') or 1


def _ok(S):
    i = S.get('index')
    return i is not None and i % _len(S) == 0 and i + _len(S) <= len(S['s'])


CONFIG = dict(
    num=3864, title='划分二进制字符串的最小费用', difficulty='Hard', category='链表、二叉树与回溯',
    author='yiduobo', technique='自底向上（像建线段树）',
    tags=['灵神题单·链表树与回溯', '难度分 2032'],
    code='''
class Solution(object):
    def minCost(self, s, encCost, flatCost):
        
        n = len(s)
        
        min_length = n
        while min_length % 2 == 0:
            min_length //= 2
        
        f = [0] * n
        one = [0] * n
        for index in range(0, n, min_length):
            for c in s[index: index + min_length]:
                one[index] += int(c)

            if one[index] == 0:
                f[index] = flatCost
            else:
                f[index] = min_length * one[index] * encCost
        
        part_length = min_length + min_length
        while part_length <= n:
            for index in range(0, n, part_length):
                f[index] += f[index + part_length // 2]
                one[index] += one[index + part_length // 2]
                if one[index] == 0:
                    v = flatCost
                else:
                    v = part_length * one[index] * encCost
                
                f[index] = min(f[index], v)

            part_length += part_length

        return f[0]
''',
    call='Solution().minCost("100000010000", 1, 5)',
    expect=12,
    views=[
        dict(type='text', fn=lambda S: (f"当前层：每段长 `{S['part_length']}`（拆成两个 `{S['part_length'] // 2}`）" if 'part_length' in S
                                         else (f"最小单元长度 `min_length = {S['min_length']}`（不断折半直到奇数）" if 'min_length' in S else '')), size=26, h=60),
        dict(type='string', var='s', label='s（蓝框 = 当前这一段）', cell=64, h=170,
             window=(lambda S: S['index'] if _ok(S) else None, lambda S: S['index'] + _len(S) - 1 if _ok(S) else None),
             color=lambda S, i, v: 'red' if v == '1' else None,
             dim=lambda S, i, v: _ok(S) and not (S['index'] <= i < S['index'] + _len(S))),
        dict(type='array', var='one', label='one[i]：以 i 开头的段里 1 的个数', cell=64, h=140, pointers={'index': 'blue'}),
        dict(type='array', var='f', label='f[i]：以 i 开头的段的最小费用', cell=64, h=140, pointers={'index': 'blue'},
             color=lambda S, i, v: 'green' if (S.get('part_length') or S.get('min_length') or 1) and i % _len(S) == 0 and 'one' in S and (v > 0) else None),
    ],
    watch=[('min_length', 'min_length', 'cyan'), ('part_length', 'part_length', 'pink'), ('index', 'index', 'blue'),
           ('v', 'v', 'yellow'), ('f[0]', lambda S: S['f'][0] if 'f' in S else None, 'green')],
    skip=['for c in s[', 'one[index] += int(c)', 'n = len(s)', 'f = [0]', 'one = [0]'],
    max_steps=75,
    captions={
        'while min_length % 2': lambda S, B, r: (f'`min_length = {S.min_length}` 是偶数，还能折半' if S.min_length % 2 == 0
                                                 else f'`min_length = {S.min_length}` 是奇数，不能再拆：这就是最小单元'),
        'min_length //= 2': '折半：`min_length` → `{min_length}`',
        'for index in range(0, n, min_length)': lambda S, B, r: ('最底层所有单元都算完了' if B.get('index') == S.index else f'最底层：每 `{S.min_length}` 个字符一段，这一段从 `{S.index}` 开始'),
        'if one[index] == 0': lambda S, B, r: (f'这一段里有 `{S.one[S.index]}` 个 1' + ('，没有敏感元素 → 费用 `flatCost`' if S.one[S.index] == 0 else '，有敏感元素 → 费用 `长度 × 1的个数 × encCost`')),
        'f[index] = flatCost': '`f[{index}] = flatCost = {flatCost}`',
        'f[index] = min_length': '`f[{index}] = {min_length} × {one[index]} × {encCost} = {f[index]}`',
        'part_length = min_length + min_length': '往上一层：两个最小单元合并，`part_length = {part_length}`',
        'while part_length <= n': lambda S, B, r: (f'`part_length = {S.part_length} <= n`：这一层还没算' if S.part_length <= S.n
                                                   else f'`part_length = {S.part_length} > n`：根都算完了，结束'),
        'for index in range(0, n, part_length)': lambda S, B, r: ('这一层所有段都算完了' if B.get('index') == S.index else f'这一层的一段从 `{S.index}` 开始，长 `{S.part_length}`'),
        'f[index] += f[index + part_length // 2]': '==拆分的费用==：左半 + 右半 `f[{index}] = {f[index]}`（右半从 `{index + part_length // 2}` 开始）',
        'one[index] += one': '1 的个数也合并：左右两半相加 `one[{index}] = {one[index]}`，不用再遍历',
        'if one[index] == 0': lambda S, B, r: (f'这一段共 `{S.one[S.index]}` 个 1' + ('，没有敏感元素 → 不拆的费用 `flatCost`' if S.one[S.index] == 0 else '，有敏感元素 → 不拆的费用 `长度 × 1的个数 × encCost`')),
        'v = flatCost': '不拆分的费用 `v = flatCost = {v}`',
        'v = part_length': '不拆分的费用 `v = {part_length} × {one[index]} × {encCost} = {v}`',
        'f[index] = min(f[index], v)': '拆分 `{B.f[index]}` 和不拆分 `{v}` 取较小：`f[{index}] = {f[index]}`',
        'part_length += part_length': '这一层算完，往上翻倍：`part_length` → `{part_length}`',
        'return f[0]': '整段 `[0, n)` 的最小费用：`f[0] = {f[0]}`',
    },
    cards=dict(
        one_liner='和线段树一样自底向上：先算最小单元，再两两合并取最小',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['二进制字符串 `s`，`1` 是敏感元素；一段长 `L`、含 `X` 个 1 的费用：`X = 0` 为 `flatCost`，否则 `L·X·encCost`',
                 '偶数长度的段可以对半拆成两段，费用变成两段之和，求最小总费用',
                 '示例：`s = "1010"`，`encCost = 2`，`flatCost = 1` → `6`；本视频：`"100000010000"`，`1`，`5` → `12`'],
        quote='题目中对于分段的计算与线段树计算区间值的方式是非常类似的，在这里可以选择自顶向下或者自底向上进行求解，我在这里选择的是后者。',
        quote_src='—— yiduobo 题解原文',
        idea=['不断对 `n` 除以 2 直到奇数，得到不能再拆的==最小单元长度== `min_length`',
              '最底层：每个单元直接按题意算费用；一趟遍历数出 1 的个数',
              '往上每层长度翻倍：费用 = `min(拆分 = 左右之和, 不拆 = 按公式)`；1 的个数也由左右相加得到'],
        summary=['时间 `O(n)`：各层段数 `1 + 2 + 4 + …` 总共 `O(n)`；1 的个数靠左右合并，不用重复遍历',
                 '空间 `O(n)`（`f` 和 `one` 数组，只用到每段的起点位置）',
                 '易错点：最小单元的长度是 `n` 一直除以 2 直到奇数；每层先把右半合并到左半再取 `min`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，无需其他修改',
                 '对比灵神：灵神自顶向下递归 + 前缀和，yiduobo 自底向上合并'],
    ),
)
