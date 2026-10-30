CONFIG = dict(
    num=2574, title='左右元素和的差值', difficulty='Easy', category='动态规划',
    author='yiduobo', technique='总和 − 前缀和 得后缀和', tags=['难度分 1206'],
    code='''
class Solution(object):
    def leftRightDifference(self, nums):

        s = sum(nums)
        res = []
        now = 0
        for v in nums:
            res.append(abs(s - now - v - now))
            now += v
        
        return res
''',
    call='Solution().leftRightDifference([10,4,8,3])',
    expect=[15, 1, 11, 22],
    views=[
        dict(type='text', fn=lambda S: f"左 `{S['now']}`，右 = `{S['s']} − {S['now']} − {S['v']}` = {S['s']-S['now']-S['v']}，差 = =={abs(S['s']-S['now']-S['v']-S['now'])}==" if S.get('_line') == 8 and 'v' in S else '右和 = 总和 − 左和 − 当前数'),
        dict(type='array', var='nums', h=170, label='nums',
             color=lambda S, i, v: ('blue' if i == len(S['res']) else 'cyan' if i < len(S['res']) else None) if 'res' in S else None),
        dict(type='array', var='res', h=170, label='res（答案）', color=lambda S, i, v: 'green'),
    ],
    watch=['s', ('now', 'now', 'cyan'), ('v', 'v', 'blue')],
    captions={
        's = sum': '先算总和 `s = {s}`，后缀和靠它倒推',
        'res = []': '`res` 存每个位置的答案',
        'now = 0': '`now` 是前缀和：当前位置左侧元素之和，起点为 0',
        'res.append': '左边 `{now}`，右边 `{s} − {now} − {v}` = {s-now-v}，差的绝对值 → =={res[-1]}== 加入 `res`',
        'now += v': '把 `{v}` 并入前缀和：`now` = {now}，再看下一个数',
        'return res': '全部算完，返回 `{res}`',
    },
    cards=dict(
        one_liner='先求总和，一趟遍历里用前缀和倒推后缀和',
        complexity='时间 `O(n)`，空间 `O(1)`（不计答案数组）',
        problem=['每个位置 `p`：左边元素和与右边元素和之差的绝对值', '示例：`[10,4,8,3]` → `[15,1,11,22]`'],
        quote='这个后缀和也可以通过总和减去前缀和以及p对应的值得到，那么就可以先计算出数组的总和s，接下来一趟遍历，同时使用一个变量now表示前缀和。',
        quote_src='—— yiduobo 题解原文',
        idea=['当前数 `v`：左边是 `now`，右边是 `s − now − v`', '算出 `abs(右 − 左)` 放进 `res`，再把 `v` 加进 `now`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '先算答案再更新 `now`，否则左侧会多算当前数',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
