def _run(S):
    if 'index' not in S or 'pos' not in S:
        return ''
    p, idx, pos = S['p'], S['index'], S['pos']
    return f"以 `{p[idx]}` 结尾的连续串：`{p[pos:idx+1]}`，长度 {idx - pos + 1}"


CONFIG = dict(
    num=467, title='环绕字符串中唯一的子字符串', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='以字母结尾的最长连续串 · 字典去重',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def findSubstringInWraproundString(self, p):
        if not p:
            return 0
        f = {}
        now = ' '
        pos = 0
        for index, char in enumerate(p):
            if now == 'z' and char == 'a' or ord(now) == ord(char) - 1:
                now = char
                f[now] = max(f.get(now, 0), index - pos + 1)
            else:
                now = char
                pos = index
                f[now] = max(f.get(now, 0), 1)
        return sum(f.values())
''',
    call='Solution().findSubstringInWraproundString("zabcab")',
    expect=10,
    views=[
        dict(type='text', fn=_run, size=26),
        dict(type='string', var='p', label='p（蓝 = 当前连续串）', cell=80, pointers={'index': 'pink', 'pos': 'blue'},
             window=('pos', 'index'), h=240),
        dict(type='map', var='f', label='f：结尾字母 → 以它结尾的最长连续串长度', h=300),
    ],
    watch=[('index', 'index', 'pink'), ('pos', 'pos', 'blue'), ('now', 'now', 'cyan'), ('sum(f)', 'sum(f.values())', 'green')],
    captions={
        'if not p': '空串没有子串，直接返回 0；本例 `p = "{p}"` 不为空',
        'f = {}': '`f[c]`：以字母 `c` 结尾的==最长==连续串长度。以 `c` 结尾、长度固定的子串是唯一的，所以保留最长的就够了',
        "now = ' '": '`now` 是上一个字符，初始用空格，保证第一个字符一定不接续',
        'pos = 0': '`pos` 是当前连续串的起点',
        'for index, char': '`index = {index}`，`char = {char}`',
        'if now == ': lambda S, B, r: (
            f"`{B.now}` 后面接 `{S.char}`：" + ("==能接上==（环绕或下一个字母），连续串继续变长" if (B.now == 'z' and S.char == 'a') or ord(B.now) == ord(S.char) - 1
                                              else "接不上，连续串在这里断开")),
        10: '`now` 更新为 `{now}`',
        11: '连续串 `p[{pos}:{index + 1}]` 长 `{index - pos + 1}`，以 `{now}` 结尾的子串有这么多种；和旧值取最大：`f["{now}"] = {f[now]}`（较短的被较长的覆盖，不重复算）',
        13: '断开：`now = {now}`',
        14: '新连续串从这里开始：`pos = {pos}`',
        15: '长度 1，`f["{now}"] = {f[now]}`（取最大，不会把已有的更长结果缩短）',
        'return': '每个字母各自最长的长度相加：`sum(f.values())` = =={ret}==',
    },
    cards=dict(
        one_liner='以每个字母结尾的最长连续串，决定了唯一子串的个数',
        complexity='时间 `O(n)`，空间 `O(26)`',
        problem=['`s` 是 `abcdefghijklmnopqrstuvwxyz` 无限环绕的字符串（`...xyzabc...`）',
                 '给定字符串 `p`，求 `p` 有多少个==不同的非空子串==出现在 `s` 中',
                 '本视频：`"zabcab"` → `10`（`z a b c za ab bc zab abc zabc`）'],
        quote='对于某个特定的字符，以该字符为首字符且长度固定的子字符是唯一的……较短的那个字符串必然被较长的字符串全面覆盖住，因此较短的那个字符串就没有保留下来的必要了。',
        quote_src='—— yiduobo 题解原文',
        idea=['先统计连续字符串的长度 `l`，它贡献 `l(l+1)/2` 个子串，但不同位置会==重复==',
              '去重：以同一字母结尾，只留最长的那个，长度 `l` 就代表 `l` 个不同子串',
              '实现时记==结尾==字母更方便：`f[c]` = 以 `c` 结尾的最长连续长度，最后求和'],
        summary=['时间 `O(n)`，空间 `O(26)`',
                 '连续的判定：`z` 后接 `a`，或者后一个字母的 ASCII 码比前一个大 1',
                 '易错：必须用 `max` 更新 `f`，后面出现的短串不能覆盖前面的长串',
                 '本题库里没有题面，题意按 LeetCode 467 原题整理',
                 '难度按 LeetCode 467 标注为 Medium'],
    ),
)
