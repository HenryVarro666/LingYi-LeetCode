def _formula(S):
    if 'right' not in S:
        return '不定长滑动窗口：==枚举右端点，窗口不合法就移动左端点=='
    l, r, s = S['left'], S['right'], S['s']
    win = s[l:r + 1]
    ok = all(v <= 1 for v in S['cnt'].values())
    state = '==合法==（无重复）' if ok else f"不合法：`'{S['c']}'` 出现 {S['cnt'][S['c']]} 次"
    return f"窗口 `s[{l}..{r}]` = `'{win}'`，长度 {r - l + 1}，{state}"


_seen = {}


def _while_cap(S, B, ret):
    if S.cnt[S.c] <= 1:
        return f"`cnt['{S.c}'] = 1`：窗口合法，不用收缩"
    first = _seen.get('r') != S.right
    _seen['r'] = S.right
    if first:
        return f"② `cnt['{S.c}'] = {S.cnt[S.c]} > 1`：==罪魁祸首只能是刚进来的 '{S.c}'==，收缩！"
    return f"`'{S.c}'` 仍有 {S.cnt[S.c]} 个 → 继续收缩"


CONFIG = dict(
    num=None, title='滑动窗口 · 通用思想与模板', author='概念讲解', category='滑动窗口',
    technique='通用思想与模板', kind='concept', difficulty='',
    code='''
def longest_unique(s):              # 3. 无重复字符的最长子串
    ans = left = 0
    cnt = defaultdict(int)          # 窗口 [left, right] 内各字符个数
    for right, c in enumerate(s):   # 枚举右端点
        cnt[c] += 1                 # ① c 进入窗口
        while cnt[c] > 1:           # ② 窗口不合法（有重复）
            cnt[s[left]] -= 1       #    s[left] 离开窗口
            left += 1               #    左端点右移
        ans = max(ans, right - left + 1)  # ③ 窗口合法，更新答案
    return ans
''',
    call="longest_unique('abcbdab')",
    expect=4,
    views=[
        dict(type='text', fn=_formula, h=60),
        dict(type='string', var='s', pointers={'left': 'blue', 'right': 'pink'}, window=('left', 'right'),
             dim=lambda S, i, v: 'right' in S and (i < S['left'] or i > S['right']),
             color=lambda S, i, v: ('red' if 'right' in S and S['left'] <= i <= S['right'] and v == S.get('c')
                                    and S['cnt'][v] > 1 else None), h=250),
        dict(type='map', var='cnt', label='cnt：窗口内每个字符的个数', fmt=lambda k, v: f'{k}: {v}', font=28, h=120),
        dict(type='text', fn=lambda S: f"历史最长 `ans = {S['ans']}`" + (
            f"，当前窗口 `'{S['s'][S['left']:S['right'] + 1]}'`" if 'right' in S else ''), size=26, h=60),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), 'c', ('ans', 'ans', 'green')],
    captions={
        'ans = left = 0': '窗口一开始为空：`left = 0`，答案 `ans = 0`',
        'cnt = defaultdict': '`cnt` 记录窗口里每个字符出现几次——判断「有没有重复」只看它',
        'for right, c': lambda S, B, ret: (f"枚举右端点：`right = {S.right}`，新字符 `'{S.c}'`"
                                           if B.get('right') != S.right else '右端点走到头，循环结束'),
        'cnt[c] += 1': "① `'{c}'` 进入窗口：`cnt['{c}'] = {cnt[c]}`",
        'while cnt[c] > 1': _while_cap,
        'cnt[s[left]] -= 1': "`'{s[left]}'` 离开窗口：`cnt['{s[left]}'] = {cnt[s[left]]}`",
        'left += 1': '`left` → {left}：左端点只右移，累计移动 {left} 次，==总共不超过 n 次==',
        'ans = max': '③ 窗口 `[{left}, {right}]` 合法，长度 `{right - left + 1}`，`ans = max({B.ans}, {right - left + 1}) = {ans}`',
        'return ans': '返回 `{ret}`：两层循环，但 `left`、`right` 都只增不减 → ==O(n)==',
    },
    cards=dict(
        one_liner='枚举右端点，窗口不合法就右移左端点；两个端点都只往右走',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`（字符集大小）',
        problem_heading='什么时候用？',
        problem=['求 ==连续== 子数组 / 子串的最长、最短或个数',
                 '有单调性：窗口合法时缩小仍合法（或不合法时扩大仍不合法）',
                 '统计窗口内字符次数、元素和（元素非负）等可以 ==增量维护== 的量',
                 '暴力枚举左右端点是 `O(n²)`，想优化到 `O(n)`'],
        before=[dict(heading='核心概念：不定长窗口三步走', lines=[
            '① 入：`s[right]` 进入窗口，更新计数 / 和',
            '② 出：窗口不合法就 `while` 右移 `left`，把 `s[left]` 移出',
            '③ 更新答案：此时窗口合法，长度 `right - left + 1`',
            '为什么是 `O(n)`：`left` 只增不减，内层循环 ==总共== 最多执行 `n` 次',
            '定长窗口：每次进一个、出一个，长度到 `k` 才开始统计']),
        ],
        idea_heading='两位作者怎么说',
        quote='如果字母 c 进入窗口后，窗口不合法（某个 cnt[x] < 0），那么罪魁祸首是谁？由于在之前的循环中，我们已经把窗口变成合法的了，所以==只能是刚进入窗口的字母 c== 导致窗口不合法……',
        quote_src='—— 灵茶山艾府 · 438. 找到字符串中所有字母异位词',
        idea=['灵神的套路：枚举右端点，不合法就缩左端点；`left` 的总移动次数 ≤ `n`',
              'yiduobo 在 3 题从 DP 出发：`f[i]` 是以 `s[i]` 结尾的最优左边界',
              'yiduobo 的关键观察：==左边界的更新是单调递增的==，所以每个字符只遍历一次'],
        summary_heading='本类 Hot100 题目 & 学习顺序',
        summary=['`3` 无重复字符的最长子串：不定长窗口，`cnt[c] > 1` 就收缩',
                 '`438` 找到所有字母异位词：定长窗口比较计数，或不定长 + 长度判定',
                 '进阶：`76` 最小覆盖子串、`239` 滑动窗口最大值（在「子串」类）',
                 '易错：先入窗口再收缩、最后更新答案；长度是 `right - left + 1`'],
    ),
)
