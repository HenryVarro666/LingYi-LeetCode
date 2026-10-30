CONFIG = dict(
    num=3201, title='找出有效子序列的最大长度 I', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='奇偶性分类 · 贪心取交替', tags=[],
    code='''
class Solution(object):
    def maximumLength(self, nums):

        even = 0
        pre = nums[0]
        res = 1
        if nums[0] % 2 == 0:
            even = 1
        
        for v in nums[1:]:
            if v % 2 == 0:
                even += 1
            
            if (pre + v) % 2 == 1:
                pre = v
                res += 1
        
        return max(res, even, len(nums) - even)
''',
    call='Solution().maximumLength([1,2,1,1,2,1,2])',
    expect=6,
    views=[
        dict(type='array', var='nums', label='nums（绿 = 偶数，粉 = 奇数）', h=220,
             color=lambda S, i, v: 'green' if v % 2 == 0 else 'pink'),
        dict(type='text', fn=lambda S: (f"情况一：全奇或全偶 → 到目前为止数到偶数 `{S['even']}` 个（奇数 = 总数 − 偶数）" if 'even' in S else ''), size=28, h=60),
        dict(type='text', fn=lambda S: (f"情况二：奇偶交替，从 nums[0] 开始 → 已选 =={S['res']}== 个，末项 `{S['pre']}`" if 'res' in S else ''), size=28, h=60),
    ],
    watch=['even', 'pre', ('res', 'res', 'green'), 'v'],
    captions={
        'even = 0': '`even` 统计偶数个数（奇数个数 = 总数 − even）',
        'pre = nums[0]': '情况二的子序列首项一定取 `nums[0]` → `pre = {pre}`',
        'res = 1': '`res` 是交替子序列的长度，已有首项 → 1',
        'if nums[0] % 2 == 0': 'nums[0] 是偶数吗？是的话 `even` 初始为 1',
        'even = 1': 'nums[0] 是偶数 → `even = 1`',
        'for v in nums[1:]': '从 `nums[1]` 往后看，当前 `v = {v}`',
        'if v % 2 == 0': lambda S, B, r: f"`{S.v}` 是{'偶' if S.v % 2 == 0 else '奇'}数" + ('，`even` +1' if S.v % 2 == 0 else '，不用计入偶数'),
        'even += 1': '`even` → {even}',
        'if (pre + v) % 2 == 1': lambda S, B, r: (f"`({S.pre} + {S.v}) % 2` = {(S.pre + S.v) % 2}：" + ('奇偶不同，==可以接在末项后面==' if (S.pre + S.v) % 2 == 1 else '和末项同奇偶，跳过')),
        'pre = v': '末项更新为 `{v}`',
        'res += 1': '交替子序列变长：`res` → =={res}==',
        'return max': lambda S, B, r: f"取三者最大：交替 `{S.res}`，全偶 `{S.even}`，全奇 `{len(S.nums) - S.even}` → =={r}==",
    },
    cards=dict(
        one_liner='相邻和的奇偶性只有两种：全同奇偶，或者奇偶交替',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['子序列相邻两项之和模 2 的结果必须都相同，求最长有效子序列长度',
                 '示例：`[1,2,1,1,2,1,2]` → `6`（取 `1,2,1,2,1,2`）'],
        quote='若最优子序列中不包含nums[0]，那么不妨设其中首项为x，当nums[0]和x同奇偶时，可以用nums[0]替换x，此时子序列的长度不变；当nums[0]和x不同奇偶时，将nums[0]加入x的左侧就可以得到更优的子序列。',
        quote_src='—— yiduobo 题解原文',
        idea=['结果为 0：整个子序列同奇偶 → 数全奇或全偶的个数',
              '结果为 1：奇偶交替，首项必取 `nums[0]`（替换或加入都不会更差）',
              '从左往右，遇到和末项奇偶不同的就接上，取三种情况最大'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：别漏掉全同奇偶的情况，比如 `[1,3]` 答案是 2',
                 '易错：交替情况要贪心取 nums[0]，不能漏掉首项',
                 '原文本身已是 Python 3 可运行，未做改动'],
    ),
)
