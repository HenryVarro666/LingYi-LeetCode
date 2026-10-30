N, DELAY, FORGET = 6, 2, 4


def _known_arr(S):
    d = S.get('diff')
    if not d:
        return [0] * (N + 1)
    out, run = [0], 0
    for j in range(1, N + 1):
        run += d[j]
        out.append(run)
    return out


def _txt(S):
    if 'i' not in S:
        return '`known[j]` = ==恰好==在第 `j` 天得知秘密的人数；区间加用差分数组 `diff` 完成'
    i, n, de, fo = S['i'], S['n'], S['delay'], S['forget']
    return (f'第 `{i}` 天得知的人，在第 `[{i + de}, {i + fo - 1}]` 天每天分享一次；'
            f'第 `{i + fo}` 天忘记。答案只统计 `i ≥ {n - fo + 1}` 的天')


def _kcol(S, j, v):
    if 'i' not in S:
        return None
    i = S['i']
    if j == i:
        return 'yellow'
    if j >= S['n'] - S['forget'] + 1 and j < i:
        return 'green'
    return None


def _dcol(S, j, v):
    if 'i' not in S or S.get('_line') not in (16, 17):
        return None
    n, i = S['n'], S['i']
    if j == min(i + S['delay'], n + 1) and S.get('_line') == 16:
        return 'green'
    if j == min(i + S['forget'], n + 1) and S.get('_line') == 17:
        return 'pink'
    return None


CONFIG = dict(
    num=2327, title='知道秘密的人数', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='差分数组优化 DP',
    tags=['灵神题单·动态规划', '灵神题单·常用数据结构'],
    code='''
class Solution:
    def peopleAwareOfSecret(self, n: int, delay: int, forget: int) -> int:
        MOD = 1_000_000_007
        diff = [0] * (n + 2)
        diff[1] = 1
        diff[2] = -1
        ans = known = 0

        for i in range(1, n + 1):
            # 加上 diff[i] 后，known 表示恰好在第 i 天得知秘密的人数
            known = (known + diff[i]) % MOD
            # 统计在第 n 天没有忘记秘密的人数
            if i >= n - forget + 1:
                ans += known
            # 恰好在第 i 天得知秘密的人，会在第 [i+delay, i+forget-1] 天分享秘密
            diff[min(i + delay, n + 1)] += known
            diff[min(i + forget, n + 1)] -= known

        return ans % MOD
''',
    call=f'Solution().peopleAwareOfSecret({N}, {DELAY}, {FORGET})',
    expect=5,
    views=[
        dict(type='text', fn=_txt, size=24, h=80),
        dict(type='array', var='diff', label='diff（绿 = 本轮 +known 的位置，粉 = 本轮 −known 的位置）', cell=84,
             pointers={'i': 'blue'}, color=_dcol, h=230),
        dict(type='array', var=_known_arr, label='known[j]（= diff 的前缀和；黄 = 今天，绿 = 计入答案的天）', cell=84,
             color=_kcol, h=200),
    ],
    watch=[('i', 'i', 'blue'), ('known', 'known', 'yellow'), ('ans', 'ans', 'green')],
    skip=['MOD =', 'diff = [0]', 'ans = known = 0'],
    captions={
        'diff[1] = 1': '第 1 天有 1 个人得知秘密：`known[1] = 1`，对应差分 `diff[1] = 1`',
        'diff[2] = -1': '`diff[2] = −1`：`known[1]` 只管第 1 天，差分在第 2 天减回去',
        'for i in range': lambda S, B, r: (f'枚举第 `i = {S.i}` 天' if S.i != B.get('i') else '第 `n` 天处理完，循环结束'),
        'known = (known + diff[i])': '`known = {B.known} + diff[{i}] ({diff[i]})` = =={known}==：恰好第 `{i}` 天得知秘密的人数',
        'if i >= n - forget + 1': lambda S, B, r: (f'`i = {S.i} ≥ n−forget+1 = {S.n - S.forget + 1}`：这一天得知的人在第 `n` 天还没忘 → 计入答案'
                                                   if S.i >= S.n - S.forget + 1 else
                                                   f'`i = {S.i} < n−forget+1 = {S.n - S.forget + 1}`：到第 `n` 天已经忘记了 → 不计'),
        'ans += known': '`ans = {B.ans} + {known}` = {ans}',
        'diff[min(i + delay': '第 `{i + delay}` 天起每天多 `{known}` 个新人：`diff[{min(i + delay, n + 1)}] += {known}`{"（下标超过 n+1，压到 n+1）" if i + delay > n + 1 else ""}',
        'diff[min(i + forget': '第 `{i + forget}` 天忘记，不再分享：`diff[{min(i + forget, n + 1)}] −= {known}`{"（下标超过 n+1，压到 n+1）" if i + forget > n + 1 else "，区间在这里结束"}',
        'return ans': '第 `n` 天没忘记秘密的人数 = `ans % MOD` = =={ret}==',
    },
    cards=dict(
        one_liner='记「恰好第 i 天得知秘密」的人数，区间分享用差分数组加',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['第 1 天一个人发现秘密；发现后 `delay` 天起==每天分享给一个新人==，满 `forget` 天忘记，忘记当天不能分享',
                 '求第 `n` 天结束时知道秘密的人数，结果对 `10^9+7` 取余',
                 '示例：`n = 6, delay = 2, forget = 4` → `5`'],
        quote='考虑维护一个数组 known，其中 known[i] 表示恰好在第 i 天得知秘密的人数。为什么是恰好？如果不这样定义，第 i 天各种人（刚知道秘密，昨天知道秘密，前天知道秘密，……）混在一起，不好处理。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`known[i]` 个人会在 `[i+delay, i+forget−1]` 天各分享一次，即把 `known[j]` 都加上 `known[i]`',
              '这是「区间加」，用差分数组：区间头 `+known`，区间尾后一位 `−known`',
              '答案 = 第 `n` 天没忘记的人 = `i ≥ n−forget+1` 的 `known[i]` 之和'],
        summary=['时间 `O(n)`，空间 `O(n)`；不用差分的暴力写法是 `O(n × (forget − delay))`',
                 '另一种写法：`known[j]` 是 `[j−forget+1, j−delay]` 的区间和，用前缀和 `s` 直接算，同样 `O(n)`',
                 '易错：下标要压到 `n+1`（`min(…, n+1)`），`diff` 长度开 `n+2`',
                 '取模放在 `known` 上；最后 `ans % MOD`'],
    ),
)
