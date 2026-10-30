PAL = ['green', 'yellow', 'purple', 'cyan', 'orange']


def _gc(S, k):
    # k 是原数组下标；循环一时只给已处理过的下标上色
    if 'belong' not in S or 'groups' not in S:
        return None
    if 'gid' not in S and k not in S['pos'][:S.get('i', -1) + 1]:
        return None
    return PAL[S['belong'][k] % len(PAL)]


CONFIG = dict(
    num=2948, title='交换得到字典序最小的数组', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='排序分段 · 段内升序回填',
    tags=['贪心与思维', '难度分 2047'],
    code='''
class Solution:
    def lexicographicallySmallestArray(self, nums: List[int], limit: int) -> List[int]:
        n = len(nums)
        pos = sorted(range(n), key=lambda i: nums[i])
        # 排序后，nums[pos[i]] 是递增的

        groups = []
        belong = [0] * n
        for i, p in enumerate(pos):
            if i == 0 or nums[p] - nums[pos[i - 1]] > limit:
                groups.append(i)  # 新的段，只需记录开始下标
            # 记录 pos[i] 属于哪一段
            belong[p] = len(groups) - 1

        ans = [0] * n
        for i, gid in enumerate(belong):
            ans[i] = nums[pos[groups[gid]]]
            groups[gid] += 1
        return ans
''',
    call='Solution().lexicographicallySmallestArray([1,7,6,18,2,1], 3)',
    expect=[1, 6, 7, 18, 1, 2],
    views=[
        dict(type='array', var='nums', label='nums', pointers={'p': 'pink'}, h=175,
             color=lambda S, i, v: _gc(S, i)),
        dict(type='array', var='pos', label='pos 排序下标', pointers={'i': 'blue'}, h=175,
             color=lambda S, i, v: _gc(S, v) if 'gid' in S or i <= S.get('i', -1) else None),
        dict(type='array', var='groups', label='groups 段起点', h=125),
        dict(type='array', var='belong', label='belong', h=125),
        dict(type='array', var='ans', label='ans', h=125, color=lambda S, i, v: 'green' if 'gid' in S and i == S['i'] else None),
    ],
    watch=['i', 'p', 'gid', ('limit', 'limit', 'yellow')],
    captions={
        'pos = sorted': '`pos` 按值排序：`{pos}`，沿着它走就是从小到大看 `nums`，同时记得每个数原来的下标',
        'if i == 0 or nums[p]': '{"第一个数，直接开新段" if i == 0 else "相邻差 `nums[" + str(p) + "] - nums[" + str(pos[i-1]) + "]` = " + str(nums[p] - nums[pos[i-1]]) + "，" + ("==大于== `limit`，连不上，开新段" if nums[p] - nums[pos[i-1]] > limit else "不超过 `limit`，属于同一段")}（排序后只看相邻差就够）',
        'groups.append': '开新段：这一段的最小值在 `pos[{i}]`，`groups` 记下起点 {i}',
        'belong[p] =': '原下标 `{p}` 属于第 `{len(groups)-1}` 段',
        'ans[i] = nums': '第 `{i}` 个位置属于第 `{gid}` 段：取该段当前最小的数 `nums[pos[groups[{gid}]]]` = =={ans[i]}==（从左到右依次填更小的）',
        'groups[gid] += 1': '这段的最小值用掉了，起点后移一位，下次填该段次小的数',
    },
    cards=dict(
        one_liner='同一连通块里的数可以任意换位：按位置从左到右放入从小到大的数',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['数组 `nums` 和 `limit`，两数之差 `<= limit` 就能交换，次数不限',
                 '求能得到的 ==字典序最小== 的数组',
                 '示例：`[1,7,6,18,2,1]`，`limit=3` → `[1,6,7,18,1,2]`'],
        quote='其实，只需要对排序后相邻元素连边。例如 1,2,3，如果知道 1 和 2 在同一个连通块，2 和 3 在同一个连通块，那么 1 和 3 就一定在同一个连通块。',
        quote_src='—— 灵茶山艾府题解',
        idea=['数值差 `<= limit` 连边，同一连通块里的数能 ==随意交换==',
              '排序后只看相邻差：差大于 `limit` 就是一个新块的开始',
              '每个块占据的位置固定，在这些位置上从左到右填块内从小到大的数'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '连通块里的数只能放回本块的位置，不能跑到别的块去，所以要记 `pos` 和 `belong`',
                 '题解还给了「sub_pos 排序回填」和「deque 队列」两种写法，思路相同，写法三只记起点最省空间',
                 '同类题：1202. 交换字符串中的元素'],
    ),
)
