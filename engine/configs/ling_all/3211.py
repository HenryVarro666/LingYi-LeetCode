def _bits(S):
    n = S.get('n')
    if n is None or 'x' not in S:
        return ''
    x, m = S['x'], S['mask']
    b = lambda v: format(v, f'0{n}b')
    ln1 = f"x = `{b(x)}`（取反后：0 变 1）"
    if 'ans' in S and S['_line'] >= 8:
        ln1 += f"　x >> 1 = `{b(x >> 1)}`　与运算 = `{b((x >> 1) & x)}`"
    return ln1


def _and(S):
    n = S.get('n')
    if n is None or 'x' not in S:
        return ''
    x = S['x']
    b = lambda v: format(v, f'0{n}b')
    if x & (x >> 1):
        return f"`{b(x)}` 和 `{b(x >> 1)}` 在同一位上都是 1 → 有相邻的 1 → ==舍弃=="
    return f"`{b(x)}` 和 `{b(x >> 1)}` 没有同位的 1 → 没有相邻的 1 → ==保留=="


def _col(S, i, v):
    return None


CONFIG = dict(
    num=3211, title='生成不含相邻零的二进制字符串', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='位运算 · 枚举取反后的数',
    tags=['灵神核心路线', '灵神题单·位运算', '难度分 1353'],
    code='''
class Solution:
    def validStrings(self, n: int) -> List[str]:
        ans = []
        mask = (1 << n) - 1
        for x in range(1 << n):
            if (x >> 1) & x == 0:
                # 0{n}b 表示长为 n 的有前导零的二进制
                ans.append(f"{x ^ mask:0{n}b}")
        return ans
''',
    call='Solution().validStrings(4)',
    expect=['1111', '1110', '1101', '1011', '1010', '0111', '0110', '0101'],
    views=[
        dict(type='text', fn=lambda S: (f"`x = {format(S['x'], '0%db' % S['n'])}`（十进制 {S['x']}）" if 'x' in S else f"长度 `n = {S['n']}`，枚举 `x` 从 0 到 {(1 << S['n']) - 1}"), size=30, h=70),
        dict(type='text', fn=lambda S: (f"`x >> 1 = {format(S['x'] >> 1, '0%db' % S['n'])}`　`x & (x >> 1) = {format(S['x'] & (S['x'] >> 1), '0%db' % S['n'])}`" if 'x' in S and S['_line'] >= 6 else ''), size=30, h=70),
        dict(type='text', fn=lambda S: (_and(S) if 'x' in S and S['_line'] >= 6 else ''), size=26, h=80),
        dict(type='text', fn=lambda S: (f"`mask = {format(S['mask'], '0%db' % S['n'])}`　`x ^ mask = {format(S['x'] ^ S['mask'], '0%db' % S['n'])}`" if 'x' in S and S['_line'] >= 8 else ''), size=30, h=70),
        dict(type='stack', var='ans', label='ans（新加入的绿色）', h=240),
    ],
    watch=[('n', 'n', 'blue'), ('x', 'x', 'pink'), ('mask', 'mask', 'cyan')],
    skip=[],
    captions={
        'ans = []': '准备答案列表',
        'mask = (1 << n) - 1': '`mask = (1 << {n}) - 1` = `{format(mask, "0%db" % n)}`：低 `{n}` 位全是 1，用来==取反==',
        'for x in range(1 << n)': lambda S, B, ret: (f"枚举 `x = {format(S.x, '0%db' % S.n)}`：它是==取反后的数==（原串里的 0 对应 x 的 1）" if 'x' in S and S.get('x') != B.get('x') or 'x' not in B
                                                      else '枚举完了'),
        'if (x >> 1) & x == 0': lambda S, B, ret: (
            f"`x & (x >> 1) = {format(S.x & (S.x >> 1), '0%db' % S.n)}`"
            + ('，不为 0：`x` 里有相邻的 1，也就是原串有相邻的 0 → 跳过' if S.x & (S.x >> 1) else '，为 0：没有相邻的 1 → 原串没有相邻的 0，是有效字符串')),
        'ans.append': '`x ^ mask` 把 `x` 取回原串：`{format(x ^ mask, "0%db" % n)}`，加入答案',
        'return ans': '共 `{len(ret)}` 个有效字符串：`{ret}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='把串取反：不含相邻 0，就是取反后不含相邻 1，一次 AND 就能判断',
        complexity='时间 `O(2^n)`，空间 `O(1)`（不计返回值）',
        problem=['返回所有长为 `n` 的二进制字符串，要求任意两个相邻字符里至少有一个 `"1"`',
                 '也就是==不能出现 `"00"`==，顺序任意',
                 '示例：`n = 3` → `["010","011","101","110","111"]`；本视频 `n = 4`'],
        quote='可以把 i 取反（保留低 n 位），记作 x。问题变成：判断 x 中是否有相邻的 1。我们可以用 x & (x >> 1) 来判断，如果这个值不为零，则说明 x 中有相邻的 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x` 右移一位后，和原来的 `x` 做 AND：同一位两个 1 就说明原来有相邻的 1',
              '直接枚举取反后的 `x`：`x & (x >> 1) == 0` 成立，就把 `x ^ mask` 加入答案',
              '`f"{v:0{n}b}"` 输出长为 `n` 的二进制，带前导零'],
        summary=['时间 `O(2^n)`：瓶颈在枚举，生成字符串的数量只有 `O(φ^n)`',
                 '`mask = (1 << n) - 1`，取反要异或 `mask`，不能用 `~x`',
                 '格式 `:0{n}b` 保证前导零，别漏了',
                 '写法一：回溯，填 1 随便填，填 0 要求前一位是 1，`path` 直接覆盖不用恢复现场，`O(nφ^n)`',
                 '思考：怎样直接跳到下一个合法数，不枚举非法的？'],
    ),
)
