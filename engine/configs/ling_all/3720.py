CONFIG = dict(
    num=3720, title='大于目标字符串的最小字典序排列', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='倒着枚举变大位置 · 维护 neg 与 mx',
    tags=['灵神题单', '难度分 1958'],
    code='''
class Solution:
    def lexGreaterPermutation(self, s: str, target: str) -> str:
        left = Counter(s)
        for c in target:
            left[c] -= 1  # 消耗 s 中的一个字母 c

        neg, mx = 0, ''
        for c, cnt in left.items():
            if cnt < 0:
                neg += 1  # 统计 left 中的负数个数
            elif cnt > 0:
                mx = max(mx, c)

        for i in range(len(s) - 1, -1, -1):
            c = target[i]
            left[c] += 1  # 撤销消耗

            if left[c] == 0:
                neg -= 1
            elif left[c] == 1:
                mx = max(mx, c)

            # left 有负数 or 没有大于 target[i] 的字母
            if neg > 0 or c >= mx:
                continue

            # 找到答案（下面的循环在整个算法中只会跑一次）
            j = ord(c) - ord('a') + 1
            while left[ascii_lowercase[j]] == 0:
                j += 1

            # 把 target[i] 增大到 ch
            ch = ascii_lowercase[j]
            left[ch] -= 1
            ans = list(target[:i + 1])
            ans[i] = ch

            for ch in ascii_lowercase:
                ans.extend(ch * left[ch])
            return ''.join(ans)

        return ""
''',
    call='Solution().lexGreaterPermutation("abc", "bba")',
    expect='bca',
    views=[
        dict(type='string', var='target', label='target（蓝 = 当前枚举的位置 i，前缀要和 s 的排列一致）', cell=100, h=190,
             pointers={'i': 'blue'}, window=(lambda S: 0, 'i'),
             color=lambda S, k, v: 'blue' if S.get('i') == k else None),
        dict(type='map', var='left', label='left（s 剩余可用次数 = s 次数 − 前缀 [0,i) 消耗；负数 = 不够）',
             fmt=lambda k, v: f"'{k}': {v}", h=170, font=34),
        dict(type='text', fn=lambda S: (f"`neg = {S['neg']}`（缺字母的种数），`mx = '{S['mx']}'`（剩余字母里最大的）" if 'mx' in S else
                                        's 的排列要严格大于 target：越靠右变大越好'), size=28, h=90),
        dict(type='array', var='ans', label='ans', cell=100, h=140),
    ],
    watch=[('i', 'i', 'blue'), ('neg', 'neg', 'pink'), ('mx', 'mx', 'orange'), ('c', 'c')],
    captions={
        'left = Counter(s)': '`left` 先记下 s 中每个字母的次数：`{dict(left)}`',
        'for c in target': lambda S, B, r: (f"先假设答案整个等于 target：消耗字母 `{S.c}`" if 'c' in S else ''),
        'left[c] -= 1': '消耗一个 `{c}` → `left[{c!r}] = {left[c]}`',
        'neg, mx': '`neg` 数负数，`mx` 记剩余字母里最大的',
        'for c, cnt in left.items()': '扫一遍 `left`：`{c!r}` 还剩 `{cnt}`',
        'if cnt < 0': lambda S, B, r: (f"`{S.c!r}` 剩 {S.cnt} < 0：s 里这个字母不够，target 的完整前缀凑不出" if S.cnt < 0
                                       else f"`{S.c!r}` 剩 {S.cnt}，不是负数"),
        'neg += 1': '负数个数 `neg = {neg}`',
        'elif cnt > 0': '`{c!r}` 还有剩余 → 可以拿来变大',
        'mx = max(mx, c)': '剩余字母里最大的 `mx = {mx!r}`',
        'for i in range': lambda S, B, r: (f"倒着枚举：尝试把 `target[{S.i}]` 变大（越靠右越好）" if 'i' in S else ''),
        'c = target[i]': '`c = target[{i}] = {c!r}`',
        'left[c] += 1': '撤销 `target[{i}]` 的消耗：前缀缩短到 `[0, {i})` → `left[{c!r}] = {left[c]}`',
        'if left[c] == 0': lambda S, B, r: (f"`left[{S.c!r}]` 变成 0：它不再缺了，`neg` 减一" if S.left[S.c] == 0
                                            else f"`left[{S.c!r}] = {S.left[S.c]}`，不为 0"),
        'neg -= 1': '缺字母的种数减少 → `neg = {neg}`',
        'elif left[c] == 1': lambda S, B, r: (f"`left[{S.c!r}] = 1`：这个字母变成有剩余，更新 `mx`" if S.left[S.c] == 1
                                              else f"`left[{S.c!r}] = {S.left[S.c]}`，`mx` 不变"),
        'if neg > 0 or c >= mx': lambda S, B, r: (f"`neg = {S.neg} > 0`：前缀 `[0,{S.i})` 凑不出来，不行" if S.neg > 0
                                                   else (f"`'{S.c}' >= mx = '{S.mx}'`：剩余字母里没有比 `{S.c}` 大的，变不大" if S.c >= S.mx
                                                         else f"`neg = 0` 且 `'{S.c}' < mx = '{S.mx}'`：==能变大，就是这个位置==")),
        'continue': '这个位置不行，继续往左',
        'j = ord(c)': '从 `{c}` 的下一个字母开始找',
        'while left[ascii_lowercase[j]] == 0': lambda S, B, r: (f"`'{ascii_lowercase[S.j]}'` 没有剩余，找下一个" if S.left[ascii_lowercase[S.j]] == 0
                                                                else f"`'{ascii_lowercase[S.j]}'` 有剩余 → 就是比 `{S.c}` 大的最小字母"),
        'j += 1': '`j` → {j}',
        'ch = ascii_lowercase[j]': '把 `target[{i}]` 增大到 `ch = {ch!r}`',
        'left[ch] -= 1': '用掉一个 `{ch}`',
        'ans = list': '答案前缀 = `target[:{i}+1]`：`{"".join(ans)}`',
        'ans[i] = ch': '最后一位换成更大的 `{ch}`：`{"".join(ans)}`',
        'for ch in ascii_lowercase': lambda S, B, r: (f"剩余字母从小到大排在后面：`{S.ch!r}` × {S.left[S.ch]}" if 'ch' in S else ''),
        'ans.extend': '追加 `{ch!r}` × {left[ch]} → `{"".join(ans)}`',
        'return': '剩余字母 `a` 从小到大接在后面，答案 `{ret!r}`',
    },
    skip=['for ch in ascii_lowercase', 'ans.extend'],
    max_steps=70,
    cards=dict(
        one_liner='变大的位置越靠右越好：倒着枚举，找到就收工',
        complexity='时间 `O(n + |Σ|)`，空间 `O(|Σ|)`',
        problem=['把 `s` 重新排列，求==严格大于== `target` 的最小排列，没有则返回 `""`',
                 '示例：`s = "abc"`，`target = "bba"` → `"bca"`',
                 '本视频用的就是这个例子'],
        quote='由于字典序要严格大于 target，且字典序越小越好，那么变大更靠右的字母是更优的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先假设整个排列等于 `target`，从 `left` 里消耗字母，次数不够就记为负',
              '倒着枚举位置 `i`：前缀 `[0, i-1]` 保持和 `target` 一致（`neg == 0`），且剩余字母里有比 `target[i]` 大的（`c < mx`）',
              '找到后把 `target[i]` 换成最小的更大字母，剩余字母从小到大排在右边'],
        result='`i = 1` 时前缀 `b` 够用、剩余有 `c`：`b` + `c` + `a` = `bca` ✓',
        after=[dict(heading='其他写法', lines=[
            '优化前：每个位置都用 `any(cnt < 0)` 判断、再从 `c+1` 到 `z` 循环找，`O(n|Σ|)`',
            '另一种写法：用二进制 `mask` 维护剩余字母集合，位运算找比 `c` 大的最小字母',
            '本视频演示的是维护 `neg` 与 `mx` 的优化写法'])],
        summary=['时间 `O(n + |Σ|)`，空间 `O(|Σ|)`',
                 '要==严格==大于 target，所以最后一个位置必须变大，不能整个等于 target',
                 '撤销消耗后再判断：`left[c]` 从 -1 变 0 时 `neg` 减一，从 0 变 1 时可能更新 `mx`',
                 '相似题：3734（回文排列）、2048、3646'],
    ),
)
