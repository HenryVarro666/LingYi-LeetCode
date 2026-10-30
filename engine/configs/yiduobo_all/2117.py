CONFIG = dict(
    num=2117, title='一个区间内所有数乘积的缩写', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='Python 大整数暴力乘',
    tags=['灵神题单', '难度分 2477'],
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
    call='Solution().abbreviateProduct(1, 16)',
    expect='20922...89888e3',
    views=[
        dict(type='text', size=34, fn=lambda S: (
            f"`now` = ==1×2×…×{S['num']}== = {S['now']}" if 'num' in S and 's' not in S else
            (f"乘积 `{S['now']}`：尾部 `{S['c']}` 个 0 已数过" if 's' in S else '先把区间内所有数乘起来'))),
        dict(type='string', var='s', pointers={'r': 'pink'}, h=150, label='s = str(now)',
             color=lambda S, i, v: ('yellow' if 'r' in S and i > S['r'] else None)),
        dict(type='text', size=30, fn=lambda S: (
            f"去掉 `{S['c']}` 个后缀 0 后还剩 `{S['r'] + 1}` 位" + ('，超过 10 位 → 取前 5 + 后 5' if S['r'] + 1 > 10 else '，不超过 10 位 → 原样输出')
            if 'r' in S and 's' in S and S['s'][S['r']] != '0' else '')),
    ],
    watch=['left', 'right', ('num', 'num', 'blue'), ('c', 'c', 'yellow'), ('r', 'r', 'pink')],
    captions={
        'c = 0': '`c` 记录末尾 0 的个数',
        'now = 1': '`now` 用 Python 大整数存乘积，不会溢出',
        'now *= num': '`now` × `{num}` = =={now}==：直接乘，乘积不到 4000 位，不怕慢',
        's = str(now)': '转成字符串 `s = "{s}"`，前后几位就能直接切片取',
        'l = 0': '`l` 这一行其实没有用到',
        'r = len(s) - 1': '`r` 从最后一位开始 = {r}',
        'while s[r] == ': lambda S, B, ret: (f"`s[{S.r}] = '{S.s[S.r]}'` 是 0 → 还是后缀 0，继续往前" if S.s[S.r] == '0'
                                           else f"`s[{S.r}] = '{S.s[S.r]}'` 不是 0 → 后缀 0 数完了，共 `{S.c}` 个"),
        'r -= 1': '`r` 左移到 {r}',
        'c += 1': '又一个后缀 0：`c` = =={c}==',
        'if r + 1 <= 10': '去掉 0 后长度 `r + 1 = {r + 1}`：{"不超过 10 位 → 不缩写" if r + 1 <= 10 else "超过 10 位 → 要缩写"}',
        'return s[:5]': '前 5 位 `{s[:5]}` + `...` + 后 5 位 `{s[r - 4 : r + 1]}` + `e{c}` = =={ret}==',
        'return s[:r + 1]': '位数不多，直接返回 `{ret}`',
    },
    cards=dict(
        one_liner='乘积不到 4000 位，直接用大整数乘，再切字符串',
        complexity='时间约 `O(n·L)`（L 为乘积位数），空间 `O(L)`',
        problem=['区间 `[left, right]` 所有整数相乘，结果要「缩写」',
                 '去掉后缀 0（记 `C` 个）；剩余超过 10 位时写成 `前5位...后5位eC`',
                 '示例：`left=2, right=11` → `"399168e2"`；本视频：`1~16` → `"20922...89888e3"`'],
        quote='在这里乘积的长度不到4000位，因此即使采用最纯粹的暴力乘法，时间复杂度也是没有问题的。',
        quote_src='—— yiduobo 题解原文',
        idea=['非暴力法的难点是前 5 位：近似会丢精度，所以作者最后还是选了暴力',
              'Python 自带大整数：`for` 一路 `now *= num` 就是精确乘积',
              '转成字符串：从尾部数 0 得到 `C`，再按位数决定要不要缩写'],
        summary=['数据范围 `1 <= left <= right <= 10^4`，乘积最多约 4000 位，暴力足够',
                 '尾部 0 要先数完、去掉，再取「后 5 位」：`s[r - 4 : r + 1]`',
                 '位数判断用 `r + 1 <= 10`（已去掉 0），不是 `len(s)`',
                 '作者提醒：Python 不要手动实现大整数乘法，慢得过分；非暴力解法卡在前 5 位的精度上',
                 '代码已是 Python 3 可运行，未做修改'],
    ),
)
