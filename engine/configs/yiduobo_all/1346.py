CONFIG = dict(
    num=1346, title='检查整数及其两倍数是否存在', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='一趟扫描 · 哈希集合',
    code='''
class Solution(object):
    def checkIfExist(self, arr):

        num_set = set()
        for num in arr:
            if num + num in num_set:
                return True
            if num % 2 == 0 and num // 2 in num_set:
                return True
            num_set.add(num)
        
        return False
''',
    call='Solution().checkIfExist([3,1,7,11,6,14])',
    expect=True,
    views=[
        dict(type='array', var='arr', h=170,
             color=lambda S, i, v: 'blue' if 'num' in S and v == S['num'] and i == S['arr'].index(S['num']) else None),
        dict(type='set', var='num_set', h=230, fmt=lambda x: str(x)),
        dict(type='text', size=30, fn=lambda S: f"当前 `num = {S['num']}`：找 `{S['num']*2}`" + (f" 或 `{S['num']//2}`" if S['num'] % 2 == 0 else '') if 'num' in S else ''),
    ],
    watch=['num', ('num_set', 'num_set', 'green')],
    captions={
        'num_set = set()': '`num_set` 存已经扫过的数',
        'for num in arr': '取到 `num = {num}`',
        'if num + num in num_set': '`num` 的两倍是 `{num + num}`，在已扫过的数里吗？→ {"在" if num + num in num_set else "不在"}',
        'num % 2 == 0 and': lambda S, B, r: (f'`{S.num}` 是偶数，它的一半是 `{S.num // 2}`，已扫过吗？→ ' + ('==在，找到一对==' if S.num // 2 in S.num_set else '不在')) if S.num % 2 == 0 else f'`{S.num}` 是奇数，没有整数的一半，跳过',
        'num_set.add': '这个数没配上对，先记下：`num_set` 加入 `{num}`',
        'return True': '找到 `num` 和它的两倍（或一半）同时出现 → ==返回 True==',
        'return False': '扫完都没有配上对 → 返回 False',
    },
    cards=dict(
        one_liner='边扫边记，每个数只看「两倍」和「一半」是否出现过',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给整数数组 `arr`，问是否存在两个不同下标 `i != j`，使 `arr[i] == 2 * arr[j]`',
                 '示例：`[3,1,7,11,6,14]`：`3` 和 `6` 是一对 → `True`'],
        quote='一趟扫描，使用哈希表储存已经访问过的数。对于当前值num，若num * 2以及num / 2出现在哈希表中，那么就返回true',
        quote_src='—— yiduobo 题解原文',
        idea=['当前数可能是「大的那个」也可能是「小的那个」',
              '它是小的：看 `num + num` 是否出现过',
              '它是大的：必须是偶数，看 `num // 2` 是否出现过'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：`0` 的两倍还是 `0`，所以先查后加，同一个 0 不能自己配自己',
                 '奇数不能除 2，所以要先判断 `num % 2 == 0`',
                 '原文为 Python 2 写法，其中 `num / 2` 为整数除法，已改为 `num // 2`'],
    ),
)
