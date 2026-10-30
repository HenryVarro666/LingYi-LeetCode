SRC = 'abbaa'
PAT = 'aba'
TGT = [0, 1, 2]
E = "j if _line in (11, 12, 13) else None"


def _inl(S):
    return S.get('_line') in (11, 12, 13) and S.get('j') is not None


def _info(S):
    if S.get('i') is None:
        return '`f[j]` = 让 `pattern[:j]` 仍是已看过部分的子序列时，最多的删除次数；`-inf` 表示不可能'
    i, x = S['i'], S['x']
    dele = '这一位在 targetIndices 里，可删（+1）' if S.get('is_del') else '这一位不在 targetIndices 里，删不了'
    if _inl(S):
        j = S['j']
        eq = '相等：可以==让它充当 pattern[j]==，取 max' if x == S['pattern'][j] else '不相等：它不能匹配 pattern[j]'
        return f"`source[{i}] = {x}`，`pattern[{j}] = {S['pattern'][j]}` → {eq}"
    return f"`source[{i}] = {x}`：{dele}" if S.get('_line', 0) >= 9 else f"`source[{i}] = {x}`"


CONFIG = dict(
    num=3316, title='从原字符串里进行删除操作的最多次数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='双序列 DP（LCS 型）· 滚动数组 + 双指针',
    tags=['灵神题单', 'LCS 进阶', '难度分 2062'],
    code='''
class Solution:
    def maxRemovals(self, source: str, pattern: str, targetIndices: List[int]) -> int:
        m = len(pattern)
        f = [0] + [-inf] * m
        k = 0
        for i, x in enumerate(source):
            if k < len(targetIndices) and targetIndices[k] < i:
                k += 1
            is_del = 1 if k < len(targetIndices) and targetIndices[k] == i else 0
            for j in range(min(i, m - 1), -1, -1):
                f[j + 1] += is_del
                if x == pattern[j]:
                    f[j + 1] = max(f[j + 1], f[j])
            f[0] += is_del
        return f[m]
''',
    call=f'Solution().maxRemovals({SRC!r}, {PAT!r}, {TGT!r})',
    expect=1,
    skip=['targetIndices[k] < i', 'for j in range', 'm = len', 'k = 0', 'k += 1', 'if x == pattern'],
    max_steps=80,
    views=[
        dict(type='string', var='source', label='source（蓝 = 当前字母 x；橙 = 在 targetIndices 里）', h=150, cell=70, pointers={'i': 'blue'},
             color=lambda S, k, v: 'blue' if k == S.get('i') else ('orange' if k in S['targetIndices'] else None)),
        dict(type='string', var='pattern', label='pattern（粉 = 正在尝试匹配的位置 j）', h=160, cell=70, pointers={E: 'pink'}, pointer_labels={E: 'j'},
             color=lambda S, k, v: 'pink' if k == S.get('j') and S.get('_line') in (11, 12, 13) else None),
        dict(type='text', fn=_info, size=24, h=80),
        dict(type='array', var='f', label='f[j]：pattern[:j] 要保持是子序列时，最多删几个', h=210, cell=100,
             pointers={E: 'pink'}, pointer_labels={E: 'j'}, index=True,
             color=lambda S, k, v: 'yellow' if S.get('j') is not None and S.get('_line') in (11, 12, 13) and k == S['j'] + 1 else None),
    ],
    watch=[('i', 'i', 'blue'), ('is_del', 'is_del', 'orange'), ('j', 'j', 'pink'), ('f[m]', 'f[-1]', 'green')],
    captions={
        'f = [0] + [-inf]': '`f[0] = 0`：还没看任何字母、pattern 取空串，删除 0 次；其余 `-inf`（还凑不出）',
        'for i, x in enumerate': lambda S, B, r: (f'看 `source[{S.i}] = {S.x}`：不选它（可能顺手删掉），或让它匹配 `pattern` 的某位'
                                                 if S.get('x') is not None and (B.get('i') is None or S.i == B.i + 1) else '`source` 全看完了'),
        'is_del = ': '`targetIndices` 有序，指针 `k` 指向第一个 `>= i` 的目标：`i = {i}` {"在" if is_del else "不在"}里 → `is_del = {is_del}`',
        'f[j + 1] += is_del': lambda S, B, r: (f'不选 `source[i]` 来匹配：它能删就 +1：`f[{S.j+1}] += {S.is_del}`' + (' → 仍是 `-inf`（还凑不出）' if S.f[S.j + 1] == -inf else f' → {S.f[S.j + 1]}')),
        'f[j + 1] = max': lambda S, B, r: (f'`x = {S.x}` == `pattern[{S.j}]`，也可以「选它」匹配：`max({B.f[S.j + 1]}, f[{S.j}] = {S.f[S.j]})` = =={S.f[S.j + 1]}=='),
        'f[0] += is_del': '`j = -1`：pattern 一个都不匹配，`source[i]` 只能删（能删就 +1）：`f[0] = {f[0]}`',
        'return f[m]': '`f[{m}]` = 整个 pattern 都保持是子序列时，最多的删除次数 = =={ret}==',
    },
    cards=dict(
        one_liner='选或不选 source[i]：不选就能删，选就匹配 pattern',
        complexity='时间 `O(nm)`，空间 `O(m)`',
        problem=['`pattern` 是 `source` 的子序列；`targetIndices` 是有序的可删下标',
                 '每次删除一个下标在 `targetIndices` 里的字符，删后 `pattern` 仍是子序列',
                 '求最多能删几次；示例：`source="abbaa", pattern="aba", targetIndices=[0,1,2]` → `1`'],
        quote='本题属于子序列相邻无关问题，用「选或不选」解决。……用 -∞ 表示不合法的状态，从而保证 max 不会取到不合法的状态。',
        quote_src='—— 灵茶山艾府题解',
        idea=['思路同 1143 LCS，从右往左「选或不选」：不选 `source[i]`，它若在 `targetIndices` 里就删除 +1',
              '`source[i] == pattern[j]` 时可以「都选」，转移来自 `f[j]`；两种取 `max`',
              '记忆化搜索 → 二维递推 → 去掉第一维，`j` 倒序，与 0-1 背包相同',
              '`targetIndices` 有序，用双指针 `k` 判断，免掉哈希集合'],
        summary=['时间 `O(nm)`，空间 `O(m)`',
                 '易错：不合法状态用 `-inf`，不能用 0；`j` 必须倒序',
                 '易错：删除不改变下标，`is_del` 看的是原下标 `i`',
                 '题解前面还有记忆化搜索和二维递推写法，这里用最终的滚动数组'],
    ),
)
