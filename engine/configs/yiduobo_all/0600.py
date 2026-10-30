CONFIG = dict(
    num=600, title='不含连续1的非负整数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='斐波那契递推 + 逐位统计',
    tags=['灵神题单', '数位 DP'],
    code='''
class Solution(object):
    def findIntegers(self, num):

        bits = []
        while num:
            bits.append(num % 2)
            num //= 2
        
        l = len(bits)
        f = [1, 2]
        for index in range(2, l):
            f.append(f[-1] + f[-2])
        
        res = f[l - 1]
        for index in range(l - 2, -1, -1):
            if bits[index] == 1:
                res += f[index]
                if bits[index + 1] == 1:
                    return res
            
        return res + 1
''',
    call='Solution().findIntegers(10)',
    expect=8,
    views=[
        dict(type='array', var='bits', label='bits（低位在前，bits[i] 是第 i 位）', cell=64, h=170,
             pointers={'index': 'blue'}, pointer_labels={'index': 'index'}),
        dict(type='array', var='f', label='f[i]：长度为 i 的合法整数个数（可有前导 0）', cell=64, h=170),
        dict(type='text', h=50, fn=lambda S: f"`res` = ==`{S['res']}`==" if 'res' in S else ''),
    ],
    watch=[('index', 'index', 'blue'), ('l', 'l', 'purple'), ('res', 'res', 'green')],
    captions={
        'bits.append': '取出最低位 `{bits[-1]}`，`bits = {bits}`',
        'num //= 2': '`num` 右移一位 → {num}',
        'l = len(bits)': '`n` 的二进制长度 `l = {l}`，最高位一定是 1',
        'f = [1, 2]': '`f[0] = 1`（空串算一个），`f[1] = 2`（0 和 1 都合法）',
        'f.append': '`f[{len(f)-1}] = f[{len(f)-2}] + f[{len(f)-3}] = {f[-1]}`：最高位填 0 → 剩 i-1 位；填 1 → 次高位必须 0，剩 i-2 位',
        'res = f[l - 1]': '最高位是 1，所以最高位为 0 的 `{l}` 位合法数全都小于 n，先加 `f[{l-1}] = {f[l-1]}`，`res = {res}`',
        'for index in range(l - 2': '从次高位往低位扫，遇 0 跳过，遇 1 就统计',
        'if bits[index] == 1': lambda S, B, r: (f'`bits[{S.index}] = 1`：把这一位改成 0、后面 {S.index} 位随便填的合法数都算进来' if S.bits[S.index] == 1
                                               else f'`bits[{S.index}] = 0`：没法在这位拿到更小的数，跳过'),
        'res += f[index]': '加上 `f[{index}] = {f[index]}` → `res = {res}`',
        'if bits[index + 1] == 1': lambda S, B, r: (f'上一位 `bits[{S.index+1}] = 1` 也是 1 → 出现 `11`，n 自己不合法且更小的都已统计 → ==直接返回 res=={S.res}' if S.bits[S.index+1] == 1
                                                    else f'上一位 `bits[{S.index+1}] = 0`，没有连续 1，继续往后看'),
        'return res + 1': '一路没遇到 `11` → n 本身也合法，前面从不统计 n 自己，所以 `res + 1 = {res + 1}`',
        'return res': '遇到 `11`，返回 `res = {res}`',
    },
    cards=dict(
        one_liner='f 是斐波那契，再沿着 n 的 1 逐位把「改成 0」的方案加起来',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['统计 `[0, n]` 中二进制表示里没有连续 1 的整数个数',
                 '示例：`n = 5` → `5`，`n = 2` → `3`',
                 '本视频：`n = 10`（二进制 `1010`）→ `8`'],
        quote='若其最高位为0，那么此时就相当于长度为i - 1的合法整数个数。若其最高位为1，那么其次高位必须是0，那么此时就相当于长度为i - 2的合法整数个数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i] = f[i-1] + f[i-2]`，`f[0] = 1`、`f[1] = 2`',
              '先加最高位为 0 的 `f[l-1]`；之后每遇到一个 1，加上「这一位改填 0」的 `f[index]`',
              '遇到连续两个 1 就停：之后不会再有合法数；扫完则 n 本身合法，加 1'],
        summary=['时间 `O(log n)`，空间 `O(log n)`',
                 '易错点：`f[0] = 1` 是为了凑递推；n 本身要最后单独 `+1`',
                 '遇到 `11` 要立刻 `return res`，不能加 1',
                 '原文为 Python 2 写法，`num /= 2` 已改为 `num //= 2`',
                 '对比灵神：他用 dfs + is_limit 记忆化，这里把同样的计数写成了递推'],
    ),
)
