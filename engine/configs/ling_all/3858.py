def _ok(S, i, j, v):
    if 'mask' not in S or S.get('_line') is None:
        return None
    return 'green' if (v | S['mask']) == S['mask'] else 'red'


def _bin(S, k):
    return format(S[k], '03b') if k in S else '---'


CONFIG = dict(
    num=3858, title='按位或的最小值', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='试填法：高位优先填 0',
    tags=['灵神题单·位运算', '难度分 1947'],
    code='''
class Solution:
    def minimumOR(self, grid: List[List[int]]) -> int:
        # 每行选个最小值，计算 OR，答案 <= OR（答案的二进制长度至多为这些数的最大值的二进制长度）
        mx = max(map(min, grid))  

        ans = 0
        # 试填法：ans 的第 i 位能不能是 0？
        # 如果在每一行的能选的数字中，都存在第 i 位是 0 的数，那么 ans 的第 i 位可以是 0，否则必须是 1
        for i in range(mx.bit_length() - 1, -1, -1):
            mask = ans | ((1 << i) - 1)  # mask 低于 i 的比特位全是 1，表示 grid[i][j] 的低位是 0 还是 1 无所谓
            for row in grid:
                for x in row:
                    # x 的高于 i 的比特位，如果 mask 是 0，那么 x 的这一位必须也是 0（注意 mask 继承了 ans 高位中的 0）
                    # x 的低于 i 的比特位，随意
                    # x 的第 i 个比特位，我们期望它是 0
                    if (x | mask) == mask:  # x 可以选，且第 i 位是 0
                        break
                else:  # 这一行的可选数字中，第 i 位全是 1
                    ans |= 1 << i  # ans 第 i 位必须是 1
                    break  # 填下一位
        return ans
''',
    call='Solution().minimumOR([[3, 5], [6, 4]])',
    expect=5,
    views=[
        dict(type='grid', var='grid', h=240, cell=96, label='grid（绿 = 能选且第 i 位为 0，红 = 不能选）', color=_ok),
        dict(type='text', size=34, fn=lambda S: f"`ans  = {_bin(S, 'ans')}`" if 'ans' in S else ''),
        dict(type='text', size=34, fn=lambda S: f"`mask = {_bin(S, 'mask')}`   （第 {S['i']} 位及更高的 0 = 不许出现的 1）" if 'mask' in S and 'i' in S else ''),
        dict(type='text', size=34, fn=lambda S: (f"`x = {S['x']:03b}`  `x | mask = {S['x'] | S['mask']:03b}` " + ('==等于 mask，能选==' if (S['x'] | S['mask']) == S['mask'] else '不等于 mask，不能选')) if 'x' in S and 'mask' in S else ''),
    ],
    watch=[('mx', 'mx', 'blue'), ('i', 'i', 'cyan'), ('x', 'x', 'pink'), ('mask', 'mask', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'mx = max': '每行的最小值里取最大 `mx = {mx}`：每行选最小值，OR 不会超过它的二进制长度，高位不用试',
        'ans = 0': '`ans` 从 0 开始，逐位试填',
        'for i in range': lambda S, B, r: (f'试填：`ans` 的第 `{S.i}` 位能不能是 ==0==？（从高到低，高位是 0 更小）' if not (S.i == 0 and B.i == 0) else '所有位都试完了，退出循环'),
        'mask = ans': '`mask = {mask:03b}`：低于第 `{i}` 位全当 1（无所谓），高位继承 `ans`，其中的 0 表示该位不许出现 1',
        'for row in grid': lambda S, B, r: (f'检查下一行 `{S.row}`：这一行有没有能选且第 `{S.i}` 位为 0 的数' if not (S.row == B.get('row') and S.row == S.grid[-1]) else f'每一行都有能选的数 → 第 `{S.i}` 位可以填 ==0==，`ans` 不变'),
        'for x in row': lambda S, B, r: (f'看这一行的 `{S.x}`' if not (B.get('x') == S.x and S.x == S.row[-1] and B.get('row') == S.row) else '这一行的数都看过了，没有一个能选'),
        'if (x | mask) == mask': lambda S, B, r: (f'`x | mask = {S.x | S.mask:03b}` 等于 `mask` → x 没有越界的 1，且第 `{S.i}` 位是 0 → ==能选==，这一行没问题' if (S.x | S.mask) == S.mask else f'`x | mask = {S.x | S.mask:03b}` ≠ `mask` → x 带了不许有的 1，==不能选==，看下一个'),
        'else:': '这一行所有数都不能选（第 `{i}` 位全是 1）',
        'ans |= 1 << i': '某一行逼得这一位必须是 1：`ans = {ans:03b}`',
        'break  # 填下一位': '这一位已经确定，不必再看后面的行，去试更低位',
        'break': '这一行有能选的数，不用再看，换下一行',
        'return': '逐位试填完成：`ans = {ans}`（选 5 和 4，5 | 4 = 5）',
    },
    max_steps=70,
    cards=dict(
        one_liner='高位优先：每一行都有第 i 位为 0 的可选数，这一位就填 0',
        complexity='时间 `O(mn log U)`，空间 `O(1)`',
        problem=['`grid` 每行恰好选一个整数，求这些整数按位或的最小值',
                 '示例：`[[3,5],[6,4]]` → `5`（选 5 和 4）'],
        quote='要想让答案尽量小，那么答案二进制的高位是 0 比是 1 更好，所以优先判断答案的高位能否是 0，即从高到低依次判断答案的第 i 位能不能是 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['已确定为 0 的比特位：这一位上是 1 的数不能选（x 必须是答案的子集）',
              '`(x | mask) == mask` 一句话判断：x 的高位合法，且第 i 位是 0',
              '每行都找到能选的数 → 这一位填 0；否则必须填 1'],
        summary=['时间 `O(mn log U)`，空间 `O(1)`',
                 '`mask` 把低于 i 的位全设为 1，表示低位随意；==高位继承 ans 里的 0==',
                 '`for ... else`：内层没有 break，说明这一行没有可选数',
                 '思考题：改成 OR 的最大值，同样用试填法，反过来先试填 1'],
    ),
)
