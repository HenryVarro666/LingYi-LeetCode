CONFIG = dict(
    num=1005, title='K 次取反后最大化的数组和', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='计数 + 从 -100 到 -1 取反',
    tags=['灵神题单', '难度分 1275'],
    code='''
class Solution(object):
    def largestSumAfterKNegations(self, A, K):

        min_abs = 101
        cnt_dict = {}
        res = 0
        for num in A:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
            res += num
            min_abs = min(min_abs, abs(num))

        for num in range(-100, 0):
            if num in cnt_dict:
                cnt = cnt_dict[num]
                if cnt <= K:
                    K -= cnt
                    res -= 2 * cnt * num
                else:
                    res -= 2 * K * num
                    K = 0
                    break
        
        if K > 0 and K % 2 == 1:
            res -= 2 * min_abs

        return res
''',
    call='Solution().largestSumAfterKNegations([-100,-99,-98,-1,5,2], 5)',
    expect=303,
    skip=['for num in range(-100, 0)', 'if num in cnt_dict'],
    views=[
        dict(type='array', var='A', label='A', h=150, cell=100),
        dict(type='map', var='cnt_dict', label='cnt_dict（数值 → 出现次数）', fmt=lambda k, v: f'{k}: {v}', h=250, font=30),
        dict(type='text', h=100, size=30,
             fn=lambda S: (f"剩余次数 `K = {S['K']}`，数组和 `res = {S['res']}`，最小绝对值 `min_abs = {S['min_abs']}`")),
    ],
    watch=[('num', 'num', 'pink'), ('K', 'K', 'orange'), ('res', 'res', 'green'), ('min_abs', 'min_abs', 'blue')],
    captions={
        'min_abs = 101': '`min_abs`：绝对值最小的数，最后可能要强行取反它',
        'cnt_dict = {}': '用字典统计每个数出现几次（数值范围只有 -100 到 100）',
        'for num in A': lambda S, B, r: (f'读入 `{S.num}`' if 'num' not in B or B.num != S.num else '数组读完了，开始处理取反'),
        'cnt_dict[num] =': '`cnt_dict[{num}] = {cnt_dict[num]}`',
        'res += num': '累加原数组和：`res = {res}`',
        'min_abs = min': '`min_abs = {min_abs}`',
        'cnt = cnt_dict[num]': '从 -100 往 -1 扫（最小的负数先改）：`{num}` 出现 `{cnt}` 次，`K = {K}`',
        'if cnt <= K': lambda S, B, r: (f'`cnt = {S.cnt} <= K = {S.K}`：次数够，这 {S.cnt} 个 `{S.num}` ==全部取反==' if S.cnt <= S.K
                                         else f'`cnt = {S.cnt} > K = {S.K}`：次数不够，只能改 `K` 个'),
        'K -= cnt': '用掉 `{cnt}` 次：`K = {K}`',
        'res -= 2 * cnt * num': '每个 `{num}` 变成 `{-num}`，和增加 `2 × {-num}`：`res = {res}`',
        'res -= 2 * K * num': '只改 `K` 个：`res = {res}`',
        'K = 0': '次数用完',
        'break': '直接结束',
        'if K > 0 and K % 2 == 1': lambda S, B, r: (f'`K = {S.K}` 是奇数：负数改完还剩次数，必须再取反一次' if S.K > 0 and S.K % 2 == 1
                                                    else f'`K = {S.K}`：偶数次可以==抵消==（或已用完），不用处理'),
        'res -= 2 * min_abs': '取反绝对值最小的 `{min_abs}`：`res` 减去 `2 × {min_abs}` → =={res}==',
        'return res': '答案 `{res}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='负数从小到大全部取反，剩下的次数看奇偶',
        complexity='时间 `O(n + C)`，空间 `O(C)`（C = 100）',
        problem=['恰好做 `K` 次取反：选一个下标，把 `A[i]` 变成 `-A[i]`（可重复选）',
                 '求操作后数组的最大和',
                 '本视频：`A = [-100,-99,-98,-1,5,2], K = 5` → `303`'],
        quote='注意到对于一个数而言，取反两次相当于没有变化，因此我们在这里可以利用这个性质使用掉多出来的取反次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['数值只在 -100 到 100，用字典计数代替排序',
              '从 -100 扫到 -1：次数够就整批取反，不够就只改 `K` 个并结束',
              '剩余 `K` 为奇数，再取反绝对值最小的数：和减去 `2 × min_abs`'],
        summary=['时间 `O(n + C)`，空间 `O(C)`，无需排序',
                 '动画里对 -100 到 -1 中不在字典里的数直接略过，只展示出现过的数',
                 '易错：最后判断 `K > 0 and K % 2 == 1`；偶数次可抵消',
                 '对比灵神：灵神先排序再从最小的负数开始改'],
    ),
)
