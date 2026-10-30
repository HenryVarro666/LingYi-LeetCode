_NUMS = [2, 1, 2]


def _pass(S):
    return 1 if list(S['nums']) == _NUMS else 2


def _cur(S):
    if 'f' not in S or 'nums' not in S:
        return None
    n, ln = len(S['nums']), S['_line']
    if ln in (10, 11, 12):
        return len(S['f']) if ln == 10 else len(S['f']) - 1
    if ln in (16, 17, 18) and 'g' in S:
        return n - 1 - len(S['g']) if ln == 16 else n - len(S['g'])
    if ln in (22, 23) and 'index' in S:
        return S['index']
    return None


def _color(S, i, v):
    c = _cur(S)
    if c is None:
        return None
    return 'blue' if i == c else None


def _label(S):
    if 'nums' not in S:
        return 'nums'
    return f"nums（第 {_pass(S)} 遍：" + ('原数组，统计递增' if _pass(S) == 1 else '翻转后，递增 = 原来的递减') + '）'


def _txt(S):
    if 'f' not in S:
        return '先数「长度 >= 1 的递增连续子序列」，再翻转数组数递减'
    ln = S['_line']
    f = S['f']
    g = S.get('g', [])
    if ln <= 12:
        return f"`f` = 以每个元素==结尾==的子序列数：`{f}`"
    if ln <= 19:
        return f"`f = {f}`    `g`（以元素==开头==）`= {g if ln != 19 else g}`"
    if 'index' in S and ln in (22, 23):
        i = S['index']
        return f"`f[{i}] × g[{i}] − 1 = {f[i] * g[i] - 1}` 个含 `{S['nums'][i]}` 的长度≥2 子序列"
    return f"`f = {f}`    `g = {g}`"


CONFIG = dict(
    num=3299, title='连续子序列的和', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='贡献法 · 哈希表 DP · 翻转数组',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def getSum(self, nums):

        mod = 10 ** 9 + 7

        def calc(nums):
            f = []
            cnt_f = {}

            for v in nums:
                f.append(cnt_f.get(v - 1, 0) + 1)
                cnt_f[v] = cnt_f.get(v, 0) + f[-1]
            
            g = []
            cnt_g = {}
            for v in nums[::-1]:
                g.append(cnt_g.get(v + 1, 0) + 1)
                cnt_g[v] = cnt_g.get(v, 0) + g[-1]
            g.reverse()

            res = 0
            for index, v in enumerate(nums):
                res = (res + (f[index] * g[index] % mod - 1 + mod) % mod * v) % mod

            return res

        res = calc(nums)
        res = (res + calc(nums[::-1])) % mod
        res = (res + sum(nums) % mod) % mod
        return res
''',
    call='Solution().getSum([2, 1, 2])',
    expect=11,
    views=[
        dict(type='text', fn=_txt, size=26, h=80),
        dict(type='array', var='nums', label='nums（蓝 = 当前元素；翻转后再来一遍）', cell=100, h=170, color=_color),
        dict(type='map', var='cnt_f', label='cnt_f[v]：以 v 结尾的子序列数', fmt=lambda k, v: f"{k}: {v}", h=130, font=30),
        dict(type='map', var='cnt_g', label='cnt_g[v]：以 v 开头的子序列数', fmt=lambda k, v: f"{k}: {v}", h=130, font=30),
    ],
    max_steps=80,
    watch=[('v', 'v', 'blue'), ('index', 'index', 'pink'), ('res', 'res', 'green')],
    skip=['mod = 10', 'f = []', 'cnt_f = {}', 'g = []', 'cnt_g = {}', 'g.reverse', 'res = 0'],
    captions={
        'for v in nums[::-1]': lambda S, B, r: ('倒着扫完了；`g` 是倒着存的，`reverse` 翻回来后 `g[i]` 对应 `nums[i]`' if len(S.g) == len(S.nums) else f'倒着扫：`v = {S.v}`，`cnt_g` 记「以 v 开头」的个数'),
        'for v in nums': lambda S, B, r: ('正着扫完了：`f[i]` = 以 `nums[i]` 结尾的递增子序列数' if len(S.f) == len(S.nums) else f'正着扫：`v = {S.v}`，`cnt_f` 记「以 v 结尾」的个数'),
        'f.append': '`f = cnt_f[{v}-1] + 1 = {f[-1]}`：接在所有以 `{v-1}` 结尾的后面，再加单独的 `{v}`',
        'cnt_f[v] =': '`cnt_f[{v}] = {cnt_f[v]}`：以 `{v}` 结尾的总数更新，给后面的 `{v+1}` 用',
        'g.append': '`g = cnt_g[{v}+1] + 1 = {g[-1]}`：后面接以 `{v+1}` 开头的，再加单独的 `{v}`',
        'cnt_g[v] =': '`cnt_g[{v}] = {cnt_g[v]}`：以 `{v}` 开头的总数更新',
        'g.reverse': '倒着存的，翻回来后 `g[i]` 对应 `nums[i]`',
        'res = 0': '贡献法：逐个元素算它出现在多少个长度≥2 的子序列里',
        'for index, v in enumerate': lambda S, B, r: ('贡献法：逐个元素算完了，每个元素的贡献都已累加' if B.get('index') == S.index and 'res' in B and B.get('index') == len(S.nums) - 1 and S.res == B.get('res') else f'`nums[{S.index}] = {S.v}`：前半段 `f[{S.index}] = {S.f[S.index]}` 种，后半段 `g[{S.index}] = {S.g[S.index]}` 种'),
        23: '`f × g − 1 = {f[index] * g[index] - 1}`：减去长度 1 的情形；贡献 `×{v}` → `res = {res}`',
        25: '这一遍（只含长度≥2）的和是 `{ret}`',
        28: '翻转数组再算一遍：翻转后的==递增==就是原数组的==递减==',
        29: '最后加上长度为 1 的子序列（元素和 `{sum(nums)}`）：`res = {res}`',
        30: '全部连续子序列的和是 `{ret}`',
    },
    cards=dict(
        one_liner='递增算一遍，翻转再算递减，最后补上长度为 1 的',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['连续数组：相邻元素差恒为 `+1` 或恒为 `-1`；长度为 1 也算',
                 '求 `nums` 所有连续子序列的元素和，对 `10^9+7` 取模',
                 '本视频：`[2,1,2]`'],
        quote='先处理递增的子序列，然后翻转数组，这样一来再处理一次递增的子序列就相当于处理了递减的子序列。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]`：以 `nums[i]` 结尾；`g[i]`：以 `nums[i]` 开头。用哈希表按值累计，免去枚举 prev',
              '`nums[i]` 在 `f[i] × g[i] − 1` 个长度≥2 的子序列里',
              '递增算完，翻转数组再算递增即递减；长度为 1 的只在最后统一加一次'],
        summary=['时间 `O(n)`，空间 `O(n)`；哈希表代替了对前驱下标的枚举',
                 '易错：长度为 1 的子序列递增、递减各数一次会重复，所以 `calc` 里要减 1，最后单独加 `sum(nums)`',
                 '`g` 倒着扫，存完要 `reverse` 才和下标对齐',
                 '原文已是 Python 3 可运行的写法，代码未改动'],
    ),
)
