CONFIG = dict(
    num=2131, title='连接两字母单词得到的最长回文串', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='分类讨论 · 正反配对',
    tags=['灵神题单', '难度分 1557'],
    code='''
class Solution:
    def longestPalindrome(self, words: List[str]) -> int:
        cnt = Counter(words)

        ans = odd = 0
        for w, c in cnt.items():
            if w[0] == w[1]:
                ans += c - c % 2
                odd |= c % 2
            elif w[0] < w[1]:
                ans += min(c, cnt[w[::-1]]) * 2
        return (ans + odd) * 2
''',
    call='Solution().longestPalindrome(["ab","ty","yt","lc","cl","ab","gg","gg","gg"])',
    expect=14,
    views=[
        dict(type='array', var='words', label='words（黄 = 当前枚举的单词）', cell=96,
             color=lambda S, i, v: 'yellow' if S.get('w') == v else None),
        dict(type='map', var='cnt', label='cnt（单词 → 出现次数）', fmt=lambda k, v: f'"{k}": {v}', h=200),
        dict(type='text', fn=lambda S: (f"已配好 `{S['ans']}` 个单词，中间可放 `{S['odd']}` 个 → 长度 = ({S['ans']} + {S['odd']}) × 2 = =={(S['ans'] + S['odd']) * 2}==" if 'ans' in S else ''), size=26),
    ],
    watch=['w', 'c', ('ans', 'ans', 'green'), ('odd', 'odd', 'orange')],
    captions={
        'cnt = Counter': '先数每种单词出现几次：`{dict(cnt)}`',
        'ans = odd = 0': '`ans` 数能放进回文串的==单词个数==，`odd` 记有没有回文单词能放正中间',
        'for w, c in cnt.items()': lambda S, B, r: ('所有不同的单词都枚举完了' if 'w' in B and B.w == S.w and B.c == S.c
                                                   else f'枚举单词 `"{S.w}"`，出现 `{S.c}` 次'),
        'if w[0] == w[1]': lambda S, B, r: (f'`"{S.w}"` 两个字母==相同== → 自己就是回文，成对放左右' if S.w[0] == S.w[1]
                                           else f'`"{S.w}"` 两个字母不同 → 要找反过来的 `"{S.w[::-1]}"` 配对'),
        'ans += c - c % 2': '`{c}` 个 `"{w}"`：成对放两侧，只能用 `{c} - {c} % 2` = `{c - c % 2}` 个 → `ans` = =={ans}==',
        'odd |= c % 2': lambda S, B, r: (f'`{S.c}` 是奇数，剩下 1 个 `"{S.w}"` 可放==正中间== → `odd = 1`' if S.c % 2
                                        else f'`{S.c}` 是偶数，没有落单的 → `odd` 不变（{S.odd}）'),
        'elif w[0] < w[1]': lambda S, B, r: (f'`"{S.w}"` 的字母顺序是小 < 大 → 只在这一侧处理一次，避免正反重复算' if S.w[0] < S.w[1]
                                            else f'`"{S.w}"` 字母是大 > 小，它的反串会处理，这里跳过'),
        'ans += min': '`"{w}"` 有 `{c}` 个，`"{w[::-1]}"` 有 `{cnt[w[::-1]]}` 个 → 取较小 `{min(c, cnt[w[::-1]])}` 对，每对 2 个单词 → `ans` = =={ans}==',
        'return': '`ans = {ans}`、`odd = {odd}`：(`{ans}` + `{odd}`) × 2 = =={ret}==（单词数乘 2 才是长度）',
    },
    cards=dict(
        one_liner='正反单词配对放两侧，相同字母的单词留一个放中间',
        complexity='时间 `O(n + |Σ|²)`，空间 `O(|Σ|²)`',
        problem=['`words` 每个元素都是 ==两个小写字母== 的单词，每个至多用一次',
                 '任意顺序拼接，求能得到的==最长回文串的长度==，没有就返回 0',
                 '示例：`["lc","cl","gg"]` → `6`（`lcggcl`）'],
        quote='字符串的两个字母不同：假设有 2 个 ab 和 3 个 ba，我们可以在回文串的左半边中放 2 个 ab，右半边中的对称位置放 2 个 ba。剩下 1 个 ba 没法用，舍去。',
        quote_src='—— 灵茶山艾府题解',
        idea=['两字母不同：`ab` 和 `ba` 各取 `min` 个，一左一右对称放',
              '两字母相同：`aa` 自己就是回文，成对放，奇数个时多出的 1 个放==正中间==',
              '先数单词个数，最后乘 2 得到字符串长度'],
        result='`ab` 配不到 `ba`；`ty/yt`、`lc/cl` 各配 1 对；`gg` 共 3 个，用 2 个 + 中间 1 个 → 7 个单词 → 14',
        summary=['时间 `O(n + |Σ|²)`，空间 `O(|Σ|²)`，|Σ| = 26',
                 '本视频演示灵神的「Python3 写法二」（Counter）；写法一是 26×26 二维数组计数，思路相同',
                 '易错：`w[0] < w[1]` 保证每对 `ab/ba` 只算一次',
                 '易错：奇数个相同字母单词只能放一个在中间，所以 `odd` 只记 0/1',
                 '最后别忘了 ×2：`ans` 统计的是单词个数'],
    ),
)
