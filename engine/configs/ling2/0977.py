FILLED_NOW = (10, 11, 13, 14, 15)  # 这些行执行完时 ans[p] 已经填好，但 p 还没减一


def _filled(S, k):
    if 'p' not in S:
        return False
    return k > S['p'] or (S.get('_line') in FILLED_NOW and k == S['p'])


def _used(S, k):
    # nums[i..j] 是还没处理的部分，两侧都已经填进 ans
    return 'i' in S and 'j' in S and (k < S['i'] or k > S['j'])


def _squares(S):
    return [v * v for v in S['nums']]


def _text(S):
    if 'i' not in S:
        return '负数部分平方后==从右往左变大==，非负部分平方后==从左往右变大=='
    if S.get('_line') == 15:
        return '每次都把剩余里==最大的==平方放到最右的空位 → ans 非递减'
    i, j = S['i'], S['j']
    if i > j:
        return '`i > j`：所有数都已经填进 ans'
    return f'剩余 `nums[{i}..{j}]`：绝对值最大的数==只可能在两端== → 比较两端的平方'


def _par(v):
    return f'({v})' if v < 0 else str(v)


def _for(S, B, ret):
    if 'p' in B and B.p == S['p']:
        return '`p` 已经走过 0，`n` 个位置全部填完，循环结束'
    return f'下一个要填的位置 `p = {S["p"]}`：要放==剩余里最大==的平方'


def _if(S, B, ret):
    x, y = S['x'], S['y']
    if x > y:
        return f'`x = {x} > y = {y}`：左端平方更大 → 放到 `ans[{S["p"]}]`'
    if x == y:
        return f'`x = y = {y}`：相等，走 else 放右端的（放哪个都一样）'
    return f'`x = {x} ≤ y = {y}`：右端平方更大 → 走 else'


CONFIG = dict(
    num=977, title='有序数组的平方', difficulty='Easy', category='双指针',
    author='灵茶山艾府', technique='相向双指针：从大到小合并',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        n = len(nums)
        ans = [0] * n
        i, j = 0, n - 1
        for p in range(n - 1, -1, -1):
            x = nums[i] * nums[i]
            y = nums[j] * nums[j]
            if x > y:  # 更大的数放右边
                ans[p] = x
                i += 1
            else:
                ans[p] = y
                j -= 1
        return ans
''',
    call='Solution().sortedSquares([-4, -1, 0, 3, 10])',
    expect=[0, 1, 9, 16, 100],
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='array', var='nums', label='nums（暗 = 已经填进 ans）', cell=96,
             pointers={'i': 'blue', 'j': 'pink'}, dim=_used, h=200),
        dict(type='array', var=_squares, label='每个数的平方（辅助观察，代码里没有这个数组）', cell=96,
             dim=_used, color=lambda S, k, v: 'cyan' if 'i' in S and k in (S['i'], S['j']) and not _used(S, k) else None,
             h=170),
        dict(type='array', var='ans', label='ans（绿 = 已填好，从右往左填）', cell=96,
             pointers={'p': 'yellow'}, color=lambda S, k, v: 'green' if _filled(S, k) else None, h=200),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('p', 'p', 'yellow'), 'x', 'y'],
    skip=['n = len(nums)'],
    captions={
        'ans = [0] * n': '先开一个长为 `n = {n}` 的空数组，打算==从右往左==填（先填最大的）',
        'i, j = 0, n - 1': '左右指针放在两端：`i = {i}`，`j = {j}`，==不用找负数和非负数的分界点==',
        'for p in range': _for,
        'x = nums[i]': lambda S, B, ret: f'左端 `nums[{S["i"]}]` 的平方：`x = {_par(S["nums"][S["i"]])} × {_par(S["nums"][S["i"]])} = {S["x"]}`',
        'y = nums[j]': lambda S, B, ret: f'右端 `nums[{S["j"]}]` 的平方：`y = {_par(S["nums"][S["j"]])} × {_par(S["nums"][S["j"]])} = {S["y"]}`',
        'if x > y': _if,
        'ans[p] = x': '`ans[{p}] = {x}`：它比剩下所有数的平方都大，==放在最右的空位==',
        'i += 1': '`nums[{i - 1}]` 用掉了，`i` 右移 → {i}',
        'ans[p] = y': '`ans[{p}] = {y}`：它比剩下所有数的平方都大，==放在最右的空位==',
        'j -= 1': '`nums[{j + 1}]` 用掉了，`j` 左移 → {j}',
        'return ans': '从大到小倒着填完：`{ret}` ==天然非递减==',
    },
    cards=dict(
        one_liner='平方最大的数一定在两端：从两边往中间合并，从右往左填答案',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计入）',
        problem=['`nums` 按==非递减==顺序排列（可能有负数）',
                 '返回每个数的平方组成的新数组，也要==非递减==',
                 '示例：`[-4,-1,0,3,10]` → `[0,1,9,16,100]`',
                 '进阶：设计 `O(n)` 的算法'],
        quote='仿照 88. 合并两个有序数组 的思路，把上述两个有序数组合并……与其从中间开始向两边合并，不如==从两边开始向中间合并==，这样无需计算从中间的哪个位置开始。',
        quote_src='—— 灵茶山艾府题解',
        idea=['负数 `[-4,-1]` 平方后是 `[16,1]`，==反过来看==就是有序的 `[1,16]`',
                 '非负数 `[0,3,10]` 平方后 `[0,9,100]` 本来就有序 → 合并两个有序数组',
                 '两端是两个数组各自的==最大值==：较大者填到 `ans[p]`，`p` 从右往左'],
        summary=['时间 `O(n)`，空间 `O(1)`（返回值不计入）',
                 '关键：更大的数放右边，所以 `p` 从 `n-1` 倒着走到 `0`',
                 '相等时放哪个都行；循环 `n` 次正好把每个数用一次',
                 '写法二：比较 `-nums[i] > nums[j]`，每轮只算一次乘法',
                 '同类：88. 合并两个有序数组（同样倒序填）'],
    ),
)
