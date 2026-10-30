CONFIG = dict(
    num=1546, title='和为目标值且不重叠的非空子数组的最大数目', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和 + 集合，贪心取最早',
    tags=['灵神题单·常用数据结构', '灵神题单·贪心与思维'],
    code='''
class Solution(object):
    def maxNonOverlapping(self, nums, target):

        n = len(nums)
        pos = 0
        res = 0
        while pos < n:
            s = set([0])
            now = 0
            while pos < n:
                now += nums[pos]
                pos += 1
                if now - target in s:
                    res += 1
                    break
                
                s.add(now)
        
        return res
''',
    call='Solution().maxNonOverlapping([-1,3,5,1,4,2,-9], 6)',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（箭头 = 下一个要读的位置 pos）', pointers={'pos': 'blue'}, h=230),
        dict(type='set', var='s', label='s：当前这一段里出现过的前缀和（含 0）', fmt=lambda x: str(x), h=170),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"`now = {S['now']}`，`now − target = {S['now'] - S['target']}`" if 'now' in S and 's' in S else '')),
    ],
    watch=['pos', 'now', 'target', ('res', 'res', 'green')],
    captions={
        's = set': '新开一段：集合只放 `0`（空前缀），不带上一段的前缀和，这样下一段不会和上一段重叠',
        'now += nums': '`now` 是这一段的前缀和：加上 `nums[{pos}]` → =={now}==',
        'if now - target in s': '看 `now − target = {now - target}` 在不在集合里：{"==在==，说明有一段和恰好为 target" if (now - target) in s else "不在，还凑不出和为 target 的段"}',
        'res += 1': '找到一段，而且是最靠前结束的：留给后面的空间最大。答案加一 → =={res}==',
        'break': '清空重来：跳出内层循环，回到外层重新建集合、`now` 清零',
        's.add': '没找到，把 `now = {now}` 记进集合，留给后面的位置当“起点前缀和”',
        'return res': '扫完整个数组，最多能切出 =={res}== 段',
    },
    cards=dict(
        one_liner='重叠就留靠前的：一找到就切一刀，前缀和从头再来',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['在数组里选尽量多段不重叠、和等于 `target` 的非空子数组',
                 '示例：`nums=[-1,3,5,1,4,2,-9]`，`target=6` → 答案 2',
                 '（`[5,1]` 和 `[4,2]`，互不相交）'],
        quote='对于两个存在重叠部分的合法的子数组而言，显然应该保留下靠前的那一个，这样的话就给后续的选择留下了更多的可能性。',
        quote_src='—— yiduobo 题解',
        idea=['从左往右扫，维护这一段的前缀和 `now`',
              '`now − target` 在集合里 → 刚好有一段和为 target，答案 +1，清零清空',
              '没出现就把 `now` 加入集合，继续往后'],
        summary=['时间 `O(n)`，空间 `O(n)`（集合最长为一段的长度）',
                 '易错点：集合要先放 `0`，否则从段首开始的子数组会漏掉',
                 '易错点：找到后必须 `now` 清零且清空集合，否则下一段会和这一段重叠',
                 '同类：560 和为 K 的子数组（前缀和 + 哈希表）'],
    ),
)
