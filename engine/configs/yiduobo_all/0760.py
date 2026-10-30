CONFIG = dict(
    num=760, title='找出变位映射', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表记录下标', tags=[],
    code='''
class Solution(object):
    def anagramMappings(self, nums1, nums2):

        pos = {}
        for index, num in enumerate(nums2):
            if num not in pos:
                pos[num] = []
            pos[num].append(index)
        
        res = []
        for num in nums1:
            res.append(pos[num][-1])
            pos[num].pop()
        
        return res
''',
    call='Solution().anagramMappings([5,3,5,2], [2,5,3,5])',
    expect=[3, 2, 1, 0],
    views=[
        dict(type='array', var='nums2', label='nums2（要查下标的数组）', h=150),
        dict(type='array', var='nums1', label='nums1', h=150),
        dict(type='map', var='pos', label='pos：值 → nums2 中的下标列表', h=260),
        dict(type='array', var='res', label='res（nums1[i] 在 nums2 中的位置）', h=150),
    ],
    watch=['num', ('pos', 'pos', 'cyan'), ('res', 'res', 'green')],
    captions={
        'pos = {}': '`pos` 记录 nums2 里每个数出现过的==所有下标==',
        'for index, num in enumerate(nums2)': '遍历 nums2：第 `{index}` 个数是 `{num}`',
        'if num not in pos': lambda S, B, r: (f'`{S.num}` 第一次出现 → 先建空列表' if S.num not in S.pos or S.pos[S.num] == [] else f'`{S.num}` 已出现过 → 直接追加下标'),
        'pos[num] = []': '为 `{num}` 建一个空下标列表',
        'pos[num].append': '记下 `{num}` 的位置 `{index}`：`pos[{num}] = {pos[num]}`',
        'res = []': '再来填答案 `res`',
        'for num in nums1': '遍历 nums1：现在要给 `{num}` 找一个 nums2 里的下标',
        'res.append': '取 `{num}` 下标列表最后一个：`{pos[num][-1]}`，写进答案 → `res = {res}`',
        'pos[num].pop()': '这个下标用掉了，弹出：重复的数不会==共用同一个位置==，`pos[{num}] = {pos[num]}`',
        'return res': '全部映射完成：`{res}`',
    },
    cards=dict(
        one_liner='先记下 nums2 每个数的所有位置，再给 nums1 逐个分配',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nums2` 是 `nums1` 的变位（打乱顺序，可有重复）',
                 '求映射 `res`：==`nums1[i]` 出现在 `nums2[res[i]]`==',
                 '本视频：`nums1=[5,3,5,2]`，`nums2=[2,5,3,5]` → `[3,2,1,0]`（答案不唯一）'],
        quote='首先对nums2进行一趟遍历，使用哈希表记录nums2中每个数出现的所有下标位置，接下来对nums1进行一趟遍历，根据哈希表中记录的位置填充最终答案即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['哈希表的值是==下标列表==，因为同一个数可能出现多次',
              '遍历 nums1 时从列表末尾取一个并删掉，保证重复数各用各的位置'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '有重复数时必须存==列表==并 `pop`，只存一个下标会让两个 5 映射到同一处',
                 '原文为 Python 2 风格，代码无需修改即可在 Python 3 运行',
                 '答案不唯一，任何合法映射都可以'],
    ),
)
