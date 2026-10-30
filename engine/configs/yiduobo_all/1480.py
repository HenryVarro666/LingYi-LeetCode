CONFIG = dict(
    num=1480, title='一维数组的动态和', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='一趟扫描累加', tags=[],
    code='''
class Solution(object):
    def runningSum(self, nums):

        res = [nums[0]]
        for index in range(1, len(nums)):
            res.append(res[-1] + nums[index])
        
        return res
''',
    call='Solution().runningSum([3,1,2,10,1,4])',
    expect=[3, 4, 6, 16, 17, 21],
    views=[
        dict(type='array', var='nums', label='nums（原数组，不修改）', pointers={'index': 'blue'}, cell=100, h=190),
        dict(type='array', var='res', label='res（动态和，边扫边追加）', cell=100, h=190,
             color=lambda S, i, v: 'green' if i == len(S['res']) - 1 else None),
        dict(type='text', fn=lambda S: (f"新末项 = 上一项 `{S['res'][-2]}` + `nums[{S['index']}]` = =={S['res'][-1]}==" if 'index' in S and S['_line'] == 6 and len(S['res']) > 1 else '前缀和：每一项 = 上一项的和 + 当前数'), h=70),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = [nums[0]]': '第一项动态和就是 `nums[0]` = =={res[0]}==，先放进 `res`',
        'for index in range': lambda S, B, r: ('已扫完所有数，循环结束' if B.get('index') == S.get('index') and 'index' in B else f"`index = {S.index}`：扫描下一个数 `nums[{S.index}] = {S.nums[S.index]}`"),
        'res.append': '`res[-1]` 是到上一位的和，加上 `nums[{index}] = {nums[index]}` → 追加 =={res[-1]}==',
        'return res': '一趟扫描完，`res` 就是前缀和数组',
    },
    cards=dict(
        one_liner='比较基础：一趟扫描，边走边累加',
        complexity='时间 `O(n)`，空间 `O(n)`（结果数组）',
        problem=['`runningSum[i] = nums[0] + … + nums[i]`，返回动态和数组',
                 '示例：`[1,2,3,4]` → `[1,3,6,10]`',
                 '本视频：`[3,1,2,10,1,4]` → `[3,4,6,16,17,21]`'],
        quote='比较基础的题目，就是要求数组的前缀和，之间一趟扫描累加即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['先放入 `nums[0]` 作为第一项', '之后每步取 `res[-1]`（上一个和）加上当前数，追加到 `res`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`range(1, len(nums))` 从 1 开始，因为第 0 项已放进 `res`',
                 '对比灵神：灵神原地改 `nums`，空间 `O(1)`；这里新开 `res`，不改输入'],
    ),
)
