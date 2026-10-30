def _ph2(S):
    return S.get('_line', 0) >= 16


def _px(S):
    return S['x'] if 'x' in S and not _ph2(S) else None


def _pn(S):
    if _ph2(S):
        return S['num'] if 'num' in S and 0 <= S['num'] < len(S['f']) else None
    return S['now'] if 'now' in S and 0 <= S['now'] < len(S['f']) else None


def _cur(S):
    a = S.get('nums')
    return getattr(a, 'cur', None) if a is not None and 'prime' in S else None


def _txt(S):
    if 'f' not in S:
        return ''
    if not _ph2(S):
        if 'x' in S and S['x'] * S['x'] <= 20 and S['f'][S['x']] == S['x']:
            return f"筛法：`x = {S['x']}` 是质数，把它的倍数的 `f` 标成 =={S['x']}=="
        return '筛法：给每个数记一个质因子 `f[i]`'
    if 'num' in S and 0 <= S['num'] < len(S['f']):
        return f"分解：`num = {S['num']}`，质因子 `f[num] = {S['f'][S['num']]}`"
    return ''


CONFIG = dict(
    num=2521, title='数组乘积中的不同质因数数目', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='筛法记质因子 · 沿 f 分解',
    tags=['灵神题单·数学算法', '难度分 1413'],
    code='''
class Solution(object):
    def distinctPrimeFactors(self, nums):

        f = list(range(21))

        x = 2
        while x * x <= 20:
            if f[x] == x:
                now = x + x
                while now <= 20:
                    f[now] = x
                    now += x

            x += 1

        prime = set()
        for num in nums:
            while num > 1:
                prime.add(f[num])
                num //= f[num]

        return len(prime)
''',
    setup='''
class _Arr(list):
    cur = -1
    live = True
    def __iter__(self):
        for k in range(len(self)):
            if self.live:
                self.cur = k
            yield self[k]
    def __deepcopy__(self, memo):
        a = _Arr(list.__iter__(self))
        a.cur = self.cur
        a.live = False
        return a
''',
    call='Solution().distinctPrimeFactors(_Arr([12, 10, 7]))',
    expect=4,
    views=[
        dict(type='text', fn=_txt, size=27, h=60),
        dict(type='array', var='f', label='f[i]：i 的一个质因子（f[i] = i 说明 i 是质数）', h=190, cell=46,
             pointers={_px: 'blue', _pn: 'pink'}, pointer_labels={_px: 'x', _pn: 'now/num'},
             color=lambda S, i, v: ('orange' if v != i else 'green' if i >= 2 else None)),
        dict(type='array', var='nums', label='nums（蓝箭头 = 正在分解的数）', pointers={_cur: 'blue'}, pointer_labels={_cur: 'num'}, cell=80, h=130),
        dict(type='set', var='prime', label='prime：不同的质因子', fmt=lambda v: str(v), h=130),
    ],
    watch=['x', ('now', 'now', 'pink'), ('num', 'num', 'pink'), ('prime', 'prime', 'green')],
    skip=['now += x', 'while now <= 20'],
    captions={
        'f = list(range': '`f[i]` 先全设为自己，之后会被改成 `i` 的一个质因子',
        'x = 2': '从 `x = 2` 开始筛',
        'while x * x <= 20': lambda S, B, r: (f'`x*x = {S.x * S.x} <= 20`：还要用 `x` 去筛' if S.x * S.x <= 20
                                               else f'`x*x = {S.x * S.x} > 20`：筛完了，合数的 `f` 都不再是自己'),
        'if f[x] == x': lambda S, B, r: (f'`f[{S.x}] == {S.x}`：没被更小的质数改过 → ==质数==，筛它的倍数' if S.f[S.x] == S.x
                                          else f'`f[{S.x}] = {S.f[S.x]}`：已经被标过，是合数 → 跳过'),
        'now = x + x': '从 `{x}` 的 2 倍开始，沿 `{x}` 的倍数一路标下去',
        'f[now] = x': '`f[{now}] = {x}`：`{now}` 有质因子 `{x}`（更大的质数后面会覆盖，所以记的是较大的那个）',
        'x += 1': '`x` → {x}',
        'prime = set()': '筛完了。用集合 `prime` 给质因子去重',
        'for num in nums': lambda S, B, r: (f'取下一个数 `num = {S.num}`' if S.nums.cur != B.nums.cur else '所有数都分解完了'),
        'while num > 1': lambda S, B, r: (f'`num = {S.num} > 1`：还没分解完' if S.num > 1 else '`num = 1`：这个数分解完了'),
        'prime.add': '`f[{num}] = {f[num]}` 是 `{num}` 的一个质因子 → 加进 `prime`：`{sorted(prime)}`',
        'num //= f[num]': '把这个质因子除掉：`num` → =={num}==，接着看剩下的部分',
        'return len(prime)': '集合大小就是答案：`len(prime)` = =={ret}==',
    },
    cards=dict(
        one_liner='先筛出每个数的质因子 f[i]，再沿着 f 一路除下去',
        complexity='时间 `O(U log log U + n log U)`，空间 `O(U)`',
        problem=['给正整数数组 `nums`，求所有元素乘积的不同质因数个数',
                 '示例：`[2,4,3,7,10,6]`，乘积 `10080 = 2^5 * 3^2 * 5 * 7` → `4`',
                 '本视频：`[12,10,7]` → `{2,3,5,7}` → `4`'],
        quote='对于寻找质因子这个操作，对于本题的数据规模可以直接暴力计算。我在这里采用的是先执行一次筛法，找出每个数最大的质因子，然后对于数组中的每个数通过这个最大值质因子来分解质因数。',
        quote_src='—— yiduobo 题解原文',
        idea=['乘积的质因子 = 各数质因子的并集，所以用集合去重就行',
              '先用筛法给每个数记一个质因子 `f[i]`（`f[i] == i` 表示质数）',
              '分解 `num`：加入 `f[num]`，再 `num //= f[num]`，直到变成 1'],
        summary=['时间：筛 `O(U log log U)`，每个数分解 `O(log U)`；空间 `O(U)`',
                 '原文筛到 1000，视频为了演示把 `1000` 缩成 `20`（共 3 处），逻辑不变',
                 '原文为 Python 2 写法，`range(1001)` 直接当列表改、`/=` 做整除，已改为 `list(range(...))` 和 `//=`',
                 '视频里用 `_Arr`（list 子类）只为记录遍历到第几个数，不影响算法',
                 '对比灵神：灵神每个数直接试除到根号，不用预处理；yiduobo 预处理后每个数只要 `O(log)`'],
    ),
)
