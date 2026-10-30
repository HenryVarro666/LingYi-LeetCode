def _t(S):
    if 'index' not in S:
        return ''
    s, k = S['s'], S['index']
    return s[k:] + s[:k]


def _top(S):
    if 'index' not in S:
        return ''
    t = _t(S)
    msg = f"左旋 `{S['index']}` 次得到 `{t}`，移位代价 ==" + str(S['index']) + "=="
    if 'cost' in S and 'left' in S:
        msg += f"；本轮配对已累计 ==" + str(S['cost']) + "=="
    return msg


CONFIG = dict(
    num=4021, title='得到旋转回文字符串的最少操作次数 I', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='枚举左旋 + 双指针配对',
    tags=['卷积'],
    code='''
class Solution(object):
    def minOperations(self, s):
        
        def calc(t):
            left, right = 0, len(t) - 1
            cost = 0
            while left < right:
                dis = abs(ord(t[left]) - ord(t[right]))
                cost += min(dis, 26 - dis)
                left += 1
                right -= 1
            
            return cost
        
        res = 26 * len(s)
        for index in range(len(s)):
            res = min(res, index + calc(s[index:] + s[:index]))
        return res
''',
    call='Solution().minOperations("zffye")',
    expect=3,
    views=[
        dict(type='text', h=60, fn=_top),
        dict(type='string', var=lambda S: S['t'] if 't' in S else _t(S), h=250, label='左旋后的字符串 t（左右两个指针往中间靠）',
             pointers={'left': 'blue', 'right': 'pink'}),
        dict(type='text', h=60, fn=lambda S: (f"目前最小 res = ==" + str(S['res']) + "==" if 'res' in S else '')),
    ],
    watch=[('index', 'index', 'blue'), ('left', 'left', 'blue'), ('right', 'right', 'pink'), ('dis', 'dis', 'yellow'),
           ('cost', 'cost', 'orange'), ('res', 'res', 'green')],
    skip=['left, right = 0', 'cost = 0', 'res = 26', 'left += 1', 'right -= 1'],
    max_steps=80,
    captions={
        'dis = abs': lambda S, B, r: f"`t[{S.left}] = {S.t[S.left]}` 和 `t[{S.right}] = {S.t[S.right]}` 要变成一样：ASCII 差 `dis = {S.dis}`",
        'cost += min': '较小的升到较大的要 `{dis}` 次，反过来绕一圈要 `26 - {dis} = {26 - dis}` 次 → 取小的 `{min(dis, 26 - dis)}`，`cost` = =={cost}==',
        'while left < right': lambda S, B, r: ((f"`left = 0`，`right = {S.right}`：从两端开始配对" if S.left == 0 else f"两端各走一步：`left = {S.left}`，`right = {S.right}`，还有一对没配") if S.left < S.right
                                               else f"`left = {S.left} ≥ right = {S.right}`：配对结束"),
        'return cost': '这个字符串变回文的递增代价 `{cost}`',
        'res = min': '左旋 `{index}` 次 → `t = s[{index}:] + s[:{index}]` = `{s[index:] + s[:index]}`，交给 `calc` 算递增次数，再加移位 `{index}`',
        'return res': '所有左旋次数都试过 → 最少操作 =={res}==',
    },
    cards=dict(
        one_liner='枚举左旋几次，再用首尾双指针算每对字母的最小递增次数',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['小写字符串 `s`：可「某位 +1（z 后是 a）」或「左旋一位」',
                 '求让 `s` 成为回文串的最少操作次数，`n ≤ 2000`',
                 '示例：`"abc"` → `2`；本视频用 `"zffye"` → `3`'],
        quote='由于题目中s的长度不大，因此在这里可以直接枚举左旋的字符数量，然后拼接得到新的字符串t。',
        quote_src='—— yiduobo 题解原文',
        idea=['`t = s[index:] + s[:index]` 就是左旋 `index` 次的字符串',
              '`left`、`right` 从两端向中间，每对字母必须变一致',
              '距离 `dis`：小升大花 `dis`，大升到小（绕过 z）花 `26 - dis`，取较小'],
        summary=['时间 `O(n^2)`：`n` 次旋转，每次拼接 + 双指针 `O(n)`',
                 '算完 `calc` 后别忘了加上移位代价 `index`',
                 '`res` 初值 `26 * len(s)` 足够大，不会误当答案',
                 '原文已是 Python 3 可运行的写法，无需改动',
                 '对比灵神：他不拼接字符串，直接用 `(rot + i) % n` 取下标'],
    ),
)
