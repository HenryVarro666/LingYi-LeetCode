NUMS = [1, 3, 2, 4]
K = 4


def _info(S):
    if 'p' not in S or 'index' not in S:
        return ''
    n = len(S['nums'])
    if S['p'] > S['index']:
        return f"当前合法窗口 `[{S['index']}, {S['p'] - 1}]`，下一个候选右端点 `p = {S['p']}`"
    return f"从 `index = {S['index']}` 起，还没有扩出合法窗口"


CONFIG = dict(
    num=3835, title='开销小于等于 K 的子数组数目', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='枚举左端点 · 右端点只增不减 + 单调队列',
    tags=['常用数据结构', '难度分 1759'],
    code='''
class Solution(object):
    def countSubarrays(self, nums, k):
        
        ma = deque()
        mi = deque()

        res = 0
        p = 0
        for index, v in enumerate(nums):
            while p < len(nums):
                x = nums[p]
                if ma:
                    x = max(nums[ma[0]], x)
                
                y = nums[p]
                if mi:
                    y = min(nums[mi[0]], y)
                
                if (x - y) * (p - index + 1) > k:
                    break
                
                while ma and nums[ma[-1]] <= nums[p]:
                    ma.pop()
                ma.append(p)

                while mi and nums[mi[-1]] >= nums[p]:
                    mi.pop()
                mi.append(p)

                p += 1
            
            res += p - index

            if ma and ma[0] == index:
                ma.popleft()
            
            if mi and mi[0] == index:
                mi.popleft()
        
        return res
''',
    call=f'Solution().countSubarrays({NUMS}, {K})',
    expect=7,
    views=[
        dict(type='text', size=26, h=55, fn=_info),
        dict(type='array', var='nums', label='nums', pointers={'index': 'blue', 'p': 'pink'}, window=('index', 'p - 1'), h=200,
             dim=lambda S, i, v: 'p' in S and 'index' in S and not (S['index'] <= i < S['p'])),
        dict(type='queue', var='ma', label='ma（下标:值，队首 = 窗口最大）', fmt=lambda i: f'{i}:{NUMS[i]}', h=110),
        dict(type='queue', var='mi', label='mi（下标:值，队首 = 窗口最小）', fmt=lambda i: f'{i}:{NUMS[i]}', h=110),
    ],
    watch=[('index', 'index', 'blue'), ('p', 'p', 'pink'), ('x', 'x', 'orange'), ('y', 'y', 'cyan'), ('res', 'res', 'green')],
    captions={
        'ma = deque()': '`ma`：最大值单调队列，存下标，值递减，队首 = 窗口最大',
        'mi = deque()': '`mi`：最小值单调队列，存下标，值递增，队首 = 窗口最小',
        'p = 0': '`p` 是合法区间的右边界（开区间），==只往右走，不回头==',
        'for index, v': lambda S, B, r: ('每个左端点都处理完了' if B.get('index') == S.index and 'v' in B
                                          else f'枚举左端点 `index = {S.index}`，先让 `p` 尽量往右扩'),
        'while p < len(nums)': lambda S, B, r: (f'`p = {S.p}` 还没越界 → 尝试把 `nums[{S.p}]` 加进窗口' if S.p < len(S.nums)
                                                 else '`p` 到头了，不能再扩'),
        'x = max(nums[ma[0]], x)': '窗口最大 = `max(队首 {nums[ma[0]]}, 新元素 {nums[p]})` = `{x}`',
        'y = min(nums[mi[0]], y)': '窗口最小 = `min(队首 {nums[mi[0]]}, 新元素 {nums[p]})` = `{y}`',
        'x = nums[p]': '先假设窗口里只有 `nums[{p}] = {x}`',
        'y = nums[p]': '同理最小值先取 `{y}`',
        'if (x - y)': lambda S, B, r: (
            f'试算开销 `({S.x} − {S.y}) × {S.p - S.index + 1}` = =={(S.x - S.y) * (S.p - S.index + 1)}== '
            + (f'> k={S.k} → 加入后超标，`p` 不能再扩' if (S.x - S.y) * (S.p - S.index + 1) > S.k else f'≤ k={S.k} → 可以加入')),
        'break': '开销超了，==right 越大开销越大==，停止扩展，跳出内层循环',
        'while ma and nums[ma[-1]] <= nums[p]': lambda S, B, r: (
            f'队尾 `{S.nums[S.ma[-1]]} ≤ {S.nums[S.p]}`：它更早离开窗口还不如新元素大 → 弹出'
            if S.ma and S.nums[S.ma[-1]] <= S.nums[S.p] else '队尾比新元素大（或队列空）→ 停止弹出'),
        'ma.pop()': '弹出 `ma` 队尾',
        'ma.append(p)': '下标 `{p}` 进 `ma`，保持递减',
        'while mi and nums[mi[-1]] >= nums[p]': lambda S, B, r: (
            f'队尾 `{S.nums[S.mi[-1]]} ≥ {S.nums[S.p]}`：它更早离开窗口还不如新元素小 → 弹出'
            if S.mi and S.nums[S.mi[-1]] >= S.nums[S.p] else '队尾比新元素小（或队列空）→ 停止弹出'),
        'mi.pop()': '弹出 `mi` 队尾',
        'mi.append(p)': '下标 `{p}` 进 `mi`，保持递增',
        'p += 1': '`nums[{B.p}]` 成功加入 → `p` 扩到 {p}',
        'res += p - index': '右端点在 `[{index}, {p - 1}]` 的区间都合法，共 `{p} − {index}` = `{p - index}` 个 → res = =={res}==',
        'if ma and ma[0] == index': lambda S, B, r: (f'`ma` 队首正好是 `index = {S.index}` → 它要离开窗口了，弹出' if S.ma and S.ma[0] == S.index
                                                      else '`ma` 队首不是 `index` → 保留'),
        'ma.popleft()': '`ma` 队首过期，出队',
        'if mi and mi[0] == index': lambda S, B, r: (f'`mi` 队首正好是 `index = {S.index}` → 弹出过期的队首' if S.mi and S.mi[0] == S.index
                                                      else '`mi` 队首不是 `index` → 保留'),
        'mi.popleft()': '`mi` 队首过期，出队',
        'return res': '共有 `{ret}` 个开销 ≤ k 的子数组',
    },
    skip=['x = nums[p]', 'y = nums[p]', 'if ma:', 'if mi:', 'ma.pop()', 'mi.pop()'],
    max_steps=130,
    cards=dict(
        one_liner='左端点右移，右端点只增不减；单调队列取窗口最值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['子数组开销 = `(最大值 − 最小值) × 长度`，数有多少个开销 `≤ k` 的子数组',
                 '示例：`nums = [1,3,2], k = 4` → `5`',
                 '本视频：`nums = [1,3,2,4], k = 4` → `7`'],
        quote='对于一个固定的left，当right越大时，max越大而min越小；(right - left + 1)也越大，也就是说right越大，对应的cost就越大。',
        quote_src='—— yiduobo 题解原文',
        idea=['固定 `left`，`right` 越大开销越大；固定 `right`，`left` 越大开销越小',
              '所以 `index` 的最大合法右边界 `p` 不会比上一个 `index` 的更小：`p` 只增不减',
              '先试算再加入：用队首和 `nums[p]` 算 max/min，合法才入队、`p += 1`',
              '右端点在 `[index, p-1]` 都合法，累加 `p - index`'],
        summary=['时间 `O(n)`：`p` 和 `index` 各走一遍，每个元素入队出队各两次',
                 '先「试算」再入队：开销超标时 `p` 不动，下一轮 `index` 变大再试',
                 '队首等于 `index` 才弹出，因为队列存的是下标',
                 '对比灵神：灵神枚举右端点、超标就缩左端点；yiduobo 枚举左端点、向右扩展右端点',
                 '原文可直接运行，无改动'],
    ),
)
