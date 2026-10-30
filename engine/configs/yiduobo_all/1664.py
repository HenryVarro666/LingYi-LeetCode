def _color(S, i, v):
    if 'now_odd' not in S or 'index' not in S:
        return 'cyan' if i % 2 else 'orange'
    if 'res' not in S:
        return 'cyan' if i % 2 else 'orange'
    k = S['index']
    if i == k:
        return 'yellow'
    return 'cyan' if i % 2 else 'orange'


def _dim(S, i, v):
    return 'res' in S and 'index' in S and 'now_odd' in S and i < S['index']


def _txt(S):
    if 'res' not in S:
        return '下标奇偶：==橙 = 偶数下标==，==青 = 奇数下标==；先求两类的总和'
    i = S['index']
    if 'suffix_odd' not in S or S.get('_line', 0) < 20:
        return f'准备删除下标 `{i}`：左侧用 `now_*`，右侧用总和减去左侧'
    a = S['now_odd'] + S['suffix_odd']
    b = S['now_even'] + S['suffix_even']
    return f'删后奇数位：`{S["suffix_odd"]} + {S["now_odd"]}` = =={a}==　偶数位：`{S["suffix_even"]} + {S["now_even"]}` = =={b}=='


CONFIG = dict(
    num=1664, title='生成平衡数组的方案数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='奇偶下标前缀和 · O(1) 空间',
    tags=['动态规划'],
    code='''
class Solution(object):
    def waysToMakeFair(self, nums):

        s_odd = s_even = 0
        for index in range(len(nums)):
            if index & 1:
                s_odd += nums[index]
            else:
                s_even += nums[index]
        
        now_odd = now_even = 0
        res = 0
        for index in range(len(nums)):
            if index == 0:
                suffix_even = s_odd
                suffix_odd = s_even - nums[0]
            else:
                suffix_even = s_odd - now_odd
                suffix_odd = s_even - now_even
                if index & 1:
                    suffix_even -= nums[index]
                else:
                    suffix_odd -= nums[index]
            
            if suffix_odd + now_odd == suffix_even + now_even:
                res += 1

            if index & 1:
                now_odd += nums[index]
            else:
                now_even += nums[index]
        
        return res
''',
    call='Solution().waysToMakeFair([1,1,2,2,4,3])',
    expect=2,
    max_steps=100,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='nums', pointers={'index': 'yellow'}, color=_color, dim=_dim, h=300,
             label='nums（橙 = 偶数下标，青 = 奇数下标，黄 = 要删除的位置，灰 = 删除位置左侧）'),
    ],
    watch=[('s_odd', 's_odd', 'cyan'), ('s_even', 's_even', 'orange'), ('now_odd', 'now_odd', 'cyan'),
           ('now_even', 'now_even', 'orange'), 'index', ('res', 'res', 'green')],
    captions={
        's_odd = s_even': '准备两个总和：奇数下标之和 `s_odd`、偶数下标之和 `s_even`',
        'if index & 1:': lambda S, B, r: ('奇数下标' if S.index & 1 else '偶数下标') + f' `{S.index}`',
        's_odd += ': '`s_odd += {nums[index]}` → =={s_odd}==',
        's_even += nums[index]': '`s_even += {nums[index]}` → =={s_even}==',
        'now_odd = now_even': '`now_odd` / `now_even` = 删除位置左侧的奇、偶下标和（前缀和，只保留两个数）',
        'res = 0': '`res` 统计平衡的删法个数',
        'if index == 0': lambda S, B, r: (f'枚举删除下标 `{S.index}`' + ('：左侧为空' if S.index == 0 else '')),
        'suffix_even = s_odd - now_odd': '右侧原奇数下标和 = `s_odd − now_odd` = {suffix_even}（删后它们挪到偶数位）',
        'suffix_odd = s_even - now_even': '右侧原偶数下标和 = `s_even − now_even` = {suffix_odd}（删后挪到奇数位）',
        'suffix_even -= nums': '删除位置自己是奇数下标，要从右侧去掉 `{nums[index]}` → `suffix_even` = =={suffix_even}==',
        'suffix_odd -= nums': '删除位置自己是偶数下标，要从右侧去掉 `{nums[index]}` → `suffix_odd` = =={suffix_odd}==',
        'suffix_odd = s_even - nums[0]': '删除下标 0：右侧原偶数位和 = `s_even − nums[0]` = =={suffix_odd}==',
        'suffix_even = s_odd': lambda S, B, r: ('删除下标 0：右侧原奇数位和就是 `s_odd` = ' + f'=={S.suffix_even}==' if S.index == 0 else ''),
        'if suffix_odd + now_odd': '删后奇数位 `{suffix_odd} + {now_odd} = {suffix_odd + now_odd}`，偶数位 `{suffix_even} + {now_even} = {suffix_even + now_even}`：{"==相等，平衡=="  if suffix_odd + now_odd == suffix_even + now_even else "不相等"}',
        'res += 1': '平衡，`res` = =={res}==',
        'now_odd += nums': '`now_odd` 加上 `{nums[index]}` → =={now_odd}==，下一轮它在左侧',
        'now_even += nums': '`now_even` 加上 `{nums[index]}` → =={now_even}==，下一轮它在左侧',
        'return res': '共 `{res}` 种删法使奇偶下标和相等',
    },
    cards=dict(
        one_liner='删掉一个数，右侧的奇偶位互换；用左右前缀和直接对比',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['删除 `nums` 中恰好一个元素，其余元素下标自动前移',
                 '若删后「奇数下标之和 = 偶数下标之和」，这种删法称为平衡',
                 '求平衡删法的个数；示例：`[1,1,2,2,4,3]` → `2`'],
        quote='设odd[index]表示0到index之间所有奇数下标的和，even[index]表示0到index之间所有偶数下标的和',
        quote_src='—— yiduobo 题解原文',
        idea=['删位置 `p`：左侧奇偶不变，右侧奇偶互换',
              '所以两边之和 = 左侧奇 + 右侧原偶 vs 左侧偶 + 右侧原奇',
              '前缀数组可省：只留 `now_odd / now_even` 两个数，后缀 = 总和 − 前缀'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：右侧要去掉被删元素本身，奇偶位置要对准',
                 '`index == 0` 单独处理：此时左侧为空，`s_even` 要减去 `nums[0]`',
                 '原文本身是 Python 3 可运行的，没有改动；题面库里缺失，按题意补写'],
    ),
)
