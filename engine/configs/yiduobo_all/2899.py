CONFIG = dict(
    num=2899, title='上一个遍历的整数', difficulty='Easy', category='模拟',
    author='yiduobo', technique='模拟 · 记录连续 prev 次数', tags=[],
    code='''
class Solution(object):
    def lastVisitedIntegers(self, words):

        nums = []
        k = 0
        res = []
        for w in words:
            if w[0] == 'p':
                k += 1
                if k > len(nums):
                    res.append(-1)
                else:
                    res.append(nums[-k])
            
            else:
                nums.append(int(w))
                k = 0
        
        return res
''',
    call='Solution().lastVisitedIntegers(["1","prev","2","prev","prev","prev"])',
    expect=[1, 2, 1, -1],
    views=[
        dict(type='array', var='words', h=170, label='words', pointers={'idx': 'blue'},
             color=lambda S, i, v: ('pink' if v[0] == 'p' else 'green') if i <= S.get('idx', -1) else None),
        dict(type='array', var='nums', h=150, label='nums（记下的数字）', pointers={'len(nums) - k': 'pink'}),
        dict(type='array', var='res', h=150, label='res', color=lambda S, i, v: 'yellow' if i == len(S['res']) - 1 else None),
    ],
    watch=['w', ('k', 'k', 'pink'), ('len(nums)', 'len(nums)')],
    captions={
        5: '`k` 记录当前连续出现 prev 的次数',
        17: '`k` 已置 0，下一个 prev 重新从 1 数起',
        "if w[0] == 'p'": '`w = "{w}"` → {"是 prev" if w[0] == "p" else "是数字"}',
        'k += 1': '连续的 prev 又多一个：`k = {k}`',
        'if k > len(nums)': '`k = {k}`，`len(nums) = {len(nums)}` → {"k 更大，凑不出" if k > len(nums) else "够取"}',
        'res.append(-1)': '数字不够 → 答案追加 `-1`',
        'res.append(nums[-k])': '取 `nums` 倒数第 `{k}` 个 → 追加 =={res[-1]}==',
        'nums.append': '数字 `{nums[-1]}` 记进 `nums`，==连续 prev 中断==，`k` 置 0',
        'return res': '遍历结束，返回 `{ret}`',
    },
    cards=dict(
        one_liner='用 nums 存数字，k 数连续 prev，取倒数第 k 个',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['本题（2899）输入是字符串数组 `words`：数字串或 `"prev"`',
                 '每个 `"prev"` 要找「上一个遍历的整数」：连续第 `k` 个 prev 取最近第 `k` 个数，不够则 `-1`',
                 '本视频：`["1","prev","2","prev","prev","prev"]` → `[1,2,1,-1]`'],
        quote='若当前遍历到的是prev，那么就将k加上1，若此时的k大于nums的长度，那么将-1添加到答案中，否则将nums中倒数第k个数添加到答案中。',
        quote_src='—— yiduobo 题解原文',
        idea=['`nums` 只记数字，`k` 只数当前连续的 prev',
              'prev：`k += 1`，`k > len(nums)` 填 `-1`，否则填 `nums[-k]`',
              '数字：加进 `nums`，`k` 置 0'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '判断 prev 用 `w[0] == "p"`，数字用 `int(w)` 转换',
                 '遇到数字必须把 `k` 清零',
                 '原文已是 Python 3 可运行写法，代码未改动'],
    ),
)
