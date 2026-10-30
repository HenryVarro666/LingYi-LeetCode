def _cur(S):
    if 'index' not in S or 'start_pos' not in S:
        return ''
    return f"单词 `{S['s']}`，从位置 `{S['start_pos']}` 切开：后缀 + 其他单词 + 前缀"


CONFIG = dict(
    num=555, title='分割连接字符串', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='预处理 + 枚举切点',
    tags=['灵神题单·贪心与思维'],
    code='''
class Solution(object):
    def splitLoopedString(self, strs):

        n = len(strs)
        best_strs = strs[:]
        for index, s in enumerate(strs):
            left, right = 0, len(s) - 1
            while left < right:
                if s[left] != s[right]:
                    if s[left] < s[right]:
                        best_strs[index] = s[::-1]
                    break
                left += 1
                right -= 1

        res = None
        for index, s in enumerate(strs):
            best_other = ''.join(best_strs[index + 1:]) + ''.join(best_strs[:index])
            for start_pos in range(len(s)):
                f = s[start_pos:]
                f += best_other
                f += s[:start_pos]
                g = s[::-1][start_pos:]
                g += best_other
                g += s[::-1][:start_pos]

                if res is None or res < f:
                    res = f
                if res is None or res < g:
                    res = g
        
        return res
''',
    call='Solution().splitLoopedString(["abc", "xyz"])',
    expect='zyxcba',
    views=[
        dict(type='array', var='strs', label='strs（原单词）', cell=84, h=200, pointers={'index': 'pink'},
             color=lambda S, i, v: 'pink' if i == S.get('index') else None),
        dict(type='array', var='best_strs', label='best_strs（每个单词正/反中字典序较大的）', cell=84, h=200,
             color=lambda S, i, v: 'green' if v != S['strs'][i] else None),
        dict(type='text', fn=lambda S: f"`best_other` = `{S['best_other']}`（其他单词按顺序拼接）" if 'best_other' in S else '', size=26),
        dict(type='text', fn=lambda S: (f"`f` = `{S['f']}`" if 'f' in S else '') + (f"　`g` = `{S['g']}`" if 'g' in S and S['_line'] >= 24 else ''), size=26),
        dict(type='text', fn=lambda S: f"当前最大 `res` = ==`{S['res']}`==" if S.get('res') else '', size=28),
    ],
    watch=['index', 'start_pos', ('res', 'res', 'green')],
    captions={
        'n = len': '`n = {n}` 个单词',
        'best_strs = strs': '`best_strs`：先放原单词，下面把需要反转的换掉',
        6: lambda S, B, r: (f'预处理：单词 `{S.s}`，比较「正着」与「反着」哪个字典序更大' if S.get('index') is not None and B.get('index') != S.index else 'for 循环结束，预处理完成'),
        'break': '第一对不同的字符已经决定了正反谁大 → 退出，不必再比',
        'res = f': '`res` 更新为 `{res}`',
        'res = g': '`res` 更新为 `{res}`',
        'left, right = 0': '`left`、`right` 从两端往中间比，找第一对不同的字符',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`，继续比较' if S.left < S.right else '两端都相同，是回文：正反一样，不用换'),
        'if s[left] != s[right]': lambda S, B, r: (f"`s[{S.left}] = {S.s[S.left]}` ≠ `s[{S.right}] = {S.s[S.right]}` → 找到第一对不同" if S.s[S.left] != S.s[S.right]
                                                    else f"`s[{S.left}] = {S.s[S.left]}` == `s[{S.right}]`，继续往里"),
        'if s[left] < s[right]': lambda S, B, r: (f"`{S.s[S.left]}` < `{S.s[S.right]}`：反转后开头是较大的字符 → ==用反转串==" if S.s[S.left] < S.s[S.right]
                                                  else f"`{S.s[S.left]}` > `{S.s[S.right]}`：原串开头更大，保持原样"),
        'best_strs[index] = s[::-1]': '`best_strs[{index}]` 换成 `{best_strs[index]}`',
        'left += 1': '`left` → {left}',
        'right -= 1': '`right` → {right}',
        'res = None': '`res` 记录目前最大的字符串',
        'best_other =': '其他单词不被切开，直接用各自较大的写法，按环的顺序拼接：`{best_other}`',
        'for start_pos': lambda S, B, r: (f'`{S.s}` 的切点都试完了' if (B.get('start_pos') == S.start_pos and B.get('index') == S.index)
                                          else f'枚举 `{S.s}` 的切点 `start_pos = {S.start_pos}`'),
        'f = s[': '正向：后缀 `{s[start_pos:]}`',
        'f += best_other': '后面接其他单词：`f = {f}`',
        'f += s[:': '最后接上被切下来的前缀：`f = {f}`',
        'g = s[::-1][': '反向：反转串的后缀 `{g}`',
        'g += best_other': '后面接其他单词：`g = {g}`',
        'g += s[::-1][:': '最后接反转串的前缀：`g = {g}`',
        'if res is None or res < f': lambda S, B, r: (f'`res` 为空或 `{S.res}` < `{S.f}` → 更新为 `f`' if (B.res is None or B.res < S.f)
                                                     else f'`{B.res}` ≥ `{S.f}`，不更新'),
        'if res is None or res < g': lambda S, B, r: (f'`res` 为空或 `{S.res}` < `{S.g}` → 更新为 `g`' if (B.res is None or B.res < S.g)
                                                     else f'`{B.res}` ≥ `{S.g}`，不更新'),
        'return res': '所有切法都试过，最大的是 `{res}`',
    },
    cards=dict(
        one_liner='其他单词取较大写法，只枚举被切开的那个单词',
        complexity='时间 `O(m²)`（m 为总字符数），空间 `O(m)`',
        problem=['把字符串数组按顺序首尾相连成环，每个单词可以正着或反着用',
                 '在环上选一个切点断开，得到一个常规字符串',
                 '求所有可能里字典序最大的；示例 `["abc","xyz"]` → `"zyxcba"`'],
        quote='最终答案一定是某个子串或者其反转从某个位置cus_pos截断，取后缀的部分，然后按顺序拼接其他单词或者反转后的单词，最后再拼接剩截断单词前缀的部分。',
        quote_src='—— yiduobo 题解原文',
        idea=['没被切开的单词：正反中字典序较大的那个一定更好 → 先预处理成 `best_strs`',
              '被切开的单词：枚举每个切点，以及正、反两种方向',
              '拼成「后缀 + 其他单词 + 前缀」，更新最大值'],
        summary=['时间 `O(m²)`，`m` 为所有单词字符总数，题目规模允许',
                 '预处理比较正反串：从两端往里找第一对不同的字符',
                 '切点两侧要用同一个方向（`f` 用原串，`g` 用反转串）',
                 '原文已是 Python 3 可运行的写法，未做修改'],
    ),
)
