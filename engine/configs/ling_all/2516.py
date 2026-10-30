def _wl(S):
    if 'right' not in S or S['left'] > S['right']:
        return None
    return S['left']


def _wr(S):
    if 'right' not in S or S['left'] > S['right']:
        return None
    return S['right']


def _txt(S):
    if 'cnt' not in S:
        return ''
    c = S['cnt']
    k = S['k']
    parts = [f"{ch}: 窗口外 {c[ch]}" + ('' if c[ch] >= k else '（不足）') for ch in 'abc']
    return f"取走的个数（需要每种 >= `{k}`）：" + '，'.join(parts)


CONFIG = dict(
    num=2516, title='每种字符至少取 K 个', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='逆向思考 · 最长窗口 = 不取的部分',
    tags=['滑动窗口与双指针', '难度分 1948'],
    code='''
class Solution:
    def takeCharacters(self, s: str, k: int) -> int:
        cnt = Counter(s)  # 一开始，把所有字母都取走
        if any(cnt[c] < k for c in "abc"):
            return -1  # 字母个数不足 k

        mx = left = 0
        for right, c in enumerate(s):
            cnt[c] -= 1  # 移入窗口，相当于不取走 c
            while cnt[c] < k:  # 窗口之外的 c 不足 k
                cnt[s[left]] += 1  # 移出窗口，相当于取走 s[left]
                left += 1
            mx = max(mx, right - left + 1)
        return len(s) - mx
''',
    call="Solution().takeCharacters('aabbcabca', 2)",
    expect=6,
    views=[
        dict(type='string', var='s', label='s（框 = 窗口 = 不取走的中间部分）', pointers={'left': 'pink', 'right': 'blue'},
             window=(_wl, _wr), h=230, cell=90),
        dict(type='map', var='cnt', label='cnt：窗口之外（= 取走的）各字母个数', fmt=lambda k, v: f"'{k}': {v}", h=130, font=32),
        dict(type='text', h=90, size=28, fn=_txt),
    ],
    watch=[('right', 'right', 'blue'), ('left', 'left', 'pink'), ('mx', 'mx', 'green')],
    captions={
        'cnt = Counter': '先假设==全部取走==：`cnt` 就是每个字母在 `s` 里的总数 `{dict(cnt)}`',
        'if any(': '检查每个字母总数是否都 `>= k = {k}`：{"有字母不足" if any(cnt[c] < k for c in "abc") else "都够取"}',
        'return -1': '某个字母总数不足 `k`，怎么取都不行 → `-1`',
        'mx = left = 0': '`mx` 记最长的“可以留下不取”的子串长度',
        'cnt[c] -= 1': '`s[{right}] = {c}` 进窗口 = 不取它：窗口外 `{c}` 变成 `{cnt[c]}`',
        'while cnt[c] < k': '窗口外 `{c}` 剩 `{cnt[c]}` 个，需要 `{k}` 个：{"不够 → 必须缩小窗口，把左边的字母取走" if cnt[c] < k else "够了，窗口合法"}',
        'cnt[s[left]] += 1': '`s[{left}] = {s[left]}` 移出窗口 = 取走它：窗口外 `{s[left]}` 变成 `{cnt[s[left]]}`',
        'left += 1': '左端点右移：`left` → {left}',
        'mx = max': '{"窗口缩空了（长度 0）" if left > right else "窗口 `[" + str(left) + ", " + str(right) + "]` 合法"}，长度 `{right - left + 1}`，`mx = max({B.mx}, {right - left + 1}) = {mx}`',
        'return len(s) - mx': '总长 `{len(s)}` − 最长可留下 `{mx}` = ==最少取 {len(s) - mx} 个==',
    },
    max_steps=110,
    cards=dict(
        one_liner='正难则反：取走两端 = 留下中间，让留下的最长',
        complexity='时间 `O(n + |Σ|)`，空间 `O(|Σ|)`',
        problem=['字符串 `s` 只含 `a b c`，每次只能取走最左或最右的字符',
                 '每种字符至少取 `k` 个，求最少取几个；取不够返回 `-1`',
                 '本视频：`s="aabbcabca"`，`k=2` → `6`'],
        quote='每种字母至少取走 k 个，等价于剩下的字母至多有 x−k、y−k、z−k 个……剩下的字母是 s 的子串，所以求最长的满足条件的子串。',
        quote_src='—— 灵茶山艾府题解（节选）',
        idea=['取走的是两端，剩下的就是连续的一段子串，要它==尽量长==',
              '技巧：`cnt` 直接维护窗口==之外==的字母个数，也就是取走的个数',
              '右端点进窗口：窗口外该字母少 1；少于 `k` 就缩左端点把字母“取回来”'],
        summary=['时间 `O(n + |Σ|)`，空间 `O(|Σ|)`，内层循环总共最多移动 `n` 次',
                 '先判断总数不足 `k` 的情况直接 `-1`，否则 `while` 会一直右移 `left` 直到越界',
                 '答案是 `len(s) - mx`，不是 `mx`',
                 '`k = 0` 时窗口可以是整个字符串，答案为 0'],
    ),
)
