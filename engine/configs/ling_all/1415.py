def _bits(S):
    if 'ans' not in S or S['_line'] < 6 or 'k' not in S:
        return ''
    n, k = S['n'], S['k']
    b = format(k, '0%db' % n)
    hi = k >> (n - 1)
    rest = format(k & ((1 << (n - 1)) - 1), '0%db' % (n - 1)) if n > 1 else ''
    return f'`k` = `{k}` = 二进制 `{b}`：最高部分 `{hi}` 选第一个字母，低 {n - 1} 位 `{rest}` 依次选后面每个字母'


def _word(S):
    if 'ans' not in S:
        return ''
    cur = ''.join(chr(c) for c in S['ans'])
    return f"当前 `ans` = ==`{cur}`==（逐位确定，修正后才是最终字母）"


CONFIG = dict(
    num=1415, title='长度为 n 的开心字符串中字典序第 k 小的字符串', difficulty='Medium', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='k-1 的二进制对应每一位的选择',
    tags=['灵神核心路线', '灵神题单·位运算'],
    code='''
class Solution:
    def getHappyString(self, n: int, k: int) -> str:
        if k > 3 << (n - 1):
            return ""
        k -= 1  # 改成从 0 开始，方便计算
        ans = [ord('a')] * n
        ans[0] += k >> (n - 1)
        for i in range(1, n):
            ans[i] += k >> (n - 1 - i) & 1
            if ans[i] >= ans[i - 1]:
                ans[i] += 1
        return ''.join(map(chr, ans))
''',
    call='Solution().getHappyString(4, 13)',
    expect='bcab',
    views=[
        dict(type='text', fn=_bits, size=28),
        dict(type='array', var='ans', label='ans（字母的 ASCII 码，a=97 b=98 c=99）', cell=110, h=260,
             pointers={'i': 'blue'}),
        dict(type='text', fn=_word, size=34),
    ],
    watch=[('n', 'n', 'blue'), ('k', 'k', 'pink'), ('i', lambda S: S.get('i'), 'cyan')],
    captions={
        'if k > 3 <<': '长度为 n 的开心字符串共 `3 · 2^(n-1) = {3 << (n - 1)}` 个，`k = {k}` 不超过它 → 答案存在',
        'k -= 1': '`k` 减一，改成从 0 开始：`k = {k}` = 二进制 `{k:b}`',
        'ans = [ord': '先全部填 `a` 的编码，后面逐位往上加',
        'ans[0] +=': '第一个字母：每个首字母后面各有 `2^(n-1) = {1 << (n - 1)}` 种填法，所以首字母是 a 往后数 `k >> (n-1) = {k >> (n - 1)}` 位的字母 → `{chr(ans[0])}`',
        'for i in range': lambda S, B, ret: (f'从左到右确定第 `{S.i + 1}` 个字母' if S.i < S.n - 1 or B.get('i') != S.i else '每一位都确定了'),
        'ans[i] += k >>': '`k` 的这一位是 `{k >> (n - 1 - i) & 1}`：先填 `{"a" if k >> (n - 1 - i) & 1 == 0 else "b"}`（0 → a，1 → b）',
        'if ans[i] >=': lambda S, B, ret: (f'`{chr(S.ans[i] if False else B.ans[S.i])}` 不小于左边的 `{chr(S.ans[S.i - 1])}` → 会和左边相同或落在它前面，要加一跳过它' if B.ans[S.i] >= S.ans[S.i - 1]
                                          else f'`{chr(B.ans[S.i])}` 小于左边的 `{chr(S.ans[S.i - 1])}` → 不会相同，不用修正'),
        'ans[i] += 1': '修正：加一 → `{chr(ans[i])}`，保证和左边不同',
        'return \'\'.join': '把编码转回字母，答案是 `{ret}`',
    },
    cards=dict(
        one_liner='开心字符串的选择恰好对应 k-1 的二进制位，一位一位读出来',
        complexity='时间 `O(n)`，空间 `O(1)`（不计返回值）',
        problem=['仅含 `a b c`、==相邻字母不同==的字符串叫开心字符串',
                 '把长为 `n` 的所有开心字符串按字典序排序，返回第 `k` 个，不足 `k` 个返回空串',
                 '本视频：`n = 4, k = 13` → `"bcab"`'],
        quote='由于每个位置都有两种填法，这和 k 的二进制可以完美对应。看填入的字母是否大于等于左侧相邻字母，如果大于等于，那么把填入的字母加一。',
        quote_src='—— 灵茶山艾府题解',
        idea=['总数 `3 · 2^(n-1)`：首位 3 种，之后每位 2 种；超过就返回空串',
              '`k` 先减一从 0 开始：高位决定首字母，低 `n-1` 位每位选「两个可选字母里的小/大」',
              '先填 a 或 b，若 ==不小于左边== 就加一，跳过和左边相同的字母'],
        result='返回 "bcab"，和 k = 13 对应 ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`k` 要先减一；位运算 `k >> (n-1-i) & 1` 取从高到低第 i 位',
                 '「加一」技巧：从剩下的两个字母里选，不用 if 分情况',
                 '同类题：60. 排列序列（康托展开）'],
    ),
)
