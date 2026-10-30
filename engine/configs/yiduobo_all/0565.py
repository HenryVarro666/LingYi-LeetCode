CONFIG = dict(
    num=565, title='数组嵌套', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='找环 + 原地标记',
    tags=[],
    code='''
class Solution(object):
    def arrayNesting(self, nums):

        res = 0

        for index in range(len(nums)):
            now = nums[index]
            if now == len(nums):
                continue
            cnt = 0
            nums[index] = len(nums)
            while now != len(nums):
                tmp = nums[now]
                nums[now] = len(nums)
                now = tmp
                cnt += 1
            
            res = max(res, cnt)

        return res
''',
    call='Solution().arrayNesting([5, 4, 0, 3, 1, 6, 2])',
    expect=4,
    views=[
        dict(type='array', var='nums', h=190, pointers={'index': 'blue', 'now': 'pink'},
             color=lambda S, i, v: 'green' if ('nums' in S and v == len(S['nums'])) else None,
             dim=lambda S, i, v: 'nums' in S and v == len(S['nums'])),
        dict(type='text', size=30,
             fn=lambda S: (f"下标 `index = {S.get('index', '')}`，这一圈已走 `cnt = {S.get('cnt', 0)}`；"
                           f"值等于 `{len(S['nums'])}` 表示已访问") if 'nums' in S else ''),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'pink'), ('cnt', 'cnt', 'orange'), ('res', 'res', 'green')],
    captions={
        'now = nums[index]': '从下标 `{index}` 出发，下一个走到 `now = {now}`',
        'if now == len(nums)': '`now = {now}`，是已访问标记 `{len(nums)}` 吗？→ {now == len(nums)}；是的话这个数已在某个环里，跳过',
        'continue': '这个位置在之前的环里算过了，直接跳过，保证每个数只访问一次',
        'cnt = 0': '开始新的一圈，计数清零',
        'nums[index] = len(nums)': '把出发点标成已访问（用 `n = {len(nums)}` 做标记，因为数值范围是 0 到 n-1）',
        'while now != len(nums)': '`now = {now}`，还没回到已标记的位置吗？→ {now != len(nums)}；没回到就继续走',
        'tmp = nums[now]': '先记下一步：`tmp = nums[{now}] = {tmp}`',
        'nums[now] = len(nums)': '当前位置标成已访问，下次不会再走',
        'now = tmp': '走到下一个位置：`now = {now}`',
        'cnt += 1': '这一圈又多了一个元素：`cnt = {cnt}`',
        'res = max': '这一圈长度 `{cnt}`，答案 `res = max({B.res}, {cnt}) = {res}`',
        'return res': '所有数都处理完，最长的环长度 =={ret}==',
    },
    max_steps=110,
    cards=dict(
        one_liner='找环：每个数只属于一个环，求最长环',
        complexity='时间 `O(n)`，空间 `O(1)`（原地标记）',
        problem=['`nums` 是 `0..n-1` 的一个排列',
                 '从下标 `i` 出发，依次访问 `nums[i]`、`nums[nums[i]]`…，直到遇到重复的数',
                 '求这样得到的集合的 ==最大长度==，示例 `[5,4,0,3,1,6,2]` → `4`'],
        quote='虽然题目描述的是数组嵌套，实际上就与之前做过的找循环是完全一样的题目。',
        quote_src='—— yiduobo 题解',
        idea=['排列里每个数恰好指向一个数，所以整个数组分成若干个环',
              '从左往右扫，遇到没处理过的位置就沿着环走一圈，数长度',
              '数值范围是 0 到 n-1，所以拿 ==n== 当已访问标记，不用额外空间'],
        summary=['时间 `O(n)`：每个位置最多被标记一次；空间 `O(1)`',
                 '易错点：出发点也要标记为 n，否则走一圈回来时判断不了终点',
                 '会修改输入数组，是 yiduobo 用 n 做标记的小技巧',
                 '同类题：287 寻找重复数（链表找环）'],
    ),
)
