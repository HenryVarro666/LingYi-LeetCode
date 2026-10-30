def _idx(S):
    if 'x' not in S:
        return None
    n = S['a'] + sum(S['cnt_s'].values())
    if S.get('_line') in (8, 10, 11):
        n -= 1
    return min(n, len(S['secret']) - 1)


def _res_txt(S):
    if 'cnt_s' not in S:
        return '公牛 a：位置和数字都对；其余位置才统计奶牛'
    inter = {k: min(v, S['cnt_g'].get(k, 0)) for k, v in S['cnt_s'].items() if min(v, S['cnt_g'].get(k, 0)) > 0}
    if 'b' in S:
        return f"`a = {S['a']}`，`b = ` 交集总数 ==`{S['b']}`=="
    return f"当前 `a = {S['a']}`；错位的数字分别计入 `cnt_s` / `cnt_g`"


CONFIG = dict(
    num=299, title='猜数字游戏', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='计数 + Counter 交集',
    tags=[],
    code='''
class Solution:
    def getHint(self, secret: str, guess: str) -> str:
        a = 0
        cnt_s = Counter()
        cnt_g = Counter()
        for x, y in zip(secret, guess):
            if x == y:
                a += 1
            else:
                cnt_s[x] += 1
                cnt_g[y] += 1
        b = (cnt_s & cnt_g).total()
        return f"{a}A{b}B"
''',
    call='Solution().getHint("1123", "0111")',
    expect='1A1B',
    views=[
        dict(type='string', var='secret', label='secret', cell=90, h=165, pointers={'a + sum(cnt_s.values()) - (1 if _line in (8, 10, 11) else 0)': 'blue'}, pointer_labels={'a + sum(cnt_s.values()) - (1 if _line in (8, 10, 11) else 0)': 'i'}),
        dict(type='string', var='guess', label='guess', cell=90, h=165, pointers={'a + sum(cnt_s.values()) - (1 if _line in (8, 10, 11) else 0)': 'pink'}, pointer_labels={'a + sum(cnt_s.values()) - (1 if _line in (8, 10, 11) else 0)': 'i'}),
        dict(type='map', var='cnt_s', label='cnt_s（错位时 secret 的数字）', fmt=lambda k, v: f"'{k}': {v}", h=115, font=32),
        dict(type='map', var='cnt_g', label='cnt_g（错位时 guess 的数字）', fmt=lambda k, v: f"'{k}': {v}", h=115, font=32),
        dict(type='text', h=70, size=28, fn=_res_txt),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('a', 'a', 'green'), ('b', 'b', 'orange')],
    captions={
        'a = 0': '`a` 统计公牛：数字和位置都猜对的个数',
        'cnt_s = Counter()': '`cnt_s`：位置不对时，secret 里每种数字出现几次',
        'cnt_g = Counter()': '`cnt_g`：位置不对时，guess 里每种数字出现几次',
        'for x, y in zip': '同时看当前这一位：secret 是 `{x}`，guess 是 `{y}`',
        'if x == y': '`{x}` 和 `{y}`：' + '{"==相同 → 公牛==" if x == y else "不同 → 可能是奶牛"}',
        'a += 1': '位置和数字都对，公牛 `a` = =={a}==',
        'cnt_s[x] += 1': '位置不对：secret 的 `{x}` 记一次，`cnt_s[{x!r}]` = {cnt_s[x]}',
        'cnt_g[y] += 1': '位置不对：guess 的 `{y}` 记一次，`cnt_g[{y!r}]` = {cnt_g[y]}',
        'b = (': '两个 Counter 取交集 `&`：每种数字取 `min(cnt_s, cnt_g)`，求和得奶牛 `b` = =={b}==',
        'return': '返回 `{a}A{b}B`：公牛 {a} 个，奶牛 {b} 个',
    },
    cards=dict(
        one_liner='公牛直接数；剩下的错位数字，两边各数一遍取最小值',
        complexity='时间 `O(n)`，空间 `O(|Σ|)`，这里 `|Σ| = 10`',
        problem=['secret 是秘密数字，guess 是猜测，求提示 `xAyB`',
                 '`x`（公牛）：数字和位置都对的位数',
                 '`y`（奶牛）：数字对但位置不对的位数',
                 '示例：secret = `1123`，guess = `0111` → `1A1B`'],
        quote='用两个数组（哈希表）分别统计 secret[i] ≠ guess[i] 时 secret[i] 的出现次数和 guess[i] 的出现次数，答案为 Σ min(cntS[i], cntG[i])。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先挑出位置相同的位：它们是公牛，不再参与奶牛统计',
              '剩下位置不对的数字，分别在两边计数',
              '同一种数字，能配成奶牛的对数 = ==两边次数的较小值==，即 Counter 交集'],
        summary=['时间 `O(n)`，空间 `O(10)`',
                 '易错：公牛的位置不能再算进奶牛，所以只在 `x != y` 时计数',
                 '`Counter &` 取每个键的 min；`.total()` 求所有计数之和（Python 3.10+）',
                 '另一种写法：先算 `Counter(secret) & Counter(guess)` 的总数，再减去公牛 `a`'],
    ),
)
