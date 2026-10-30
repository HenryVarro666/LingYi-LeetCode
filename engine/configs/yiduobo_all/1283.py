NUMS = [1, 2, 5, 9]
TH = 6


def _color(S, i, v):
    if 'l' not in S or i == 0:
        return None
    if i < S['l']:
        return 'red'
    if i >= S['r']:
        return 'green'
    return None


def _num_color(S, i, v):
    if 'num' in S and S['_line'] in (9, 10, 11, 12) and S['nums'].index(S['num']) == i:
        return 'yellow'
    return None


def _top(S):
    if 'mid' in S and 'tmp' in S and 8 <= S['_line'] <= 14:
        return f"除数 `mid = {S['mid']}`：逐个累加 `ceil(num / mid)`，目前 `tmp = {S['tmp']}`（阈值 `{TH}`）"
    if 'l' in S:
        return f"答案在 `[l, r] = [{S['l']}, {S['r']}]` 里：红 = 太小，绿 = 满足"
    return '除数越大，结果越小 → ==二分除数=='


def _ceil(S, B, ret):
    if S.num % S.mid != 0:
        return f'`{S.num} % {S.mid} = {S.num % S.mid} ≠ 0`：除不尽 → 向上取整，再 +1'
    return f'`{S.num} % {S.mid} = 0`：正好整除，不用 +1'


def _cmp(S, B, ret):
    if S.tmp > S.threshold:
        return f'`tmp = {S.tmp} > {S.threshold}`：除数 `{S.mid}` 太小 → 答案在右边，`l = mid + 1`'
    return f'`tmp = {S.tmp} ≤ {S.threshold}`：除数 `{S.mid}` 满足 → 答案 `≤ {S.mid}`，`r = mid`'


CONFIG = dict(
    num=1283, title='使结果不超过阈值的最小除数', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分除数 · 左闭右闭收缩',
    tags=['灵神核心路线', '灵神题单·二分算法', '难度分 1542'],
    code='''
class Solution(object):
    def smallestDivisor(self, nums, threshold):

        l = 1
        r = max(nums)
        while l < r:
            mid = (l + r) >> 1
            tmp = 0
            for num in nums:
                tmp += num // mid
                if num % mid != 0:
                    tmp += 1

            if tmp > threshold:
                l = mid + 1
            else:
                r = mid
        

        return l
''',
    call=f'Solution().smallestDivisor({NUMS}, {TH})',
    expect=5,
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='array', var=lambda S: list(range(max(NUMS) + 1)),
             label='候选除数（红 = 太小，绿 = 已知满足；0 不是候选）', cell=80, index=False, color=_color,
             dim=lambda S, i, v: i == 0,
             pointers={'l': 'blue', 'mid': 'yellow', 'r': 'pink'}, h=240),
        dict(type='array', var='nums', label='nums（黄 = 正在累加的 num）', cell=100, color=_num_color, h=180),
    ],
    watch=[('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow'), ('num', 'num'),
           ('tmp', 'tmp', 'green'), 'threshold'],
    skip=['tmp = 0'],
    max_steps=62,
    captions={
        'l = 1': '除数是正整数：`l = 1`',
        'r = max(nums)': '`r = max(nums) = {r}`：此时每项都是 1，和为 `n ≤ threshold`，一定满足',
        'while l < r': lambda S, B, r: (f'`l = {S.l} < r = {S.r}`：还没确定 → 继续二分' if S.l < S.r
                                        else f'`l = r = {S.l}`：区间缩成一个数，就是答案'),
        'mid = (l + r) >> 1': '`mid = ({l} + {r}) >> 1 = {mid}`，从 `tmp = 0` 开始累加',
        'tmp += num // mid': '`tmp += {num} // {mid}` → {tmp}',
        'if num % mid != 0': _ceil,
        'tmp += 1': '`tmp` → {tmp}',
        'if tmp > threshold': _cmp,
        'l = mid + 1': '`l` → {l}',
        'r = mid': '`r` → {r}',
        'return l': '返回最小除数 =={ret}==',
    },
    cards=dict(
        one_liner='除数越大结果越小：直接二分这个除数',
        complexity='时间 `O(n log U)`，空间 `O(1)`，`U = max(nums)`',
        problem=['选一个正整数除数，`nums` 每个数除以它并==向上取整==后求和',
                 '求使和 `≤ threshold` 的==最小==除数，保证有解',
                 '示例：`nums = [1,2,5,9], threshold = 6` → `5`'],
        quote='有一点可以明确的是，==除数越大，最后得到的结果就越小==，因此可以二分这个除数，然后根据除法的结果与阈值的大小关系来调整除数。',
        quote_src='—— yiduobo 题解原文',
        idea=['向上取整：先 `num // mid`，有余数再 `+1`',
              '`tmp > threshold`：除数太小，`l = mid + 1`',
              '否则 `mid` 可能就是答案，`r = mid`；`l == r` 时结束'],
        summary=['时间 `O(n log U)`，空间 `O(1)`',
                 '`l = 1` 起步：除数不能为 0；`r = max(nums)` 一定满足',
                 '`r = mid` 不能写成 `mid − 1`：mid 本身可能就是答案',
                 '原文为 Python 2 写法，整数除法 `num / mid` 已改为 `num // mid`'],
    ),
)
