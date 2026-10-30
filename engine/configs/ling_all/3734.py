CONFIG = dict(
    num=3734, title='大于目标字符串的最小字典序回文排列', difficulty='Hard', category='贪心与思维',
    author='灵茶山艾府', technique='只排左半 · 倒着枚举变大位置',
    tags=['灵神题单', '难度分 2330'],
    code='''
class Solution:
    def lexPalindromicPermutation(self, s: str, target: str) -> str:
        left = Counter(s)

        def valid() -> bool:
            return all(c >= 0 for c in left.values())

        mid_ch = ''
        for ch, c in left.items():
            if c % 2 == 0:
                continue
            # s 不能有超过一个字母出现奇数次
            if mid_ch:
                return ""
            # 记录填在正中间的字母
            mid_ch = ch
            left[ch] -= 1

        n = len(s)
        # 先假设答案左半与 t 的左半（不含正中间）相同
        for i, b in enumerate(target[:n // 2]):
            left[b] -= 2

        neg, left_max = 0, ''
        for c, cnt in left.items():
            if cnt < 0:
                neg += 1  # 统计 left 中的负数个数
            elif cnt > 0:
                left_max = max(left_max, c)  # 剩余可用字母的最大值

        if neg == 0:
            # 特殊情况：把 target 左半翻转到右半，能否比 target 大？
            left_s = target[:n // 2]
            right_s = mid_ch + left_s[::-1]
            if right_s > target[n // 2:]:  # 由于左半是一样的，所以只需比右半
                return left_s + right_s

        for i in range(n // 2 - 1, -1, -1):
            b = target[i]
            left[b] += 2  # 撤销消耗

            if left[b] == 0:
                neg -= 1
            elif left[b] == 2:
                left_max = max(left_max, b)

            # left 有负数 or 没有大于 target[i] 的字母
            if neg > 0 or left_max <= b:
                continue

            # 找到答案（下面的循环在整个算法中只会跑一次）
            j = ord(b) - ord('a') + 1
            while left[ascii_lowercase[j]] == 0:
                j += 1

            # 把 target[i] 增大到 ch
            ch = ascii_lowercase[j]
            left[ch] -= 2
            ans = list(target[:i + 1])
            ans[i] = ch

            # 中间可以随便填
            for ch in ascii_lowercase:
                ans.extend(ch * (left[ch] // 2))

            # 镜像翻转
            right_s = ans[::-1]
            ans.append(mid_ch)
            ans += right_s

            return ''.join(ans)

        return ""
''',
    call='Solution().lexPalindromicPermutation("baba", "abba")',
    expect='baab',
    skip=['for ch in ascii_lowercase', 'ans.extend', 'def valid', 'return all('],
    views=[
        dict(type='string', var='target', label='target（左半是要排的部分；蓝 = 当前位置 i）', cell=100, h=190,
             pointers={'i': 'blue'}, color=lambda S, k, v: 'blue' if S.get('i') == k else None,
             dim=lambda S, k, v: k >= len(S['target']) // 2),
        dict(type='map', var='left', label='left（左半还能用的“对数”×2；负数 = 不够）', fmt=lambda k, v: f"'{k}': {v}", h=170, font=34),
        dict(type='text', fn=lambda S: (f"`neg = {S['neg']}`，`left_max = '{S['left_max']}'`" if 'left_max' in S else
                                        '回文只需决定左半；右半是左半的镜像'), size=28, h=90),
        dict(type='array', var='ans', label='ans', cell=90, h=140),
    ],
    watch=[('i', 'i', 'blue'), ('neg', 'neg', 'pink'), ('left_max', 'left_max', 'orange'), ('mid_ch', 'mid_ch', 'green')],
    captions={
        'left = Counter(s)': '`left` 统计 s 每个字母的次数：`{dict(left)}`',
        'for ch, c in left.items()': '检查 `{ch!r}` 出现 `{c}` 次',
        'if c % 2 == 0': lambda S, B, r: (f"`{S.ch!r}` 出现偶数次，可以左右对称摆放" if S.c % 2 == 0 else f"`{S.ch!r}` 出现奇数次 {S.c}：只能放正中间"),
        'if mid_ch': lambda S, B, r: ('已经有一个奇数次的字母 → 超过一个，无法组成回文，返回空' if S.mid_ch else '这是第一个奇数次字母，放正中间'),
        'mid_ch = ch': '正中间的字母 `mid_ch = {mid_ch!r}`',
        'left[ch] -= 1': '正中间用掉一个 `{ch!r}`',
        'n = len(s)': '`n = {n}`，左半长度 `n // 2 = {n // 2}`',
        'for i, b in enumerate': lambda S, B, r: (f"先假设左半等于 `target[:{S.n // 2}]`：消耗 `{S.b!r}`" if 'b' in S else ''),
        'left[b] -= 2': '左右各一个，消耗两个 `{b!r}` → `left[{b!r}] = {left[b]}`',
        'neg, left_max': '`neg` 数负数，`left_max` 记剩余可用的最大字母',
        'for c, cnt in left.items():': '看 `{c!r}`：剩 `{cnt}`',
        'if cnt < 0': lambda S, B, r: (f"`{S.c!r}` 剩 {S.cnt} < 0：不够" if S.cnt < 0 else f"`{S.c!r}` 剩 {S.cnt}，不为负"),
        'neg += 1': '`neg = {neg}`',
        'elif cnt > 0': '`{c!r}` 还有剩余',
        'left_max = max(left_max, c)': '`left_max = {left_max!r}`',
        'if neg == 0': lambda S, B, r: ('`neg == 0`：左半能原样照抄 target，先试试看' if S.neg == 0 else '`neg > 0`：照抄不行，必须变小前缀'),
        'left_s = target': '`left_s = {left_s!r}`：照抄 target 的左半',
        'right_s = mid_ch': '右半 = 中间字母 + 左半翻转 = `{right_s!r}`',
        'if right_s > target': lambda S, B, r: (f"右半 `{S.right_s}` > `{S.target[S.n // 2:]}`：照抄就够大了，直接返回" if S.right_s > S.target[S.n // 2:]
                                                else f"右半 `{S.right_s}` <= `{S.target[S.n // 2:]}`：镜像后不够大，左半必须变大"),
        'for i in range(n // 2 - 1': lambda S, B, r: (f"倒着枚举左半的位置：尝试把 `target[{S.i}]` 变大" if 'i' in S and S.get('i', 99) < S.n // 2 else ''),
        'b = target[i]': '`b = target[{i}] = {b!r}`',
        'left[b] += 2': '撤销 `target[{i}]` 的消耗（一对）→ `left[{b!r}] = {left[b]}`',
        'if left[b] == 0': lambda S, B, r: (f"`left[{S.b!r}]` 变 0：不再缺了，`neg` 减一" if S.left[S.b] == 0 else f"`left[{S.b!r}] = {S.left[S.b]}`，不为 0"),
        'neg -= 1': '`neg = {neg}`',
        'elif left[b] == 2': lambda S, B, r: (f"`left[{S.b!r}] = 2`：这个字母有可用的一对，更新 `left_max`" if S.left[S.b] == 2 else f"`left[{S.b!r}] = {S.left[S.b]}`，不更新"),
        'left_max = max(left_max, b)': '`left_max = {left_max!r}`',
        'if neg > 0 or left_max <= b': lambda S, B, r: (f"`neg = {S.neg} > 0`：前缀凑不出，换更靠左" if S.neg > 0
                                                         else (f"剩余最大字母 `{S.left_max!r}` <= `{S.b}`：变不大，换更靠左" if S.left_max <= S.b
                                                               else f"`neg = 0` 且 `left_max = {S.left_max!r}` > `{S.b}`：==能变大，就是这个位置==")),
        'continue': lambda S, B, r: ('这个位置不行，继续往左' if S['_line'] > 40 else '看下一个字母'),
        'mid_ch = \'\'': '`mid_ch`：放在正中间的字母（长度为偶数时为空）',
        'j = ord(b)': '从 `{b}` 的下一个字母开始找',
        'while left[ascii_lowercase[j]] == 0': lambda S, B, r: (f"`{ascii_lowercase[S.j]!r}` 没有可用的一对，找下一个" if S.left[ascii_lowercase[S.j]] == 0
                                                                else f"`{ascii_lowercase[S.j]!r}` 可用 → 比 `{S.b}` 大的最小字母"),
        'j += 1': '`j` → {j}',
        'ch = ascii_lowercase[j]': '把 `target[{i}]` 增大到 `{ch!r}`',
        'left[ch] -= 2': '用掉一对 `{ch!r}`',
        'ans = list': '答案左半前缀：`{"".join(ans)}`',
        'ans[i] = ch': '位置 `{i}` 换成 `{ch!r}`：`{"".join(ans)}`',
        'right_s = ans[::-1]': '左半 `{"".join(ans)}` 填好了（剩余字母已按从小到大补上），镜像得 `{"".join(right_s)}`',
        'ans.append(mid_ch)': '中间放 `{mid_ch!r}`',
        'ans += right_s': '接上镜像：`{"".join(ans)}`',
        'return \'\'.join(ans)': '返回 `{ret!r}`',
        'return ""': '无解，返回空串',
    },
    max_steps=80,
    cards=dict(
        one_liner='回文只排左半，左半就是 3720 题的做法',
        complexity='时间 `O(n + |Σ|)`，空间 `O(n + |Σ|)`',
        problem=['把 `s` 重排成==回文串==，要求严格大于 `target` 且字典序最小，没有返回 `""`',
                 '示例：`s = "baba"`，`target = "abba"` → `"baab"`',
                 '回文排列只有 `abba` 和 `baab`'],
        quote='回文串的特点是，一旦确定了左半的字母，就确定了右半的字母，所以只需考虑左半字母如何排列。也就是对于左半，计算 3720 题。',
        quote_src='—— 灵茶山艾府题解',
        idea=['奇数次的字母最多一个，放正中间；其余字母两个一对，左右各一个',
              '特判：把 `target` 左半镜像后已经更大，左半==不用变==（3720 必须变大）',
              '否则同 3720：倒着枚举左半位置，`neg == 0` 且有更大的字母就变大，剩余从小到大，最后镜像'],
        result='`i = 0`：`a` 换成 `b`，剩一对 `a` 排后面，左半 `ba`，镜像成 `baab` ✓',
        after=[dict(heading='其他写法', lines=[
            '优化前：每个位置用 `valid()` 遍历判断、再从 `b+1` 到 `z` 循环找，`O(n|Σ|)`',
            '本视频演示的是维护 `neg` 与 `left_max` 的优化写法'])],
        summary=['时间 `O(n + |Σ|)`，空间 `O(n + |Σ|)`',
                 '一对字母每次消耗/撤销 2，所以判断条件是 `left[b] == 2`',
                 '易错：忘记 3720 里不需要的特判——镜像后刚好大于 target 时，左半不变',
                 '相似题：3720（普通排列版）'],
    ),
)
