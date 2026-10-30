CONFIG = dict(
    num=2269, title='找到一个数字的 K 美丽值', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='滑动窗口 · 逐位滚动子串的值',
    tags=[],
    code='''
class Solution(object):
    def divisorSubstrings(self, num, k):

        digits = list(str(num))
        res = 0

        now = 0
        for digit in digits[:k]:
            now = now * 10 + int(digit)

        if now > 0 and num % now == 0:
            res += 1
        
        mod = 10 ** k
        for digit in digits[k:]:
            now = (now * 10 + int(digit)) % mod
            if now > 0 and num % now == 0:
                res += 1

        return res
''',
    call='Solution().divisorSubstrings(12036, 2)',
    expect=2,
    views=[
        dict(type='array', var='digits', label='digits（黄框 = 当前窗口，蓝箭头 = 刚读入的数位）', cell=90,
             window=('max(0, digits.index(digit) - k + 1)', 'digits.index(digit)'), pointers={'digits.index(digit)': 'blue'}, pointer_labels={'digits.index(digit)': 'digit'},
             dim=lambda S, i, v: 'digit' in S and i > S['digits'].index(S['digit']), h=230),
        dict(type='text', fn=lambda S: (f"窗口的值 `now = {S['now']}`；`num % now` = {S['num'] % S['now'] if S['now'] else '—'}") if 'now' in S and S['now'] is not None else '', size=28, h=70),
    ],
    watch=[('now', 'now', 'yellow'), ('mod', 'mod', 'blue'), ('res', 'res', 'green')],
    captions={
        'digits = list': '把 `num` 拆成数位列表 `digits = {digits}`',
        'res = 0': '`res` 统计答案',
        'now = 0': '`now` 保存当前长为 `k` 的子串对应的数',
        'for digit in digits[:k]': lambda S, B, r: ('前 `k` 位读完了' if B.get('digit') == S.digit else f'读入数位 `{S.digit}`'),
        'for digit in digits[k:]': lambda S, B, r: ('所有数位都滑过了，窗口走到了最右边' if B.get('digit') == S.digit else f'读入下一个数位 `{S.digit}`，窗口右移一格'),
        'now = now * 10 + int(digit)': '先读入前 `k` 位：`now` → {now}',
        'if now > 0 and num % now == 0': lambda S, B, r: (
            '`now = 0`：0 不能整除任何数 → 不计数' if S.now == 0
            else '`num % now = {0} % {1} = {2}` → {3}'.format(S.num, S.now, S.num % S.now, '==整除，计一个==' if S.num % S.now == 0 else '不能整除')),
        'res += 1': '`res` → {res}',
        'mod = 10 ** k': '`mod = 10^k = {mod}`：用它去掉窗口最左边的一位',
        'now = (now * 10 + int(digit)) % mod': lambda S, B, r: '窗口右移：`({0} × 10 + {1}) % {2}` = =={3}==（左边一位被 `% mod` 丢掉）'.format(B.now, S.digit, S.mod, S.now),
        'return res': '所有窗口检查完，返回 `{res}`',
    },
    cards=dict(
        one_liner='窗口大小固定为 k：新数位进来、最高位用取模挤出去',
        complexity='时间 `O(n)`，空间 `O(n)`（`n` 为位数）',
        problem=['`num` 的 ==k 美丽值==：`num` 中长为 `k`、且能整除 `num` 的子串个数',
                 '子串允许前导 0；`0` 不能整除任何数',
                 '示例：`num = 12036`，`k = 2` → `2`（`12` 和 `03` 能整除）'],
        quote='由于num的长度有限，那么完全可以从左向右一趟遍历，枚举num所有长为k的子串，然后判断num是否为这个子串的倍数并更新答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把前 `k` 位拼成数 `now`，判断一次',
              '之后每读入一位：`now = (now * 10 + digit) % 10^k`，==旧的最高位被取模挤出==',
              '每次得到新窗口的值，都判断 `now > 0 and num % now == 0`'],
        summary=['时间 `O(n)`，空间 `O(n)`；`n` 是位数',
                 '易错：第一个窗口（前 `k` 位）要单独判断一次，后面的循环从 `digits[k:]` 开始',
                 '易错：`now = 0` 时先判 `now > 0`，避免除以 0',
                 '原文为 Python 2 风格，代码无需改动，直接运行'],
    ),
)
