CONFIG = dict(
    num=2239, title='找到最接近 0 的数字', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='一趟遍历 · 比绝对值',
    tags=[],
    code='''
class Solution(object):
    def findClosestNumber(self, nums):

        res = nums[0]
        for num in nums[1:]:
            if abs(num) < abs(res) or (abs(num) == abs(res) and num > res):
                res = num
        
        return res
''',
    call='Solution().findClosestNumber([2,-4,-1,1,8])',
    expect=1,
    views=[
        dict(type='array', var='nums', h=260, label='nums',
             color=lambda S, i, v: 'green' if 'res' in S and v == S['res'] else None),
        dict(type='text', h=60, fn=lambda S: f"当前 `num = {S['num']}`（`|num| = {abs(S['num'])}`），`res = {S['res']}`（`|res| = {abs(S['res'])}`）" if 'num' in S and 'res' in S else ''),
    ],
    watch=[('num', 'num', 'blue'), ('res', 'res', 'green')],
    captions={
        'res = nums[0]': '先拿第一个数当答案：`res = {res}`',
        'if abs(num)': '`|num| = {abs(num)}` vs `|res| = {abs(res)}`：{"更小 → 更新" if abs(num) < abs(res) else ("绝对值相同且 num 更大 → 更新" if abs(num) == abs(res) and num > res else "不更接近 0 → 跳过")}',
        'res = num': '更新 `res = {res}`',
        'return res': '绝对值最小的数 =={ret}==',
    },
    cards=dict(
        one_liner='越接近 0 绝对值越小，绝对值相同取较大的',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定整数数组 `nums`，返回最接近 `0` 的数',
                 '若两个数距离相同，返回较大的那个',
                 '示例：`[2,-1,1]` → `1`'],
        quote='越接近0绝对值就越小，因此只需一趟遍历，找出绝对值最小的数字就行了。另外根据题目要求，若两个数绝对值相同，那么取其中较大的作为答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历，`res` 记录目前绝对值最小的数',
              '平局时直接比较数值 `num > res`，较大者胜出',
              '用 `nums[1:]` 从第二个数开始遍历'],
        summary=['时间 `O(n)`，空间 `O(1)`（切片 `nums[1:]` 会额外复制，严格说是 `O(n)`）',
                 '易错点：平局条件要和绝对值相等一起判断',
                 '原文无需改动即可在 Python 3 运行'],
    ),
)
