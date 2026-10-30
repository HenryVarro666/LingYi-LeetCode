def _p(v):
    return f'({v})' if v < 0 else str(v)


def _tgt(S):
    return (S['index'] + S['nums'][S['index']]) % len(S['nums']) if 'index' in S else None


CONFIG = dict(
    num=3379, title='转换数组', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟遍历 · 下标取模', tags=[],
    code='''
class Solution(object):
    def constructTransformedArray(self, nums):
        
        res = []
        for index in range(len(nums)):
            res.append(nums[(index + nums[index]) % len(nums)])
        
        return res
''',
    call='Solution().constructTransformedArray([3,-2,1,1,-3,2])',
    expect=[1, 2, 1, -3, -2, -2],
    views=[
        dict(type='text', h=80, size=26, fn=lambda S: (
            f'`index = {S["index"]}`：新下标 = `({S["index"]} + {S["nums"][S["index"]]}) % {len(S["nums"])}` = =={(S["index"] + S["nums"][S["index"]]) % len(S["nums"])}=='
            if 'index' in S else '三种情况都是 `index + nums[index]`，再对长度取模')),
        dict(type='array', var='nums', label='nums（循环数组）', h=190,
             pointers={'index': 'blue', _tgt: 'pink'}, pointer_labels={_tgt: '落脚'}),
        dict(type='array', var='res', label='res（结果）', h=170,
             color=lambda S, i, v: 'green' if i == len(S['res']) - 1 else None),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = []': '`res` 用来收集每个位置落脚处的值',
        'for index in range': lambda S, B, r: (f'处理下标 `index = {S.index}`，`nums[{S.index}] = {S.nums[S.index]}`' if len(S.res) == S.index else '每个下标都处理过了，循环结束'),
        'res.append': lambda S, B, r: f'`nums[{S.index}] = {S.nums[S.index]}` → 新下标 `({S.index} + {_p(S.nums[S.index])}) % {len(S.nums)} = {(S.index + S.nums[S.index]) % len(S.nums)}` → `res` 加入 =={S.nums[(S.index + S.nums[S.index]) % len(S.nums)]}==',
        'return res': '全部下标处理完：`res = {res}`',
    },
    max_steps=40,
    cards=dict(
        one_liner='正、负、零三种情况，统一成 `index + nums[index]`',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计入）',
        problem=['循环数组 `nums`：按 `nums[i]` 的正负向右/向左走 `|nums[i]|` 步，落脚处的值写进 `result[i]`',
                 '`nums[i] == 0` 时落在自己',
                 '示例：`[3,-2,1,1]` → `[1,1,1,3]`；本视频：`[3,-2,1,1,-3,2]`'],
        quote='综合起来可以发现，实际上就可以认为每一轮都是把nums中下标i + nums[i]的元素赋值给result[i]，直接一趟遍历进行赋值操作即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`nums[i] > 0`：新下标 `i + nums[i]`',
              '`nums[i] < 0`：`i - abs(nums[i])`，去掉 abs 就是 `i + nums[i]`',
              '`nums[i] == 0`：新下标还是 `i`，也是 `i + nums[i]`',
              '越界用 `% len(nums)`，Python 里负数也不用特殊处理'],
        summary=['时间 `O(n)`，空间 `O(1)`（返回值不计入）',
                 '易错：必须读原数组 `nums`，结果写进新数组 `res`',
                 '易错：取模的是数组长度 `len(nums)`',
                 '原文为 Python 2 风格，代码未改，只删去了类型说明文档字符串',
                 '对比灵神：灵神用一行列表推导式，yiduobo 用 for 循环 + append，逻辑一致'],
    ),
)
