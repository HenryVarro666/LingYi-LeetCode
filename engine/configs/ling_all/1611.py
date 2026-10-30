W = 4


def _bits(S):
    return [(S['n'] >> (W - 1 - i)) & 1 for i in range(W)]


def _low(S):
    n = S['n']
    return W - 1 - ((n & -n).bit_length() - 1) if n > 0 else None


def _txt(S):
    n = S['n']
    s = f"`n` = `{n:0{W}b}`"
    if 'lb' in S:
        s += f"，最低位的 1：`lb` = `{S['lb']}`"
    return s


CONFIG = dict(
    num=1611, title='使整数变为 0 的最少操作次数', difficulty='Hard', category='位运算',
    author='灵茶山艾府', technique='格雷码：从最低位的 1 往上逐个交替加减',
    tags=['位运算', '贪心与思维'],
    code='''
class Solution:
    def minimumOneBitOperations(self, n: int) -> int:
        ans = 0
        while n > 0:
            lb = n & -n  # n 的最低 1
            ans = (lb << 1) - 1 - ans
            n ^= lb  # 去掉 n 的最低 1
        return ans
''',
    call='Solution().minimumOneBitOperations(13)',
    expect=9,
    views=[
        dict(type='text', fn=_txt, size=30, h=70),
        dict(type='array', var=_bits, label='n 的二进制（从高位到低位：8 4 2 1），蓝 = 最低位的 1', cell=84, h=190,
             pointers={_low: 'blue'}, pointer_labels={_low: 'lb'},
             color=lambda S, i, v: 'green' if v else None, dim=lambda S, i, v: not v),
        dict(type='text', fn=lambda S: (f"`ans = lb×2 − 1 − ans`" if 'lb' in S else '`ans` 从 0 开始（递归边界 `f(0) = 0`）'), size=28, h=70),
    ],
    watch=[('n', 'n', 'cyan'), ('lb', 'lb', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans = 0`：相当于递归边界 `f(0) = 0`',
        'while n > 0': lambda S, B, r: (f'`n = {S.n} > 0`：还有 1 没处理，继续' if S.n > 0 else '`n = 0`：所有 1 都处理完了'),
        'lb = n & -n': '`n & -n` 取最低位的 1：`lb = {lb}`，它是递归写法里的 `2^(k-1)`：从 0 走到 `{lb}` 共 `{lb}×2 - 1` 步',
        'ans = (lb << 1)': '走到 `{lb}` 要 `{lb}×2 - 1` 步，低位部分 `{B.ans}` 步重复了，要减掉：`ans = {lb}×2 - 1 - {B.ans}` = =={ans}==',
        'n ^= lb': lambda S, B, r: f'去掉最低位的 1：`n` → `{S.n}`' + ('，下一轮处理更高一位的 1' if S.n else '，没有 1 了'),
        'return ans': '没有 1 了，答案 ==`{ans}`==',
    },
    cards=dict(
        one_liner='从 0 往回走，到 2^k 要 2^(k+1)-1 步；多出来的部分一正一负地减',
        complexity='时间 `O(log n)`（循环次数 = `n` 里 1 的个数），空间 `O(1)`',
        problem=['操作 1：翻转最低位；操作 2：若第 `i-1` 位是 1 且更低位全 0，翻转第 `i` 位',
                 '求把 `n` 变成 `0` 的最少操作次数',
                 '示例：`n = 3` → `2`；`n = 6` → `4`；本视频用 `n = 13`'],
        quote='逆向思维，从 0 开始操作……最优操作方案是唯一的。f(n) = 2^k - 1 - f(n - 2^(k-1))，其中 n - 2^(k-1) 表示 n 去掉最高的 1 后的值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['操作可逆，从 0 往外走：两种操作交替，路线唯一，经过 `2^k` 前走完 `0..2^(k+1)-1` 所有数',
              '`f(2^k) = 2^(k+1) - 1`；一般数 `f(n) = 2^k - 1 - f(去掉最高 1)`',
              '写法二从低到高遍历 1：`ans = lb×2 - 1 - ans`，相当于只在「归」时算'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '易错点：用「减」，所以每一层符号交替；`ans` 初值为 0',
                 '`n & -n` 是最低位的 1，`n ^= lb` 去掉它',
                 '写法一（递归）：`(1<<k) - 1 - f(n - (1<<(k-1)))`，与本写法等价',
                 '这个序列就是格雷码，答案是 `n` 的格雷码逆变换（`n ^= n>>1 ...`）'],
    ),
)
