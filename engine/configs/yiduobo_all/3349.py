NUMS = [2, 5, 7, 8, 9, 2, 3, 4, 3, 1]


def _states():
    """模拟原代码：返回每处理完 nums[i] 时的 (pre_len, now_len)，用来在可视化里定位当前元素"""
    out = {0: (0, 1)}
    pl, nl = 0, 1
    for i in range(1, len(NUMS)):
        if NUMS[i] > NUMS[i - 1]:
            nl += 1
        else:
            pl, nl = nl, 1
        out[i] = (pl, nl)
    return out


ST = _states()


def _pos(S):
    """当前正在处理的下标（v 在 nums 里的位置）"""
    if 'v' not in S:
        return 0
    v, pl, nl = S['v'], S['pre_len'], S['now_len']
    for i in range(1, len(NUMS)):
        if NUMS[i] == v and (ST[i] == (pl, nl) or ST[i - 1] == (pl, nl)):
            return i
    return len(NUMS) - 1


def _run_id(i):
    r = 0
    for j in range(1, i + 1):
        if NUMS[j] <= NUMS[j - 1]:
            r += 1
    return r


def _color(S, i, v):
    if 'now_len' not in S:
        return None
    p = _pos(S)
    if i > p:
        return None
    return 'green' if _run_id(i) % 2 == 0 else 'cyan'


def _txt(S):
    if 'now_len' not in S:
        return '先求「最大可能的 k」，再和题目给的 `k=3` 比较'
    return f'上一段递增长度 `pre_len = {S["pre_len"]}`，当前段长度 `now_len = {S["now_len"]}`；目前最大 k = =={S.get("res", 0)}=='


CONFIG = dict(
    num=3349, title='检测相邻递增子数组 I', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='拆成最长递增段 · 求最大 k', tags=[],
    code='''
class Solution(object):
    def maxIncreasingSubarrays(self, nums):
        
        res = 0
        pre_len = 0
        pre = nums[0]
        now_len = 1
        for v in nums[1:]:
            if v > pre:
                now_len += 1
            else:
                res = max(res, now_len // 2, min(pre_len, now_len))
                pre_len = now_len
                now_len = 1
            
            pre = v
        
        res = max(res, now_len // 2, min(pre_len, now_len))
        return res
''',
    setup='',
    call='Solution().maxIncreasingSubarrays([2,5,7,8,9,2,3,4,3,1]) >= 3',
    expect=True,
    views=[
        dict(type='text', fn=_txt, h=70, size=26),
        dict(type='array', var='nums', label='nums（相同颜色 = 同一段递增）', h=230,
             pointers={_pos: 'blue'}, pointer_labels={_pos: 'v'},
             color=_color,
             dim=lambda S, i, v: 'now_len' in S and i > _pos(S)),
    ],
    watch=['v', 'pre', ('pre_len', 'pre_len', 'cyan'), ('now_len', 'now_len', 'green'), ('res', 'res', 'yellow')],
    captions={
        'res = 0': '`res` 记录「最大可能的 k」，最后和题目的 `k` 比较',
        'pre = nums[0]': '`pre` 是上一个数，从 `nums[0] = {pre}` 开始',
        'now_len = 1': '`now_len = 1`：当前递增段暂时只有 `nums[0]`',
        'for v in nums[1:]': lambda S, B, r: (f'依次看后面每个数 `v = {S.v}`' if 'now_len' in S and S._line == 8 and B.get('v') != S.v or S.get('pre') != S.v else '数组走完，别忘了还要结算最后一段'),
        'if v > pre': lambda S, B, r: (f'`{S.v} > {S.pre}` → 仍严格递增，当前段继续' if S.v > S.pre else f'`{S.v} <= {S.pre}` → 递增断了，要结算这一段'),
        'now_len += 1': '当前递增段长度 `now_len` → =={now_len}==',
        'res = max(res, now_len': lambda S, B, r: f'一段断开：k 取 `{S.now_len}//2 = {S.now_len // 2}`（从段中间劈开）或 `min({S.pre_len}, {S.now_len}) = {min(S.pre_len, S.now_len)}`（相邻两段），`res = {S.res}`' if 'now_len' in S else '',
        'pre_len = now_len': '当前段变成「上一段」：`pre_len = {pre_len}`',
        'now_len = 1': lambda S, B, r: ('当前递增段暂时只有 `nums[0]`，`now_len = 1`' if S['_line'] == 7 else '新的一段从 `v` 开始，`now_len = 1`'),
        'pre = v': '`pre` 更新为 `{pre}`',
        'return res': '最大的 `k = {res}`；题目 `k = 3`，`{res} >= 3` → ==存在==，返回 `True`',
    },
    skip=['pre = v'],
    max_steps=80,
    cards=dict(
        one_liner='先求最大可能的 k，再和题目的 k 比大小',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['找两个==相邻==、长度都是 `k` 的严格递增子数组（第二个紧接在第一个后面）',
                 '示例：`[2,5,7,8,9,2,3,4,3,1]`，`k=3` → `true`',
                 '`[7,8,9]` 和 `[2,3,4]` 紧挨着，都严格递增'],
        quote='实际上只需要知道3350题中最大可能的k是多少，对比3349题中指定的k就可以得到3349题的答案，因此在这里先将问题统一成最大可能的k是多少。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历，把数组拆成若干段==尽量长的递增段==',
              '情况一：相邻两段，k 取 `min(前一段长, 后一段长)`',
              '情况二：同一段从中间劈开，k 取 `段长 // 2`',
              '所有情况取最大，再判断 `最大 k >= k`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '本视频演示原文给出的 3350 版函数 `maxIncreasingSubarrays`，3349 的答案 = `该函数结果 >= k`',
                 '易错：循环结束后还要结算最后一段，否则漏掉',
                 '易错：`v > pre` 是严格递增，相等也算断开',
                 '原文为 Python 2 风格，代码未改，只删去了类型说明文档字符串'],
    ),
)
