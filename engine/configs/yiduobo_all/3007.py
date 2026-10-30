K0, X0 = 9, 1


def _bits(S):
    if 'res' not in S or 'p' not in S:
        return None
    return [str(S['res'] >> j & 1) for j in range(3, -1, -1)]


def _fml(S):
    if 'cnt' in S and 'index' in S and 'prefix_one' in S:
        return (f'第 {S["index"]} 位置 1 的额外 1 个数：`prefix_one × 2^{S["index"] - 1}` + `f[{S["index"] - 1}]` = '
                f'{S["prefix_one"]} × {1 << (S["index"] - 1)} + {S["f"][S["index"] - 1]} = =={S["cnt"]}==')
    if 'f' in S:
        return '`f[i]` = 0 到 2^i - 1 中，x 倍数位上 1 的总数；`f[i] = 2·f[i-1]`，若 i 是 x 的倍数再加 `2^(i-1)`'
    return ''


CONFIG = dict(
    num=3007, title='价值和小于等于 K 的最大数字', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='预处理 f[i] + 高位到低位构造',
    tags=['位运算', '难度分 2258'],
    code='''
class Solution(object):
    def findMaximumNumber(self, k, x):

        f = [0]
        p = 1
        while f[-1] <= k:
            f.append(f[-1] + f[-1])
            if p % x == 0:
                f[-1] += (1 << (p - 1)) 
            p += 1

        print(f)

        p -= 1
        res = 1 << (p - 1)
        if p % x == 0:
            prefix_one = 1
        else:
            prefix_one = 0
        k -= f[-2]

        for index in range(p - 1, 0, -1):
            cnt = prefix_one * (1 << (index - 1)) + f[index - 1]

            if cnt <= k:
                res |= 1 << (index - 1)
                k -= cnt
                if index % x == 0:
                    prefix_one += 1
        
        return res - 1
''',
    call=f'Solution().findMaximumNumber({K0}, {X0})',
    expect=6,
    skip=['f = [0]', 'p = 1', 'p += 1', 'print(f)', 'else:', 'prefix_one = 0', 'prefix_one += 1'],
    views=[
        dict(type='text', fn=_fml, size=24, h=110),
        dict(type='array', var='f', label='f[i]：0 到 2^i - 1 中，x 倍数位上 1 的总数（蓝 = 当前用到的 f[index-1]）',
             pointers={'index - 1 if index else p - 1': 'blue'} if False else {}, cell=110, h=200,
             color=lambda S, i, v: 'blue' if 'index' in S and i == S['index'] - 1 else None),
        dict(type='array', var=_bits, index=False, label='res 的二进制（左高右低，共 4 位；绿 = 已确定为 1）', cell=100, h=190,
             color=lambda S, i, v: 'green' if v == '1' else None),
    ],
    watch=[('p', 'p', 'blue'), ('index', 'index', 'blue'), ('cnt', 'cnt', 'orange'), ('k', 'k', 'yellow'),
           ('prefix_one', 'prefix_one', 'purple'), ('res', 'res', 'green')],
    captions={
        'while f[-1] <= k': lambda S, B, r: (f'`f[-1] = {S["f"][-1]}` ≤ `k = {S["k"]}`：还没超过 k，继续向上算 f' if S['f'][-1] <= S['k']
                                              else f'`f[-1] = {S["f"][-1]}` > `k = {S["k"]}`：超过了 → 答案的位数就是 `p - 1` 位'),
        'f.append(f[-1] + f[-1])': '`f[{p}] = 2·f[{p - 1}]`：高 `{p}` 位数里，低 `{p - 1}` 位那部分对齐地出现两次，先加两倍',
        'if p % x == 0': lambda S, B, r: (f'`p = {S["p"]}` 是 `x = {S["x"]}` 的倍数：最高位也算价值' if S['p'] % X0 == 0
                                          else f'`p = {S["p"]}` 不是 `x` 的倍数，最高位不算价值'),
        'f[-1] += (1 << (p - 1))': '加上 `2^{p - 1}`：这些数的最高位（第 {p} 位）都是 1，且恰好是 x 的倍数位 → `f[{p}]` = =={f[-1]}==',
        'p -= 1': '循环多算了一格：答案的最高位是第 `p = {p}` 位',
        'res = 1 << (p - 1)': '答案最高位一定是 1：`res` = =={res}==（二进制 `{res:b}`）',
        'prefix_one = 1': '最高位本身是 x 的倍数位 → `prefix_one = 1`',
        'k -= f[-2]': '最高位已定为 1：比它小的 `0 ~ 2^{p - 1} - 1` 全部合法，它们的价值和 `f[{p - 1}]` = {f[-2]} 要先花掉 → `k` = =={k}==',
        'for index in range': lambda S, B, r: (f'从第 `{S["index"]}` 位往低位逐位试填（`index` 从 1 数起）' if S.get('index') != B.get('index') else '所有低位都试完了'),
        'cnt = prefix_one': ('这位置 1，新增 2^{index-1} 个数：前缀里 `prefix_one = {prefix_one}` 个有效 1 各贡献一次，'
                             '低位部分正好是完整的 `f[{index - 1}]` = {f[index - 1]} → ==cnt = {cnt}=='.replace('==cnt = {cnt}==', 'cnt = =={cnt}==')),
        'if cnt <= k': lambda S, B, r: (f'`cnt = {S["cnt"]}` ≤ `k = {S["k"]}`：预算够，这位==置 1=='
                                        if S['cnt'] <= S['k'] else f'`cnt = {S["cnt"]}` > `k = {S["k"]}`：预算不够，这位保持 0'),
        'res |= 1 << (index - 1)': '第 `{index}` 位置 1：`res` = =={res}==（二进制 `{res:b}`）',
        'k -= cnt': '预算用掉 `cnt`：`k` = =={k}==',
        'if index % x == 0': lambda S, B, r: ('第 `index` 位是 x 的倍数位 → `prefix_one` 加一'.replace('index', str(S['index'])) if S['index'] % X0 == 0
                                              else '这一位不是 x 的倍数位，`prefix_one` 不变'),
        'return res - 1': '构造出的 `res` 统计的是 ==0 到 res-1== 的价值，所以返回 `res - 1` = =={res - 1}=='
    },
    cards=dict(
        one_liner='先算 f[i]（0 到 2^i-1 的价值和），再从高位到低位构造答案',
        complexity='时间 `O(log k)`，空间 `O(log k)`',
        problem=['`num` 的价值 = 二进制中第 `x, 2x, 3x…` 位上 1 的个数（从低位数起）',
                 '累加价值 = 1 到 num 的价值之和；要 ≤ `k`，求最大的 `num`',
                 '示例：`k = 9, x = 1` → `6`（1 到 6 累加价值恰为 9）'],
        quote='因此，如果将答案的第m位置为1，那么就会添加prefix_one * 2^(m - 1) + f[m - 1]个额外的1，不妨记为cnt。',
        quote_src='—— yiduobo 题解原文',
        idea=['先看 x=1：`f[i] = 2·f[i-1] + 2^(i-1)`，x>1 时只在 i 是 x 的倍数才加后一项',
              '不断算 f，直到 `f[i]` 超过 k，就得到答案的位数',
              '再从次高位往下填：置 1 的代价 `cnt = prefix_one·2^(m-1) + f[m-1]`，付得起就置 1'],
        summary=['时间 `O(log k)`：f 的长度和填位次数都是位数级别',
                 '易错：填出的 v 统计的是 0 到 v-1 的价值，答案要 `v - 1`',
                 '易错：`p` 循环结束后多加了 1，要先 `p -= 1`',
                 '原文已是 Python 3 可运行的写法，代码未改（`print(f)` 只是原文留下的调试输出）'],
    ),
)
