SECRET = 0b10110


def _bits(v, n=8):
    return [int(c) for c in format(v, f'0{n}b')]


def _res(S):
    if 'res' not in S:
        return '要猜的数 `n` 藏在 `commonBits` 里，只能靠它的返回值来推'
    s = f"已确定的低位 `res` = `{format(S['res'], '08b')}` = =={S['res']}=="
    if 'zero' in S:
        s += f"　　`zero`（此刻 n 里 0 的个数）= =={S['zero']}=="
    return s


CONFIG = dict(
    num=3094, title='使用按位查询猜测数字II', difficulty='Medium', category='位运算',
    author='yiduobo', technique='逐位探测 · 对比 zero 计数',
    tags=['灵神题单'],
    setup='''
_n = 22  # 隐藏的 n = 0b10110
def commonBits(num):
    global _n
    cnt = 30 - bin((_n ^ num) & ((1 << 30) - 1)).count('1')
    _n ^= num
    return cnt
''',
    code='''
class Solution(object):
    def findNumber(self):
        
        zero = commonBits(0)
        res = 0
        v = 1
        for index in range(30):
            if commonBits(v) > zero:
                res += v
                zero += 1
            else:
                zero -= 1
            v += v
        
        return res
''',
    call='Solution().findNumber()',
    expect=22,
    views=[
        dict(type='text', fn=_res, size=28, h=110),
        dict(type='array', var=lambda S: _bits(S['res']), h=200, index=False, label='res 的低 8 位（高位在左）',
             color=lambda S, i, v: 'green' if v else None),
        dict(type='text', fn=lambda S: (f"当前探测第 `{S['index']}` 位，`v = {S['v']}`" if 'index' in S and 'v' in S else ''), size=28, h=100),
    ],
    watch=['zero', 'res', 'v', 'index'],
    captions={
        'zero = commonBits(0)': '`commonBits(0)`：n 不变，返回「和 0 相同的位数」= ==n 里 0 的个数==，`zero = {zero}`（共 30 位）',
        'res = 0': '`res` 用来拼出 n 的每一位',
        'v = 1': '`v` 是 2 的幂，每次只探测一位，先从最低位 `2^0` 开始',
        'for index in range(30)': '逐位探测，n 最多 30 位',
        'if commonBits(v) > zero': '调用 `commonBits({v})`：只翻转第 `{index}` 位，并返回相同位数，和 `zero = {zero}` 比较：多了 1 就是 1，少了 1 就是 0',
        'res += v': '这一位是 1：`res += {B.v}` → {res}',
        'zero += 1': '这一位被 `commonBits(v)` 翻转成 0，n 里 0 多了一个：`zero += 1` → {zero}',
        'zero -= 1': '返回值不大于 zero，该位是 ==0==；它被翻转成 1，n 里 0 少了一个：`zero -= 1` → {zero}',
        'v += v': '`v` 翻倍，探测下一位：`v = {v}`',
        'return res': '30 位探测完，`n = {res}`',
    },
    cards=dict(
        one_liner='对每个 2 的幂探测一次：返回值比 zero 大就是 1',
        complexity='时间 `O(30)` 次调用，空间 `O(1)`',
        problem=['有隐藏整数 `n`，只能调用 `commonBits(num)`',
                 '它返回 n 与 num 在 30 位里取值相同的位数，并把 n 改成 `n ^ num`',
                 '通过调用确定 n（本视频用 `n = 22` 演示）'],
        quote='如果知道在进行commonBits前n中0的数量zero，就可以通过commonBits(v)的结果是等于zero还是zero + 1来判断v对应的这一位是0还是1了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`commonBits(0)` 不改 n，得到 n 里 0 的个数 `zero`',
              '探测 `v = 2^k`：该位是 1 → 返回 `zero + 1`，是 0 → 返回 `zero - 1`',
              '每次调用都会翻转该位，所以要同步更新 `zero`'],
        summary=['最多 31 次调用，空间 `O(1)`',
                 '探测会翻转 n 的该位，`zero` 必须跟着 `+1` 或 `-1`',
                 '判断条件用 `> zero`，同时覆盖 `zero + 1` 与 `zero - 1`',
                 '原文为 Python 2 风格写法，代码未改动；`commonBits` 在 `setup` 里按题意实现（含隐藏的 n）'],
    ),
    max_steps=46,
    skip=['for index in range'],
)
