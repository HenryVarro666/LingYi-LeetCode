CONFIG = dict(
    num=2966, title='划分数组并满足最大差限制', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='排序后三个一组',
    code='''
class Solution:
    def divideArray(self, nums: List[int], k: int) -> List[List[int]]:
        nums.sort()
        ans = []
        for i in range(0, len(nums), 3):
            if nums[i + 2] - nums[i] > k:
                return []
            ans.append(nums[i: i + 3])
        return ans
''',
    call='Solution().divideArray([1,3,4,8,7,9,3,5,1], 2)',
    expect=[[1, 1, 3], [3, 4, 5], [7, 8, 9]],
    views=[
        dict(type='array', var='nums', pointers={'i': 'blue'}, h=220,
             color=lambda S, j, v: 'blue' if 'i' in S and S['i'] <= j <= S['i'] + 2 else None),
        dict(type='text', fn=lambda S: f"这一组 `{S['nums'][S['i']:S['i']+3]}`：最大 − 最小 = `{S['nums'][S['i']+2]} − {S['nums'][S['i']]}` = =={S['nums'][S['i']+2]-S['nums'][S['i']]}==，限制 `k = {S['k']}`" if 'i' in S else '先排序，再三个一组切'),
        dict(type='text', fn=lambda S: f"已切出的组：`{S['ans']}`" if 'ans' in S else ''),
    ],
    watch=['i', 'k', ('ans', 'ans', 'green')],
    captions={
        'nums.sort': '排序后，最小值 x 必须和次小 y、第三小 z 同组，否则别的组要和更小的数在一起，更难满足 → 排完直接三个一组',
        'if nums[i + 2]': '这组最大最小差 `{nums[i + 2]} - {nums[i]} = {nums[i + 2] - nums[i]}`，和 `k = {k}` 比 → =={"超过，无解" if nums[i + 2] - nums[i] > k else "不超过，合法"}==',
        'return []': '差超过 `k`：这一组已经是最优分法，仍不满足 → 无解，返回空列表',
        'ans.append': '这一组合法，收进答案：`{nums[i: i + 3]}`',
        'return ans': '所有组都满足，返回 `ans`',
    },
    cards=dict(
        one_liner='排序后三个一组，组内最大最小之差超过 k 就无解',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['把数组分成若干个长度为 3 的组（是子集，不是连续子数组）',
                 '每组任意两数之差 `<= k`，返回任意一种分法，不行返回 `[]`',
                 '示例：`[1,3,4,8,7,9,3,5,1], k=2` → `[[1,1,3],[3,4,5],[7,8,9]]`'],
        quote='对于 nums 的最小值 x 来说，应该把 x 与次小值 y 和第三小值 z 放在同一组。',
        quote_src='—— 灵茶山艾府题解',
        idea=['若最小值不和次小、第三小同组，别的组就要和更小的 y、z 在一起，只会更糟',
              '所以排序后从小到大每三个一切，只检查每组首尾之差'],
        summary=['时间 `O(n log n)`，瓶颈在排序',
                 '易错：题目的“子数组”是子集，可以打乱顺序',
                 '只需检查每组 `nums[i+2] - nums[i]`，中间数自然满足'],
    ),
)
