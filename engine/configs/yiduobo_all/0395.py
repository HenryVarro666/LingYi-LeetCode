S0, K0 = 'aaab', 3
KEYS = sorted(set(S0))


def _right(S):
    return S['r'] - 1 if 'r' in S and 'char_cnt' in S else None


def _left(S):
    return S['l'] if 'l' in S and 'char_cnt' in S else None


def _table(S):
    d = S.get('sum_dict') or {}
    return [d[c] for c in KEYS if c in d] if d else [[0]]


def _rows(S):
    d = S.get('sum_dict') or {}
    return [f"'{c}'" for c in KEYS if c in d] or ['']


def _top(S):
    if 'char_cnt' not in S:
        return '预处理：`sum_dict[c][i]` = `s[0..i]` 中字符 c 的个数（前缀和）'
    l, r, cc = S['l'], S['r'], S['char_cnt']
    t = S0[l:r]
    return (f"恰好 =={cc}== 种字符：窗口 `[{l}, {r})` = `{t!r}`，"
            f"char_set = `{{{', '.join(sorted(S['char_set']))}}}`，res = `{S['res']}`")


def _expand(S, B, ret):
    r, cs, cc = S.r, S.char_set, S.char_cnt
    if r < len(S.s) and (len(cs) < cc or S.s[r] in cs):
        why = f'种类不足 {cc}' if len(cs) < cc else f"`{S.s[r]!r}` 已在集合里"
        return f'{why} → `s[{r}]` 可以加入，r 右移'
    if r >= len(S.s):
        return '`r` 到末尾了，停止扩展'
    return f"再加 `{S.s[r]!r}` 就超过 {cc} 种了 → 停止扩展"


def _check(S, B, ret):
    cs, cc, w = S.char_set, S.char_cnt, S.r - S.l
    if len(cs) == cc and S.res < w:
        return f'窗口恰好 {cc} 种字符，长度 `{w}` > `res = {S.res}` → ==检查每种字符是否 ≥ k=='
    if len(cs) == cc:
        return f'窗口长度 `{w}` 不比 `res = {S.res}` 大，不用检查'
    return '字符种数不对，跳过'


def _shrink(S, B, ret):
    if S.l < S.r and len(S.char_set) >= S.char_cnt:
        return f'窗口仍有 {len(S.char_set)} 种字符 → 左移 l，直到少一种'
    return f'窗口只剩 {len(S.char_set)} 种字符，停止收缩'


CONFIG = dict(
    num=395, title='至少有K个重复字符的最长子串', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举字符种数 + 滑动窗口 + 前缀和',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def longestSubstring(self, s, k):

        if not s:
            return 0

        sum_dict = {}
        for char in s:
            sum_dict[char] = [0]
        sum_dict[s[0]] = [1]

        for char in s[1:]:
            for key in sum_dict:
                sum_dict[key].append(sum_dict[key][-1])
            sum_dict[char][-1] += 1

        res = 0
        for char_cnt in range(len(sum_dict), 0, -1):
            char_set = set()
            l = 0
            r = 0
            while l < r or r < len(s):
                while r < len(s) and (len(char_set) < char_cnt or s[r] in char_set):
                    char_set.add(s[r])
                    r += 1

                if len(char_set) < char_cnt:
                    break

                if len(char_set) == char_cnt and res < r - l:
                    flag = True
                    for char in char_set:
                        if l == 0:
                            cnt = sum_dict[char][r - 1]
                        else:
                            cnt = sum_dict[char][r - 1] - sum_dict[char][l - 1]
                        if cnt < k:
                            flag = False
                            break
                    if flag:
                        res = r - l

                while l < r and len(char_set) >= char_cnt:
                    if sum_dict[s[l]][l] == sum_dict[s[l]][r - 1]:
                        char_set.remove(s[l])
                    l += 1

        return res
''',
    call=f'Solution().longestSubstring({S0!r}, {K0})',
    expect=3,
    views=[
        dict(type='text', fn=_top, size=24, h=80),
        dict(type='string', var='s', label='s（框 = 窗口 [l, r−1]）',
             pointers={'l': 'cyan', 'r': 'orange'}, window=(_left, _right), cell=110, h=260),
        dict(type='table', var=_table, rows=_rows, label='sum_dict（前缀和：s[0..i] 中该字符的个数）', h=240),
    ],
    watch=[('char_cnt', 'char_cnt', 'purple'), ('l', 'l', 'cyan'), ('r', 'r', 'orange'), 'cnt', 'flag', ('res', 'res', 'green')],
    skip=['for key in sum_dict', 'sum_dict[key].append', 'for char in s:', 'sum_dict[char] = [0]', 'flag = True', 'char_set.add(s[r])', 'r = 0', 'flag = False', 'if l == 0', 'for char in s[1:]', 'char_set = set()', 'while l < r or r < len(s)'],
    captions={
        'if not s': '`s` 非空',
        'sum_dict = {}': '`sum_dict[c][i]`：前 i+1 个字符中 c 出现的次数',
        'for char in s:': '先给每种字符建一个列表',
        'sum_dict[s[0]] = [1]': "第 0 个字符 `{s[0]!r}` 的计数为 1",
        'for char in s[1:]': lambda S, B, r: '前缀和预处理完毕' if S.get('res') is not None else f"处理下一个字符 `{S.char!r}`：每个列表先复制上一格",
        'sum_dict[char][-1] += 1': "复制上一格，`{char!r}` 自己那一行再加 1",
        'res = 0': '`res` 记录最长合法子串长度',
        'for char_cnt in range': lambda S, B, r: (f'枚举答案里==恰好有 {S.char_cnt} 种==字符' if 'char_cnt' not in B or B.char_cnt != S.char_cnt else '枚举结束'),
        'char_set = set()': '`char_set`：窗口 `[l, r)` 中出现的字符',
        'l = 0': '清空 `char_set`，`l = r = 0`，窗口 `[l, r)` 为空',
        'while l < r or r < len(s)': lambda S, B, r: '窗口还能继续滑动',
        'while r < len(s) and (': _expand,
        'char_set.add(s[r])': "`{s[r]!r}` 加入 `char_set`",
        'r += 1': "`{s[r - 1]!r}` 加入 `char_set`，`r` → {r}",
        'if len(char_set) < char_cnt': lambda S, B, r: (f'窗口里不足 {S.char_cnt} 种字符，后面也凑不齐 → break' if len(S.char_set) < S.char_cnt
                                                       else f'窗口恰好 {len(S.char_set)} 种字符'),
        'if len(char_set) == char_cnt and res': _check,
        'for char in char_set': lambda S, B, r: ('每种字符都检查完了' if 'cnt' in B and B.char == S.char else f"检查字符 `{S.char!r}`"),
        'cnt = sum_dict[char][r - 1]': "`l = 0`：`{char!r}` 次数 = `sum_dict[{char!r}][{r - 1}]` = `{cnt}`",
        'cnt = sum_dict[char][r - 1] - sum_dict': "前缀和相减：`{char!r}` 在窗口中出现 `{cnt}` 次",
        'if cnt < k': lambda S, B, r: (f'`{S.cnt} < {S.k}`：这种字符太少 → ==窗口不合法==' if S.cnt < S.k else f'`{S.cnt} ≥ {S.k}`，这种字符够了'),
        'flag = False': '标记不合法',
        'if flag': lambda S, B, r: ('每种字符都至少 k 次 → ==合法==' if S.flag else '不合法，不更新'),
        'res = r - l': '`res` → =={res}==',
        'while l < r and len(char_set) >= char_cnt': _shrink,
        'if sum_dict[s[l]][l] == sum_dict[s[l]][r - 1]': lambda S, B, r: (
            f"`sum_dict[{S.s[S.l]!r}][{S.l}] == sum_dict[{S.s[S.l]!r}][{S.r - 1}]`：l 之后窗口里==再没有== {S.s[S.l]!r}"
            if S.sum_dict[S.s[S.l]][S.l] == S.sum_dict[S.s[S.l]][S.r - 1]
            else f"窗口后面还有 {S.s[S.l]!r}，它仍留在集合里"),
        'char_set.remove(s[l])': "从 `char_set` 删掉 `{s[l]!r}`",
        'l += 1': '`l` → {l}',
        'return res': '最长合法子串长度为 =={ret}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='限定窗口里恰好 c 种字符，滑窗才有单调性；c 从 26 种往下枚举',
        complexity='时间 `O(26^2 · n)`，空间 `O(26 · n)`',
        problem=['给字符串 `s`（只含小写字母）和整数 `k`',
                 '求最长子串，使其中==每个字符的出现次数都不少于 k==，返回长度',
                 '示例：`s = "ababbc", k = 2` → `5`（`"ababb"`）；本视频 `"aaab", k = 3` → `3`'],
        quote='注意到题目保证了s中只有小写字符，因此我在这里采用的是==枚举答案中不同字符的个数==，然后使用滑动窗口的方式来找是否存在符合条件的子串。',
        quote_src='—— yiduobo 题解原文',
        idea=['固定种数 `char_cnt`：r 尽量右扩，直到再加就超过 char_cnt 种',
              '用前缀和 `sum_dict` 在 `O(char_cnt)` 内算出窗口里每种字符的次数',
              '判完后 l 右移，直到窗口少一种字符，再继续扩 r'],
        summary=['时间 `O(26^2 · n)`：最多枚举 26 次，每次扫描 `O(26n)`',
                 '种数不满足二分性质，只能逐个枚举',
                 '另一思路是分治：次数 < k 的字符不可能在答案中，用它切分 s',
                 '窗口是左闭右开 `[l, r)`，前缀和下标要用 `r − 1` 和 `l − 1`',
                 '原文为 Python 2 风格，代码无需改动；`set` 遍历顺序不固定，不影响结果'],
    ),
)
