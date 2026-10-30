def _bin(S):
    f, n = S.get('f'), S.get('n')
    if f is None:
        return ''
    out = '  '.join(format(x, '0%db' % n) for x in f)
    return f'二进制：{out}'


def _gray(S):
    f, n = S.get('f'), S.get('n')
    if f is None or len(f) < 2:
        return ''
    bad = [i for i in range(len(f)) if bin(f[i] ^ f[(i + 1) % len(f)]).count('1') != 1]
    return '相邻两项（含首尾）都只差一位' if len(f) == 2 ** n and not bad else f'前 {len(f)} 项：相邻只差一位 ✓'


def _newcolor(S, i, v):
    ins = S.get('_inner', {})
    if 'tmp' in ins and 'index' in ins and S['_line'] >= 8 and i >= 2 ** (ins['index'] - 1) and i < 2 ** ins['index']:
        return 'green'
    return None


CONFIG = dict(
    num=1238, title='循环码排序', difficulty='Medium', category='位运算',
    author='yiduobo', technique='镜像反射构造格雷码',
    tags=['灵神题单', '位运算'],
    code='''
class Solution(object):
    def circularPermutation(self, n, start):

        f = [0]
        for index in range(1, n + 1):
            tmp = [x + (1 << (index - 1)) for x in f]
            tmp.reverse()
            f.extend(tmp)
        
        p = 0
        for index, num in enumerate(f):
            if num == start:
                p = index
                break
        
        return f[p:] + f[:p]
''',
    call='Solution().circularPermutation(3, 2)',
    expect=[2, 6, 7, 5, 4, 0, 1, 3],
    views=[
        dict(type='text', fn=_bin, size=24),
        dict(type='array', var='f', label='f（绿 = 本轮新接上的后半段）', color=_newcolor, cell=96, pointers={'p': 'pink'}, h=200),
        dict(type='array', var='tmp', label='tmp = f 每项加上最高位后反转', cell=96, h=200),
        dict(type='text', fn=_gray, size=24),
    ],
    watch=[('n', 'n'), ('start', 'start', 'yellow'), ('index', 'index', 'blue'), ('p', 'p', 'pink')],
    captions={
        'f = [0]': '`n = 0` 时合法序列只有 `[0]`，从它出发一层层扩张',
        'tmp = [': '`f` 每项加上 `1 << {index - 1}` = {1 << (index - 1)}（最高位补 1）→ `tmp = {tmp}`，和 `f` 逐项只差一位',
        'tmp.reverse': '==反过来==：`f` 的最后一项和 `tmp` 的第一项只差最高位，接缝处也合法 → `tmp = {tmp}`',
        'f.extend': '把 `tmp` 接到 `f` 后面：现在 `f` 是 0 ~ {2 ** index - 1} 的合法序列 `{f}`',
        'p = 0': '先随便造出一个合法排列，再找 `start` 的位置，循环移位即可',
        'for index, num': lambda S, B, r: f"检查 `f[{S.index}] = {S.num}`" if 'num' in S else '',
        'if num == start': lambda S, B, r: (f'`{S.num} == start = {S.start}` → ==找到了==' if S.num == S.start
                                            else f'`{S.num} ≠ start = {S.start}`，继续往后找'),
        'p = index': '`start` 在 `f` 的下标 `p = {p}`',
        'break': '找到就停，不用看后面',
        'return': '`f[p:] + f[:p]`：把 `start` 之前的部分挪到末尾，首尾仍只差一位（环）→ =={ret}==',
    },
    cards=dict(
        one_liner='镜像反射：旧序列 + 反转后加最高位的旧序列',
        complexity='时间 `O(2^n)`，空间 `O(2^n)`',
        problem=['给 `n` 和 `start`，把 `0 ~ 2^n − 1` 排成一列：首项是 `start`，',
                 '==相邻两数二进制只差一位==，首尾也只差一位（循环码）',
                 '示例：`n = 3, start = 2` → `[2,6,7,5,4,0,1,3]`'],
        quote='f[0] + 2^(n - 1)，f[1] + 2^(n - 1)，...，反过来，然后拼接在原来的p[0]到p[2^(n - 1) - 1]的后面就可以得到0到2^n - 1的合法序列。',
        quote_src='—— yiduobo 题解原文',
        idea=['只需找到任意一种合法排列，再循环移动到 `start` 开头',
              '设 `0 ~ 2^(n-1)−1` 已有合法排列 `f`；每项加最高位 1 仍合法',
              '`f` 末项与它的加高位版本只差一位，所以把后者==反转==后接上去'],
        result='`f = [0,1,3,2,6,7,5,4]`，`start = 2` 在下标 3 → 循环移位得 `[2,6,7,5,4,0,1,3]` ✓',
        summary=['时间/空间都是 `O(2^n)`，输出本身就这么大',
                 '==必须反转==后半段，否则接缝处 `f[-1]` 和 `f[0]+高位` 差不止一位',
                 '循环移位不破坏“首尾只差一位”，因为这是一个环',
                 '这就是格雷码；灵神也可用公式 `i ^ (i >> 1)` 直接生成'],
    ),
)
