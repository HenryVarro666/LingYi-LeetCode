CONFIG = dict(
    num=1330, title='翻转子数组得到最大的数组值', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='拆绝对值 · 四组最大最小',
    tags=['灵神题单·数学算法', '灵神题单·贪心与思维', '难度分 2482'],
    code='''
class Solution(object):
    def maxValueAfterReverse(self, nums):
        
        x = []
        y = []
        res = 0
        n = len(nums)
        for i in range(n - 1):
            x.append(nums[i] - nums[i + 1])
            y.append(nums[i] + nums[i + 1])
            res += abs(x[-1])
        
        tmp = res
        mi = [x[0] + abs(x[0]), -x[0] + abs(x[0]), y[0] + abs(x[0]), -y[0] + abs(x[0])]
        ma = [x[0] - abs(x[0]), -x[0] - abs(x[0]), y[0] - abs(x[0]), -y[0] - abs(x[0])]
        for i in range(1, n - 1):
            res = max(res, tmp + abs(nums[i + 1] - nums[0]) - abs(x[i]))
            res = max(res, tmp + abs(nums[-1] - nums[i - 1]) - abs(x[i - 1]))
            mi[0] = min(mi[0], x[i] + abs(x[i]))
            mi[1] = min(mi[1], -x[i] + abs(x[i]))
            mi[2] = min(mi[2], y[i] + abs(x[i]))
            mi[3] = min(mi[3], -y[i] + abs(x[i]))
            ma[0] = max(ma[0], x[i] - abs(x[i]))
            ma[1] = max(ma[1], -x[i] - abs(x[i]))
            ma[2] = max(ma[2], y[i] - abs(x[i]))
            ma[3] = max(ma[3], -y[i] - abs(x[i]))

        return max(res, tmp + max(ma[0] - mi[0], ma[1] - mi[1], ma[2] - mi[2], ma[3] - mi[3]))
''',
    call='Solution().maxValueAfterReverse([2,3,1,5,4])',
    expect=10,
    views=[
        dict(type='array', var='nums', label='nums', h=170,
             color=lambda S, i, v: ('yellow' if 'i' in S and S['_line'] >= 15 and i in (S['i'] - 1, S['i'], S['i'] + 1) else None)),
        dict(type='array', var='x', label='x[i] = nums[i] − nums[i+1]', h=170),
        dict(type='array', var='y', label='y[i] = nums[i] + nums[i+1]', h=170),
        dict(type='array', var='mi', label='mi：四种式子「后半部分」的最小值', h=170, color=lambda S, i, v: 'pink'),
        dict(type='array', var='ma', label='ma：四种式子「前半部分」的最大值', h=170, color=lambda S, i, v: 'cyan'),
    ],
    watch=[('res', 'res', 'green'), ('tmp', 'tmp', 'blue'), 'i'],
    skip=['y = []', 'res = 0', 'n = len'],
    max_steps=64,
    captions={
        'x = []': '`x` 存相邻差，`y` 存相邻和（再配 `res` 累计原数组值）：后面拆绝对值全靠这两个数组',
        'x.append': '`x[{i}] = nums[{i}] − nums[{i+1}]` = {x[i]}',
        'y.append': '`y[{i}] = nums[{i}] + nums[{i+1}]` = {y[i]}',
        'res += abs(x[-1])': '累加原数组值：`res` → =={res}==',
        'tmp = res': '`tmp = {res}` 是不翻转的数组值，后面只看翻转带来的变化',
        'mi = [': '先用第 0 对相邻数初始化四个「后半」最小值 `mi = {mi}`',
        'ma = [': '同样初始化四个「前半」最大值 `ma = {ma}`；四组对应拆开绝对值的四种符号，最后用 `ma − mi` 求翻转收益',
        'for i in range(1, n - 1)': lambda S, B, r: (f'扫到第 `{S.i}` 对相邻数：先试边界翻转，再把它并进四组最值' if S.i != B.get('i') or 'i' not in B else '所有 `i` 都扫完'),
        'res = max(res, tmp + abs(nums[i + 1]': '特殊情形 `i=0` 翻前缀：变化 = `|nums[{i+1}] − nums[0]| − |x[{i}]|` = {abs(nums[i+1]-nums[0])-abs(x[i])}；`res` → =={res}==',
        'res = max(res, tmp + abs(nums[-1]': '特殊情形 `j=n−1` 翻后缀：变化 = `|nums[-1] − nums[{i-1}]| − |x[{i-1}]|` = {abs(nums[-1]-nums[i-1])-abs(x[i-1])}；`res` → =={res}==',
        'mi[0] = min': '第 1 组「后半」：`min({B.mi[0]}, {x[i] + abs(x[i])})` → =={mi[0]}==',
        'mi[1] = min': '第 2 组「后半」：`min({B.mi[1]}, {-x[i] + abs(x[i])})` → =={mi[1]}==',
        'mi[2] = min': '第 3 组「后半」：`min({B.mi[2]}, {y[i] + abs(x[i])})` → =={mi[2]}==',
        'mi[3] = min': '第 4 组「后半」：`min({B.mi[3]}, {-y[i] + abs(x[i])})` → =={mi[3]}==',
        'ma[0] = max': '第 1 组「前半」：`max({B.ma[0]}, {x[i] - abs(x[i])})` → =={ma[0]}==',
        'ma[1] = max': '第 2 组「前半」：`max({B.ma[1]}, {-x[i] - abs(x[i])})` → =={ma[1]}==',
        'ma[2] = max': '第 3 组「前半」：`max({B.ma[2]}, {y[i] - abs(x[i])})` → =={ma[2]}==',
        'ma[3] = max': '第 4 组「前半」：`max({B.ma[3]}, {-y[i] - abs(x[i])})` → =={ma[3]}==',
        'return max': lambda S, B, r: f'四组 `ma−mi` = `{[S.ma[k]-S.mi[k] for k in range(4)]}`，取最大 {max(S.ma[k]-S.mi[k] for k in range(4))}，加上 `tmp={S.tmp}`；再和边界翻转的 `res={S.res}` 比，答案 =={r}==',
    },
    cards=dict(
        one_liner='和曼哈顿距离同一招：拆开绝对值，分四种符号各求一个最值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组值 = 相邻差的绝对值之和；可翻转一个子数组一次，求最大数组值',
                 '示例：`[2,3,1,5,4]` → 翻转 `[3,1,5]` 得 `[2,5,1,3,4]`，数组值 `10`'],
        quote='翻转之后，除了首位两组差值，中间的部分是完全相同的，因此实际上的变化就是 abs(a[i - 1] - a[j]) + abs(a[i] - a[j + 1]) - abs(a[i - 1] - a[i]) - abs(a[j] - a[j + 1])',
        quote_src='—— yiduobo 题解原文',
        idea=['翻转只改变两端的两项，变化量 = 新两项 − 旧两项',
              '`i=0` 或 `j=n−1` 少一项，先单独扫一遍',
              '其余：前两个绝对值拆成四种符号，整理成「只含 i」减「只含 j」，各维护最大 / 最小，一趟扫完'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '先处理 `i=0`、`j=n−1` 两种边界，再处理一般情形',
                 '易错：只拆前两个绝对值；`|x[i−1]|`、`|x[j]|` 符号固定，不用拆',
                 '作者说明：违反绝对值符号的取值会自动落到另一种合法情形，所以取最大是安全的',
                 '对比灵神：灵神用恒等式一次化成 `2(mx−mn)`，yiduobo 用四组最值，思路更直接',
                 '原文已是 Python 3 可运行，未做修改'],
    ),
)
