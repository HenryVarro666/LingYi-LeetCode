CONFIG = dict(
    num=522, title='最长特殊序列 II', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='字符串排序 + 判断子序列',
    tags=['灵神题单', '滑动窗口与双指针', '难度分 1700'],
    code='''
class Solution:
    def findLUSlength(self, strs: List[str]) -> int:
        # 判断 s 是否为 t 的子序列
        def is_subseq(s: str, t: str) -> bool:
            i = 0
            for c in t:
                if s[i] == c:
                    i += 1
                    if i == len(s):  # 所有字符匹配完毕
                        return True  # s 是 t 的子序列
            return False

        strs.sort(key=lambda s: -len(s))
        for i, s in enumerate(strs):
            if all(j == i or not is_subseq(s, t) for j, t in enumerate(strs)):
                return len(s)
        return -1
''',
    call="Solution().findLUSlength(['abc', 'abc', 'aad', 'ab'])",
    expect=3,
    views=[
        dict(type='array', var='strs', label='strs（按长度从大到小）', h=200, cell=130),
        dict(type='string', var='s', label='s（待判断是否独有）', pointers={'i': 'blue'}, h=200),
        dict(type='string', var='t', label='t（其他字符串）', h=200),
    ],
    watch=[('i', 'i', 'blue'), ('c', 'c', 'pink')],
    captions={
        'strs.sort(': '按长度从大到小排：越长越不容易是别人的子序列，==第一个满足的就是最长答案==',
        'for i, s in enumerate': '枚举候选 `s = strs[{i}] = {s!r}`：它是否==不是其他任何字符串的子序列==？',
        'if all(': lambda S, B, r: f'判断 `{S.s!r}` 是否是其他字符串的子序列：只要有一个 t 包含它，就不是独有的',
        'i = 0': '`i` 指向 `s` 里下一个要匹配的字符，从 0 开始',
        'for c in t': '扫描 `t` 的字符 `c = {c!r}`',
        'if s[i] == c': lambda S, B, r: (f"`s[{S.i}] = {S.s[S.i]!r}` == `c = {S.c!r}` → ==匹配上=="
                                         if S.s[S.i] == S.c else f"`s[{S.i}] = {S.s[S.i]!r}` ≠ `c = {S.c!r}` → 跳过 `c`（相当于删掉）"),
        'i += 1': '匹配成功，`i` → {i}',
        'if i == len(s)': lambda S, B, r: (f'`i = {S.i} == len(s)`：`s` 全部匹配完毕' if S.i == len(S.s) else f'`i = {S.i} < len(s) = {len(S.s)}`，还没匹配完，继续扫 `t`'),
        'return True': '==`s` 是 `t` 的子序列== → 它不独有，这个候选作废',
        'return False': '扫完 `t` 也没匹配完 → `s` ==不是== `t` 的子序列',
        'return len(s)': '`{s!r}` 不是任何其他字符串的子序列 → 它自己就是独有子序列，返回 ==`{len(s)}`==',
        'return -1': '每个字符串都是别人的子序列 → 不存在特殊序列，返回 -1',
    },
    cards=dict(
        one_liner='只需检查每个字符串本身，是不是别人的子序列',
        complexity='时间 `O(n²m)`，空间 `O(1)`',
        problem=['在字符串列表中找最长的==独有子序列==：它不能是其他字符串的子序列',
                 '不存在则返回 `-1`',
                 '示例：`["aba","cdc","eae"]` → `3`；视频用 `["abc","abc","aad","ab"]` → `3`'],
        quote='如果短的子序列是「独有子序列」，那么更长的子序列也会是「独有子序列」。……所以只需要枚举字符串 s=strs[i]，判断 s 是否为其它字符串的子序列。',
        quote_src='—— 灵茶山艾府题解',
        idea=['子序列越长越不可能是别人的子序列 → 最优答案一定是某个原字符串本身',
              '`is_subseq(s, t)`：同向双指针，扫 `t`，匹配上就让 `i` 加一（同 392 题）',
              '写法二先按长度从大到小排序，第一个独有的就直接返回'],
        summary=['时间 `O(n²m)`：`n²` 对字符串，每对 `O(m)` 判断',
                 '`all(j == i or ...)`：别拿自己和自己比',
                 '相同的字符串互为子序列，所以重复串不可能独有（如示例 2 → -1）',
                 '写法一不排序，用 `len(s) > ans` 剪枝并取最大值'],
    ),
)
