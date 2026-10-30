def _txt(S):
    if 'num' not in S or S.get('_line') not in (14, 16, 17, 18, 19, 20):
        return '按数值从小到大扫描：`res` = 到目前为止的最优，`res_prev` = 上上一档的最优'
    if S.get('_line') == 14:
        return f'数值 `{S["num"]}` 权重 `{S["value"]}`：`last = {S["last"]}`，' + ('相邻（差 1）→ 只能从 `res_prev` 接' if S['last'] == S['num'] - 1 else '不相邻 → 可以接在 `res` 后面')
    return f'`now = {S.get("now")}`，`res = {S["res"]}`，`res_prev = {S["res_prev"]}`'


CONFIG = dict(
    num=740, title='删除并获得点数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='（数值, 权重）排序后线性 DP',
    tags=['灵神核心路线', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def deleteAndEarn(self, nums):

        if not nums:
            return 0

        value_dict = {}
        for num in nums:
            value_dict[num] = value_dict.get(num, 0) + num
        
        res = 0
        res_prev = 0
        last = None
        for num, value in sorted(value_dict.items(), key=lambda d:d[0]):
            if last == num - 1:
                now = res_prev + value
            else:
                now = res + value

            res_prev = res
            res = max(res, now)
            last = num

        return res
''',
    call='Solution().deleteAndEarn([2,2,3,3,3,4,6])',
    expect=15,
    views=[
        dict(type='array', var='nums', label='nums', h=150, cell=80),
        dict(type='map', var='value_dict', label='value_dict：数值 → 该数值全部加起来的权重', h=130, fmt=lambda k, v: f'{k}: {v}'),
        dict(type='text', fn=_txt, size=24, h=80),
    ],
    watch=[('num', 'num', 'blue'), 'value', ('last', 'last', 'pink'), ('now', 'now', 'yellow'), ('res_prev', 'res_prev', 'cyan'), ('res', 'res', 'green')],
    captions={
        'if not nums': '空数组直接返回 0',
        'for num in nums': '取下一个数 `{num}`',
        'value_dict[num] = ': '先去重：数值 `{num}` 的权重累加到 =={value_dict[num]}==（选了就全选）',
        'for num, value in sorted': lambda S, B, r: ('所有数值都处理完了' if S.get('last') == S.num else f'按数值从小到大取：`num = {S.num}`，权重 `{S.value}`'),
        'if last == num - 1': lambda S, B, r: (f'`last = {S.last}`，`num - 1 = {S.num - 1}`：' + ('==相邻==，选它就不能选上一档' if S.last == S.num - 1 else '不相邻，互不影响')),
        'now = res_prev': '相邻：只能接在 `res_prev = {res_prev}` 后面，`now = {res_prev} + {value}` = =={now}==',
        'now = res +': '不相邻：直接接在 `res = {res}` 后面，`now = {res} + {value}` = =={now}==',
        'res_prev = res': '`res_prev` 记下旧的 `res = {res}`，给下一档用',
        'res = max': '`res = max({B.res}, {now}) = {res}`：选这档不一定更优',
        'last = num': '`last = {num}`，供下一档判断是否相邻',
        'return res': '最大点数 = =={ret}==',
    },
    cards=dict(
        one_liner='先合并成（数值, 权重），再按数值排序做线性 DP',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['选 `nums[i]` 得 `nums[i]` 分，同时删光所有 `nums[i]±1`',
                 '求最多能得多少分',
                 '示例：`[2,2,3,3,3,4,6]` → `15`'],
        quote='首先，我们可以统计出每个数字出现的次数，然后将其转化为（数值，权重值）这种形式的数对，那么问题就变成了从中选出一些数对，要求数值不能相邻，且权重之和最大。',
        quote_src='—— yiduobo 题解',
        idea=['`f[i]` = 前 `i` 个数值对能选出的最大结果',
              '数值和上一个相邻：`f[i] = max(f[i-1], f[i-2] + value)`',
              '不相邻：`f[i] = f[i-1] + value`；只用三个变量滚动'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '关键是「相邻」要用 `last == num - 1` 判断，不是下标相邻',
                 '不相邻时直接累加：它和前面的选择互不冲突',
                 '这是 198 打家劫舍的变形：把「房子」换成「出现过的数值」'],
    ),
)
