def _txt(S):
    if 'cnt' not in S or 'num' not in S:
        return ''
    p = S['pos_dict'][S['num']]
    if 'right_res' in S and S['_line'] >= 15 and 'index' in S:
        return (f"左 `{S['index']}×{p[S['index']]} − {S['now_sum'] - p[S['index']]}` = {S['left_res']}；"
                f"右 `{S['all_sum']} − {S['now_sum']} − {S['cnt'] - S['index'] - 1}×{p[S['index']]}` = {S['right_res']}")
    return f"值 `{S['num']}` 的下标 `{p}`，总和 `all_sum = {S.get('all_sum', '?')}`"


CONFIG = dict(
    num=2121, title='相同元素的间隔之和', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表分组 + 前缀和',
    tags=[],
    code='''
class Solution(object):
    def getDistances(self, arr):

        pos_dict = {}
        for index, num in enumerate(arr):
            if num not in pos_dict:
                pos_dict[num] = []
            pos_dict[num].append(index)
        
        res = [0] * len(arr)
        for num in pos_dict:
            cnt = len(pos_dict[num])
            all_sum = sum(pos_dict[num])
            now_sum = 0
            for index in range(cnt):
                left_res = index * pos_dict[num][index] - now_sum
                now_sum += pos_dict[num][index]

                right_res = all_sum - now_sum - (cnt - index - 1) * pos_dict[num][index]

                res[pos_dict[num][index]] = left_res + right_res
        
        return res
''',
    call='Solution().getDistances([2,1,3,1,2,3,3])',
    expect=[4, 2, 7, 2, 4, 4, 5],
    max_steps=80,
    skip=['pos_dict = {}', 'res = [0]', 'pos_dict[num] = []'],
    views=[
        dict(type='array', var='arr', label='arr（蓝 = 当前这一组的元素，粉 = 正在算的元素）', cell=90, h=190,
             color=lambda S, i, v: ('pink' if S['_line'] >= 16 and 'cnt' in S and S['pos_dict'][S['num']][S['index']] == i
                                    else 'blue' if S['_line'] >= 12 and 'cnt' in S and i in S['pos_dict'][S['num']] else None)),
        dict(type='map', var='pos_dict', label='pos_dict（值 → 下标列表）', fmt=lambda k, v: f'{k}: {v}', font=30, h=190),
        dict(type='array', var='res', label='res（间隔和）', cell=90, h=170),
        dict(type='text', fn=_txt, size=26, h=90),
    ],
    watch=[('index', 'index', 'pink'), ('cnt', 'cnt'), ('all_sum', 'all_sum', 'blue'), ('now_sum', 'now_sum', 'yellow'),
           ('left_res', 'left_res', 'cyan'), ('right_res', 'right_res', 'orange')],
    captions={
        'if num not in pos_dict': '值 `{num}` 第一次出现吗？',
        'pos_dict[num].append(index)': '下标 `{index}` 记进 `pos_dict[{num}] = {pos_dict[num]}`',
        'for num in pos_dict': '处理值 `{num}` 这一组，下标 `{pos_dict[num]}`',
        'cnt = len': '这组共 `cnt = {cnt}` 个下标',
        'all_sum = sum': '先求整组下标总和 `all_sum = {all_sum}`：右侧区间和要用它减前缀和',
        'now_sum = 0': '`now_sum` 记录已经走过的下标和（前缀和），边走边累加',
        'for index in range(cnt)': '处理组内第 `{index}` 个下标 `{pos_dict[num][index]}`',
        'left_res =': '左半部分：`{index}` 个下标，每个差 `x − 前面的`：`{index}×{pos_dict[num][index]} − {B.now_sum}` = =={left_res}==',
        'now_sum +=': '把当前下标加进前缀和：`now_sum = {now_sum}`',
        'right_res =': '右半部分：后面 `{cnt - index - 1}` 个下标：`{all_sum} − {now_sum} − {cnt - index - 1}×{pos_dict[num][index]}` = =={right_res}==',
        'res[pos_dict[num][index]] =': '下标 `{pos_dict[num][index]}` 的答案 = `{left_res} + {right_res}` = =={left_res + right_res}==',
        'return res': '全部算完：`{ret}`',
    },
    cards=dict(
        one_liner='把绝对值拆成左右两段，用前缀和一步求出区间和',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`intervals[i]` = `arr[i]` 与每个相同元素的下标差的绝对值之和',
                 '示例：`[2,1,3,1,2,3,3]` → `[4,2,7,2,4,4,5]`',
                 '本视频用的就是这个示例'],
        quote='该下标与其他下标间隔之和可以分为左右两个部分……可以发现，在这里就变成了求解两个区间和。对于区间和问题，经典的做法就是采用前缀和来进行优化。',
        quote_src='—— yiduobo 题解原文',
        idea=['哈希表把相同元素的下标按从左到右聚合，设为 `nums`，长度 `cnt`',
              '左半 = `nums[index]×index − 前面下标之和`；右半 = `后面下标之和 − nums[index]×(cnt−index−1)`',
              '左边前缀和边遍历边算；右边 = 总和 − 前缀和，不用预处理数组'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：`now_sum` 要先算 `left_res`，再加入当前下标，然后算 `right_res`',
                 '对比灵神：灵神用相邻元素的变化量递推，yiduobo 直接用前缀和拆成左右两段',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
