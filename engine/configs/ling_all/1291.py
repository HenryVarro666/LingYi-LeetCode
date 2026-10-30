D = '123456789'


def _win(S, k):
    x = S.get('x')
    if x is None:
        return None
    s = D.find(str(x))
    if s < 0:
        return None
    return s if k == 0 else s + len(str(x)) - 1


def _col(S, i, v):
    a = _win(S, 0)
    if a is None:
        return None
    b = _win(S, 1)
    if a <= i <= b:
        if S['x'] > S['high']:
            return 'red'
        return 'green' if S['x'] >= S['low'] else 'yellow'
    return None


def _text(S):
    if 'x' not in S:
        return '顺次数 = ==123456789 的子串==；定长窗口右移，一步算出下一个数'
    x, low, high = S['x'], S['low'], S['high']
    if D.find(str(x)) < 0:
        return f'窗口滑出了 `123456789`，这一轮结束'
    if x > high:
        return f'`{x}` > high={high}：太大了，后面的更大 → 直接返回'
    if x >= low:
        return f'`{x}` 在 [{low}, {high}] 内 → 收下'
    return f'`{x}` < low={low}：太小，不收，继续滑动'


CONFIG = dict(
    num=1291, title='顺次数', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='数字滑窗（123456789 的子串）',
    code='''
class Solution:
    def sequentialDigits(self, low: int, high: int) -> List[int]:
        ans = []
        x0 = 12  # 第一个窗口
        pow10 = 10
        length = 2  # 窗口长度，同时也是第一个窗口的个位数字
        while x0 <= high:
            pow10 *= 10
            x = x0
            for i in range(length, 10):
                if x > high:
                    return ans
                if x >= low:
                    ans.append(x)
                # 窗口向右滑动，i+1 进入窗口，i+1-length 离开窗口
                x = x * 10 + i + 1 - (i + 1 - length) * pow10
            length += 1
            x0 = x0 * 10 + length
        return ans
''',
    call='Solution().sequentialDigits(100, 300)',
    expect=[123, 234],
    views=[
        dict(type='text', fn=_text, h=80),
        dict(type='string', var=lambda S: D, window=(lambda S: _win(S, 0), lambda S: _win(S, 1)),
             color=_col, label='123456789（窗口 = 当前顺次数）', h=250),
        dict(type='array', var='ans', label='ans', h=200),
    ],
    watch=['length', 'x0', 'x', 'pow10', ('ans', 'ans', 'green')],
    captions={
        'ans = []': '`ans` 收集答案；窗口从小到大滑，答案天然有序',
        'x0 = 12': '`x0 = 12`：长度为 2 的第一个窗口，即 `12`',
        'pow10 = 10': '`pow10` 先设成 10，每轮长度变大时再乘 10',
        'length = 2': '`length = 2`：窗口长度，也等于第一个窗口末位数字',
        'while x0 <= high': '`x0 = {x0}`：这个长度的第一个顺次数 {"≤" if x0 <= high else ">"} `high = {high}`' + '{"，这一长度还可能有解" if x0 <= high else "，更长的更大，结束"}',
        'pow10 *= 10': '`pow10 = {pow10}` = 10^{length}，用来去掉窗口最高位',
        'x = x0': '从这个长度的第一个窗口 `{x0}` 开始往右滑',
        'for i in range': lambda S, B, r: ('长度 `{}` 的窗口已滑完'.format(S.length) if ('i' in B and B.i == S.i == 9) else f'`i = {S.i}`：窗口末位数字是 `{S.i}`'),
        'if x > high': '`x = {x}` {"大于" if x > high else "不大于"} `high = {high}`' + '{" → 后面窗口只会更大，直接返回" if x > high else ""}',
        'if x >= low': '`x = {x}` {"≥" if x >= low else "<"} `low = {low}`' + '{" → 在范围内" if x >= low else " → 太小，不收"}',
        'ans.append': '`{x}` 是合法顺次数，加入答案 → `ans = {ans}`',
        'x = x * 10': lambda S, B, r: (f'`i = 9` 已是最后一个窗口，再滑出的 `{S.x}` 不是顺次数（越过了 9），下一轮会丢掉' if S.i == 9 else f'滑窗：`x*10` 左移一位，`+ (i+1)` 新数字进来，减去最高位 `{S.i+1-S.length} × pow10` → `{S.x}`'),
        'xx_unused': '滑窗：`x*10` 左移一位，`+ (i+1)` 新数字进来，减去最高位 `{i+1-length} × pow10` → `{x}`',
        'length += 1': '这一长度滑完，窗口变长：`length = {length}`',
        'x0 = x0 * 10': '新长度的第一个窗口：`x0 = {x0}`（在末尾接上 `{length}`）',
        'return ans': '返回 `{ans}`',
    },
    cards=dict(
        one_liner='顺次数就是 123456789 的子串，定长窗口一步算下一个',
        complexity='时间 `O(log² high)`，空间 `O(1)`',
        problem=['顺次数：每一位都比前一位大 `1` 的整数',
                 '返回 `[low, high]` 内所有顺次数，从小到大',
                 '示例：`low=100, high=300` → `[123,234]`'],
        quote='顺次数的十进制表示是 123456789 的子串。枚举 123456789 的子串，如果其数值 x 在 [low,high] 中，则把 x 加入答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['合法的数只有 36 个：`123456789` 的所有长度 ≥ 2 的子串',
              '先枚举长度 `length`，再把窗口从左往右滑，天然有序，无需排序',
              '滑动一步 `O(1)`：乘 10、加新数字、减去离开窗口的最高位'],
        summary=['时间 `O(log² high)`，空间 `O(1)`',
                 '`pow10` 要随 `length` 增长，减去的是 `(i+1-length) × 10^length`',
                 '一旦 `x > high` 就能直接 `return`，因为后面的窗口更大',
                 '题解还有写法一（枚举最高位，末尾补数，最后排序）和写法二（枚举长度和位置，用 `int(DIGITS[l:r])`）'],
    ),
)
