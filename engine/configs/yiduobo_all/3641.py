def _wr(S):
    p, i = S.get('p'), S.get('index')
    if p is None or i is None or p - 1 < i:
        return None
    return p - 1


def _wl(S):
    p, i = S.get('p'), S.get('index')
    if p is None or i is None or p - 1 < i:
        return None
    return i


def _txt(S):
    if 'dup' not in S:
        return ''
    return f"窗口里重复的元素有 `dup = {S['dup']}` 种（上限 `k = {S['k']}`）"


CONFIG = dict(
    num=3641, title='最长半重复子数组', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='变长滑动窗口 · cnt 计数 + dup 重复种数',
    tags=[],
    code='''
class Solution(object):
    def longestSubarray(self, nums, k):
        
        cnt = {}
        p = 0
        dup = 0
        res = 0
        for index, v in enumerate(nums):
            while p < len(nums):
                x = nums[p]
                if cnt.get(x, 0) == 1 and dup == k:
                    break
                cnt[x] = cnt.get(x, 0) + 1
                if cnt[x] == 2:
                    dup += 1
                p += 1
            
            res = max(res, p - index)
            cnt[v] -= 1
            if cnt[v] == 1:
                dup -= 1
        
        return res
''',
    call='Solution().longestSubarray([1,2,2,3,1,1,4], 1)',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums（框 = 当前窗口 [index, p)）', pointers={'index': 'pink', 'p': 'blue'},
             window=(_wl, _wr), h=190, cell=90),
        dict(type='map', var='cnt', label='cnt：窗口内每种数的次数', fmt=lambda k, v: f"{k}: {v}", h=150, font=30),
        dict(type='text', h=90, size=30, fn=_txt),
    ],
    watch=[('index', 'index', 'pink'), ('p', 'p', 'blue'), 'dup', ('res', 'res', 'green')],
    captions={
        'cnt = {}': '`cnt` 记窗口内每种数的次数，`dup` 记“出现不止一次”的数有几种',
        'p = 0': '`p` 是窗口右边界（开区间），只增不减',
        'while p < len': '`p = {p}`：{"还没到数组末尾，尝试吸收 nums[p]" if p < len(nums) else "已到数组末尾，不能再扩了"}',
        'x = nums[p]': '看看下一个数 `x = {x}`',
        'if cnt.get(x, 0) == 1': '`x = {x}` 窗口里已有 `{cnt.get(x, 0)}` 个，`dup = {dup}`，`k = {k}`：{"再加它会多出一种重复，而重复种数已满 k → 停下" if cnt.get(x, 0) == 1 and dup == k else "加入后不会超过 k 种重复 → 可以吸收"}',
        'break': '窗口不能再往右了，当前右边界就是 `p = {p}`',
        'cnt[x] = cnt.get': '`{x}` 进窗口，次数变成 `{cnt[x]}`',
        'if cnt[x] == 2': '{"这个数刚好变成第 2 次：成了重复元素，`dup` 加 1 → " + str(dup + 1) if cnt[x] == 2 else "次数是 " + str(cnt[x]) + "，不是 2，重复种数不变"}',
        'dup += 1': '`dup` → {dup}',
        'p += 1': '右边界右移：`p` → {p}',
        'res = max': '窗口长度 `p - index = {p - index}`，`res = max({B.res}, {p - index}) = {res}`',
        'cnt[v] -= 1': '左边界 `{v}` 离开窗口，它的次数变成 `{cnt[v]}`',
        'if cnt[v] == 1': '{"次数从 2 降到 1：它不再重复，`dup` 减 1 → " + str(dup - 1) if cnt[v] == 1 else ("它在窗口里已经没有了" if cnt[v] == 0 else "它仍重复（次数大于 1），重复种数不变")}',
        'dup -= 1': '`dup` → {dup}',
        'return res': '最长半重复子数组长度 `{res}`',
    },
    skip=['x = nums[p]', 'p += 1', 'dup += 1', 'dup -= 1'],
    max_steps=110,
    cards=dict(
        one_liner='左边界右移时右边界不回头，窗口只前进',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给定整数数组 `nums` 和整数 `k`：窗口里“重复的元素”最多 `k` 种，称为半重复子数组',
                 '求最长的半重复子数组长度',
                 '本视频：`[1,2,2,3,1,1,4]`，`k=1` → `5`'],
        quote='对于以 index 为左边界的最长半重复子数组的右边界为 r，那么对于 index + 1 为左边界的，右边界必然是大于等于 r 的。',
        quote_src='—— yiduobo 题解原文',
        idea=['枚举左边界 `index`，在上一轮基础上把右边界 `p` 尽量右推',
              '`cnt` 记次数，某个数次数刚到 2 就 `dup += 1`',
              '新数已出现 1 次、且 `dup` 已满 `k` → 再加就超标，停下',
              '算完长度后左边界出窗口：次数从 2 降到 1 就 `dup -= 1`'],
        summary=['时间 `O(n)`，空间 `O(n)`：`p` 和 `index` 都只增不减',
                 '先更新答案，再把 `nums[index]` 移出窗口',
                 '判断“会不会新增重复”看的是 `cnt == 1`，不是 `cnt >= 1`',
                 '题意按代码理解：窗口里出现次数不少于 2 的不同元素种数 `<= k`'],
    ),
)
