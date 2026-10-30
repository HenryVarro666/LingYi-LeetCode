def _cnt_color(S, i, v):
    ln = S.get('_line')
    num = S['_inner'].get('num')
    if ln == 5 and i == num:
        return 'yellow'
    if ln == 9 and isinstance(num, int) and i == num - 1:
        return 'cyan'
    return 'green' if v else None


def _res_color(S, i, v):
    ln = S.get('_line')
    if ln == 9 and i == len(S['res']) - 1:
        return 'yellow'
    if ln == 9 and i == len(S['res']) - 2:
        return 'cyan'
    if ln == 11 and i in S['nums']:
        return 'green'
    return None


def _formula(S):
    ln = S.get('_line')
    res = S.get('res')
    if ln == 9 and res and len(res) >= 2:
        k = len(res) - 1
        return (f"`res[{k}] = res[{k - 1}] + cnt_list[{k - 1}] = {res[k - 1]} + {S['cnt_list'][k - 1]}` = =={res[k]}==")
    if ln == 11:
        return '答案：每个 `num` 直接查 `res[num]`（比它小的数的个数）'
    if 'cnt_list' in S and res is None:
        return '桶排：`cnt_list[x]` = 数字 `x` 出现了几次（值域只有 0..100）'
    return '`res[x]` = 严格小于 `x` 的数的个数 = `cnt_list[0..x-1]` 之和'


CONFIG = dict(
    num=1365, title='有多少小于当前数字的数字', difficulty='Easy', category='哈希',
    author='yiduobo', technique='桶排计数 + 前缀和',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def smallerNumbersThanCurrent(self, nums):
        cnt_list = [0] * 101
        for num in nums:
            cnt_list[num] += 1

        res = [0]
        for num in range(1, 101):
            res.append(res[-1] + cnt_list[num - 1])

        return [res[num] for num in nums]
''',
    call='Solution().smallerNumbersThanCurrent([8, 1, 2, 2, 3])',
    expect=[4, 0, 1, 1, 3],
    skip=['for num in nums:', 'for num in range(1, 101)'],
    views=[
        dict(type='array', var='nums', label='nums', cell=78, h=150,
             color=lambda S, i, v: ('yellow' if S.get('_line') == 5 and i == sum(S['cnt_list']) - 1
                                   else 'green' if S.get('_line') == 5 and i < sum(S['cnt_list']) else None)),
        dict(type='array', var='cnt_list[:10]', label='cnt_list[0..9]（桶：每个数出现几次，后面 91 个全是 0）', cell=78, h=150,
             color=_cnt_color),
        dict(type='array', var='res[:10]', label='res[0..9]（res[x] = 小于 x 的数有几个）', cell=78, h=150,
             color=_res_color),
        dict(type='text', fn=_formula, size=26, h=70),
    ],
    watch=[('num', lambda S: S['_inner'].get('num'), 'yellow'), ('len(res)', lambda S: len(S['res']) if 'res' in S else None, 'cyan')],
    captions={
        'cnt_list = [0] * 101': '数字范围只有 `0..100` → 开 ==101 个桶==，代替排序',
        'cnt_list[num] += 1': '把 `{num}` 扔进桶：`cnt_list[{num}] = {cnt_list[num]}`',
        'res = [0]': '`res[0] = 0`：没有比 0 更小的数（题目保证非负）',
        'res.append': lambda S, B, r: (f'比 `{len(S.res) - 1}` 小的个数 = 比 `{len(S.res) - 2}` 小的 `{S.res[-2]}` '
                                       f'+ 等于 `{len(S.res) - 2}` 的 `{S.cnt_list[len(S.res) - 2]}` → =={S.res[-1]}=='),
        'return [res[num]': '每个数查表：`nums = {nums}` → 返回 =={ret}==',
    },
    max_steps=22,
    cards=dict(
        one_liner='值域只有 0..100：桶排计数，再做一遍前缀和',
        complexity='时间 `O(n + 101)`，空间 `O(101)`',
        problem=['对每个 `nums[i]`，统计数组中有多少个数==严格小于==它',
                 '`0 ≤ nums[i] ≤ 100`',
                 '示例：`nums = [8,1,2,2,3]` → `[4,0,1,1,3]`'],
        quote='比较直观的做法是先从小到大进行排序，然后一趟扫描统计。==由于这里数字最多到100，因此我在这里采用的是桶排。==',
        quote_src='—— yiduobo 题解原文',
        idea=['`cnt_list[x]`：数字 `x` 出现了几次（桶排的“桶”）',
              '`res[x] = res[x-1] + cnt_list[x-1]`：比 `x` 小的 = 比 `x-1` 小的 + 等于 `x-1` 的',
              '最后每个数直接查 `res[num]`，重复的数自然得到同一个答案'],
        result='`res[8]=4, res[1]=0, res[2]=1, res[2]=1, res[3]=3` → 返回 `[4, 0, 1, 1, 3]`',
        summary=['时间 `O(n + C)`，`C = 101` 是值域大小；比排序的 `O(n log n)` 更快',
                 '易错：`res[x]` 加的是 `cnt_list[x-1]`，==不含 x 本身==（要严格小于）',
                 '值域大时换成“排序 + 二分 / 记录首次出现位置”的做法',
                 '原文为 Python 2 风格：删去了类型说明文档字符串，逻辑未改'],
    ),
)
