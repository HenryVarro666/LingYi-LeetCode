MOD = 10 ** 9 + 7


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n = S.get('n', 4)
    rows = [
        ('26^n', '全部字符串', pow(26, n, MOD), T['blue'], '+'),
        ('(75+n)·25^(n-1)', '至少满足 1 个条件（不含 l / 不含 t / e 少于 2 个）', pow(25, n - 1, MOD) * (75 + n), T['pink'], '−'),
        ('(72+2n)·24^(n-1)', '至少满足 2 个条件', pow(24, n - 1, MOD) * (72 + n * 2), T['orange'], '+'),
        ('(23+n)·23^(n-1)', '满足 3 个条件', pow(23, n - 1, MOD) * (23 + n), T['purple'], '−'),
    ]
    cv.text((x0 + 18, y0 + 4), f'容斥原理，n = {n}：好字符串 = 全部 − 不含 leet 的', 24, T['muted'], bold=True)
    cv.text((x0 + 18, y0 + 44), '不含 leet ＝ 三个条件至少满足一个：①不含 l  ②不含 t  ③e 的个数 ≤ 1', 22, T['text'])
    y = y0 + 100
    ln = S.get('_line', 99)
    cnt = 0
    for k, (f, d, v, c, sg) in enumerate(rows):
        if ln < 4 + k:
            break
        cnt += 1
        cv.rect((x0 + 18, y, x1 - 18, y + 78), fill=T['panel2'] if 'panel2' in T else (30, 36, 46), r=10, outline=c, width=2)
        cv.text((x0 + 36, y + 10), f'{sg}  {f}', 28, c, bold=True, mono=True)
        cv.text((x0 + 36, y + 46), d, 20, T['muted'])
        cv.text((x1 - 36, y + 39), v, 30, T['text'], anchor='rm', bold=True, mono=True)
        y += 92
    if cnt < 4:
        return
    tot = (rows[0][2] - rows[1][2] + rows[2][2] - rows[3][2])
    cv.text((x0 + 18, y + 12), f'= {tot}   →   取模 {tot % MOD}', 30, T['green'], bold=True, mono=True)


CONFIG = dict(
    num=2930, title='重新排列后包含指定子字符串的字符串数目', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='正难则反 · 容斥原理',
    tags=['灵神题单', '动态规划', '难度分 2227'],
    code='''
class Solution:
    def stringCount(self, n: int) -> int:
        MOD = 10 ** 9 + 7
        return (pow(26, n, MOD)
              - pow(25, n - 1, MOD) * (75 + n)
              + pow(24, n - 1, MOD) * (72 + n * 2)
              - pow(23, n - 1, MOD) * (23 + n)) % MOD
''',
    call='Solution().stringCount(4)',
    expect=12,
    views=[dict(type='custom', draw=_draw, h=520)],
    watch=[('n', 'n', 'blue'), ('MOD', 'MOD', 'muted')],
    captions={
        'MOD = ': '答案要对 `10^9+7` 取模，先记下 `MOD`',
        'return (pow(26': '容斥从「全部字符串」开始：每个位置 26 种字母，`26^n` = =={pow(26, n, MOD)}==，再逐项加减、累计',
        '- pow(25': '减去「至少满足 1 个条件」：不含 l、不含 t、e 少于 2 个，共 `(75+n)·25^(n-1)` = =={pow(25, n - 1, MOD) * (75 + n)}==',
        '+ pow(24': '这样「同时满足 2 个条件」的被多减了，加回来：`(72+2n)·24^(n-1)` = =={pow(24, n - 1, MOD) * (72 + n * 2)}==',
        '- pow(23': '「同时满足 3 个条件」又被多加了，再减去：`(23+n)·23^(n-1)` = =={pow(23, n - 1, MOD) * (23 + n)}==，最后 `% MOD`',
    },
    cards=dict(
        one_liner='正难则反：总数减去「不含 leet」，用容斥原理',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['只含小写字母的字符串，重新排列后能包含子串 `"leet"` 就是好字符串',
                 '求长度为 `n` 的好字符串个数，对 `10^9+7` 取模',
                 '示例：`n = 4` → `12`'],
        quote='正难则反。总共有 26^n 个字符串，减去不含 leet 的字符串个数，就得到了答案。不含 leet 的字符串，需要至少满足如下三个条件中的一个：1. 不含 l。2. 不含 t。3. 不含 e 或者恰好包含一个 e。',
        quote_src='—— 灵茶山艾府题解',
        idea=['「不含 leet」= 不含 `l`、不含 `t`、`e` 少于 2 个 三者至少一个成立',
              '容斥：加上满足 1 个的，减去满足 2 个的，再加上满足 3 个的',
              '每项都是「某些字母不能用」× 「恰好 1 个 e 的位置」，用快速幂 `pow(x, n, MOD)` 计算'],
        before=[dict(heading='各项怎么数', lines=['不含 `l`：每格 25 种，`25^n`；不含 `t` 同理',
                                               '`e` 不足 2 个：`25^n + n·25^(n-1)`（0 个或选 1 个位置放 e）',
                                               '两个条件：多禁一个字母，底数变 24；三个条件：底数 23'])],
        after=[dict(heading='附：记忆化搜索', lines=['也可以看成「至少装满型」分组背包：`dfs(i, L, t, e)`',
                                                  '每位选 l / t / e / 其它 23 个字母，目标至少 1 个 l、1 个 t、2 个 e，时间 `O(n)`'])],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '容斥符号：+ 全部，− 一个条件，+ 两个条件，− 三个条件',
                 '`pow(x, n, MOD)` 内置快速幂；最后统一 `% MOD`，Python 负数取模自动变非负',
                 '同类：容斥原理 + 乘法原理的计数题'],
    ),
)
