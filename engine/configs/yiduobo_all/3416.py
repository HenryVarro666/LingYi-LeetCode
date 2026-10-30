def _pairs(n):
    return n * (n - 1) // 2


def _nums_color(S, i, v):
    if 'index' not in S or 'x' not in S:
        return None
    if i == S['index']:
        return 'yellow'
    if v == S['x']:
        return 'orange'
    return None


def _nums_dim(S, i, v):
    return False


def _row1(S):
    if 'prefix_x' not in S or S['_line'] < 72:
        return '枚举每个位置当中间元素 x：前缀里的 x / 非 x 个数，和后缀里的 x / 非 x 个数，决定能怎么选另外 4 个'
    return (f"前缀：x 有 =={S['prefix_x']}== 个，其他 `{S['prefix_other']}` 个　|　"
            f"后缀：x 有 `{S['suffix_x']}` 个，其他 `{S['suffix_other']}` 个")


def _row2(S):
    if 'a_x_a' not in S:
        return ''
    return f"实时维护：`a_x_a` = {S['a_x_a']}，`a_x_aa` = {S['a_x_aa']}，`aa_x_a` = {S['aa_x_a']}"


CONFIG = dict(
    num=3416, title='唯一中间众数子序列 II', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='枚举中间 x · 组合计数 + 容斥',
    code='''
class Solution(object):
    def subsequencesWithMiddleMode(self, nums):
        
        n = len(nums)

        cnt = {}
        prefix_same_pair = []
        for index in range(n):
            v = nums[index]
            if index == 0:
                prefix_same_pair.append(0)
            else:
                prefix_same_pair.append(prefix_same_pair[-1] + cnt.get(v, 0))
            cnt[v] = cnt.get(v, 0) + 1
        
        cnt = {}
        suffix_same_pair = []
        for index in range(n - 1, -1, -1):
            v = nums[index]
            if index == n - 1:
                suffix_same_pair.append(0)
            else:
                suffix_same_pair.append(suffix_same_pair[-1] + cnt.get(v, 0))
            cnt[v] = cnt.get(v, 0) + 1
        suffix_same_pair.reverse()

        def calc_pair(cnt):
            if cnt < 2:
                return 0
            return cnt * (cnt - 1) // 2

        mod = 10 ** 9 + 7
        n = len(nums)
        res = 0
        prefix_cnt = {}
        a_x_a = 0
        aa_x_a = 0
        a_x_aa = 0

        for index, x in enumerate(nums):
            if index > 0:
                v = nums[index - 1]
                suffix_v_cnt = cnt[v] - prefix_cnt[v]
                if x == v:
                    suffix_v_cnt -= 1
                a_x_a += suffix_v_cnt

                prefix_x_cnt = prefix_cnt.get(x, 0)
                if x == v:
                    prefix_x_cnt -= 1
                a_x_a -= prefix_x_cnt

                suffix_x_cnt = cnt[x] - prefix_cnt.get(x, 0) - 1

                a_x_aa += calc_pair(suffix_v_cnt)
                a_x_aa -= prefix_x_cnt * suffix_x_cnt

                prefix_v_cnt = prefix_cnt[v] - 1
                suffix_x_cnt = cnt[x] - prefix_cnt.get(x, 0) - 1
                aa_x_a += prefix_v_cnt * suffix_v_cnt 
                aa_x_a -= calc_pair(prefix_x_cnt)

            if index < 2:
                prefix_cnt[x] = prefix_cnt.get(x, 0) + 1
                continue
            if index > n - 3:
                break
            
            prefix_x = prefix_cnt.get(x, 0)
            suffix_x = cnt[x] - 1 - prefix_x
            prefix_other = index - prefix_x
            suffix_other = n - index - 1 - suffix_x

            prefix_x_pair = calc_pair(prefix_x)
            suffix_x_pair = calc_pair(suffix_x)

            res = (res + prefix_x_pair * suffix_x_pair) % mod

            res = (res + prefix_x_pair * suffix_x * suffix_other) % mod
            res = (res + suffix_x_pair * prefix_x * prefix_other) % mod

            res = (res + prefix_x_pair * calc_pair(suffix_other)) % mod
            res = (res + suffix_x_pair * calc_pair(prefix_other)) % mod
            res = (res + prefix_x * suffix_x * prefix_other * suffix_other) % mod

            y_x_y = a_x_a - prefix_x * suffix_x
            y_x_yy = a_x_aa - prefix_x * calc_pair(suffix_x)
            yy_x_y = aa_x_a - calc_pair(prefix_x) * suffix_x

            if suffix_other >= 2:
                x_yz = calc_pair(suffix_other) - (suffix_same_pair[index + 1] - suffix_x_pair)
                res = (res + prefix_x * prefix_other * x_yz) % mod
                res = (res - prefix_x * (y_x_y * (n - index - 1 - suffix_x - 1) - y_x_yy * 2) % mod + mod) % mod

            if prefix_other >= 2:
                yz_x = calc_pair(prefix_other) - (prefix_same_pair[index - 1] - prefix_x_pair)
                res = (res + suffix_x * suffix_other * yz_x) % mod
                res = (res - suffix_x * (y_x_y * (index - prefix_x - 1) - yy_x_y * 2) % mod + mod) % mod
            
            prefix_cnt[x] = prefix_cnt.get(x, 0) + 1

        return res
''',
    call='Solution().subsequencesWithMiddleMode([1,2,2,3,2,4])',
    expect=3,
    views=[
        dict(type='array', var='nums', pointers={'index': 'blue'}, color=_nums_color, label='nums（黄 = 当前中间元素，橙 = 与它相同的值）', h=230),
        dict(type='array', var='prefix_same_pair', label='prefix_same_pair：前缀里相同元素对数', h=150),
        dict(type='array', var='suffix_same_pair', label='suffix_same_pair：后缀里相同元素对数', h=150),
        dict(type='text', fn=_row1, size=24, h=100),
        dict(type='text', fn=_row2, size=24, h=70),
    ],
    watch=['index', 'x', 'prefix_x', 'suffix_x', 'prefix_other', 'suffix_other', ('res', 'res', 'green')],
    captions={
        32: '预处理已完成：`prefix_same_pair[i]`、`suffix_same_pair[i]` 是前 / 后缀里相同元素对数，`cnt` 是每个值的总次数',
        40: lambda S, B, r: f'枚举中间元素：`index = {S.index}`，`x = {S.x}`',
        46: '`a_x_a`（x 的左右各取一个相同的 a）：x 右移一位，左侧新增 `nums[index-1]`，右边还有 `{suffix_v_cnt}` 个同值 → `a_x_a` = {a_x_a}',
        51: '原来当过右侧 a 的这个位置变成了 x，左侧 `{prefix_x_cnt}` 个 x 配的方案作废 → `a_x_a` = {a_x_a}',
        66: lambda S, B, r: (f'`index = {S.index} > n - 3 = {S.n - 3}`：右边已凑不够 2 个元素，停止' if S.index > S.n - 3 else f'`index = {S.index} <= n - 3`：右边够 2 个，继续'),
        72: '前缀 x 有 `{prefix_x}` 个、其他 `{prefix_other}` 个；后缀 x 有 `{suffix_x}` 个、其他 `{suffix_other}` 个',
        82: lambda S, B, r: f'前缀 2 个 x（`{S.prefix_x_pair}` 种）+ 后缀任取 2 个非 x（`{_pairs(S.suffix_other)}` 种）：x 有 3 个，别的至多 2 个 → 必唯一众数',
        83: lambda S, B, r: f'对称：后缀 2 个 x（`{S.suffix_x_pair}` 种）+ 前缀任取 2 个非 x（`{_pairs(S.prefix_other)}` 种）',
        84: '前后各取 1 个 x 和 1 个非 x：`{prefix_x} × {suffix_x} × {prefix_other} × {suffix_other}`，x 共 3 个，必唯一众数；`res` = {res}',
        86: '`y_x_y` = `a_x_a` 中 a ≠ x 的方案：减去 a = x 的 `prefix_x × suffix_x` → `y_x_y` = {y_x_y}',
        91: lambda S, B, r: f'后缀取互不相同且 ≠ x 的 `y、z`：`C({S.suffix_other}, 2) = {_pairs(S.suffix_other)}`，减去相同的对 `{S.suffix_same_pair[S.index + 1] - S.suffix_x_pair}` → `x_yz` = =={_pairs(S.suffix_other) - (S.suffix_same_pair[S.index + 1] - S.suffix_x_pair)}==',
        92: 'a x _ x _ y z：前缀选 1 个 x、1 个非 x，后缀选 yz → `{prefix_x} × {prefix_other} × {x_yz}`，`res` = {res}',
        93: lambda S, B, r: f'a 若等于 y 或 z，a 和 y 都出现 2 次，与 x 并列，不合法 → 用 `y_x_y`、`y_x_yy` 容斥减掉 `{(B.res - S.res) % 1000000007}`，`res` = {S.res}',
        96: lambda S, B, r: f'对称：x 在后缀时，前缀取互异的 yz：`yz_x` = =={_pairs(S.prefix_other) - (S.prefix_same_pair[S.index - 1] - S.prefix_x_pair)}==',
        97: '`yz_x` 配上后缀的 1 个 x 和 1 个非 x：`res` = {res}',
        98: lambda S, B, r: f'同样容斥减掉 a 与 y/z 相同的不合法情况 `{(B.res - S.res) % 1000000007}`，`res` = {S.res}',
    },
    skip=[4] + list(range(6, 26)) + [27, 28, 29, 30, 67, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 48, 49, 50, 53, 55, 56, 58, 59, 60, 61,
                                    63, 64, 65, 69, 70, 71, 74, 75, 77, 79, 80, 87, 88, 90, 95, 100],
    max_steps=80,
    cards=dict(
        one_liner='枚举中间众数 x，前后缀计数，用容斥去掉「别的数也并列」',
        complexity='时间 `O(n)`，空间 `O(n)`（`mod = 10^9 + 7`）',
        problem=['整数数组 `nums`，统计长度为 5 的子序列个数：正中间的元素是众数，且众数==唯一==',
                 '答案对 `10^9 + 7` 取模，`n` 最大 `10^5`（3395 题的 `O(n^2)` 不够用）',
                 '本视频：`[1,2,2,3,2,4]` → `3`'],
        quote='可以依然按照枚举中间x的处理方法遍历nums，然后针对两个x的情况进行优化。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举中间的 `x`，按子序列里 x 的个数分类：5、4、3 个 x 直接用组合数；只有 2 个 x 时要小心别的数并列',
              '2 个 x 的情形：先算「x 加上任意其他数」，再减去 `xy_x_yz` 这种 y 也出现 2 次的',
              '减法需要 `y_x_y` 等量，用 `a_x_a`、`a_x_aa` 这些随 `index` 右移 `O(1)` 更新的计数，再扣掉 a = x 的部分'],
        summary=['时间 `O(n)`，空间 `O(n)`；全程对 `10^9+7` 取模，减法要 `+ mod` 再取模',
                 '易错点：容斥里 `xy_x_yy` 被 `xy_x_ya` 多算了一次，所以要减去 2 倍',
                 '`a_x_a` 的更新分两步：加上新进入左侧的 v 能配的，减去变成 x 的那个位置作废的',
                 '原文是 Python 2 风格，仅 `class Solution(object)`，代码无需改动；原文 `//` 已是整数除法',
                 '视频只展开 `index = 2、3` 两个中间位置；5 个 x / 4 个 x 的项在本例中为 0，已快进'],
    ),
)
