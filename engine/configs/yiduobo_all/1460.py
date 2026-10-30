CONFIG = dict(
    num=1460, title='通过翻转子数组使两个数组相等', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='构造证明 · 计数比较', tags=[],
    code='''
class Solution(object):
    def canBeEqual(self, target, arr):

        cnt_list = [0] * 1001
        for num in target:
            cnt_list[num] += 1
        
        for num in arr:
            cnt_list[num] -= 1
            if cnt_list[num] < 0:
                return False

        return True
''',
    call='Solution().canBeEqual([1,2,3,4,2], [2,4,1,3,2])',
    expect=True,
    views=[
        dict(type='array', var='target', pointers={}, label='target', h=150, color=lambda S, i, v: 'green' if S.get('_line') is not None and False else None),
        dict(type='array', var='arr', pointers={}, label='arr', h=150),
        dict(type='map', var=lambda S: {k: c for k, c in enumerate(S['cnt_list']) if c != 0}, label='cnt_list 中非 0 的项（数字: 剩余次数）', h=220,
             fmt=lambda k, v: f'{k} 剩 {v}'),
        dict(type='text', fn=lambda S: (f"当前数字 `{S['num']}`，cnt_list[{S['num']}] = ==`{S['cnt_list'][S['num']]}`==" if 'num' in S else '')),
    ],
    watch=[('num', 'num', 'blue')],
    captions={
        'cnt_list = [0]': '`cnt_list[x]` 记录数字 `x` 的剩余计数，数值范围 1..1000，开 1001 个格子',
        'for num in target': '处理 target 里的数字 `{num}`',
        'cnt_list[num] += 1': '`target` 里出现一次 `{num}`：计数加一，`cnt_list[{num}] = {cnt_list[num]}`',
        'for num in arr': '现在处理 arr 里的数字 `{num}`，用来抵消 target 的计数',
        'cnt_list[num] -= 1': '`arr` 里出现一次 `{num}`：计数减一，`cnt_list[{num}] = {cnt_list[num]}`',
        'if cnt_list[num] < 0': lambda S, B, r: f"`cnt_list[{S['num']}] = {S['cnt_list'][S['num']]}`" + ('，小于 0：arr 里的 `%d` 比 target 多 → 不可能相等' % S['num'] if S['cnt_list'][S['num']] < 0 else '，不小于 0：数量还对得上'),
        'return False': 'arr 比 target 多出一个 `{num}`，直接返回 False',
        'return True': 'arr 的数字都能在 target 里抵消（两数组等长）→ 出现次数完全一致，返回 True',
    },
    cards=dict(
        one_liner='能翻转成功，当且仅当两个数组里每个数出现的次数相同',
        complexity='时间 `O(n + V)`，空间 `O(V)`，V = 1001',
        problem=['给两个等长数组 `target` 和 `arr`，每一步可以翻转 `arr` 的任意一个非空子数组，次数不限',
                 '问能否让 `arr` 变成 `target`',
                 '示例：`target=[1,2,3,4,2]`，`arr=[2,4,1,3,2]` → `True`'],
        quote='若此时的target[index]不等于arr[index]，那么我们找出最小的p，满足p > index以及arr[p] = target[index]。翻转index到p这一段，就能让target[index]与arr[index]相等了。',
        quote_src='—— yiduobo 题解原文',
        idea=['不要求次数最少 → 逐位构造：每一位都能翻转一次把需要的数换到位',
              '所以只要两个数组 ==元素出现次数一致==，就一定能做到',
              '用定长数组计数：target 加一，arr 减一，减到负数就不一致'],
        summary=['时间 `O(n + V)`，空间 `O(V)`；也可以直接 `sorted(target) == sorted(arr)`',
                 '关键是构造证明：翻转 `[index, p]` 会让 `arr[index] = target[index]`，后面逐位继续',
                 '易错点：两数组等长，所以只检查「arr 不超过 target」就够了',
                 '本视频用示例做了小改动，题目值域 1..1000，所以开 1001 个格子'],
    ),
)
