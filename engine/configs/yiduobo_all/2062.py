W = 'cuaieuouac'
V = 'aeiou'


def _lo(S):
    # 最小右边界（闭区间）= min_r − 1
    if 'min_r' not in S or 'flag' not in S:
        return None
    return S['min_r'] - 1


def _hi(S):
    if 'max_r' not in S or 'flag' not in S:
        return None
    return S['max_r'] - 1


def _color(S, i, v):
    if 'res' in S and S.get('_line') == 42 and S['min_r'] - 1 <= i <= S['max_r'] - 1:
        return 'green'
    return None


def _top(S):
    if 'flag' not in S:
        return '对每个左边界 l：找最小右边界 min_r 和最大右边界 max_r'
    l, a, b = S['l'], S['min_r'], S['max_r']
    if S.get('_line') == 42:
        return f"左边界 {l}：右端点取 `{a - 1}..{b - 1}` 都合法 → =={b - a + 1}== 个"
    if l >= S['n']:
        return '左边界走到末尾'
    return f"`l = {l}`，窗口 `word[l : min_r]` = `{S['word'][l:a]}`，五种齐了？{'是' if S['flag'] else '否'}"


CONFIG = dict(
    num=2062, title='统计字符串中的元音子字符串', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举左边界 · 维护最小/最大右边界',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def countVowelSubstrings(self, word):

        l = 0
        min_r = 0
        max_r = 0
        n = len(word)
        cnt_dict = {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0}
        res = 0
        flag = False
        while l < n:
            while l < n and word[l] not in cnt_dict:
                l += 1
                flag = False

            if l == n:
                break

            if min_r < l:
                min_r = l
            
            while min_r < n and word[min_r] in cnt_dict and not flag:
                cnt_dict[word[min_r]] += 1
                min_r += 1
                flag = True
                for cnt in cnt_dict.values():
                    if cnt == 0:
                        flag = False
                        break

            if not flag:
                for char in word[l : min_r]:
                    cnt_dict[char] -= 1
                l = min_r
                continue

            if max_r < min_r:
                max_r = min_r
            while max_r < n and word[max_r] in cnt_dict:
                max_r += 1

            res += max_r - min_r + 1

            cnt_dict[word[l]] -= 1
            if cnt_dict[word[l]] == 0:
                flag = False
            l += 1
        
        return res
''',
    call=f'Solution().countVowelSubstrings({W!r})',
    expect=7,
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='string', var='word', label='word（暗 = 辅音，框 = [l, min_r−1]，绿 = 合法右端点）',
             pointers={'l': 'blue', _lo: 'pink', _hi: 'orange'}, pointer_labels={_lo: 'min_r−1', _hi: 'max_r−1'},
             window=('l', _lo), color=_color, dim=lambda S, i, v: v not in V, cell=96, h=300),
        dict(type='map', var='cnt_dict', label='cnt_dict（窗口 word[l : min_r] 内的元音次数）', fmt=lambda k, v: f"'{k}': {v}", h=150, font=34),
    ],
    watch=[('l', 'l', 'blue'), ('min_r', 'min_r', 'pink'), ('max_r', 'max_r', 'orange'), ('flag', 'flag', 'cyan'), ('res', 'res', 'green')],
    skip=['min_r = 0', 'max_r = 0', 'n = len(word)', 'res = 0', 11, 16, 17, 24, 25, 26, 27, 29, 32, 33],
    captions={
        'l = 0': '`l` 左边界；`min_r`/`max_r` 是右边界（==开区间==，都只会右移）',
        'cnt_dict = {': '`cnt_dict` 统计窗口内五种元音的次数',
        10: '`flag`：窗口是否已包含全部五种元音',
        11: lambda S, B, r: ('`l < n`，继续' if S.l < S.n else '`l` 到末尾，结束'),
        12: lambda S, B, r: (f'`word[{S.l}] = {S.word[S.l]!r}` 是辅音 → 不能当左边界' if S.l < S.n and S.word[S.l] not in V
                             else ('`l` 到末尾了' if S.l >= S.n else f'`word[{S.l}] = {S.word[S.l]!r}` 是元音，可以当左边界')),
        13: '`l` → {l}',
        14: '跨过辅音，窗口作废：`flag = False`',
        'if l == n': lambda S, B, r: ('`l == n`：结束' if S.l == S.n else '还没到末尾'),
        'if min_r < l': lambda S, B, r: (f'`min_r = {S.min_r} < l`：右边界不能在左边界左边' if S.min_r < S.l else f'`min_r = {S.min_r} ≥ l`，沿用上一轮'),
        'min_r = l': '`min_r` → {min_r}',
        22: lambda S, B, r: (f'五种元音已齐（`flag = True`），min_r 不用再动' if S.flag
                             else (f'`word[{S.min_r}] = {S.word[S.min_r]!r}` 是元音，还没凑齐 → 扩展' if S.min_r < S.n and S.word[S.min_r] in V
                                   else '遇到辅音/末尾，扩展不下去了')),
        'cnt_dict[word[min_r]] += 1': '`{word[min_r]!r}` 进入窗口（次数 → {cnt_dict[word[min_r]]}），`min_r` 随后右移',
        'min_r += 1': '`min_r` → {min_r}',
        'flag = True': '先假设齐了，再检查五个次数',
        28: '有元音次数为 0 → 还没凑齐，`flag = False`',
        'if not flag': lambda S, B, r: ('`flag = False`：`l..min_r−1` 凑不齐五种元音 → 这一段的左边界==全部作废==' if not S.flag
                                        else f'`flag = True`：`word[{S.l}:{S.min_r}]` 是最短合法子串'),
        'for char in word[l : min_r]': lambda S, B, r: f'把 `word[{S.l}:{S.min_r}]` 的次数全部撤销 → {dict(S.cnt_dict)}',
        'cnt_dict[char] -= 1': '`cnt_dict[{char!r}]` → {cnt_dict[char]}',
        'l = min_r': '撤销 `word[{B.l}:{l}]` 的计数，左边界直接跳到 `min_r = {l}`',
        'continue': '回到循环开头',
        'if max_r < min_r': lambda S, B, r: (f'`max_r < min_r`，先置为 min_r' if S.max_r < S.min_r else f'`max_r = {S.max_r}` 沿用上一轮'),
        'max_r = min_r': '`max_r` → {max_r}',
        'while max_r < n': lambda S, B, r: (f'`word[{S.max_r}] = {S.word[S.max_r]!r}` 仍是元音 → 继续延伸' if S.max_r < S.n and S.word[S.max_r] in V
                                            else '遇到辅音/末尾：最长只能到这里'),
        'max_r += 1': '`max_r` → {max_r}',
        'res += max_r': '右端点在 `{min_r - 1}..{max_r - 1}` 都合法：`{max_r} − {min_r} + 1` 个 → `res` = =={res}==',
        44: '`word[{l}] = {word[l]!r}` 移出窗口 → `cnt_dict[{word[l]!r}] = {cnt_dict[word[l]]}`',
        45: lambda S, B, r: (f'{S.word[S.l]!r} 没了 → 不再齐全' if S.cnt_dict[S.word[S.l]] == 0 else f'窗口里还有 {S.word[S.l]!r}，仍然齐全'),
        46: '`flag = False`：下一轮要继续扩展 min_r',
        47: '左边界右移 → `l = {l}`',
        'return res': '一共 =={ret}== 个元音子字符串',
    },
    max_steps=90,
    cards=dict(
        one_liner='枚举左边界 l：合法右端点是一段区间，长度 max_r − min_r + 1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['==元音子串==：只由元音组成，且五种元音都出现',
                 '统计 `word` 中元音子串的个数',
                 '示例：`"aeiouu"` → `2`；`"cuaieuouac"` → `7`'],
        quote='以l为左边界的合法子字符串，其最小右边界为min_r，最大右边界为max_r，因此一共有max_r - min_r + 1种合法的子字符串。',
        quote_src='—— yiduobo 题解原文',
        idea=['min_r：从 l 起==刚好凑齐==五种元音的位置',
              'max_r：从 l 起==一直是元音==能延伸到的位置',
              'l 右移时两者只会右移；凑不齐就让 l 直接跳到 min_r'],
        summary=['时间 `O(n)`：l、min_r、max_r 都只右移',
                 '代码里 min_r、max_r 是==开区间==（指向下一个位置），所以计数是 `max_r − min_r + 1`',
                 '跨过辅音时要把 flag 置 False，并撤销窗口计数',
                 '对比灵神：灵神枚举右端点，用 start 处理辅音；这里枚举左端点',
                 '代码本身可在 Python 3 运行，未做改动'],
    ),
)
