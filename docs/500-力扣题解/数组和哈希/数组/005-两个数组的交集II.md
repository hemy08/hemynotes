# 两个数组的交集 II

<span style="color:rgb(100,180,246);font-size:11pt">最后更新：2023-12-01</span>

链接：https://leetcode.cn/leetbook/read/top-interview-questions-easy/x2y0c2/

!!! Question "题目描述"
    给你两个整数数组 `nums1` 和 `nums2` ，请你以数组形式返回两数组的交集。返回结果中每个元素出现的次数，应与元素在两个数组中都出现的次数一致（如果出现次数不一致，则考虑取较小值）。可以不考虑输出结果的顺序。

!!! example "题目示例"

    === "示例 1："
        **输入：** `nums1 = [1,2,2,1], nums2 = [2,2]`

        **输出：** `[2,2]`

    === "示例 2:"
        **输入：** `nums1 = [4,9,5], nums2 = [9,4,9,8,4]`

        **输出：** `[4,9]`

!!! tip "提示："
    - $1 <= nums1.length, nums2.length <= 1000$
    - $0 <= nums1[i], nums2[i] <= 1000$


!!! note "进阶："
    如果给定的数组已经排好序呢？你将如何优化你的算法？

    如果nums1的大小比nums2 小，哪种方法更优？
    
    如果nums2的元素存储在磁盘上，内存是有限的，并且你不能一次加载所有的元素到内存中，你该怎么办？

=== "Go语言双层for循环"

    ```go
    import "sort"

    func intersect(nums1 []int, nums2 []int) []int {
        // 排序
        sort.Ints(nums1)
        sort.Ints(nums2)

        n1, n2 := len(nums1), len(nums2)
        result := make([]int, 0)
        // 遍历，找到两张表都存在的，放入要返回的表中
        start := 0
        for i := 0; i < n1; i++ {
            v1 := nums1[i]
            for j := start; j < n2; j++ {
                v2 := nums2[j]
                // 表1的值比表2的值大，需要表二继续往后移
                if v1 > v2 {
                    continue
                }

                // 找到了，表二下标后移，下次从当前值的后一个值开始找
                if v1 == v2 {
                    result = append(result, v2)
                    start = j + 1
                }

                // 表1比表2的值小,或者找到了一个交集，都跳出当前循环，表1继续往下，表二不动
                break
            }
        }

        return result
    }
    ```

=== "Go语言双指针"

    ```go
    import "sort"

    func intersect(nums1 []int, nums2 []int) []int {
        // 排序
        sort.Ints(nums1)
        sort.Ints(nums2)

        n1, n2 := len(nums1), len(nums2)
        result := make([]int, 0)
        // 遍历，找到两张表都存在的，放入要返回的表中
        i, j := 0, 0
        for i < n1 && j < n2 {
            v1 := nums1[i]
            v2 := nums2[j]
            // 表1的值比表2的值大，需要表二继续往后移
            if v1 > v2 {
                j++
            } else if v1 < v2 {
                // 表1比表2的值小，表1继续往下，表二不动
                i++
            } else {
                // 找到了，表二下标后移，下次从当前值的后一个值开始找
                result = append(result, v2)
                j++
                i++
            }
        }

        return result
    }
    ```


=== "Go语言map表实现"

    ```go
    func intersect(nums1 []int, nums2 []int) []int {
        result := make([]int, 0)
        hasMap := map[int]int{}

        for _, v := range nums1 {
            hasMap[v]++
        }

        for _, v := range nums2 {
            if hasMap[v] > 0 {
                result = append(result, v)
                hasMap[v]--
            }
        }

        return result
    }

    ```

=== "C语言暴力破解"

    ```c
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include "uthash.h"

    static inline int GetMinValue(int a, int b) {
        return a > b ? b : a;
    }

    int *intersect(int* nums1, int nums1Size, int* nums2, int nums2Size, int* returnSize)
    {
        int retSize = GetMinValue(nums1Size, nums2Size);
        int *result = NULL;
        int count = 0;

        result = (int*)malloc(sizeof(int) * (retSize + 1));
        if (result == NULL) {
            *returnSize = 0;
            return NULL;
        }

        // 获取值
        for (int i = 0; i < nums1Size; i++) {
            for (int j = i; j < nums2Size && j < nums1Size; j++) {
                if (nums1[i] == nums2[j]) {
                    result[count] = nums1[i];
                    count++;
                    break;
                }
            }
        }

        *returnSize = count;

        return result;
    }
    ```

=== "C语言qsort实现"

    ```c
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include "uthash.h"

    #define MIN_VAL(a, b)  (((a) > (b)) ? (b) : (a))

    // 快速排序，数组，升序排序
    static inline int QsortCmpArrayAscOrder(const void *p1, const void *p2)
    {
        return *(int *)p1 - *(int *)p2;
    }

    int* intersect(int* nums1, int nums1Size, int* nums2, int nums2Size, int* returnSize)
    {
        int retSize = MIN_VAL(nums1Size, nums2Size);
        int *result = NULL;
        int count = 0;

        if ((nums1 == NULL) || (nums1Size == 0) || (nums2 == NULL) || (nums2Size == 0)) {
            *returnSize = 0;
            return NULL;
        }

        qsort(nums1, nums1Size, sizeof(int), QsortCmpArrayAscOrder);
        qsort(nums2, nums2Size, sizeof(int), QsortCmpArrayAscOrder);

        result = (int*)malloc(sizeof(int) * (retSize + 1));
        if (result == NULL) {
            *returnSize = 0;
            return NULL;
        }

        // 获取值
        int tmp = 0;
        for (int i = 0; i < nums1Size; i++) {
            if (tmp >= nums2Size) {
                break;
            }

            for (int j = tmp; j < nums2Size; j++) {
                if (nums1[i] == nums2[j]) {
                    tmp = j + 1;
                    result[count] = nums1[i];
                    count++;
                    break;
                }
            }
        }

        *returnSize = count;

        return result;
    }

    ```

=== "C语言qsort双指针实现"

    ```c
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include "uthash.h"

    int compForIntersect(const void *p1, const void *p2)
    {
        return *(int *)p1 - *(int *)p2;
    }

    int* intersect(int* nums1, int nums1Size, int* nums2, int nums2Size, int* returnSize)
    {
        int retSize = (int)fmin(nums1Size, nums2Size);
        int *result = NULL;
        int count = 0;

        if ((nums1 == NULL) || (nums1Size == 0) || (nums2 == NULL) || (nums2Size == 0)) {
            *returnSize = 0;
            return NULL;
        }

        qsort(nums1, nums1Size, sizeof(int), compForIntersect);
        qsort(nums2, nums2Size, sizeof(int), compForIntersect);

        result = (int*)malloc(sizeof(int) * (retSize + 1));
        if (result == NULL) {
            *returnSize = 0;
            return NULL;
        }

        // 获取值
        int index1 = 0, index2 = 0;
        while (index1 < nums1Size && index2 < nums2Size) {
            if (nums1[index1] < nums2[index2]) {
                index1++;
            } else if (nums1[index1] > nums2[index2]) {
                index2++;
            } else {
                result[count++] = nums1[index1];
                index1++;
                index2++;
            }
        }

        *returnSize = count;

        return result;
    }

    ```


=== "C语言哈希实现"

    ```c
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include "uthash.h"

    struct hashTable {
        int key;
        int nums;
        UT_hash_handle hh;
    };

    int* intersect(int* nums1, int nums1Size, int* nums2, int nums2Size, int* returnSize)
    {
        struct hashTable* set = NULL;
        for (int i = 0; i < nums1Size; i++) {
            struct hashTable* tmp;
            HASH_FIND_INT(set, nums1+i, tmp);
            if (tmp == NULL) {
                tmp = (struct hashTable*)malloc(sizeof(struct hashTable));
                tmp->key = nums1[i];
                tmp->nums  = 1;
                HASH_ADD_INT(set, key, tmp);
            }  else {
                tmp->nums += 1;
            }
        }
        *returnSize = 0;

        int len = (int)fmax(nums1Size,nums2Size);

        int* res = (int*)malloc(len*sizeof(int));
        for (int i = 0; i < nums2Size; i++) {
            struct hashTable* tmp;
            HASH_FIND_INT(set, nums2+i, tmp);
            if ((tmp != NULL) && (tmp->nums != 0)) {
                tmp->nums--;
                res[(*returnSize)++] = nums2[i];
            }
        }
        return res;
    }

    ```