CONFIG = dict(
    num=2117, title='一个区间内所有数乘积的缩写', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='Python 大整数暴力连乘再切字符串',
    tags=['灵神题单', '数学算法', '难度分 2477'],
    code='''
class Solution(object):
    def abbreviateProduct(self, left, right):

        c = 0
        now = 1
        for num in range(left, right + 1):
            now *= num

        s = str(now)
        l = 0
        r = len(s) - 1
        while s[r] == '0':
            r -= 1
            c += 1
        if r + 1 <= 10:
            return s[:r + 1] + 'e' + str(c)
        else:
            return s[:5] + '...' + s[r - 4 : r + 1] + 'e' + str(c)
''',
    call='Solution().abbreviateProduct(3, 16)',
    expect='10461...94944e3',
    views=[
        dict(type='text', fn=lambda S: (f"目前乘积 `now` = =={S['now']}==" if 'now' in S else '')),
        dict(type='array', var=lambda S: list(range(S['left'], S['right'] + 1)) if 'left' in S else [], label='[left, right]', h=130,
             color=lambda S, k, v: ('green' if 'num' in S and v <= S['num'] and 's' not in S else None)),
        dict(type='string', var=lambda S: S['s'] if 's' in S else '', label='s = str(now)（从右往左数掉末尾的 0）', h=190,
             pointers={'r': 'pink'}, cell=60,
             color=lambda S, i, v: ('yellow' if i < 5 or ('r' in S and S['r'] - 4 <= i <= S['r']) else None) if S.get('_line', 0) >= 15 else None),
        dict(type='text', fn=lambda S: (f"末尾零个数 `c` = =={S['c']}==，去零后长度 `r + 1` = {S['r'] + 1}" if 'r' in S else '')),
    ],
    watch=[('c', 'c', 'yellow'), ('r', 'r', 'pink'), 'now'],
    captions={
        'c = 0': '`c` 统计末尾 0 的个数',
        'now = 1': '`now` 用来存乘积，Python 大整数不会溢出，直接乘',
        'now *= num': '乘上 `{num}`：`now` = =={now}==',
        's = str(now)': '乘积转成字符串 `s`，后面就是字符串操作：长度 `{len(s)}`',
        'r = len(s) - 1': '`r` 从最后一位开始往前找第一个非 0',
        'while s[r]': lambda S, B, ret: (f"`s[{S.r}] = '{S.s[S.r]}'`：是 0 → 继续往前" if S.s[S.r] == '0' else f"`s[{S.r}] = '{S.s[S.r]}'`：不是 0 → 停，`r` 就是去零后的最后一位"),
        'r -= 1': '去掉一个末尾 0：`r` → {r}',
        'c += 1': '末尾零计数 `c` → =={c}==',
        'if r + 1 <= 10': '去零后剩 `{r + 1}` 位：' + '{"不超过 10 位 → 原样输出" if r + 1 <= 10 else "超过 10 位 → 需要缩写"}',
        'return s[:5]': '前 5 位 `{s[:5]}`，后 5 位 `{s[r - 4 : r + 1]}`，再加 `e{c}` → ==`{ret}`==',
        'return s[:r': '不需要缩写：`{ret}`',
    },
    cards=dict(
        one_liner='Python 大整数直接连乘，再按字符串切前后 5 位',
        complexity='时间 约 `O(n · L)`（L 为乘积位数，数据 ≤ 4000 位），空间 `O(L)`',
        problem=['求 `[left, right]` 内所有整数的乘积，缩写成 `前5位...后5位eC`',
                 '`C` 为末尾 0 的个数；去零后不超过 10 位则不缩写',
                 '示例：`left=2, right=11` → `"399168e2"`；本视频：`3~16` → `"10461...94944e3"`'],
        quote='最直观的做法自然是暴力计算。使用python的话直接乘就行了……在这里乘积的长度不到4000位，因此即使采用最纯粹的暴力乘法，时间复杂度也是没有问题的。',
        quote_src='—— yiduobo 题解原文',
        idea=['乘积不到 4000 位，Python 大整数直接乘',
              '转成字符串后，从右往左数末尾 0，得到 `c`',
              '剩余位数 ≤ 10 原样输出，否则取前 5 位 + `...` + 末 5 位',
              '作者提到：前 5 位没有好办法，近似算法会丢精度，所以采用暴力法'],
        summary=['时间 约 `O(n · L)`，空间 `O(L)`，L < 4000',
                 '不要手写大整数乘法，Python 自带的快得多（作者原话）',
                 '易错点：缩写判断用的是==去零后==的长度 `r + 1`，不是原长度',
                 '代码本身已是 Python 3 可运行写法，无需改动',
                 '对比灵神：灵神拆因子 2/5 + 取模，不依赖暴力乘'],
    ),
)
