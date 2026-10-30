CONFIG = dict(
    num=1224, title='最大相等频率', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='从后往前删 + 次数的次数',
    tags=[],
    code='''
class Solution(object):
    def maxEqualFreq(self, nums):

        num_dict = {}
        cnt_dict = {}
        for num in nums:
            num_dict[num] = num_dict.get(num, 0) + 1
        
        for cnt in num_dict.values():
            cnt_dict[cnt] = cnt_dict.get(cnt, 0) + 1

        n = len(nums)
        if self.check(cnt_dict):
            return n

        res = n
        for index in range(n - 1, -1, -1):
            cnt = num_dict[nums[index]]
            num_dict[nums[index]] -= 1
            res -= 1
            cnt_dict[cnt] -= 1
            if cnt_dict[cnt] == 0:
                cnt_dict.pop(cnt)
            if cnt > 1:
                cnt_dict[cnt - 1] = cnt_dict.get(cnt - 1, 0) + 1
            if self.check(cnt_dict):
                return res

    def check(self, cnt_dict):
        if len(cnt_dict) == 1 and (list(cnt_dict.keys())[0] == 1 or list(cnt_dict.values())[0] == 1):
            return True

        if len(cnt_dict) == 2:
            cnt1, cnt2 = cnt_dict.keys()
            if cnt1 < cnt2:
                cnt1, cnt2 = cnt2, cnt1
            if cnt1 == cnt2 + 1 and cnt_dict[cnt1] == 1:
                return True
            if cnt2 == 1 and cnt_dict[cnt2] == 1:
                return True
        
        return False
''',
    call='Solution().maxEqualFreq([1,2,2,3,3,4,4,4,5])',
    expect=7,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前要删的最后一个数；暗 = 已删掉）', cell=72,
             pointers={'index': 'blue'}, dim=lambda S, i, v: 'res' in S and i >= S['res'], h=170),
        dict(type='map', var='num_dict', label='num_dict：数字 → 出现次数', h=200),
        dict(type='map', var='cnt_dict', label='cnt_dict：出现次数 → 有几个数是这个次数', h=200),
    ],
    watch=[('res', 'res', 'green'), ('index', 'index', 'blue'), ('cnt', 'cnt')],
    max_steps=90,
    captions={
        'num_dict[num] = num_dict.get': '统计每个数的出现次数：`num_dict[{num}] = {num_dict[num]}`',
        'cnt_dict[cnt] = cnt_dict.get': '再统计「出现次数」本身：次数 `{cnt}` 对应 `{cnt_dict[cnt]}` 个数',
        'n = len(nums)': '先看整个数组 `n = {n}` 是否合法',
        'if self.check(cnt_dict)': '调用 `check`：用 `cnt_dict` 判断这个前缀能否删掉一个数后次数全相等',
        'res = n': '`res` 表示当前前缀长度，从 `n` 开始往前缩',
        'for index in range': '从后往前，每轮删掉最后一个数 `nums[{index}] = {nums[index]}`',
        'cnt = num_dict': '它当前出现 `{cnt}` 次',
        'num_dict[nums[index]] -= 1': '删掉一个：`num_dict[{nums[index]}]` 变成 `{num_dict[nums[index]]}`',
        'res -= 1': '前缀缩短为 `res = {res}`',
        'cnt_dict[cnt] -= 1': '「出现 `{cnt}` 次的数」少了一个：`cnt_dict[{cnt}]` = {cnt_dict[cnt]}',
        'cnt_dict.pop': '次数 `{cnt}` 已没有数对应，从 `cnt_dict` 去掉',
        'cnt_dict[cnt - 1] =': '这个数现在出现 `{cnt - 1}` 次：`cnt_dict[{cnt - 1}]` 加一',
        'len(cnt_dict) == 1 and': '`len(cnt_dict) = {len(cnt_dict)}`：只有一种次数时，要么次数是 1（每个数各一次），要么只有一个数 → 才合法',
        'len(cnt_dict) == 2': '`len(cnt_dict) = {len(cnt_dict)}`：恰有两种次数，才可能「删一个数后全相等」',
        'cnt1, cnt2 = cnt_dict.keys()': '取出两种次数 `cnt1 = {cnt1}`，`cnt2 = {cnt2}`',
        'cnt1 < cnt2': '保证 `cnt1` 是较大的次数',
        'cnt1 == cnt2 + 1': '情况 2-1：较大的次数只有一个数，删一次后等于较小次数 → `{cnt1} == {cnt2} + 1` 且 `cnt_dict[{cnt1}] = {cnt_dict[cnt1]}`',
        'cnt2 == 1 and': '情况 2-2：较小次数是 1 且只有一个数，把它整个删掉 → `cnt2 = {cnt2}`，`cnt_dict[{cnt2}] = {cnt_dict[cnt2]}`',
        'return True': '==合法==：删掉一个数后，其余次数都相等',
        'return False': '不合法，继续往前缩短前缀',
        'return res': '这是从后往前第一个合法的前缀，长度 `{res}`',
        'return n': '整个数组就合法，返回 `{n}`',
    },
    cards=dict(
        one_liner='从后往前删数，用「次数的次数」几句话判断是否合法',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给定正整数数组 `nums`，求最长前缀长度',
                 '要求：从中==恰好删掉一个元素==后，剩下每个数出现次数都相同',
                 '（删完没有元素也算，视作每个数出现 0 次）',
                 '本视频：`[1,2,2,3,3,4,4,4,5]` → `7`'],
        quote='从后向前，每一轮移除最后一个数，然后判断当前前缀数组是否符合要求。我们可以先使用num_dict统计出每个数字出现的次数，然后将这些次数加入到cnt_dict当中。',
        quote_src='—— yiduobo 题解原文',
        idea=['`num_dict`：数字出现几次；`cnt_dict`：出现 k 次的数有几个',
              '删最后一个数，只改动两个字典里的一两项，`O(1)`',
              '合法只有几种形状：只有一种次数（全 1 或只一个数）；或两种次数，较大者多 1 且仅一个数，或较小者是 1 且仅一个数'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`cnt_dict` 里次数降为 0 要 `pop`，否则会误判有两种次数',
                 '易错：只有一种次数时，要么次数是 1，要么只有一个数',
                 '原文为 Python 2 写法，`cnt_dict.keys()[0]` / `.values()[0]` 已改为 `list(cnt_dict.keys())[0]` / `list(cnt_dict.values())[0]`'],
    ),
)
