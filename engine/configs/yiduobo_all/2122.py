CONFIG = dict(
    num=2122, title='还原原数组', difficulty='Hard', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举 2k + 单调双指针验证',
    tags=['灵神题单', '难度分 2159'],
    code='''
class Solution(object):
    def recoverArray(self, nums):

        def check(double_k):
            used = set()
            p = 0
            for index in range(len(sorted_nums)):
                if index not in used:
                    if p <= index:
                        p = index + 1
                    while p < len(sorted_nums) and sorted_nums[p] != sorted_nums[index] + double_k:
                        p += 1
                    if p == len(sorted_nums):
                        return False

                    used.add(p)
                    p += 1
                    res.append(sorted_nums[index] + double_k // 2)
            
            return True
        
        sorted_nums = sorted(nums)
        for num in sorted_nums[1:]:
            double_k = num - sorted_nums[0]
            res = []
            if double_k % 2 == 0 and double_k > 0 and check(double_k):
                break
        
        return res
''',
    call='Solution().recoverArray([8,5,11,2,10,4])',
    expect=[5, 7, 8],
    views=[
        dict(type='text', size=28, h=80, fn=lambda S: (
            f"试 `{S['num']}` 当 `arr[0] + k` → `2k = {S['double_k']}`"
            if 'double_k' in S and 'num' in S else '先排序：最小的数一定是 lower[0]')),
        dict(type='array', var='sorted_nums', h=260, label='sorted_nums（粉 = 已配成 higher，蓝 = 当前 lower）',
             pointers={'index': 'blue', 'p': 'pink'},
             color=lambda S, k, v: ('pink' if 'used' in S and k in S['used'] else 'blue' if S.get('index') == k else None)),
        dict(type='set', var='used', h=110, label='used：已配成 higher 的下标'),
        dict(type='array', var='res', h=130, label='res：还原出的 arr'),
    ],
    skip=['res = []', 'if p <= index', 'used = set()', 'if p == len'],
    max_steps=52,
    watch=[('double_k', 'double_k', 'yellow'), ('index', 'index', 'blue'), ('p', 'p', 'pink'), 'res'],
    captions={
        'sorted_nums = sorted': '先排序：`sorted_nums[0]` 必然是 `arr[0] − k`，所有数都是正数，它不可能是 higher',
        'for num in sorted_nums[1:]': '试 `{num}` 当作 `arr[0] + k`：它和最小值的差正好是 `2k`',
        'double_k = num': '`double_k = {num} − {sorted_nums[0]} = {double_k}`',
        'res = []': '清空 `res`，重新还原',
        'if double_k % 2 == 0': lambda S, B, r: (f"`2k = {S.double_k}` 必须是正偶数：" + ("成立，去验证每个数能否配对" if S.double_k % 2 == 0 and S.double_k > 0 else "不成立（奇数），==换下一个候选==")),
        'used = set()': '`used` 记哪些下标已经当过 higher',
        'p = 0': '`p` 是找配对 higher 的指针，==只往右走，不回头==',
        'for index in range': lambda S, B, r: (f"检查 `sorted_nums[{S.index}]`" if 'index' in S else "每个数都配好了"),
        'if index not in used': lambda S, B, r: (f"下标 `{S.index}` 已经是别人的 higher，跳过" if S.index in S.used else f"下标 `{S.index}` 不在 `used` → 它是 lower，要给它找 higher"),
        'p = index + 1': '`p` 落后了就追到 `index + 1`：higher 必须在 lower 的右边',
        'while p < len': lambda S, B, r: ((f"找 `{S.sorted_nums[S.index]} + {S.double_k} = {S.sorted_nums[S.index] + S.double_k}`：`sorted_nums[{S.p}] = {S.sorted_nums[S.p]}` 不是它 → `p` 右移" if S.p < len(S.sorted_nums) and S.sorted_nums[S.p] != S.sorted_nums[S.index] + S.double_k else (f"`sorted_nums[{S.p}] = {S.sorted_nums[S.p]}` 正好是 `lower + 2k` → 找到了" if S.p < len(S.sorted_nums) else "`p` 走到头了，没找到配对"))),
        12: '没配上，`p` 右移一格 → {p}',
        'if p == len': lambda S, B, r: ("`p == len`：找不到 higher，这个 `2k` 不合法 → 返回 False" if S.p == len(S.sorted_nums) else f"`p = {S.p}` 在范围内，找到了配对"),
        'return False': '这个 `2k` 验证失败，回到外层试下一个候选',
        'used.add(p)': '`sorted_nums[{p}]` 记为 higher，`used` = {used}',
        17: '`p` 往后一格 → {p}：下一个 lower 的 higher 一定更靠右',
        'res.append': 'arr 的元素 = `lower + k` = `{sorted_nums[index]} + {double_k // 2}` = =={res[-1]}==，`res` = {res}',
        'return True': '全部配对成功，`2k = {double_k}` 合法',
        'break': '找到合法的 `k`，停止枚举',
        'return res': '还原出的数组：=={res}==',
    },
    cards=dict(
        one_liner='最小的数必是 lower[0]，枚举它的 higher 得出 2k，再单调验证',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`arr` 每个数 `-k` 得 `lower`、`+k` 得 `higher`，两数组混在一起打乱成 `nums`',
                 '已知 `nums`（共 `2n` 个数），还原任一合法的 `arr`',
                 '本视频：`[8,5,11,2,10,4]` → `[5,7,8]`（k = 3）'],
        quote='由于题目中所有的数都是正整数，那么必然有sorted_nums[0] = arr[0] - k。……尝试通过sorted_nums[1] - sorted_nums[0]计算出k，然后在sorted_nums中向后遍历验证k是否合法。',
        quote_src='—— yiduobo 题解原文',
        idea=['排序后最小的数一定是 `arr[0] − k`；`arr[0] + k` 在后面某处，',
              '于是逐个试 `sorted_nums[1:]`：差值就是 `2k`，奇数或 0 直接跳过',
              '验证：每个没用过的数 `x` 都要有 `x + 2k` 配对；`p` 随下标单调右移'],
        summary=['时间 `O(n^2)`：最多试 `2n` 个候选，每个验证 `O(n)`',
                 '`double_k` 必须是正偶数，`k` 才是正整数',
                 '`p` 只增不减，所以验证是线性的；重复的数靠 `used` 区分',
                 '原文为 Python 2 写法，`double_k / 2` 已改为 `double_k // 2`'],
    ),
)
