S0, N0 = '11101000', 8


def _win(S):
    if 'index' not in S or 'l' not in S:
        return None
    ln, i, l = S['_line'], S['index'], S['l']
    table = {
        17: (0, i), 18: (0, i), 20: (0, l - 1),
        21: (i - l, i - 1), 22: (i - l + 1, i - 1), 23: (i - l + 1, i), 24: (i - l + 1, i),
        28: (0, i), 29: (0, i), 31: (0, l - 2),
        33: (i - l + 1, i - 1), 34: (i - l + 2, i - 1), 35: (i - l + 2, i), 36: (i - l + 2, i),
    }
    return table.get(ln)


def _wl(S):
    w = _win(S)
    return w and w[0]


def _wr(S):
    w = _win(S)
    return w and w[1]


def _txt(S):
    if 'num_set' not in S:
        if 'pow2' in S:
            return f"`pow2 = {S['pow2']}`，`l = {S['l']}`：找满足 `2^k ≤ N < 2^(k+1)` 的 `2^k` 和位数 `l = k + 1`"
        return '先找 `k`：`2^k ≤ N < 2^(k+1)`'
    if 'num' in S:
        return f"检查 `[2^k, N]`：`{S['num']}` = `{S['num']:b}` " + ('在哈希表中' if S['num'] in S['num_set'] else '==不在==哈希表中')
    return f"`now = {S['now']}` = `{S['now']:b}`　`pow2 = {S['pow2']}`（`% pow2` 去掉最高位）"


CONFIG = dict(
    num=1016, title='子串能表示从 1 到 N 数字的二进制串', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='必要条件剪枝 + 长 k、k+1 滑窗哈希',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def queryString(self, S, N):

        pow2 = 1
        l = 1
        while pow2 <= N:
            pow2 += pow2
            l += 1

        pow2 //= 2
        l -= 1
        if max(pow2 // 2, N - pow2 + 1) > len(S) - l + 1:
            return False

        num_set = set()
        now = 0
        for index in range(l):
            now += now + int(S[index])

        num_set.add(now)
        for index in range(l, len(S)):
            now %= pow2
            now += now + int(S[index])
            num_set.add(now)

        if l > 1:
            now = 0
            for index in range(l - 1):
                now += now + int(S[index])

            num_set.add(now)
            pow2 //= 2
            for index in range(l - 1, len(S)):
                now %= pow2
                now += now + int(S[index])
                num_set.add(now)

        for num in range(pow2 + pow2, N + 1):
            if num not in num_set:
                return False

        return True
''',
    call=f'Solution().queryString({S0!r}, {N0})',
    expect=True,
    views=[
        dict(type='string', var='S', label='S（框 = 当前窗口）', h=210, cell=96,
             pointers={'index': 'blue'}, window=(_wl, _wr)),
        dict(type='text', h=90, size=28, fn=_txt),
        dict(type='set', var='num_set', label='num_set（长 l 和 l−1 的子串编码）', h=200, font=30,
             fmt=lambda v: f'{v:b} ({v})'),
    ],
    watch=[('pow2', 'pow2', 'purple'), ('l', 'l'), ('index', 'index', 'blue'), ('now', 'now', 'orange'), ('num', 'num', 'green')],
    captions={
        'pow2 = 1': '先找 `k`：`2^k ≤ N < 2^(k+1)`，`pow2` 从 1 开始翻倍',
        'l = 1': '`l` 记录 `pow2` 的二进制位数',
        'while pow2 <= N': lambda S, B, r: (f'`pow2 = {S.pow2} ≤ {S.N}`，继续翻倍' if S.pow2 <= S.N
                                            else f'`pow2 = {S.pow2} > {S.N}`，停止'),
        'pow2 += pow2': '`pow2` 翻倍 → `{pow2}`',
        'l += 1': '位数 `l` → `{l}`',
        10: '退回一步：`pow2 = 2^k = {pow2}`',
        'l -= 1': '`l = k + 1 = {l}`：`2^k` 到 `N` 都是 `{l}` 位数',
        'if max(': lambda S, B, r: (f'需要 `{S.pow2 // 2}` 个不同的 {S.l - 1} 位数、`{S.N - S.pow2 + 1}` 个 {S.l} 位数；'
                                    f'`S` 只有 `{len(S.S) - S.l + 1}` 个长 {S.l} 的子串 → ==必要条件成立=='
                                    if max(S.pow2 // 2, S.N - S.pow2 + 1) <= len(S.S) - S.l + 1
                                    else '子串数量不够，必然 False'),
        'num_set = set()': '把长为 `l` 和 `l − 1` 的子串都放进哈希表',
        16: '`now`：窗口的二进制值',
        17: '先读入前 `l = {l}` 个字符',
        18: '`now = now + now + {S[index]}` → `{now}`（`{now:b}`）',
        20: '第一个长 `{l}` 的子串 `{now:b}` 加入哈希表',
        21: lambda S, B, r: ('长 l 的子串统计完' if B.get('index') == S.index else f'窗口右移，读入 `S[{S.index}]`'),
        22: '`now %= {pow2}`：去掉最高位，最左边的字符离开 → `{now}`',
        23: '`now + now + {S[index]}`：新字符从右边进入 → `{now:0{l}b}`',
        24: '`{now:0{l}b}` 加入哈希表',
        'if l > 1': '`l = {l} > 1`：再统计长为 `l − 1 = {l - 1}` 的子串',
        27: '`now` 清零，重新开始',
        28: '先读入前 `l − 1 = {l - 1}` 个字符',
        29: '`now = now + now + {S[index]}` → `{now}`（`{now:b}`）',
        31: '第一个长 `{l - 1}` 的子串 `{now:b}` 加入哈希表',
        32: '`pow2` 再减半为 `{pow2}`，用来去掉 `l − 1` 位窗口的最高位',
        33: lambda S, B, r: ('长 l − 1 的子串统计完' if B.get('index') == S.index else f'窗口右移，读入 `S[{S.index}]`'),
        34: '`now %= {pow2}`：最左边的字符离开 → `{now}`',
        35: '新字符进入 → `{now:0{l - 1}b}`',
        36: '`{now:0{l - 1}b}` 加入哈希表',
        'for num in range': '逐个检查 `[{pow2 + pow2}, {N}]` 里的数',
        'if num not in num_set': lambda S, B, r: (f'`{S.num}`（`{S.num:b}`）==在==哈希表里' if S.num in S.num_set
                                                  else f'`{S.num}` 不在哈希表里'),
        'return True': '全部找到 → `True`',
    },
    skip=[8, 17, 28],
    max_steps=70,
    cards=dict(
        one_liner='N 看着吓人，但 S 只有 1000 长：先用必要条件把大 N 全部筛掉',
        complexity='时间 `O(|S|)`，空间 `O(|S|)`',
        problem=['给二进制串 `S` 和 `N`，判断 `1..N` 的二进制是否==都是== `S` 的子串',
                 '示例：`S = "0110", N = 3` → `true`；`N = 4` → `false`',
                 '本视频：`S = "11101000", N = 8` → `true`'],
        quote='若S的子串可以覆盖住2^(k - 1)到2^k - 1，那么其必然也能覆盖住1到2^(k - 1) - 1……例如1到7分别是9到15的后缀。',
        quote_src='—— yiduobo 题解原文',
        idea=['必要条件：`len(S) − k + 1 ≥ 2^(k−1)` 且 `len(S) − k ≥ N − 2^k + 1`',
              '条件成立时 k 很小（≤ 10），把长 `k`、`k+1` 的子串编码全放进哈希表',
              '加上最高位的 1 得到的数以原数为==后缀==，所以更短的数不用再查'],
        summary=['时间 `O(|S|)`：两次滑窗，最后检查的数不超过 `|S|` 个',
                 '原文为 Python 2 写法，`pow2 /= 2`、`pow2 / 2` 已改为整数除法 `//`',
                 '`now %= pow2` 等价于去掉窗口最高位，和灵神的 `& mask` 作用相同',
                 '注意：原代码最后只核对了 `[2^k, N]`；长 k 的那组（如 `S="1000", N=4` 缺 `11`）没有核对',
                 '对比灵神：思路一致，灵神额外只查 `[N/2+1, 2^k−1]`，并用 `check` 函数复用滑窗'],
    ),
)
