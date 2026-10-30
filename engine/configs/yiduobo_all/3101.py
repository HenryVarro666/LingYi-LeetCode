CONFIG = dict(
    num=3101, title='交替子数组计数', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='按相同相邻元素切段 · 求和公式', tags=[],
    code='''
class Solution(object):
    def countAlternatingSubarrays(self, nums):

        res = 0
        p = 0
        while p < len(nums):
            q = p + 1
            while q < len(nums) and nums[q] != nums[q - 1]:
                q += 1
            res += (q - p) * (q - p + 1) // 2
            p = q
        
        return res
''',
    call='Solution().countAlternatingSubarrays([0,1,1,0,1,1])',
    expect=10,
    views=[
        dict(type='array', var='nums', pointers={'p': 'blue', 'q': 'pink'}, h=200,
             color=lambda S, i, v: ('green' if 'q' in S and S['p'] <= i < S['q'] else None) if 'p' in S else None),
        dict(type='text', size=34, fn=lambda S: (f"当前段 `[{S['p']}, {S['q']})` 长 `k = {S['q']-S['p']}`，可选子数组 `k(k+1)/2` = =={(S['q']-S['p'])*(S['q']-S['p']+1)//2}==") if 'q' in S and 'p' in S and S['p'] < len(S['nums']) else ''),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 累计答案',
        'p = 0': '`p` 是当前交替段的起点',
        'q = p + 1': '`q` 从 `p+1` 开始向右扩展，段内至少有 1 个元素',
        'while p < len': '`p = {p}`：还有没处理的段' ,
        'while q < len': lambda S, B, r: (f"`nums[{S.q}] = {S.nums[S.q]}` 与前一个 `{S.nums[S.q-1]}` 不同 → 仍然交替，`q` 继续右移" if S.q < len(S.nums) and S.nums[S.q] != S.nums[S.q-1]
                                         else f"`q = {S.q}`：到末尾或遇到相同的相邻元素 → 这一段结束"),
        'q += 1': '`q` → {q}',
        'res += (q - p)': '段长 `k = {q-p}`，段内有 `k(k+1)/2 = {(q-p)*(q-p+1)//2}` 个合法子数组 → `res` = =={res}==',
        'p = q': '下一段从 `q` 开始：`p` → {p}',
        'return res': '所有段的个数相加：=={res}==',
    },
    cards=dict(
        one_liner='相同相邻元素把数组切成交替段，每段 k(k+1)/2',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制数组 `nums`，没有相邻相同元素的子数组叫交替子数组', '返回交替子数组的数量',
                 '示例：`[0,1,1,1]` → `5`；本视频：`[0,1,1,0,1,1]` → `10`'],
        quote='对于一个长度为k的交替子数组，其中有k个长度为1的合法子数组，k - 1个长度为2的合法子数组，以此类推。',
        quote_src='—— yiduobo 题解原文',
        idea=['值相同的相邻元素不能在同一子数组，先据此切成若干段', '段内 01 交替，任选子数组都合法：`k + (k-1) + … + 1`',
              '双指针一趟：`p` 定起点，`q` 找终点，边切边加'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`q` 停在段的下一个位置，下一段直接 `p = q`',
                 '代码原样照搬，整数除法已是 `//`，可直接在 Python 3 运行',
                 '对比灵神：灵神按右端点逐个累加 cnt，这里按整段套公式'],
    ),
)
