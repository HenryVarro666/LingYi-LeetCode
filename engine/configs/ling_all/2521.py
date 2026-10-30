def _cur(S):
    a = S.get('nums')
    return getattr(a, 'cur', None) if a is not None and 'x' in S else None


def _txt(S):
    if 'x' not in S or 'nums' not in S:
        return ''
    if 'i' not in S or S.get('_line') == 4:
        return f"取出 `x = {S['x']}`，准备分解"
    return f"当前数分解中：试除 `i = {S['i']}`，剩余 `x = {S['x']}`"


CONFIG = dict(
    num=2521, title='数组乘积中的不同质因数数目', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='试除分解质因数 · 哈希集合去重',
    tags=['灵神题单·数学算法', '难度分 1413'],
    code='''
class Solution:
    def distinctPrimeFactors(self, nums: List[int]) -> int:
        s = set()
        for x in nums:
            i = 2
            while i * i <= x:
                if x % i == 0:
                    s.add(i)
                    x //= i
                    while x % i == 0:
                        x //= i
                i += 1
            if x > 1:
                s.add(x)
        return len(s)
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
        dict(type='array', var='nums', label='nums（蓝箭头 = 正在分解的数）', pointers={_cur: 'blue'}, pointer_labels={_cur: 'x'}, cell=110, h=170),
        dict(type='text', fn=_txt, size=28, h=70),
        dict(type='set', var='s', label='s：已发现的不同质因数（乘积的质因数 = 各数质因数的并集）', fmt=lambda v: str(v), h=240),
    ],
    watch=['x', ('i', 'i', 'pink'), ('s', 's', 'green')],
    captions={
        's = set()': '用哈希集合 `s` 收集质因数，重复的自动去掉：乘积的质因数 = 每个数的质因数的并集',
        'for x in nums': lambda S, B, r: (f'取下一个数 `x = {S.x}`，把它拆成质因数' if S.nums.cur != B.nums.cur else '数组遍历完了，集合里就是全部质因数'),
        'i = 2': '试除数 `i` 从 2 开始',
        'while i * i <= x': lambda S, B, r: (f'`i*i = {S.i * S.i} <= x = {S.x}`：x 还可能有 ≤ 根号 x 的因数，继续试除' if S.i * S.i <= S.x
                                              else f'`i*i = {S.i * S.i} > x = {S.x}`：x 里不会再有 ≤ 根号 x 的因子，停止试除'),
        'if x % i == 0': lambda S, B, r: (f'`{S.x} % {S.i} == 0`：`{S.i}` 整除 x，而更小的因子都已除尽 → `{S.i}` ==一定是质数==' if S.x % S.i == 0
                                           else f'`{S.x} % {S.i} != 0`：`{S.i}` 不是因子，跳过'),
        's.add(i)': '把质因数 `{i}` 加进 `s`：`s = {sorted(s)}`（已有则不变）',
        'x //= i': '把 `x` 里所有的 `{i}` 除干净（只关心质因数种类，不关心次数）：`x` → {x}',
        'while x % i == 0': lambda S, B, r: (f'`{S.x} % {S.i} == 0`：`{S.i}` 还能再除' if S.x % S.i == 0
                                              else f'`{S.x} % {S.i} != 0`：`{S.i}` 除干净了'),
        'i += 1': '`i` → {i}',
        'if x > 1': lambda S, B, r: (f'`x = {S.x} > 1`：剩下一个比根号大的质数（至多一个）' if S.x > 1
                                      else '`x = 1`：已经分解干净，没有剩余'),
        's.add(x)': '剩下的 `x = {x}` 本身是质数，加进 `s`：`s = {sorted(s)}`',
        'return len(s)': '答案是集合大小：`len(s)` = =={ret}==',
    },
    cards=dict(
        one_liner='每个数分解质因数，丢进集合，集合大小就是答案',
        complexity='时间 `O(n√U)`，空间 `O(U/log U)`',
        problem=['给正整数数组 `nums`，求所有元素乘积的不同质因数个数',
                 '示例：`[2,4,3,7,10,6]`，乘积 `10080 = 2^5 * 3^2 * 5 * 7` → `4`',
                 '本视频用小例子：`[12,10,7]`，质因数 `{2,3,5,7}` → `4`'],
        quote='遍历每个数，分解质因数，把质因数加到哈希表中。……答案为哈希表的大小。',
        quote_src='—— 灵茶山艾府题解',
        idea=['乘积的质因数 ==就是每个数的质因数的并集==，不用真的去算乘积',
              '试除法分解：小的因子先除干净，所以 `i` 整除 x 时 `i` 一定是质数',
              '循环结束若 `x > 1`，剩下的就是一个大质数，补进集合'],
        summary=['时间 `O(n√U)`，`U = max(nums)`；集合最多 `O(U/log U)` 个质数',
                 '易错点：别漏了循环后 `x > 1` 的那个大质因数',
                 '这里 `x //= i` 后接 `while` 除干净，保证之后的 `i` 都是质数',
                 '视频里用 `_Arr`（list 子类）只为记录当前遍历到第几个数，不影响算法',
                 '同类题：2507 使用质因数之和替换后可以取到的最小值'],
    ),
)
