CONFIG = dict(
    num=1897, title='重新分配字符使所有字符串都相等', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='统计字母个数 · 是否都是 n 的倍数（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def makeEqual(self, a: List[str]) -> bool:
        c = [0] * 26
        for s in a:
            for b in s:
                c[ord(b) - ord('a')] += 1
        for v in c:
            if v % len(a) > 0:
                return False
        return True
''',
    call='Solution().makeEqual(["abc","aabc","bc"])',
    expect=True,
    views=[
        dict(type='array', var='a', h=190, label='a（words）', cell=100,
             color=lambda S, i, v: 'blue' if S.get('s') is not None and S.get('v') is None and v == S['s'] and i == _idx(S) else None),
        dict(type='map', var=lambda S: {chr(97 + i): n for i, n in enumerate(S['c']) if n}, h=250, label='c：各字母出现次数（只画出现过的）',
             fmt=lambda k, v: f'{k}:{v}'),
        dict(type='text', size=32, h=90, fn=lambda S: (
            f"字符串个数 `len(a) = {len(S['a'])}`" + (f"；当前统计 `{S['b']}` → c[{ord(S['b']) - 97}]" if S.get('b') and S.get('v') is None else '')
            + (f"；检查第 {S['v']} 个计数" if S.get('v') is not None and 'b' in S else ''))),
    ],
    watch=[('s', 's', 'blue'), ('b', 'b', 'cyan'), ('v', 'v', 'yellow')],
    skip=['for v in c'],
    captions={
        'c = [0] * 26': '26 个计数器，`c[0]` 数 `a`，`c[1]` 数 `b` ……',
        'c[ord(b)': '字母 `{b}` 出现次数 +1：`c[{ord(b) - ord("a")}]` = =={c[ord(b) - ord("a")]}==（不管它在哪个字符串里）',
        'if v % len(a) > 0': lambda S, B, r: (
            f'这个字母共 `{S.v}` 个，`{S.v} % {len(S.a)} = {S.v % len(S.a)}` > 0 → ==不能平均分，返回 False=='
            if S.v % len(S.a) > 0 else (f'`{S.v} % {len(S.a)} = 0`，能平均分' if S.v else '`0 % n = 0`，没出现的字母不用管')),
        'return False': '有字母分不匀，不可能让每个字符串都相等 → `False`',
        'return True': '每个字母的个数都是 `{len(a)}` 的倍数 → 可以均分 → ==True==',
    },
    cards=dict(
        one_liner='字符可以随便搬，只要每个字母的总数都能被 n 整除',
        complexity='时间 `O(L)`，空间 `O(1)`（L 为字符总数，26 个计数器）',
        problem=['每步可以把某个字符串里的任意一个字符，挪到另一个字符串的任意位置',
                 '问能否让 `words` 里所有字符串都相等',
                 '示例：`["abc","aabc","bc"]` → `true`'],
        quote='func makeEqual(a []string) bool { c := [26]int{} ... if v%len(a) > 0 { return false } ... }',
        quote_src='—— 灵茶山艾府题解代码（原文为 Go）',
        idea=['搬字符不改变每个字母的总数，也不限制每个字符串的位置',
              '最后 `n` 个字符串一模一样 → 每个字母的总数必须是 `n` 的倍数',
              '反过来，是倍数就能平均分给每个字符串，所以只数 26 个字母'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python：Go 的 `b - \'a\'` 对应 `ord(b) - ord(\'a\')`',
                 '时间 `O(L)`，空间 `O(26)`',
                 '易错点：除数是字符串个数 `len(a)`，不是字符串长度',
                 '没出现的字母 `0 % n = 0`，不影响结论'],
    ),
)


def _idx(S):
    try:
        return S['a'].index(S['s'])
    except Exception:
        return -1
