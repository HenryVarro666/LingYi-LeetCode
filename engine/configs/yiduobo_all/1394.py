CONFIG = dict(
    num=1394, title='找出数组中的幸运数', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='数组计数 · 从大到小找',
    code='''
class Solution(object):
    def findLucky(self, arr):

        cnt_list = [0] * 501
        for num in arr:
            cnt_list[num] += 1
        
        for num in range(500, 0, -1):
            if cnt_list[num] == num:
                return num
        
        return -1
''',
    call='Solution().findLucky([1,2,2,3,3,3])',
    expect=3,
    views=[
        dict(type='array', var='arr', label='arr', h=120, color=lambda S, i, v: 'blue' if 'num' in S and S.get('_line') and v == S['num'] and 'cnt_list' in S and False else None),
        dict(type='text', h=70, fn=lambda S: (f"`cnt_list[{S['num']}]` = {S['cnt_list'][S['num']]}" if 'num' in S and 'cnt_list' in S else '')),
        dict(type='text', h=70, fn=lambda S: ('已统计的次数（只列出非 0）：' + '，'.join(f'{k}→{v}' for k, v in enumerate(S['cnt_list']) if v)) if 'cnt_list' in S else ''),
    ],
    watch=['num'],
    max_steps=40,
    captions={
        'cnt_list = [0]': '`cnt_list[v]` 记录数值 v 的出现次数，值域 1~500，开 501 格',
        'for num in arr': '读到数 `{num}`',
        'cnt_list[num] += 1': '`{num}` 的次数加一 → `{cnt_list[num]}`',
        'for num in range(500': '从大到小检查数值 `{num}`',
        'if cnt_list[num] == num': lambda S, B, r: f'`cnt_list[{S.num}] = {S.cnt_list[S.num]}`，数值 `{S.num}` → ' + ('==相等，是幸运数，且是最大的=='  if S.cnt_list[S.num] == S.num else '不相等'),
        'return num': '从大往小第一个命中的就是最大幸运数：`{num}`',
        'return -1': '都不满足，返回 `-1`',
    },
    cards=dict(
        one_liner='计数数组 + 从大到小找，第一个命中就是答案',
        complexity='时间 `O(n + 500)`，空间 `O(1)`',
        problem=['幸运数：出现次数恰好等于自身数值的整数',
                 '返回最大的幸运数，没有则返回 `-1`',
                 '示例：`[1,2,2,3,3,3]` → `3`'],
        quote='比较基础的题目，统计每个数出现的次数，然后遍历每个数，找出符合条件的数即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['值域只有 1~500，用长度 501 的数组计数',
              '从 500 往 1 找 `cnt_list[num] == num`',
              '倒着找，第一个命中的就是最大的'],
        summary=['时间 `O(n)`，空间固定 501 格',
                 '倒序遍历省掉了取最大值',
                 '原文已是 Python 3 可运行写法，无需修改',
                 '对比灵神：灵神方法一用 Counter 哈希表遍历取 max，这里用数组和倒序扫描'],
    ),
)
