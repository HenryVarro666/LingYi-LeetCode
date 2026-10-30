CONFIG = dict(
    num=3684, title='至多 K 个不同元素的最大和', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='降序排序 + 逐个去重',
    tags=['灵神题单', '滑动窗口与双指针'],
    code='''
class Solution(object):
    def maxKDistinct(self, nums, k):
        
        res = []
        for v in sorted(nums, reverse=True):
            if not res or res[-1] != v:
                res.append(v)
            if len(res) == k:
                break
        
        return res
''',
    call='Solution().maxKDistinct([84,93,100,77,93], 3)',
    expect=[100, 93, 84],
    views=[
        dict(type='array', var='nums', h=200, label='nums（原数组）'),
        dict(type='array', var=lambda S: sorted(S['nums'], reverse=True), h=200, label='从大到小排序后（v 在其中遍历）',
             color=lambda S, i, v: 'blue' if S.get('v') == v and 'res' in S and S['res'] and S['res'][-1] == v else None),
        dict(type='array', var='res', h=200, label='res（答案）', color=lambda S, i, v: 'green'),
    ],
    watch=[('v', 'v', 'blue'), ('len(res)', 'len(res)', 'cyan'), 'k'],
    captions={
        'res = []': '`res` 存选出来的数，保持严格递减',
        'for v in sorted': '按从大到小取下一个数 `v = {v}`',
        'if not res or res[-1] != v': '{"`res` 还是空 → 直接选" if not B.res else "`res` 末尾是 " + str(B.res[-1]) + "，`v` 是 " + str(v) + "：" + ("不同 → 选它" if B.res[-1] != v else "相同 → 重复，跳过")}',
        'res.append(v)': '`{v}` 加入答案：`res = {res}`',
        'if len(res) == k': '`len(res) = {len(res)}`，`k = {k}`：{"选够了，停止" if len(res) == k else "还不够，继续"}',
        'break': '已选够 `k` 个，提前结束',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='从大到小排好，跳过重复的，选满 k 个就停',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['正整数数组 `nums`，选至多 `k` 个互不相同的数使和最大',
                 '按递减顺序返回选出的数',
                 '示例：`[84,93,100,77,93], k=3` → `[100,93,84]`'],
        quote='将nums按从大到小的顺序进行排序，接下来一趟遍历，若当前答案数组为空，或者答案数组的最后一个元素与当前元素不同，则将其加入到答案数组中。',
        quote_src='—— yiduobo 题解原文',
        idea=['降序排序后，相同的数挨在一起',
              '只和 `res` 最后一个数比：不同才是新数，加入',
              '`len(res) == k` 立刻 `break`'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '`not res` 判空要放在 `res[-1]` 前，避免越界',
                 '`break` 在 append 之后判断，所以 k 个刚好选满',
                 '原文本身已兼容 Python 3，无需修改',
                 '对比灵神：灵神用 `set` 去重 + `nlargest`，yiduobo 手写相邻去重'],
    ),
)
