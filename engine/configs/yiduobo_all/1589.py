CONFIG = dict(
    num=1589, title='所有排列中的最大和', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='差分数组统计次数 + 排序配对',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def maxSumRangeQuery(self, nums, requests):

        n = len(nums)
        end_pos = [0] * n
        requests = sorted(requests, key=lambda d:d[0])
        now = 0
        p = 0
        cnt_dict = {}
        for index in range(n):
            now -= end_pos[index]
            while p < len(requests) and requests[p][0] == index:
                now += 1
                if requests[p][1] < n - 1:
                    end_pos[requests[p][1] + 1] += 1
                p += 1
            
            if now > 0:
                cnt_dict[now] = cnt_dict.get(now, 0) + 1
        
        nums = sorted(nums, reverse=True)
        offset = 0
        res = 0
        mod = 10 ** 9 + 7
        for cnt in sorted(cnt_dict.keys(), reverse=True):
            for index in range(cnt_dict[cnt]):
                res += nums[offset + index] * cnt
                res %= mod
            offset += cnt_dict[cnt]
        
        return res
''',
    call='Solution().maxSumRangeQuery([1,2,3,4,5], [[1,3],[0,1]])',
    expect=19,
    views=[
        dict(type='text', fn=lambda S: (
            f"requests = `{S['requests']}`：每个 `[l, r]` 让 l..r 各被算一次" if 'requests' in S else ''), size=26),
        dict(type='array', var='end_pos', label='end_pos（r+1 处要把生效区间数减掉几个）',
             pointers={'index': 'blue'}, h=200),
        dict(type='text', fn=lambda S: (f"当前位置 `index = {S['index']}`，生效区间数 `now` = =={S['now']}==" if 'now' in S and 'index' in S and 'offset' not in S else ''), size=28),
        dict(type='map', var='cnt_dict', label='cnt_dict：被算 cnt 次的位置有几个',
             fmt=lambda k, v: f'被算 {k} 次 → {v} 个位置', h=170),
        dict(type='array', var='nums', label='nums（降序后，大的配给次数多的位置）',
             pointers={'offset': 'pink'}, h=200,
             color=lambda S, i, v: ('green' if 'offset' in S and 'index' in S and 'cnt' in S and i == S['offset'] + S['index'] else None)),
    ],
    watch=['index', 'now', 'p', 'offset', 'cnt', ('res', 'res', 'green')],
    captions={
        'end_pos = [0]': '`end_pos[i]`：区间在 `i - 1` 结束，到 `i` 要把 `now` 减掉的个数',
        'requests = sorted': '请求按起点从小到大排序 → 扫到 `index` 时，起点等于它的请求在 `p` 处依次取出',
        'now -= end_pos': lambda S, B, r: (f'`end_pos[{S.index}] = {S.end_pos[S.index]}`：有区间在 `{S.index - 1}` 结束，`now` {B.now} → =={S.now}==' if S.end_pos[S.index] else f'`end_pos[{S.index}] = 0`：没有区间刚结束，`now` 仍是 =={S.now}=='),
        'while p <': lambda S, B, r: (f"`requests[{S.p}][0] = {S.requests[S.p][0]}` 等于 `index = {S.index}` → 有区间从这里开始" if S.p < len(S.requests) and S.requests[S.p][0] == S.index else f'没有更多起点是 `{S.index}` 的请求，进入计数'),
        'now += 1': '一个区间从 `index` 开始生效：`now` = =={now}==',
        'end_pos[requests[p][1] + 1] += 1': '这个区间到 `{requests[p][1]}` 为止，下标 `{requests[p][1] + 1}` 起不再生效 → `end_pos` 记一笔',
        'if requests[p][1] < n - 1': lambda S, B, r: (f'终点 `{S.requests[S.p][1]}` 不是最后一格，要在后一位登记结束' if S.requests[S.p][1] < len(S.nums) - 1 else f'终点 `{S.requests[S.p][1]}` 已是最后一格，不用登记'),
        'if now > 0': '下标 `{index}` 被 `{now}` 个请求覆盖' ,
        'cnt_dict[now]': '统计：被算 `{now}` 次的位置多了一个 → `cnt_dict = {cnt_dict}`',
        'nums = sorted': '数组从大到小排序：==大数配给被算次数多的位置==（排序不等式）',
        'for cnt in sorted': lambda S, B, r: (f'次数从多到少：先处理 `cnt = {S.cnt}`，它有 `{S.cnt_dict[S.cnt]}` 个位置' if 'cnt' not in B or B.cnt != S.cnt else '所有次数档都分配完，循环结束'),
        'for index in range(cnt_dict': lambda S, B, r: (f'这一档共 `{S.cnt_dict[S.cnt]}` 个位置，取第 `{S.index + 1}` 个：下标 `index = {S.index}`' if not (S.index == S.cnt_dict[S.cnt] - 1 and B.index == S.index and S.res > 0) else '这一档的位置都配完，内层循环结束'),
        'res += nums': '`nums[{offset + index}] = {nums[offset + index]}` 放到被算 `{cnt}` 次的位置：`res` += `{nums[offset + index]} × {cnt}` → =={res}==',
        'res %= mod': '取模 `10^9 + 7`（这里数值小，不变）：`res = {res}`',
        'offset += cnt_dict[cnt]': '这一档的数用完，`offset` 后移 `{cnt_dict[cnt]}` → {offset}',
        'return res': '最大和 =={res}==',
    },
    skip=['mod = ', 'offset = 0', 'now = 0', 'p = 0', 'cnt_dict = {}', 'res = 0', 'n = len'],
    cards=dict(
        one_liner='先数每个位置被查询几次，再把大数配给高频位置',
        complexity='时间 `O(n + q log q + n log n)`，空间 `O(n)`',
        problem=['`nums` 可以任意重排；`requests[i] = [l, r]` 表示要求 `nums[l..r]` 的区间和',
                 '求所有请求的区间和之和的==最大值==，结果对 `10^9+7` 取模',
                 '示例：`nums=[1,2,3,4,5]`，`requests=[[1,3],[0,1]]` → `19`'],
        quote='每个request实际上是求一个区间的和，那么如果将这些区间和展开，就可以得到0到n - 1这n个位置每个位置被计算的次数。为了使得最终结果最大，显然就应该将较大的数放在使用次数较多的位置上。',
        quote_src='—— yiduobo 题解原文',
        idea=['问题拆成两半：==每个位置被算几次==，以及==怎么分配数字==',
              '静态区间、每次只加 1，用差分的思路一趟扫描：起点 `now += 1`，终点后一位 `now -= 1`',
              '把「被算 cnt 次」的位置个数记进 `cnt_dict`，数组降序后按次数从多到少依次分配'],
        summary=['时间 `O(n + q log q + n log n)`，空间 `O(n)`',
                 '`end_pos` 是 yiduobo 版的差分：不直接改差分数组，而是在 `r+1` 登记「要减掉几个」',
                 '终点是最后一格时不能写 `end_pos[n]`（越界），所以有 `< n - 1` 的判断',
                 '原文是 Python 2 风格，只删去了类型说明，代码无需其他改动',
                 '对比常见写法：直接差分数组得到每格次数，再把次数数组和 nums 各排序后逐位相乘'],
    ),
)
