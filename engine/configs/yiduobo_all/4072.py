CONFIG = dict(
    num=4072, title='一次删除后的最大交替子数组和', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='状态机 DP · 四个滚动变量',
    code='''
class Solution(object):
    def maxAlternatingSum(self, nums):
        
        f, g, h, t = nums[0], None, None, None
        res = nums[0]
        for v in nums[1:]:
            pre_f, pre_g, pre_h, pre_t = f, g, h, t
            f = v
            if pre_g is not None and pre_g > 0:
                f += pre_g
            res = max(res, f)

            g = pre_f - v
            res = max(res, g)

            h = pre_f
            if pre_t is not None:
                h = max(h, pre_t + v)
            res = max(res, h)

            t = None
            if pre_g is not None:
                t = pre_g
            if pre_h is not None and (t is None or t < pre_h - v):
                t = pre_h - v
                
            if t is not None:
                res = max(res, t)

        return res
''',
    call='Solution().maxAlternatingSum([2, -1, 4, 3, -2])',
    expect=9,
    views=[
        dict(type='array', var='nums', label='nums', h=200),
        dict(type='text', size=34, fn=lambda S: (f"未删：`f` 末位加 = =={S['f']}==　`g` 末位减 = =={S['g']}==" if 'f' in S else '')),
        dict(type='text', size=34, fn=lambda S: (f"已删：`h` 末位加 = =={S['h']}==　`t` 末位减 = =={S['t']}==" if 'f' in S else '')),
        dict(type='text', fn=lambda S: f"答案 `res` = =={S['res']}==" if 'res' in S else ''),
    ],
    watch=['v', 'f', 'g', 'h', 't', ('res', 'res', 'green')],
    captions={
        'f, g, h, t = nums[0]': '第 0 个元素：`f = nums[0] = {f}`（以它结尾且被加进去）；g/h/t 还不存在',
        'res = nums[0]': '`res = {res}`',
        'for v in nums[1:]': '处理下一个元素 `v = {v}`',
        'pre_f, pre_g': '先把上一轮的 f/g/h/t 存进 `pre_*`，保证四个状态都用旧值更新',
        'f = v': '`f` 另立门户：从 `v = {v}` 重新开始',
        'f += pre_g': '`pre_g = {pre_g} > 0`：接在 g 后面有赚 → `f = {f}`',
        'g = pre_f - v': '`g = pre_f − v = {pre_f} − ({v}) = {g}`：v 被减掉，只能接在 f 后',
        'h = pre_f': '`h` 先取 `pre_f = {pre_f}`：未删时到上一位，删掉 v 本身',
        'h = max(h, pre_t + v)': '`h = max({B.h}, {pre_t} + ({v}))` = {h}：已删过，接在 t 后面加上 v',
        't = None': '`t` 重新计算：先设为不存在',
        't = pre_g': '`t = pre_g = {pre_g}`：未删时到 g，删掉 v 本身',
        't = pre_h - v': '`t = pre_h − v = {pre_h} − ({v}) = {t}`：已删过，接在 h 后面减去 v',
        'res = max': '`res = max(…)` = =={res}==：每个状态都可能是答案',
        'return res': '最大交替子数组和 `{res}`',
    },
    cards=dict(
        one_liner='未删、已删各两个状态：末位被加、末位被减',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['最多删除 `nums` 中一个元素，再选一个子数组',
                 '交替和 = 偶数下标之和 − 奇数下标之和（下标从子数组起点算）',
                 '求最大交替和。本视频：`[2,-1,4,3,-2]`'],
        quote='f[index]与g[index]在没有执行过删除操作这一前提下保持原意，另外h[index]与t[index]则表示执行过删除操作后',
        quote_src='—— yiduobo 题解原文',
        idea=['先想不删的版本：`f` 末位被加，可接 g 或自立；`g` 末位被减，只能接 f',
              '加入删除后多两个状态 `h`、`t`，表示已经删过',
              '`h` 来自 `pre_f`（删掉当前）或 `pre_t + v`；`t` 来自 `pre_g` 或 `pre_h − v`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：必须先存 `pre_*` 再更新，四个状态互相依赖',
                 '用 `None` 表示状态不存在，别当成 0',
                 '删除可发生在子数组内部，被删元素不占奇偶位置',
                 '原文为 Python 2 风格（`class Solution(object)`），代码无需修改'],
    ),
)
