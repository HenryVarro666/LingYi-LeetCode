def _ans(S):
    if 'ans' not in S:
        return '把每个括号对替换成 knowledge 里的 value；没有就替换成 `?`'
    return f"当前答案 `ans = {''.join(S['ans'])!r}`"


def _colr(S, i, v):
    if 'left' not in S or 'i' not in S:
        return None
    if S['left'] >= 0 and S['left'] <= i <= S['i']:
        return 'yellow'
    return None


CONFIG = dict(
    num=1807, title='替换字符串中的括号内容', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='哈希表 + 记录左括号下标',
    tags=[],
    code='''
class Solution:
    def evaluate(self, s: str, knowledge: List[List[str]]) -> str:
        # 每个 knowledge[i] 都是一个键值对，插入字典
        # 查字典时，如果 key 不在字典中，那么 value 为 '?'
        d = defaultdict(lambda: '?', knowledge)

        ans = []
        left = -1
        for i, ch in enumerate(s):
            if ch == '(':
                left = i  # 记录左括号的位置
            elif ch == ')':
                # 替换左右括号之间的子串
                t = s[left + 1: i]
                ans.append(d[t])
                left = -1
            elif left < 0:  # ch 不在左右括号之间
                ans.append(ch)
        return ''.join(ans)
''',
    call='Solution().evaluate("(a)b(c)(a)", [["a", "yes"]])',
    expect='yesb?yes',
    views=[
        dict(type='text', h=70, fn=_ans),
        dict(type='string', var='s', pointers={'i': 'blue', 'left': 'pink'}, h=230, color=_colr),
        dict(type='map', var='d', label='d（defaultdict：查不到时 value 为 "?"）', fmt=lambda k, v: f'{k} → {v}', h=190),
    ],
    watch=[('i', 'i', 'blue'), ('ch', 'ch'), ('left', 'left', 'pink'), ('t', 't', 'yellow')],
    captions={
        'd = defaultdict': '`knowledge` 转成哈希表 `d`；==查不到的 key 默认给 `\'?\'`==',
        'ans = []': '`ans` 收集每一段结果，最后拼成字符串',
        8: '`left = -1` 表示当前==不在括号里==',
        16: '替换完成，`left` 置回 `-1`：之后的字母又在括号外了',
        'for i, ch': lambda S, B, ret: ('整个字符串扫完了' if B.get('i') == S.i else f"看 `s[{S.i}] = {S.ch!r}`"),
        "if ch == '('": lambda S, B, ret: ("`'('` → 一个括号对开始" if S.ch == '(' else f"`{S.ch!r}` 不是 `'('`，看看是不是 `')'`"),
        'left = i': '记录左括号的位置：`left = {left}`',
        "elif ch == ')'": lambda S, B, ret: ("`')'` → 括号对结束，该替换了" if S.ch == ')' else f"`{S.ch!r}` 也不是 `')'`，看它在不在括号里"),
        't = s[left + 1: i]': '括号里的 key：`s[{left + 1}:{i}]` = `{t!r}`',
        'ans.append(d[t])': lambda S, B, ret: (f"`d[{S.t!r}] = {S.d[S.t]!r}` → 替换括号对，追加到 `ans`" if S.t in B['d']
                                                else f"`{S.t!r}` 不在 knowledge 里 → ==默认值 `'?'`==，追加到 `ans`（defaultdict 还会把它记进 d）"),
        'elif left < 0': lambda S, B, ret: (f"`left = {S.left} < 0` → `{S.ch!r}` 在括号外，原样保留" if S.left < 0
                                             else f"`left = {S.left} >= 0` → `{S.ch!r}` 在括号里，它是 key 的一部分，暂时不放进答案"),
        'ans.append(ch)': '括号外的字母直接追加：`ans = {"".join(ans)!r}`',
        "return ''.join(ans)": '拼接得到 `{ret!r}`',
    },
    cards=dict(
        one_liner='遇到左括号记下标，遇到右括号就查表替换',
        complexity='时间 `O((m+n)L)`，空间 `O(m+nL)`',
        problem=['字符串 `s` 里有若干括号对，括号内是非空的 key，不嵌套',
                 '`knowledge` 给出 key → value；括号对连同括号替换成 value，查不到替换成 `?`',
                 '示例：`"(a)b(c)(a)"`，`[["a","yes"]]` → `"yesb?yes"`'],
        quote='遇到左括号时，用一个变量 left 记录该左括号的下标。遇到右括号 s[i] 时，子串 [left+1,i-1] 即为要替换的子串。替换后，把 left 置为 -1，这样我们可以判断一个字母是否在括号中。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先把 `knowledge` 变成哈希表，查 key 是 `O(L)`',
              '`left` 既记下标又当状态：`left < 0` 说明不在括号里',
              '用 `defaultdict(lambda: \'?\', knowledge)`，查不到自动是 `?`，不用写 if'],
        summary=['时间 `O((m+n)L)`，`L ≤ 10` 是单个字符串长度',
                 '易错：右括号处理完要把 `left` 置回 `-1`，否则后面括号外的字母会被丢掉',
                 '`defaultdict` 查不到 key 时会把默认值写进字典，不影响本题答案',
                 '另一种写法：括号换成 `{}`，`format_map(d)` 一行搞定'],
    ),
)
