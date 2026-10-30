def _col(S, i, v):
    if v == -1:
        return 'orange'
    if 'min_l' in S and S['min_l'] != inf and v in (S['min_l'], S['max_r']) and S.get('_line', 0) >= 12:
        pass
    if 'i' in S and i == S['i']:
        return 'blue'
    if 'pre_i' in S and i == S['pre_i']:
        return 'cyan'
    return None


def _txt(S):
    if 'min_l' not in S:
        return ''
    ml = S['min_l'] if S['min_l'] != inf else '∞'
    return f"与空位相邻的最小值 min_l = =={ml}==，最大值 max_r = =={S['max_r']}==　｜　已得 ans = =={S.get('ans', 0)}=="


CONFIG = dict(
    num=3357, title='最小化相邻元素的最大差值', difficulty='Hard', category='贪心算法',
    author='灵茶山艾府', technique='从特殊到一般 · 分类讨论',
    tags=['贪心与思维', '难度分 3077'],
    code='''
class Solution:
    def minDifference(self, nums: List[int]) -> int:
        n = len(nums)
        # 和空位相邻的最小数字 min_l 和最大数字 max_r
        min_l, max_r = inf, 0
        for i, v in enumerate(nums):
            if v != -1 and (i > 0 and nums[i - 1] == -1 or i < n - 1 and nums[i + 1] == -1):
                min_l = min(min_l, v)
                max_r = max(max_r, v)

        def calc_diff(l: int, r: int, big: bool) -> int:
            d = (min(r - min_l, max_r - l) + 1) // 2
            if big:
                d = min(d, (max_r - min_l + 2) // 3)  # d 不能超过上界
            return d

        ans = 0
        pre_i = -1
        for i, v in enumerate(nums):
            if v == -1:
                continue
            if pre_i >= 0:
                if i - pre_i == 1:
                    ans = max(ans, abs(v - nums[pre_i]))
                else:
                    ans = max(ans, calc_diff(min(nums[pre_i], v), max(nums[pre_i], v), i - pre_i > 2))
            elif i > 0:
                ans = max(ans, calc_diff(v, v, False))
            pre_i = i
        if 0 <= pre_i < n - 1:
            ans = max(ans, calc_diff(nums[pre_i], nums[pre_i], False))
        return ans
''',
    call='Solution().minDifference([2,-1,-1,10,-1,5])',
    expect=3,
    views=[
        dict(type='text', fn=_txt, size=24, h=60),
        dict(type='array', var='nums', label='nums（橙色 = 空位 -1）', pointers={'i': 'blue', 'pre_i': 'cyan'}, color=_col, h=230),
        dict(type='text', fn=lambda S: (f"空位 `l={S['l']}, r={S['r']}`：填一种数 `ceil(min(r-min_l, max_r-l)/2)` = `{(min(S['r']-S['min_l'], S['max_r']-S['l'])+1)//2}`；连续空位再封顶 `ceil((max_r-min_l)/3)` = `{(S['max_r']-S['min_l']+2)//3}`" if 'l' in S and 'r' in S and S.get('_line', 0) in (12, 13, 14, 15) else ''), size=22, h=70),
    ],
    watch=[('min_l', 'min_l', 'cyan'), ('max_r', 'max_r', 'orange'), ('ans', 'ans', 'green'), 'pre_i'],
    captions={
        'min_l, max_r = inf, 0': '`min_l` 和 `max_r`：与空位相邻的数字里的最小、最大值',
        'if v != -1 and': '`nums[{i}] = {v}`：{"是数字且挨着空位 → 参与统计" if v != -1 and (i > 0 and nums[i-1] == -1 or i < n-1 and nums[i+1] == -1) else "不是「与空位相邻的数字」"}',
        'min_l = min': '`min_l = {min_l}`',
        'max_r = max': '`max_r = {max_r}`',
        'd = (min(r - min_l': '填一种数：`d = ceil(min(r-min_l, max_r-l)/2)` = `({min(r - min_l, max_r - l)}+1)//2` = =={d}==',
        'if big': '{"中间有连续空位，可以填 x、y 两种数 → 用三等分上界" if big else "只有单个空位，只能填一种数，不用封顶"}',
        'd = min(d,': '三等分上界 `(max_r-min_l+2)//3 = {(max_r - min_l + 2) // 3}`，`d = min({B.d}, {(max_r - min_l + 2) // 3})` = =={d}==',
        'continue': '空位不单独处理，留到前后两个数字确定后一起算',
        'return d': '这一段的最大绝对差是 `{d}`，回去用它更新 `ans = max(ans, {d})`',
        'if v == -1': '`nums[{i}] = {v}`：{"空位，先跳过" if v == -1 else "是数字，看它和前一个数字之间的关系"}',
        'if i - pre_i == 1': '`i - pre_i = {i - pre_i}`：{"两个数相邻，没有空位，差值固定" if i - pre_i == 1 else "两数之间夹着空位"}',
        'ans = max(ans, abs': '直接相邻：`|{v} - {nums[pre_i]}|` = {abs(v - nums[pre_i])} → `ans` = =={ans}==',
        'ans = max(ans, calc_diff(min': '两数 `{nums[pre_i]}` 和 `{v}` 之间有 `{i - pre_i - 1}` 个空位 → 调用 `calc_diff` 算这一段的最大绝对差，`big = {i - pre_i > 2}`',
        'elif i > 0': '{"这是第一个数字，但前面还有空位（只有右侧一个邻居）" if i > 0 else "`i = 0`：第一个数字就在开头，前面没有空位，不用算"}',
        'ans = max(ans, calc_diff(v, v': '前缀空位全填靠近 `{v}` 的数：`ans` = =={ans}==',
        'pre_i = i': '记下 `pre_i = {pre_i}`；到这里 `ans` = =={ans}==',
        'if 0 <= pre_i < n - 1': '最后一个数字之后{"还有空位（后缀）" if 0 <= pre_i < n - 1 else "没有空位"}',
        'ans = max(ans, calc_diff(nums[pre_i]': '后缀空位：调用 `calc_diff` 算这一段，结果并入 `ans`',
        'return ans': '答案：`{ans}`',
    },
    cards=dict(
        one_liner='空位只填 x、y：靠近最小邻居和最大邻居',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 里 `-1` 是空位，选一对正整数 `(x, y)`，每个空位填 `x` 或 `y`',
                 '要让相邻元素绝对差的最大值尽量小，求这个最小值',
                 '示例：`[1,2,-1,10,8]` → `4`；本视频：`[2,-1,-1,10,-1,5]` → `3`'],
        quote='一旦我们填了两个不同的数，就不能再填其他数字了。取 minL 和 maxR 之间的三等分点，可以得到 max(d1,d2)=ceil((maxR-minL)/3)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先找出和空位相邻的最小数 `min_l`、最大数 `max_r`：x 去贴近 `min_l`，y 去贴近 `max_r`',
              '一段空位两侧是 `l, r`：都填一种数，差值是 `ceil(min(r-min_l, max_r-l)/2)`',
              '连续空位还能填 x 和 y 两种，上界是 `ceil((max_r-min_l)/3)`，两者取小，再对所有段取最大'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '前缀、后缀空位只有一个邻居，所以传 `calc_diff(v, v, False)`',
                 '只有「中间夹着 ≥ 2 个空位」才用 `big=True` 封顶',
                 '相邻两数之间没有空位时，差值是固定的 `abs(v - nums[pre_i])`'],
    ),
)
