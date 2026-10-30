def _info(S):
    if 'res' in S and 'index' in S:
        n = len(S['arr'])
        i = S['index']
        k = i if i + i - 1 <= n else n - i + 1
        return f"长度 `{i}` 的子数组总和 = `s[{k - 1}]`（{'展开充分，直接取' if i + i - 1 <= n else '重叠次数只有 n−长度+1，对称取'}）"
    if 'l' in S and 'r' in S and 'prefix' in S:
        return f"`s[k] = s[k−1] + prefix[{S['r'] - 1}] − prefix[{S['l']}]`：每多一层，中间一段再多算一遍"
    return 'prefix = 前缀和；s[k−1] = 所有长度为 k 的子数组之和'


CONFIG = dict(
    num=1588, title='所有奇数长度子数组的和', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='前缀和 · 逐层叠加',
    tags=[],
    code='''
class Solution(object):
    def sumOddLengthSubarrays(self, arr):

        prefix = [arr[0]]
        for num in arr[1:]:
            prefix.append(prefix[-1] + num)
        
        s = [prefix[-1]]
        n = len(arr)
        l = 0
        r = n - 1
        while l < r:
            s.append(s[-1] + prefix[r - 1] - prefix[l])
            l += 1
            r -= 1
        
        res = 0
        for index in range(1, n + 1, 2):
            if index + index - 1 <= n:
                res += s[index - 1]
            else:
                res += s[n - index]
        
        return res
''',
    call='Solution().sumOddLengthSubarrays([1,4,2,5,3])',
    expect=58,
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='array', var='arr', label='arr', pointers={'l': 'blue', 'r': 'pink'}, window=('l', 'r'), cell=84, h=150),
        dict(type='array', var='prefix', label='prefix（前缀和）', cell=84, h=130),
        dict(type='array', var='s', label='s[k−1] = 所有长度为 k 的子数组之和', cell=84, h=130,
             color=lambda S, i, v: 'green' if 'index' in S and 'res' in S and i == (S['index'] - 1 if 2 * S['index'] - 1 <= len(S['arr']) else len(S['arr']) - S['index']) else None),
    ],
    watch=['n', ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('index', 'index', 'yellow'), ('res', 'res', 'green')],
    captions={
        'prefix = [arr[0]]': '`prefix[i]` 是 `arr[0..i]` 的和，用来 O(1) 求区间和',
        'prefix.append': '`prefix` 追加 `{prefix[-1]}`（前一项 + `{num}`）',
        's = [prefix[-1]]': '长度 1 的子数组之和 `s[0]` = 整个数组之和 `{s[0]}`，每个数各出现 1 次',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}`：还有更长的长度要算' if S.l < S.r else f'`l = {S.l} ≥ r = {S.r}`：展开到头了，结束'),
        's.append': '长度再加 1：两端各少一次，中间那段 `prefix[{r-1}] − prefix[{l}]`（`arr[{l+1}..{r-1}]`）多出现一次 → `s` 追加 `{s[-1]}`',
        'l += 1': '`l` 右移到 {l}：下一层的中间段更短',
        'r -= 1': '`r` 左移到 {r}',
        'res = 0': '`res` 累计所有奇数长度的和',
        'for index in range': '枚举奇数长度 `index = {index}`',
        'if index + index - 1 <= n': lambda S, B, r: (f'`{S.index}+{S.index}−1 = {2 * S.index - 1} ≤ n = {S.n}`：长度 {S.index} 的子数组足够多，中间部分被完整叠满 → 展开充分，直接用 `s[{S.index - 1}]`' if 2 * S.index - 1 <= S.n else f'`{2 * S.index - 1} > n = {S.n}`：展开不充分，只有 `n−{S.index}+1 = {S.n - S.index + 1}` 个子数组 → 对称地取 `s[{S.n - S.index}]`'),
        'res += s[index - 1]': '`res += s[{index - 1}] = {s[index - 1]}` → `{res}`',
        'res += s[n - index]': '长度 `{index}` 的和等于长度 `{n - index + 1}` 的和 `s[{n - index}] = {s[n - index]}`，`res` → `{res}`',
        'return res': '所有奇数长度子数组之和 = `{res}`',
    },
    cards=dict(
        one_liner='每个长度的总和，只比上一个长度多一段前缀和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给你正整数数组 `arr`，求==所有奇数长度子数组==的和',
                 '长度 1、3、5…… 的每一个连续子数组都要算',
                 '示例：`[1,4,2,5,3]` → `58`'],
        quote='可以发现，此时除arr[0]以及arr[n - 1]之外，其他位置上的数都出现了两次。',
        quote_src='—— yiduobo 题解原文（分析长度为 2 的子数组和）',
        idea=['设长度为 k 的子数组和为 `s[k]`：长度 1 时每个数出现一次',
              '长度 2：除两端外每个数出现两次；长度 3：再往里一层出现三次……',
              '所以 `s[k] = s[k−1] + prefix[n−k] − prefix[k−2]`（中间一段多算一遍）',
              '`k×2−1 ≤ n` 时展开充分；否则 `s[k]` 等于 `s[n−k+1]`'],
        result='运行结束，返回 `58`：`15 + 28 + 15`（长度 1、3、5）',
        summary=['时间 `O(n)`，空间 `O(n)`；暴力法是 `O(n²)`，本题规模小也能过',
                 '`s` 下标从 0 开始，所以长度 `index` 对应 `s[index − 1]`，要注意偏移',
                 '展开不充分时重叠次数最多 `n−k+1`，恰好是 `s[n−k+1]` 的含义',
                 '原文为 Python 2 风格，仅沿用原代码，没有需要改动的地方'],
    ),
)
