def _txt(S):
    L = S['_line']
    d = S.get('d')
    if L < 11 or d is None:
        return '先统计：数字种类、非零种类、恰好出现一次的非零数字'
    t = f'个位填 `{d}`'
    if L >= 16:
        t += f'：十位 `{S["k"]}` 种'
    if L >= 19:
        t += f' × 百位 `{S["nz"]}` 种'
    if L >= 22:
        t += f' − 撞同一个单个数字 `{S["s"]}` 种'
    if L >= 29:
        t += f' = =={S["k"] * S["nz"] - S["s"]}=='
    return t


CONFIG = dict(
    num=3483, title='不同三位偶数的数目', difficulty='Easy', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='枚举个位 + 乘法原理（组合数学）',
    tags=['灵神核心路线', '灵神题单·数学算法', '难度分 2094'],
    code='''
class Solution:
    def totalNumbers(self, digits: List[int]) -> int:
        cnt = Counter(digits)

        kinds = len(cnt)
        non_zeros = kinds - (0 in cnt)
        singles = sum(c == 1 for c in cnt.values()) - (cnt.get(0, 0) == 1)
        ans = 0

        # 枚举个位填偶数 d
        for d, c in cnt.items():
            if d % 2 > 0:
                continue

            # 十位填任意数字
            k = kinds - (c == 1)

            # 百位填任意非零数字
            nz = non_zeros - (d > 0 and c == 1)

            # 恰好出现一次的非零数字，不能同时填入十位和百位
            s = singles
            if d > 0:
                if c == 1:
                    s -= 1
                elif c == 2:
                    s += 1

            ans += k * nz - s

        return ans
''',
    call='Solution().totalNumbers([0, 2, 2, 3, 4])',
    expect=21,
    views=[
        dict(type='map', var='cnt', label='cnt：数字 → 个数', h=170,
             fmt=lambda k, v: f'{k}: {v}'),
        dict(type='text', fn=lambda S: _txt(S), size=30),
    ],
    watch=[('kinds', 'kinds', 'blue'), ('non_zeros', 'non_zeros', 'cyan'), ('singles', 'singles', 'orange'),
           ('d', lambda S: S.get('d'), 'pink'), ('ans', 'ans', 'green')],
    captions={
        'cnt = Counter': '先数一遍：`cnt` = {cnt}',
        'kinds = len': '`kinds` = 数字种类数 = `{kinds}`',
        'non_zeros =': '`non_zeros` = 非零数字的种类 = `{kinds}` − {int(0 in cnt)} = `{non_zeros}`',
        'singles =': '`singles` = 恰好出现一次的非零数字的种类 = `{singles}`',
        'if d % 2 > 0': lambda S, B, ret: (f'`{S.d}` 是奇数，不能当个位 → continue' if S.d % 2 else f'`{S.d}` 是偶数，可以当个位'),
        'k = kinds': '个位用掉一个 `{d}`；若它只有 1 个，十位就少一种可选：`k = {kinds} − {int(c == 1)} = {k}`',
        'nz = non_zeros': '百位要非零；若个位用掉的是唯一一个非零数字，百位少一种：`nz = {non_zeros} − {int(d > 0 and c == 1)} = {nz}`',
        's = singles': '`s` 先取全局的 `singles = {singles}`：这些数十位百位不能同时用',
        'if d > 0': lambda S, B, ret: ('个位是 0，不影响 `singles`' if S.d == 0 else '个位是非零数，要修正 `s`'),
        'if c == 1': lambda S, B, ret: (f'`{S.d}` 原来只有 1 个 → 用掉后没了，不再是「恰好一个」→ `s` 减一' if S.c == 1 else f'`{S.d}` 有 {S.c} 个，不是单个'),
        'elif c == 2': lambda S, B, ret: (f'`{S.d}` 有 2 个 → 用掉一个后变成恰好 1 个 → `s` 加一' if S.c == 2 else '个数 ≥ 3，用掉一个后仍不止 1 个 → `s` 不变'),
        's -= 1': '`s` → {s}',
        's += 1': '`s` → {s}',
        'ans += k * nz - s': '十位×百位 `{k} × {nz} − {s}` = {k * nz - s}，累加：`ans` = {ans}',
        'return ans': '共 `{ans}` 个不同的三位偶数',
    },
    cards=dict(
        one_liner='先定个位，再用乘法原理数十位×百位，减去「同一个单个数字填两次」',
        complexity='时间 `O(n)`，空间 `O(1)`（数字只有 10 种）',
        problem=['从 `digits` 中选三个数字组成==不同的三位偶数==，求个数',
                 '每个数字只能用一次（按出现次数），==不能有前导零==',
                 '本视频：`[0,2,2,3,4]`'],
        quote='枚举个位数为 d = 0,2,4,6,8。消耗一个 d 后，在剩余数字中，十位有 kinds 种填法，百位有 nonZeros 种填法，十位百位都填「恰好出现一次」的数字是不合法的，要减去。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['不枚举具体的数，只数「有几种」：个位、十位、百位依次用乘法原理',
              '个位用掉一个 `d` 后，`kinds`、`nonZeros`、`singles` 都要跟着修正',
              '答案 = 十位种数 × 百位种数 − 十位百位撞同一个单个数字的方案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：个位是 0 与非零要分开修正；个数为 1、2 时 `singles` 的增减不同',
                 '另一种写法：三重循环枚举下标 / `permutations(digits, 3)`，把数放进集合去重，`O(n^3)`'],
    ),
)
