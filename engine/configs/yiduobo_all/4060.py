LO, HI = 13, 30


def _good(x):
    return sum(1 for c in str(x) if int(c) % 2 == 0) % 2 == 0


def _color(S, i, v):
    n = LO + i
    if 'l' in S and 'r' in S:
        l, r = S['l'], S['r']
        if (n == LO and l % 2 == 1) or (n == HI and r % 2 == 0):
            return 'yellow'
        if l % 2 == 0 and r % 2 == 1 or True:
            lo, hi = (l + l % 2), (r - (1 - r % 2))
            if lo <= n <= hi:
                return 'cyan' if (n - lo) // 2 % 2 == 0 else 'purple'
    return None


def _txt(S):
    if 'l' not in S:
        return ''
    l, r = S['l'], S['r']
    if l % 2 == 1 or r % 2 == 0:
        return '端点落单：先单独检查，再收缩成「偶数开头、奇数结尾」'
    if l > r:
        return f'区间空了，配对部分 `{(r - l + 1)}` 个，不多算'
    return f'中间 `[{l}, {r}]` 共 `{r - l + 1}` 个数，两两一组（`2k` 与 `2k+1`），每组恰好 ==1 个==偶好数 → `{(r - l + 1) // 2}` 个'


CONFIG = dict(
    num=4060, title='计算偶好数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='按 2k、2k+1 配对，每组恰有一个偶好数',
    tags=[],
    code='''
class Solution(object):
    def countEvenlyGoodIntegers(self, l, r):
        
        res = 0

        if l % 2 == 1:
            x = l
            cnt = 0
            while x:
                if x % 2 == 0:
                    cnt += 1
                x //= 10
            if cnt % 2 == 0:
                res += 1
            l += 1
        
        if r % 2 == 0:
            x = r
            cnt = 0
            while x:
                if x % 2 == 0:
                    cnt += 1
                x //= 10
            if cnt % 2 == 0:
                res += 1
            r -= 1
        
        return res + (r - l + 1) // 2
''',
    setup='LO, HI = 13, 30',
    call='Solution().countEvenlyGoodIntegers(13, 30)',
    expect=9,
    views=[
        dict(type='array', var=lambda S: list(range(13, 31)), cell=50, h=230, label='13..30（青/紫成对 = 配好对的区间；黄 = 单独检查的端点）',
             color=_color, index=False),
        dict(type='text', fn=_txt, size=28, h=110),
        dict(type='text', fn=lambda S: (f"逐位数偶数：`x = {S['x']}`，目前偶数位 `{S['cnt']}` 个" if 'x' in S and 'cnt' in S else ''), size=28, h=80),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('x', 'x', 'yellow'), ('cnt', 'cnt', 'orange'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记单独处理的端点里有几个偶好数',
        'if l % 2 == 1': lambda S, B, r: (f'`l = {S.l}` 是奇数 → 它是某一组的「2k+1」，对应的「2k」不在区间内，==必须单独检查==' if S.l % 2 == 1
                                          else f'`l = {S.l}` 是偶数，正好是一组的开头 → 不用单独处理'),
        'if r % 2 == 0': lambda S, B, r: (f'`r = {S.r}` 是偶数 → 它是某一组的「2k」，配对的「2k+1」不在区间内，==必须单独检查==' if S.r % 2 == 0
                                          else f'`r = {S.r}` 是奇数，正好是一组的结尾 → 不用单独处理'),
        'x = l': '把端点 `{x}` 拷出来逐位拆',
        'x = r': '把端点 `{x}` 拷出来逐位拆',
        'cnt = 0': '`cnt` 统计偶数数字的个数',
        'while x': lambda S, B, r: (f'`x = {S.x}` 还有数位 → 继续' if S.x else '所有数位看完了'),
        'if x % 2 == 0': lambda S, B, r: (f'个位 `{S.x % 10}` 是偶数 → 偶数数字 +1' if S.x % 10 % 2 == 0 else f'个位 `{S.x % 10}` 是奇数，不算'),
        'cnt += 1': '偶数数字共 `{cnt}` 个',
        'x //= 10': '去掉个位：`x = {x}`',
        'if cnt % 2 == 0': lambda S, B, r: (f'`cnt = {S.cnt}` 是偶数 → 这个端点本身就是偶好数' if S.cnt % 2 == 0
                                            else f'`cnt = {S.cnt}` 是奇数 → 它不是偶好数'),
        'res += 1': '端点是偶好数，`res` = {res}',
        'l += 1': '`l` 变成偶数 `{l}`，从这里起两两成组',
        'r -= 1': '`r` 变成奇数 `{r}`，到这里止',
        'return res': '`{res}` 个端点 + `{(r - l + 1) // 2}` 组 × 1 = =={ret}==',
    },
    max_steps=90,
    cards=dict(
        one_liner='相邻的 2k 和 2k+1 恰有一个是偶好数，直接数组数',
        complexity='时间 `O(log r)`，空间 `O(1)`',
        problem=['偶好数：数字中「偶数数字」的个数是偶数个',
                 '给出 `l`、`r`（`1 ≤ l ≤ r ≤ 10^15`），求区间内偶好数的个数',
                 '示例：`l = 13, r = 30` → `9`'],
        quote='无论x中偶数数字的数量是多少个，最后这一位上的0到9刚好是5个奇数5个偶数，因此其中5个与x组合后必然具有偶数个偶数数字。',
        quote_src='—— yiduobo 题解',
        idea=['`2k` 和 `2k+1` 除个位外完全相同；个位一奇一偶 → ==恰好一个是偶好数==',
              '所以配好对的区间，答案就是对数 `(r-l+1) // 2`',
              '落单的端点（`l` 为奇、`r` 为偶）手动数偶数数字'],
        summary=['时间 `O(log r)`，不需要数位 DP',
                 '分组必须是 `2k` 和 `2k+1`：例如 `39` 和 `40` 个位以外不同，不能成对',
                 '`l` 为奇数先单独处理再 `l += 1`；`r` 为偶数先单独处理再 `r -= 1`',
                 '原文代码整数除法已是 `//`，无需改动'],
    ),
)
