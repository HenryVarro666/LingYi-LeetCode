def _top(S):
    if 'n' not in S:
        return ''
    n = S['n']
    if 'left' not in S:
        return f'`n = {n}`：前半段 `s[:{n // 2}]` 的字符组成不能改'
    return f'前半段排序后 `left = {S["left"]}`' + (f'，落单的 `mid = {S["mid"]}`' if S.get('mid') else '')


def _res(S):
    if 'left' not in S:
        return ''
    r = S.get('right')
    return f'`left = {S["left"]}`' + (f'　`right = {r}`' if r else '')


CONFIG = dict(
    num=3517, title='最小回文排列 I', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='前半段排序 + 翻转',
    tags=['灵神题单', '难度分 1357'],
    code='''
class Solution(object):
    def smallestPalindrome(self, s):
        n = len(s)
        left = ''.join(sorted(s[:n // 2]))
        right = left[::-1]
        mid = ''
        if n % 2 == 1:
            mid = s[n // 2]
        return left + mid + right
''',
    call='''Solution().smallestPalindrome("babab")
Solution().smallestPalindrome("daccad")''',
    expect='acddca',
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='s', label='s（蓝 = 前半段，粉 = 落单的中间字符）', cell=84,
             color=lambda S, i, v: ('blue' if i < S['n'] // 2 else 'pink' if (S['n'] % 2 and i == S['n'] // 2) else None) if 'n' in S else None,
             dim=lambda S, i, v: 'n' in S and i >= S['n'] // 2 + S['n'] % 2),
        dict(type='string', var='left', label='left（排好序的前半段）', cell=84, color=lambda S, i, v: 'green'),
        dict(type='string', var='right', label='right（left 翻转）', cell=84, color=lambda S, i, v: 'cyan'),
        dict(type='text', fn=_res, size=28),
    ],
    watch=['n', ('left', 'left', 'green'), ('right', 'right', 'cyan'), ('mid', 'mid', 'pink')],
    captions={
        'n = len(s)': '`n = len(s) = {n}`',
        'left =': '前半段的字符组成不能变，要字典序最小就把它排序：`left = {left}`',
        'right =': '后半段 = 前半段翻转，回文才成立：`right = {right}`',
        "mid = ''": '`mid` 先设为空串，留给奇数长度的中间字符',
        'if n % 2 == 1': lambda S, B, r: (f'`n = {S.n}` 是奇数 → 有一个落单的中间字符' if S.n % 2 == 1
                                          else f'`n = {S.n}` 是偶数 → 没有中间字符，`mid` 保持空串'),
        'mid = s[n // 2]': '落单的中间字符 `mid = {mid}`，排序时不能漏掉',
        'return': '拼接 `left + mid + right` = `{left}` + `{mid}` + `{right}` → `{ret}`',
    },
    cards=dict(
        one_liner='前半段排序保证字典序最小，翻转当后半段，别漏中间字符',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['给一个回文串 `s`，重排字符，求字典序==最小==的回文串',
                 '示例：`"babab"` → `"abbba"`',
                 '本视频依次跑：`"babab"` → `"abbba"`；`"daccad"` → `"acddca"`'],
        quote='为了保证得到的字符串依然是回文串，那么s前半段和后半段各自的字符组成是不能改的。而为了使得字典序最小，那么就应该保证s前半段的字典序最小。',
        quote_src='—— yiduobo 题解原文',
        idea=['前、后半段的字符组成不能变，换位置只能在各自半段内',
              '字典序由前面的字符决定 → ==前半段排序==即可最小',
              '后半段把它翻转，保持回文；奇数长度再把中间字符拼在中间'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错：长度为奇数时，中间落单的 `mid` 要拼进答案',
                 '原文代码已是 Python 3 可运行写法，未做修改',
                 '对比灵神：灵神用 `reversed` 拼接并提到计数排序；这里用切片 `[::-1]`'],
    ),
)
