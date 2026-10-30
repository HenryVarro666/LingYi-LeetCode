def _txt(S):
    n, s = S['n'], S['s']
    a = S.get('ans')
    if a is None:
        return f"要填 `n = {n}` 位，数位和 `s = {s}`（最多 `9×{n} = {9*n}`）"
    return f"已填 `{len(a)}` 位：`{a}`　　还需补 `{max(0, n-len(a))}` 个 0"


CONFIG = dict(
    num=3723, title='数位平方和的最大值', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='字符串贪心 · 尽量多填 9',
    tags=['灵神题单', '难度分 1537'],
    setup='from string import digits',
    code='''
class Solution:
    def maxSumOfSquares(self, n: int, s: int) -> str:
        if n * 9 < s:
            return ""
        ans = '9' * (s // 9)
        if s % 9:
            ans += digits[s % 9]
        return ans + '0' * (n - len(ans))
''',
    call='Solution().maxSumOfSquares(4, 22)',
    expect='9940',
    views=[
        dict(type='text', fn=_txt, size=28),
        dict(type='text', fn=lambda S: (f"分数 = " + ' + '.join(f"{c}²" for c in (S['ans'] + '0' * (S['n'] - len(S['ans'])))) + f" = =={sum(int(c)**2 for c in S['ans'])}==") if 'ans' in S else '平方是凸函数：数字越不均匀，平方和越大', size=26),
        dict(type='string', var='ans', label='ans（9 越多、越靠前越好）', cell=90, h=200,
             color=lambda S, i, v: 'green' if v == '9' else ('yellow' if v != '0' else None)),
    ],
    watch=['n', 's', 'ans'],
    captions={
        'if n * 9 < s': lambda S, B, r: (f'全填 9 最多 `{S.n}×9 = {S.n*9}`，< `s = {S.s}` → 无解，返回空串' if S.n * 9 < S.s
                                        else f'全填 9 最多 `{S.n}×9 = {S.n*9}` ≥ `s = {S.s}` → 有解'),
        'return ""': '无解，返回空串',
        "ans = '9'": '`9² > 5² + 4²`，拆成 `9+0` 比 `5+4` 好 → 先填 `{s} // 9 = {s // 9}` 个 9，放在最前面保证字典序最大',
        'if s % 9': lambda S, B, r: (f'`s % 9 = {S.s % 9}` > 0：还剩一个余数要填' if S.s % 9 else '`s % 9 = 0`，没有余数'),
        'ans += digits': '再填一个余数 `{s % 9}` → `ans = {ans}`',
        'return ans': '剩下 `{n} − {len(ans)}` 位补 0 → =={ret}==',
    },
    cards=dict(
        one_liner='平方和是凸函数，数位越不均匀越大：9 尽量多、尽量靠前',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['找 `num` 位、数位和恰为 `sum` 的整数，使数位平方和最大',
                 '分数相同取数值最大的；不存在返回空串',
                 '示例：`num = 2, sum = 17` → `"98"`'],
        quote='把 9 拆分成 9+0 还是 5+4？由于 9² > 5² + 4²，拆分成 9+0 更好。一般地，由于 f(x)=x² 是凸函数，当元素分布最不均匀时，平方和最大。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先判无解：全填 9 都凑不到 `s`，返回空串',
              '凸函数 → 先填 `s // 9` 个 9；字典序要大，9 放最前面',
              '再填余数 `s % 9`，最后补 0 到 `n` 位'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '先判 `n * 9 < s`，否则会出现位数超过 `n`',
                 '`s % 9 == 0` 时不能多填一个 0，补 0 由最后一行统一处理',
                 '原代码用到 `digits`（LeetCode 预置的 `string.digits`），已在 setup 里 `from string import digits`',
                 '同类：字典序最小/最大的字符串贪心'],
    ),
)
