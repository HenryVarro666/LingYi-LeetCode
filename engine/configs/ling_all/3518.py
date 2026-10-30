def _fmt(S):
    perm, k = S.get('perm'), S.get('k')
    if perm is None:
        return '左半边字母 `total` 决定了排列个数；目标：第 `k` 小'
    i = S.get('i')
    return f'已确定排列数 `perm = {perm}`，还差第 `k = {k}` 小' + (f'，当前填第 `{i}` 位' if i is not None and i >= 0 else '')


CONFIG = dict(
    num=3518, title='最小回文排列 II', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='试填法 + 倒着算排列数',
    tags=['组合数学', '难度分 2375'],
    code='''
class Solution:
    def smallestPalindrome(self, s: str, k: int) -> str:
        n = len(s)
        m = n // 2

        total = [0] * 26
        for b in s[:m]:
            total[ord(b) - ord('a')] += 1

        cnt = [0] * 26
        perm = 1
        i, j = m - 1, 25
        # 倒着计算排列数
        while i >= 0 and perm < k:
            while cnt[j] == total[j]:
                j -= 1
            cnt[j] += 1
            perm = perm * (m - i) // cnt[j]
            i -= 1

        if perm < k:
            return ""

        left_s = []
        # 已经有足够的排列数了，<= i 的位置直接填字典序最小的排列
        for ch, c in enumerate(cnt[:j + 1]):
            left_s.append(ascii_lowercase[ch] * (total[ch] - c))

        # 试填法
        j0 = j
        for i in range(i + 1, m):
            for j in range(j0, 26):
                if cnt[j] == 0:
                    continue
                # 假设填字母 j，根据 perm = p * (m - i) / cnt[j] 倒推 p
                p = perm * cnt[j] // (m - i)
                if p >= k:
                    left_s.append(ascii_lowercase[j])
                    cnt[j] -= 1
                    perm = p
                    break
                k -= p

        ans = left_s = ''.join(left_s)
        if n % 2:
            ans += s[n // 2]
        return ans + left_s[::-1]
''',
    call="Solution().smallestPalindrome('aabbcbbaa', 2)",
    expect='ababcbaba',
    skip=['while cnt[j] == total[j]', 'j -= 1', 'break', 'if cnt[j] == 0', 'continue', 'n = len(s)', 'for b in s[:m]', 'total[ord(b)'],
    views=[
        dict(type='string', var='s', label='s（回文，只看左半边，奇数长度的正中间固定不动）', h=130, cell=60),
        dict(type='array', var='total', label='total：左半边每个字母的个数（下标 0=a, 1=b, …）', h=130, cell=34,
             color=lambda S, i, v: 'green' if v else None, dim=lambda S, i, v: v == 0),
        dict(type='array', var='cnt', label='cnt：已经（倒着）放进来的个数', h=165, cell=34, pointers={'j': 'pink'},
             color=lambda S, i, v: 'blue' if v else None, dim=lambda S, i, v: v == 0),
        dict(type='text', fn=_fmt, size=26, h=60),
        dict(type='array', var='left_s', label='left_s：左半边答案（一段一段拼）', h=130, cell=70),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('perm', 'perm', 'green'), ('k', 'k', 'yellow')],
    captions={
        'm = n // 2': '只需排左半边，长度 `m = {m}`',
        'perm = 1': '`perm` = 当前已放入的这些字母能排出多少种排列，先从 1 开始',
        'while i >= 0 and perm < k': lambda S, B, r: (f'`perm = {S.perm}` 还不到 `k = {S.k}`，==继续倒着加字母==' if S.i >= 0 and S.perm < S.k
                                                       else f'`perm = {S.perm} ≥ k = {S.k}`，排列数已经够了 → ==前 {S.i + 1} 位直接填最小的=='),
        'cnt[j] += 1': '从最大的字母往小放：放入字母 `{ascii_lowercase[j]}`，`cnt[{j}]` = {cnt[j]}',
        'perm = perm * (m - i) // cnt[j]': '新排列数 = 旧 × `{m - i}` ÷ `{cnt[j]}` = =={perm}==（多一个位置，相同字母要去重）',
        'if perm < k': lambda S, B, r: ('所有排列加起来也不到 `k` → 返回空串' if S.perm < S.k else f'`perm = {S.perm} ≥ k = {S.k}` → 一定有解'),
        'left_s.append(ascii_lowercase[ch]': '`perm ≥ k`，前面这些位置不影响名次 → 把剩余的字母按==从小到大==直接放：{left_s}',
        'for i in range(i + 1': '前 `{i + 1}` 位已经定了；从第 `{i + 1}` 位起用==试填法==一位一位定',
        'p = perm * cnt[j] // (m - i)': '假设这一位填字母 `{ascii_lowercase[j]}`：剩余位置排列数 `p = {perm} × {cnt[j]} ÷ {m - i}` = =={p}==',
        'if p >= k': lambda S, B, r: (f'`p = {S.p} ≥ k = {S.k}`：够 k 个 → ==这一位就填 {ascii_lowercase[S.j]}==' if S.p >= S.k
                                       else f'`p = {S.p} < k = {S.k}`：这一整组都排在第 k 小之前 → 跳过'),
        'left_s.append(ascii_lowercase[j])': '填入 `{ascii_lowercase[j]}`，`cnt[{j}] -= 1`，`perm` 变成 `p` = {p}（排列数缩小）',
        'k -= p': '跳过了 `p` 个排列，`k -= {p}` → =={k}==（像在搜索树里剪掉一棵子树）',
        'ans = left_s': '左半边 `{left_s}` 完成',
        'return ans': '左半边 + 中间 + 左半边翻转 = =={ret}==',
    },
    cards=dict(
        one_liner='试填法：每一位试填 a、b、c…，用排列数跳过前面的组',
        complexity='时间 `O(n|Σ|)`，空间 `O(n+|Σ|)`',
        problem=['给回文串 `s` 和整数 `k`，返回 `s` 的字典序第 `k` 小的==回文排列==',
                 '不同回文才算不同；不足 `k` 个返回空串',
                 '示例：`s = "aabbcbbaa", k = 2` → `"ababcbaba"`'],
        quote='其实如下公式是可以用的 sz!/∏cnt_j!。我们可以倒着填，从 i=m-1 以及 j=z 开始枚举，用上述公式计算已经填入的字母的排列个数。一旦排列个数 ≥ k，就退出循环。',
        quote_src='—— 灵茶山艾府题解',
        idea=['回文由左半边决定；奇数长度时正中间那个字母固定',
              '倒着放字母，`perm` 一边乘一边除，一旦 ≥ k 就停，不会溢出',
              '前面几位随便放都够 k 个，直接按字典序最小排；后面几位才逐位试填'],
        summary=['时间 `O(n|Σ|)`，空间 `O(n+|Σ|)`',
                 '易错：`perm * (m - i) // cnt[j]` 必须先乘后除，才能整除',
                 '试填时 `p = perm * cnt[j] // (m - i)` 是把上面的公式反过来用',
                 '题解还给了「优化前」写法：每位试填、用组合数循环算排列数，复杂度更高',
                 '同类题：试填法（位运算题单「五、试填法」）、第 k 个排列'],
    ),
)
