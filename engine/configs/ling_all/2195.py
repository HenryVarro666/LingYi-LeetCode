def _txt(S):
    if 'x' not in S or 'y' not in S or 'fill' not in S:
        return ''
    x, y, fill = S['x'], S['y'], S['fill']
    ys = 'inf' if y == inf else y
    if fill <= 0:
        return f'`{ys} − {x} − 1 = {fill}`：中间没有空位'
    if y == inf or fill >= S['k']:
        return f'空位 `{x+1} … {x+fill if y != inf else "∞"}` 够用，只取前 `k = {S["k"]}` 个：`{x+1} … {x+S["k"]}`'
    return f'`{x}` 和 `{y}` 之间有 `{fill}` 个空位：`{x+1} … {y-1}` 全部填上'


CONFIG = dict(
    num=2195, title='向数组中追加 K 个整数', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='排序 · 哨兵 · 填补空隙',
    tags=['灵神题单', '数学算法', '难度分 1659'],
    code='''
class Solution:
    def minimalKSum(self, nums: List[int], k: int) -> int:
        ans = 0
        nums.extend([0, inf])  # 加入两个哨兵
        nums.sort()
        for x, y in pairwise(nums):
            fill = y - x - 1  # 可以填充的数字个数
            if fill <= 0:  # 没有可以填充的位置
                continue
            if fill >= k:  # 填充剩余的 k 个数
                return ans + (x * 2 + 1 + k) * k // 2  # 等差数列求和
            ans += (x + y) * fill // 2  # 填充 fill 个数：等差数列求和
            k -= fill  # 更新剩余要填充的数字个数
''',
    call='Solution().minimalKSum([5,6,12], 8)',
    expect=44,
    views=[
        dict(type='array', var='nums', label='nums（排序后，两端是哨兵 0 和 inf）', h=240,
             color=lambda S, i, v: ('blue' if 'x' in S and v == S['x'] and 'fill' in S else 'pink' if 'y' in S and v == S['y'] and 'fill' in S else None)),
        dict(type='text', fn=_txt, size=32, h=130),
    ],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), 'fill', 'k', ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 累计已追加数字的和',
        'nums.extend': '加入哨兵 `0` 和 `inf`：开头的空位 `1 … nums[0]-1` 和结尾的无限空位就都能统一成“相邻两数之间”',
        'nums.sort': '排序后，相邻两数之间的空位就是可以追加的数',
        'fill = y - x': '`{x}` 和 `{y}` 之间可填 `{y} − {x} − 1` = =={fill}== 个数',
        'if fill <= 0': '`fill = {fill}`：{"没有空位，看下一对" if fill <= 0 else "有空位，继续"}',
        'if fill >= k': '`fill = {fill}`，剩余 `k = {k}`：{"空位够了 → 只取前 k 个，答案收尾" if fill >= k else "空位不够 → 整段全填，还要继续找"}',
        'return ans': '填 `{x+1} … {x+k}`，和 `({x}*2+1+{k})·{k}/2` = =={ret}==（含之前累计的 `ans`）',
        'ans += (x + y)': '整段 `{x+1} … {y-1}` 等差数列求和：`({x}+{y})·{fill}/2` → `ans` = =={ans}==',
        'k -= fill': '用掉 `{fill}` 个名额，还剩 `k` = =={k}==',
    },
    cards=dict(
        one_liner='排序后，从小到大把相邻数字之间的空位填满',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['向 `nums` 追加 `k` 个没出现过、互不相同的正整数，使和最小',
                 '返回追加的 `k` 个数之和',
                 '示例：`[1,4,25,10,25]`，`k=2` → `5`（追加 2、3）',
                 '本视频：`[5,6,12]`，`k=8` → `44`'],
        quote='排序后，在相邻数字之间填充数字。通过加入两个哨兵来简化代码。',
        quote_src='—— 灵茶山艾府题解',
        idea=['要和最小，就从 1 开始尽量填小的、没出现过的数',
              '排序后，每对相邻数 `x, y` 之间有 `y − x − 1` 个空位',
              '加哨兵 `0` 和 `inf`：开头、结尾也成了普通的“相邻之间”；空位够就取前 `k` 个，不够就整段填完继续'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '重复数字会使 `fill = -1`，所以判断 `fill <= 0`，不能只判 `== 0`',
                 '连续数字求和用等差数列公式，不要逐个加（`k` 最大 10^9）',
                 '`inf` 哨兵保证循环里一定会 `return`，所以函数末尾没有 return'],
    ),
)
