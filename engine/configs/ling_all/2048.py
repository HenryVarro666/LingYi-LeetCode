def _status(S):
    ln = S.get('_line')
    if 'free' in S and 'j' in S and 'cnt' in S and 'target' not in S:
        return f"试 `s[{S['i']}] = {S['j']}`：补满后可随便填的位数 `free = {S['free']}`（< 0 即不合法）"
    if 'target' in S:
        return f"0-1 背包：从 `a` 里选字典序最小、和为 `{S['target']}` 的数字"
    return '`s` 是 n 的数位（前面补了一个前导 0），`cnt[x]` = 数字 x 已固定的个数'


CONFIG = dict(
    num=2048, title='下一个更大的数值平衡数', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='倒序贪心 + 0-1 背包',
    tags=['贪心与思维'],
    code='''
class Solution:
    # 从 a 中选一个字典序最小的、元素和等于 target 的子序列
    # a 已经从小到大排序
    # 无解返回 None
    def zeroOneKnapsack(self, a: List[int], target: int) -> Optional[List[int]]:
        n = len(a)
        f = [[False] * (target + 1) for _ in range(n + 1)]
        f[n][0] = True

        # 倒着 DP，这样后面可以正着（从小到大）选
        for i in range(n - 1, -1, -1):
            v = a[i]
            for j in range(target + 1):
                if j < v:
                    f[i][j] = f[i + 1][j]
                else:
                    f[i][j] = f[i + 1][j] or f[i + 1][j - v]

        if not f[0][target]:
            return None

        ans = []
        j = target
        for i, v in enumerate(a):
            if j >= v and f[i + 1][j - v]:
                ans.append(v)
                j -= v
        return ans

    def nextBeautifulNumber(self, n: int) -> int:
        s = "0" + str(n)  # 补一个前导零，方便处理答案十进制串比 n 的十进制串长的情况
        s = list(map(int, s))  # 避免在后续循环中反复调用 int
        m = len(s)

        MX = 10
        cnt = [0] * MX
        for i in range(1, m):
            cnt[s[i]] += 1

        # 从右往左尝试
        for i in range(m - 1, -1, -1):
            if i > 0:
                cnt[s[i]] -= 1  # 撤销

            # 增大 s[i] 为 j
            for j in range(s[i] + 1, MX):
                cnt[j] += 1

                # 后面 [i+1, m-1] 需要补满 0 < cnt[k] < k 的数字 k，剩余数位可以随便填
                free = m - 1 - i  # 统计可以随便填的数位个数
                for k, c in enumerate(cnt):
                    if k < c:  # 不合法
                        free = -1
                        break
                    if c > 0:
                        free -= k - c
                if free < 0:  # 不合法，继续枚举
                    cnt[j] -= 1
                    continue

                # 对于可以随便填的数位，计算字典序最小的填法
                a = [k for k in range(1, MX) if cnt[k] == 0]
                missing = self.zeroOneKnapsack(a, free)
                if missing is None:  # 无解，继续枚举
                    cnt[j] -= 1
                    continue

                for v in missing:
                    cnt[v] = -v  # 用负数表示可以随便填的数

                s[i] = j
                del s[i + 1:]
                for k, c in enumerate(cnt):
                    s += [k] * (k - c if c > 0 else -c)
                return int(''.join(map(str, s)))

        return -1  # 无解（本题不会发生，但为了可扩展性保留）
''',
    call='Solution().nextBeautifulNumber(1)',
    expect=22,
    skip=['for j in range(target + 1)', 'v = a[i]', 'n = len(a)', 'MX = 10', 'for k, c in enumerate(cnt)', 'if c > 0', 'free -= k - c',
          'for i, v in enumerate(a)', 'ans = []', 'if k < c', 'free = -1', 'break', 'for v in missing', 'cnt[v] = -v', 'else:', 'if j < v', 'cnt[j] -= 1', 'j = target', 'continue', 'free = m - 1 - i', 'cnt[j] += 1', 'for i in range(n - 1', 'f[i][j] = f[i + 1][j]', 'if j >= v and', 'ans.append(v)', 'j -= v'],
    views=[
        dict(type='text', fn=_status, size=24, h=60),
        dict(type='array', var='s', label='s（数位，首位补 0）', pointers={'i': 'pink'}, h=170,
             color=lambda S, k, v: 'yellow' if k == S.get('i') else None),
        dict(type='array', var='cnt', label='cnt[x]：数字 x 的计数（负数 = 可随便填）', pointers={'j': 'blue'}, h=170, cell=64),
        dict(type='array', var='a', label='a：计数为 0 的非零数字', h=150, cell=64),
        dict(type='table', var='f', label='f[i][j]：a[i:] 能否凑出和 j', h=200, cell=60),
    ],
    max_steps=110,
    watch=['i', 'j', 'free', ('missing', 'missing', 'green'), ('target', 'target')],
    captions={
        's = "0"': '`n = {n}` 转成数位，前面补个前导 0：答案可能比 n 多一位',
        'cnt[s[i]] += 1': '统计 `s` 里各数字出现次数：`cnt[{s[i]}]` = {cnt[s[i]]}',
        'for i in range(m - 1': '==从右往左==试：尽量只改靠后的数位，这样结果最小。`i = {i}`',
        'cnt[s[i]] -= 1': '撤销 `s[{i}]` 的计数，准备把它改大',
        'for j in range(s[i] + 1': '把 `s[{i}]` 增大为 `j = {j}`（必须比原来的大）',
        'cnt[j] += 1': '放入数字 `{j}`，`cnt[{j}]` = {cnt[j]}',
        'free = m - 1 - i': '后面还有 `{m - 1 - i}` 位可以填，先全算作自由位',
        'if free < 0': lambda S, B, r: ('`free < 0`：某数字超过 x 次，或补不满 → `j = {}` ==不合法==，放弃，试更大的'.format(S.j) if S.free < 0
                                         else f'`free = {S.free} >= 0`：把 0 < cnt[x] < x 的数字补满后，还剩 {S.free} 位随便填'),
        'a = [k': '剩下的自由位只能用 ==还没出现过的非零数字==：`a = {a}`',
        'missing = self': '用 0-1 背包在 `a` 里选字典序最小、和恰好为 `free = {free}` 的数字',
        'f[n][0] = True': '空集凑出和 0：`f[n][0] = True`',
        'if not f[0][target]': lambda S, B, r: ('表填完了：`f[0][%d]` 为假，凑不出 → 返回 `None`' % S.target if not S.f[0][S.target]
                                                 else '表填完了：`f[0][%d]` 为真有解 → 下面正着（从小到大）还原方案' % S.target),
        'return ans': '背包选出的数字：`{ans}`',
        'if missing is None': lambda S, B, r: ('无解，继续枚举下一个 `j`' if S.missing is None else f'有解 `{S.missing}`：这些数字要补进去'),
        's[i] = j': '确定答案：`s[{i}] = {j}`，后面的数位重新构造',
        'del s[i + 1:]': '删掉 `i` 后面的数位，准备按计数重新填',
        's += [k]': '数字 `k` 填 `k - cnt[k]` 个（负数表示填 `-cnt[k]` 个），从小到大排列',
        'return int': '拼出答案 `{s}` → =={int("".join(map(str, s)))}==',
    },
    cards=dict(
        one_liner='倒着改数位，后面用背包补出字典序最小的填法',
        complexity='时间 `O(D²log²n)`，`D = 10`；空间 `O(D log n)`',
        problem=['数值平衡数：每个数位 `d` 恰好出现 `d` 次',
                 '给定 `n`，求==严格大于== `n` 的最小数值平衡数',
                 '示例：`n = 1` → `22`；`n = 1000` → `1333`；本视频演示 `n = 1`'],
        quote='倒着遍历 s，设 d = s[i]，尝试把 s[i] 增大为 d+1, d+2, ..., 9。剩余位置可以随便填，我们需要补满 0 < cnt[x] < x 的数字 x，把 x 的出现次数变成 x。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['先补前导 0，因为答案可能比 n 长一位',
              '从右往左枚举改哪一位、改成多大：==越靠右改，结果越小==',
              '改完后检查：已有数字不能超过自己的值；缺的数字先补满；剩下的位数用 0-1 背包凑出字典序最小的组合'],
        result='`n = 1` → 把末位试到 2 不行，最后把前导 0 改成 2，再补一个 2 → `22` ✓',
        after=[dict(heading='另一种写法：方法一暴力枚举', lines=[
            '`n` 加一，用 `Counter` 看每个数字出现次数是否等于自身',
            '本题 `n ≤ 10^6`，答案不超过 7 位，枚举即可，时间 `O(n log n)`',
            '倒序贪心的优点：`n` 到 `10^18` 也能瞬间算出'])],
        summary=['时间 `O(D²log²n)`，空间 `O(D log n)`，`D = 10`',
                 '易错：忘记补前导 0，答案比 n 长一位时会丢解',
                 '`cnt` 里用负数表示「可随便填」的数字，最后统一展开',
                 '同类题：3720 大于目标字符串的最小字典序排列、3646 下一个特殊回文数'],
    ),
)
