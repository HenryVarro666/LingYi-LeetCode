def _txt(S):
    if 'pow10' not in S:
        return ''
    return f"当前位权 `pow10 = {S['pow10']}`，剩余 `n = {S['n']}`"


CONFIG = dict(
    num=3697, title='计算十进制表示', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='逐位取模 + 位权', tags=[],
    code='''
class Solution:
    def decimalRepresentation(self, n: int) -> List[int]:
        ans = []
        pow10 = 1
        while n:
            n, d = divmod(n, 10)
            if d:
                ans.append(d * pow10)
            pow10 *= 10
        ans.reverse()
        return ans
''',
    call='Solution().decimalRepresentation(5072)',
    expect=[5000, 70, 2],
    views=[
        dict(type='text', h=70, size=36, fn=_txt),
        dict(type='array', var='ans', label='ans（从低位到高位收集）', cell=130, h=200),
    ],
    watch=[('n', 'n', 'blue'), ('d', 'd', 'cyan'), ('pow10', 'pow10', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'ans = []': '`ans` 收集非零数位对应的分量',
        'pow10 = 1': '`pow10` 是当前数位的权：个位 1，十位 10，……',
        'while n': lambda S, B, r: (f'`n = {S.n}` 还不为 0，继续拆数位' if S.n else '`n = 0`：数位拆完了'),
        'divmod': '`n` 除以 10：商 `{n}` 留作下一轮，余数 `d = {d}` 就是当前数位',
        'if d': lambda S, B, r: (f'`d = {S.d}` 非零 → 要用一个分量表示' if S.d else '`d = 0` → 这一位不需要分量，跳过'),
        'ans.append': '分量 = 数位 × 位权 = `{d} × {pow10}` = =={d * pow10}==，加入 `ans`',
        'pow10 *= 10': '往高一位：`pow10` → {pow10}',
        'ans.reverse': '我们是从低位算到高位的，反转成降序：`{ans}`',
        'return ans': '答案 `{ret}`',
    },
    cards=dict(
        one_liner='每个非零数位 × 位权，就是一个分量',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['把 `n` 拆成最少个「一位数字 × 10 的幂」之和',
                 '返回这些分量，按降序排列',
                 '示例：`537` → `[500,30,7]`；本视频：`5072` → `[5000,70,2]`'],
        quote='不断地把 n 除以 10（下取整）直到 0，这个过程中的 n mod 10，即为每个数位。我们需要对其中不为 0 的数位，乘以 10^k。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`divmod(n, 10)` 一步同时得到「下一轮的 n」和「当前数位」',
              '数位非零才加入答案：每个非零数位恰好需要一个分量，所以个数最少',
              '从低位算到高位，最后 `reverse` 得到降序'],
        summary=['时间 `O(log n)`，空间 `O(1)`（返回值不计入）',
                 '易错：数位为 0 不能加入 0；`pow10` 无论如何都要乘 10',
                 '易错：别忘了最后反转，题目要求降序'],
    ),
)
