def _win_text(S):
    if 'right' not in S:
        return '`cnt[x]` = p 中 x 的个数 − 窗口中 x 的个数'
    s, l, r, p = S['s'], S['left'], S['right'], S['p']
    w = s[l:r + 1]
    L = r - l + 1
    return f"窗口 `\"{w}\"`，长度 `{L}`，`len(p) = {len(p)}`" + ('　→ ==异位词==' if L == len(p) and min(S['cnt'].values()) >= 0 else '')


def _color(S, i, v):
    if 'ans' in S and i in S['ans']:
        return 'green'
    return None


def _cnt_fmt(k, v):
    return f'{k}: {v}' + (' 多了' if v < 0 else '')


def _dec(S, B, ret):
    c, k = S.c, S.cnt[S.c]
    if k < 0:
        return f'`"{c}"` 进入窗口：`cnt["{c}"]` → `{k}` ==< 0==，窗口里的 `"{c}"` 比 p 多了'
    return f'`"{c}"` 进入窗口：`cnt["{c}"]` → `{k}`'


def _left_at_start(s, p, right):
    cnt, left = Counter(p), 0
    for r in range(right):
        cnt[s[r]] -= 1
        while cnt[s[r]] < 0:
            cnt[s[left]] += 1
            left += 1
    return left


def _while(S, B, ret):
    c, k = S.c, S.cnt[S.c]
    if k < 0 and S.left == _left_at_start(S.s, S.p, S.right):
        return f'字母 `"{c}"` 太多了：之前窗口合法，==罪魁祸首只能是刚进来的 {c}== → 右移左端点'
    if k < 0:
        return f'`cnt["{c}"] = {k}`，还是太多 → 继续缩'
    if S.right == 0:
        return f'`cnt["{c}"] = {k} ≥ 0`：窗口里每种字母都不超过 p'
    return f'`cnt["{c}"] = {k} ≥ 0`，没有超标'


def _len(S, B, ret):
    L = S.right - S.left + 1
    if L == len(S.p):
        return f'长度 `{L} == len(p)`，且没有字母超标 → ==每种字母次数都相同=='
    return f'长度 `{L}` ≠ `{len(S.p)}`'


CONFIG = dict(
    num=438, title='找到字符串中所有字母异位词', difficulty='Medium', category='滑动窗口',
    author='灵茶山艾府', technique='不定长滑动窗口 · 合并计数',
    code='''
# 请选择 Python3 提交代码，而不是 Python
class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        cnt = Counter(p)  # 统计 p 的每种字母的出现次数
        ans = []

        left = 0
        for right, c in enumerate(s):
            cnt[c] -= 1  # 右端点字母进入窗口
            while cnt[c] < 0:  # 字母 c 太多了
                cnt[s[left]] += 1  # 左端点字母离开窗口
                left += 1
            if right - left + 1 == len(p):  # t 和 p 的每种字母的出现次数都相同（证明见上）
                ans.append(left)  # t 左端点下标加入答案

        return ans
''',
    call='Solution().findAnagrams("cbaebabac", "abc")',
    expect=[0, 6],
    views=[
        dict(type='text', fn=_win_text),
        dict(type='string', var='s', pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'),
             color=_color, cell=88, h=270, label='s'),
        dict(type='map', var='cnt', fmt=_cnt_fmt, font=30, h=150,
             label='cnt：p 还"欠"窗口的个数（负数 = 窗口里多了）'),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('c', 'c', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'cnt = Counter(p)': '先统计 p：`{dict(cnt)}`。==之后窗口每进一个字母就减一==',
        'ans = []': '`ans` 收集异位词的起点',
        'left = 0': '窗口左端点 `left = 0`',
        'for right, c in': lambda S, B, r: ('枚举结束' if 'right' in B and B.right == S.right
                                            else f'右端点 `right = {S.right}`，字母 `"{S.c}"`'),
        'cnt[c] -= 1': _dec,
        'while cnt[c] < 0': _while,
        'cnt[s[left]] += 1': '`"{s[left]}"` 离开窗口：`cnt["{s[left]}"]` → {cnt[s[left]]}',
        'left += 1': '`left` → {left}，窗口 `"{s[left:right + 1]}"`',
        'if right - left + 1 == len(p)': _len,
        'ans.append(left)': '`{left}` 是异位词 `"{s[left:right + 1]}"` 的起点，加入答案',
        'return ans': '返回 `{ans}`',
    },
    cards=dict(
        one_liner='窗口里没有字母超标、且长度等于 len(p)，就是异位词',
        complexity='时间 `O(m + n)`，空间 `O(|Σ|)`',
        problem=['找出 `s` 中所有是 `p` 的==字母异位词==的子串，返回这些子串的起始下标',
                 '示例：`s = "cbaebabacd", p = "abc"` → `[0,6]`',
                 '本视频去掉末尾的 `d`：`"cbaebabac"`，答案同样是 `[0,6]`'],
        quote='内层循环结束后，t 的每种字母的出现次数，都小于等于 p 的每种字母的出现次数。……所以==只要 t 的长度等于 p 的长度==，就说明……t 是 p 的异位词。',
        quote_src='—— 灵茶山艾府题解「方法二」',
        idea=['把两份计数合成一个 `cnt`：p 的字母 +1，进入窗口的字母 −1',
              '`cnt[c] < 0`：窗口里 c 比 p 多 → 右移左端点，直到 `cnt[c] ≥ 0`',
              '为什么只查 c？之前窗口已合法，==只有刚进来的 c 可能超标=='],
        summary=['时间 `O(m+n)`：`left` 总共至多右移 m 次',
                 '没有超标 + 长度相等 ⇒ 每种都相等（某种少了，长度就凑不够）',
                 '易错：不在 p 中的字母（如 `e`）一进来 `cnt` 就变负，窗口会一直缩到它后面',
                 '方法一：定长滑窗，每步比较两个 Counter，`O(|Σ|m + n)`'],
    ),
)
