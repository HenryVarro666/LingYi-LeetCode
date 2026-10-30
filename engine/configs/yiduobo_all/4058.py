CONFIG = dict(
    num=4058, title='一个子数组循环移动后的最大脉冲值', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='分奇偶起点 + 最小子段和',
    tags=['灵神题单·常用数据结构', '难度分 1899'],
    code='''
class Solution(object):
    def maxValue(self, nums):
        
        ori = 0
        f = []
        g = []
        for index, v in enumerate(nums):
            if index % 2 == 0:
                ori += v
                if index + 1 < len(nums):
                    f.append(v - nums[index + 1])
            else:
                ori -= v
                if index + 1 < len(nums):
                    g.append(nums[index + 1] - v)
        
        def calc(arr):
            mi = 0
            s = 0
            for v in arr:
                s += v
                if s > 0:
                    s = 0
                else:
                    mi = min(mi, s)
            
            return mi

        return ori - min(calc(f), calc(g)) * 2
''',
    call='Solution().maxValue([2,6,3,7,1])',
    expect=11,
    views=[
        dict(type='array', var='nums', label='nums（箭头 = 当前下标 index）', pointers={'index': 'blue'}, h=170),
        dict(type='array', var='f', label='f：偶数起点的 nums[i] − nums[i+1]', h=130, cell=70),
        dict(type='array', var='g', label='g：奇数起点的 nums[i+1] − nums[i]', h=130, cell=70),
        dict(type='text', h=110, size=28,
             fn=lambda S: (f"`calc` 中：`s = {S['s']}`（当前累加），最小子段和 `mi = {S['mi']}`" if 'mi' in S and 'arr' in S
                           else f"原脉冲值 `ori = {S['ori']}`" if 'ori' in S else '')),
    ],
    watch=['ori', ('mi', 'mi', 'pink'), 's'],
    captions={
        'ori = 0': '`ori` 记原数组的脉冲值：偶数下标加，奇数下标减',
        'ori += v': '偶数下标 `{index}`，加上 `{v}` → `ori = {ori}`',
        'ori -= v': '奇数下标 `{index}`，减去 `{v}` → `ori = {ori}`',
        'f.append': '偶数起点：把一对相邻元素的“脉冲贡献” `{v} − {nums[index+1]}` = {v - nums[index+1]} 放进 `f`',
        'g.append': '奇数起点：把 `−nums[{index}] + nums[{index+1}]` = {nums[index+1] - v} 放进 `g`',
        'mi = 0': '求偶数长度子数组的最小和，等价于在 `arr` 里求最小子段和；`mi` 从 0 开始（可以不操作）',
        's += v': '`s` 是以当前位置结尾的子段和：加上 `{v}` → `s = {s}`',
        'if s > 0': '`s = {s}`：{"为正，接上去只会更大，丢掉前面，重新从 0 开始" if s > 0 else "不为正，继续保留，可能刷新最小值"}',
        'mi = min': '`mi = min({B.mi}, {s}) = {mi}`：最小子段和越负，取反后增益越大',
        'return ori': '`f`、`g` 中较小的最小子段和是 `{min(calc(f), calc(g))}`，答案 = `ori − 2 × 它` = =={ret}==',
    },
    cards=dict(
        one_liner='把操作拆成奇偶起点，整段取反 = 找最负的偶数长度段',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['脉冲值 = `a0 − a1 + a2 − …`',
                 '选一个子数组循环左移一位，至多一次',
                 '示例：`[2,6,3,7,1]` → 11'],
        quote='题目到了这里就是要找出一段偶数长度的子数组，这个子数组在原脉冲计算中的结果最小。',
        quote_src='—— yiduobo 题解',
        idea=['按起点、终点奇偶分四种情况推导，结果都是“把一整段取反”',
              '偶数长度段 = 两两相邻元素相减，分偶数起点的 `f`、奇数起点的 `g`',
              '对 `f`、`g` 各求最小子段和，较小者 `mi`，答案 = `ori − 2×mi`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：`mi` 从 0 起步，表示可以不操作',
                 '易错点：`s > 0` 就归零，贪心求最小子段和',
                 '同类：53 最大子数组和（取反后同构）'],
    ),
)
