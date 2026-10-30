NUM, T = '129', 24


def _txt(S):
    if 'cnt' not in S:
        return f'目标：`≥ {NUM}` 的最小无零数，数位乘积是 `t = {T}` 的倍数'
    cnt = S['cnt']
    need = ' × '.join(f'{p}^{e}' for p, e in zip((2, 3, 5, 7), cnt) if e > 0) or '1'
    if 'p' not in S:
        return f'还需要凑出的因子（`cnt`）：`{need}`'
    p = S['p']
    return f'前 `{p}` 位不动，试着改第 `{p}` 位；还需要凑出的因子：`{need}`'


def _mi_txt(S):
    mi = S.get('mi')
    if mi is None:
        return ''
    mi = ''.join(mi) if isinstance(mi, list) else mi
    if 'p' in S and 'v' in S and S.get('_line', 0) >= 69:
        return f"改成 `num[{S['p']}] = {S['v']}` 后，后缀要凑出 `mi = {mi!r}`，后缀一共 `{len(S['num']) - S['p'] - 1}` 位"
    return f"最小凑法 `mi = {mi!r}`"


def _col(S, i, v):
    if 'p' in S and i == S['p']:
        return 'blue'
    return None


CONFIG = dict(
    num=3348, title='最小可整除数位乘积 II', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='质因子计数 + 构造最小后缀，从后往前改位',
    tags=['灵神题单·动态规划', '灵神题单·贪心与思维', '难度分 3101'],
    code='''
class Solution(object):
    def smallestNumber(self, num, t):

        def update(v, cnt, delta):
            if v == 0:
                return v
            for index, x in enumerate([2, 3, 5, 7]):
                while v % x == 0:
                    cnt[index] += delta
                    v //= x
            return v

        cnt = [0] * 4
        t = update(t, cnt, 1)
        if t > 1:
            return "-1"

        def generate():
            if max(cnt) <= 0:
                return ''
            tmp = [max(0, x) for x in cnt]
            nine = ['9'] * (tmp[1] // 2)
            eight = ['8'] * (tmp[0] // 3)
            seven = ['7'] * tmp[3]
            five = ['5'] * tmp[2]

            mi = []

            if tmp[0] % 3 == 0:
                if tmp[1] % 2 == 0:
                    mi = five + seven + eight + nine
                else:
                    mi = ['3'] + five + seven + eight + nine
            elif tmp[0] % 3 == 1:
                if tmp[1] % 2 == 0:
                    mi = ['2'] + five + seven + eight + nine
                else:
                    mi = five + ['6'] + seven + eight + nine
            elif tmp[0] % 3 == 2:
                if tmp[1] % 2 == 0:
                    mi = ['4'] + five + seven + eight + nine
                else:
                    mi = ['2'] + five + ['6'] + seven + eight + nine
            
            return ''.join(mi)

        mi = generate()
        if len(mi) > len(num):
            return mi

        res = '1' * (len(num) - len(mi) + 1) + mi

        start = None
        for p, c in enumerate(num):
            if c == '0':
                start = p
                break
            update(int(c), cnt, -1)

        if start is None:
            if max(cnt) <= 0:
                return num
            start = len(num) - 1

        for p in range(start, -1, -1):
            update(int(num[p]), cnt, 1)

            for v in range(int(num[p]) + 1, 10):
                update(v, cnt, -1)
                
                mi = generate()
                if len(mi) <= len(num) - p - 1:
                    return num[:p] + str(v) + '1' * (len(num) - p - 1 - len(mi)) + mi
                
                update(v, cnt, 1)
        
        return res
''',
    call=f'Solution().smallestNumber({NUM!r}, {T})',
    expect='138',
    views=[
        dict(type='text', fn=_txt, size=24, h=80),
        dict(type='string', var=lambda S: S['num'] if 'num' in S else NUM, label='num（蓝 = 当前尝试修改的位 p）', cell=100,
             pointers={'p': 'blue'}, color=_col, h=210),
        dict(type='table', var=lambda S: [S['cnt']] if 'cnt' in S else [[0, 0, 0, 0]], label='cnt：还需要的质因子个数（负数 = 已经多余）',
             rows=['个数'], cols=['2', '3', '5', '7'], cell=100, h=180),
        dict(type='text', fn=_mi_txt, size=26, h=80),
    ],
    watch=['t', 'p', 'v', ('mi', 'mi', 'yellow'), ('res', 'res', 'green')],
    skip=['if v == 0', 'for index, x in enumerate', 'while v % x == 0', 'cnt[index] += delta', 'v //= x', 'cnt = [0] * 4',
          'if max(cnt) <= 0:', "return ''", 'tmp = [max', 'nine = ', 'eight = ', 'seven = ', 'five = ', 'mi = []', 'if tmp[0] % 3 == 0',
          'elif tmp[0] % 3 == 1', 'elif tmp[0] % 3 == 2', 'if tmp[1] % 2 == 0', 'else:', "for p, c in enumerate(num)", "if c == '0'",
          'start = None', 'if start is None', 'for v in range',
          't = update(t, cnt, 1)', 'update(int(c), cnt, -1)', 'update(int(num[p]), cnt, 1)', 'update(v, cnt, -1)', 'update(v, cnt, 1)',
          'mi = generate()'],
    captions={
        'return v': lambda S, B, r: (f'`update`：{"把质因子个数加进" if S.delta > 0 else "用这个数的质因子抵消"} `cnt`，现在 `cnt = {S.cnt}`'
                                     '（正数 = 还缺，负数 = 已经多余）'),
        'if t > 1': '`t` 剩下 `{t}`，说明 `t` 只含质因子 2、3、5、7 → 答案存在；各质因子个数 `cnt = {cnt}`',
        "mi = five + seven + eight + nine": '没有落单的 2 和 3：5、7、8、9 直接拼起来',
        "['3'] + five + seven + eight + nine": '2 的个数是 3 的倍数、3 剩一个：落单的 `3` 放到最前面，后面是 5、7、8、9',
        "['2'] + five + seven + eight + nine": '落单一个 2、3 成对：`2` 放最前面，后面是 5、7、8、9',
        "five + ['6'] + seven + eight + nine": '落单一个 2 和一个 3：合成 `6`，放在 5 的后面',
        "['4'] + five + seven + eight + nine": '落单两个 2：合成 `4` 放最前面',
        "['2'] + five + ['6'] + seven + eight + nine": '落单两个 2 和一个 3：先合成 `6`，剩下的 `2` 放最前面',
        "return ''.join(mi)": '`generate()` 返回最小凑法 `{ret!r}`：2、3 尽量先合成 8、9，余下的小数放在最前面',
        'if len(mi) > len(num)': lambda S, B, r: (f'最小凑法 `{S.mi!r}` 比 `num` 还长 → 它就是答案' if len(S.mi) > len(S.num)
                                                  else f'`len(mi) = {len(S.mi)}` 不超过 `len(num) = {len(S.num)}`：先用“左边补 1”构造一个备选'),
        "res = '1' *": '备选解 `res = "1" × ({len(num)} − {len(mi)} + 1) + mi` = `{res}`：比 `num` 长一位，肯定合法',
        'start = len(num) - 1': '`num` 自己还不满足（`cnt` 还有正数）→ 从最后一位开始往前改',
        'for p in range(start': lambda S, B, r: (f'试着修改第 `p = {S.p}` 位：改得越靠后，答案越小；先把 `num[{S.p}]` 对 `cnt` 的抵消还回去' +
                                                 ('。这一位是 `9`，没法再增大，直接往前' if S.num[S.p] == '9' else '')),
        'if len(mi) <= len(num) - p - 1': lambda S, B, r: (f'`mi = {S.mi!r}` 长 `{len(S.mi)}`，后缀只有 `{len(S.num) - S.p - 1}` 位：' +
                                                           ('放得下 → 找到答案' if len(S.mi) <= len(S.num) - S.p - 1 else '放不下 → 这个 `v` 不行，换更大的')),
        'return num[:p]': '`num[:{p}]` 不动 + 这一位 `{v}` + 补 `1` + `mi` = =={ret}==',
        'return num': '`num` 自己就满足 → 直接返回',
        'return res': '没有改法 → 返回备选解 `{res}`',
    },
    cards=dict(
        one_liner='先造“最小凑法”，再从后往前改位，让后缀去凑剩下的因子',
        complexity='时间 `O(n + 10 log t)` 量级，空间 `O(n)`',
        problem=['给定正整数字符串 `num` 和整数 `t`，找 `≥ num` 的==最小无零整数==（不含数字 0）',
                 '要求各数位乘积能被 `t` 整除；找不到返回 `"-1"`',
                 '示例：`num = "1234", t = 256` → `"1488"`；视频用 `num = "129", t = 24` → `"138"`'],
        quote='为了使得构造出来的整数最小，因此修改的位置应该尽量靠后，尽量保持 num 的高位不变。……从 num 的最后一个数位开始，从后往前尝试修改。',
        quote_src='—— yiduobo 题解',
        idea=['`t` 分解成 `2^a·3^b·5^c·7^d`，别的质因子就无解；`cnt` 记还缺多少',
              '`generate()`：尽量把 2、3 合成 8 和 9（数位少、剩余小），5、7 照数放，剩下的小数放最前',
              '从后往前改位：改成更大的 `v` 后，剩下的因子交给 `generate()`，放得进后缀就是答案；全不行就用“补 1”的备选解'],
        summary=['时间约 `O(n + 10 log t)`，空间 `O(n)`',
                 '原文为 Python 2 风格写法，本代码已是 Python 3 可运行，无需改动',
                 '`num` 中有 `0` 必须改，所以从最左边的 `0` 开始往前改',
                 '易错：改位后要把旧位的质因子还给 `cnt`，试下一个 `v` 前也要还',
                 '组合规则：先做 8、9，余下 2/3 按 6、4、2、3 的规则放在 5 的前后'],
    ),
)
