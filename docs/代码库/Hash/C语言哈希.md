# C语言实现HashMgr

<span style="color:rgb(100,180,246);font-size:11pt">最后更新：2019-01-29</span>

```c
//   hash_table
//  |------------|
//  |____________|     _hlist_node1__       _hlist_node2__       _hlist_node3__
//  | hlist_head |    |     next     |\--->|     next     |\--->|     next     |
//  |___frist____|\-->|--------------|  \  |--------------|  \  |--------------|
//  |            |  \ |_____pprev____|    \|_____pprev____|    \|_____pprev____|
//  |____________|
//hash_table为散列表（数组），其中的元素类型为struct hlist_head。以hlist_head为链表头的链表，其中的节点hash值是相同的（也叫冲突）。
// first指针指向链表中的节点①，然后节点①的pprev指针指向hlist_head中的first，节点①的next指针指向节点②。以此类推。
//
//hash_table的列表头仅存放一个指针,也就是first指针,指向的是对应链表的头结点,没有tail指针也就是指向链表尾节点的指针,
// 这样的考虑是为了节省空间——尤其在hash bucket(数组size)很大的情况下可以节省一半的指针空间。
//
//为什么pprev是一个指向指针的指针呢？按照这个设计，我们如果想要得到尾节点，必须遍历整个链表，可如果是一个指向节点的指针，
//那么头结点现在的pprev便可以直接指向尾节点，也就是list_head的做法。
//
//对于散列表来说，一般发生冲突的情况并不多（除非hash设计出现了问题），所以一个链表中的元素数量比较有限，遍历的劣势基本可以忽略。
//在删除链表头结点的时候，pprev这个设计无需判断删除的节点是否为头结点。如果是普通双向链表的设计，那么删除头结点之后，hlist_head中的first指针需要指向新的头结点

/*(uint8_t *pstHashkey, u32 ulHashkeyLen,u32 ulHashbit)*/
typedef unsigned int (*HashFunc)(unsigned char *, unsigned int ,unsigned int );

typedef struct
{
    uint32_t usSize;              //元素个数
    THListHead hlistfirst;          //每个哈希值对应 链表头，hlist的结构
    pthread_spinlock_t bucketlock;  //桶节点的锁
}THashHead;

/* 哈希散列结构数据节点 */
typedef struct
{
    uint32_t ulBitWidth;      /* 表示hash计算值的位宽，比如16位宽，32位宽*/
    uint32_t ulNumUsed;           /*使用的节点个数*/
    THashHead   *pstHashHead;    /*哈希表节点，类似指针数组，数组内每个模块存一个链*/
    HashFunc pHashFunc; //哈希算法
}THashManager;

typedef struct
{
    THListNode hlistnode;   //当前哈希值对应的哈希链表
    uint64_t ulData;         //哈希节点的具体数值
    uint32_t ulKeyLen;       //哈希Key长度
    uint8_t pucKey[0];       //key,因为key的长度未知，存储key都是动态申请内存，因此这里需要将key放在最后，否则数据就会乱。从这个地址往后keylen长度就可以存储可以
}THashElem;

//最多支持32位宽的hash
#define MAX_BIT_WIDTH    32
#define TINY_MASK(x)   (((uint32_t)1<<(x))-1)
#define HASH_BUCKET_NUM(x)    ((uint32_t)1<<(x))

/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * Function Name ：HashFuncAdditive
 * Description ：加法哈希
 * Input  ：
 *          uint8_t *ptHashKey //哈希key
 *          uint32_t ulHashkeyLen//key长度
 *          uint32_t prime//素数
 * Output  ：
 * Return  ：void
 * Mark :
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
uint32_t HashFuncAdditive(uint8_t *ptHashKey, uint32_t ulHashkeyLen,uint32_t prime)
{
    uint32_t hash, i;

    for(hash = ulHashkeyLen, i = 0; i < ulHashkeyLen; ++i)
    {
        hash += (uint32_t)(ptHashKey[i]);
    }
    return (hash%prime);
}
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * Function Name ：HashFuncMultiplication
 * Description ：乘法哈希
 * Input  ：
 *          uint8_t *ptHashKey //哈希key
 *          uint32_t ulHashkeyLen//key长度
 * Output  ：
 * Return  ：void
 * Mark :
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
uint32_t HashFuncMultiplication(uint8_t *ptHashKey, uint32_t ulHashkeyLen,uint32_t ulHashbit)
{
    uint32_t hash, i;
    for(hash = 0, i = 0; i < ulHashkeyLen; ++i)
    {
        hash = 33*hash + (uint32_t)(ptHashKey[i]);
    }
    return hash;
}
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * Function Name ：HashFuncFowlerNollVo
 * Description ：FNV哈希算法
 * Input  ：
 *          uint8_t *ptHashKey //哈希key
 *          uint32_t ulHashkeyLen//key长度
 *          uint32_t ulHashbit//位宽
 * Output  ：
 * Return  ：void
 * Mark :
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
uint32_t HashFuncFowlerNollVo(uint8_t *ptHashKey, uint32_t ulHashkeyLen,uint32_t ulHashbit)
{
    uint32_t i ;
    uint32_t ulMask ;
    uint32_t ulHashValue = 2166136261;

    if(null_ptr == ptHashKey || 0 == ulHashkeyLen)
    {
        // LOG_RECORD(LOG_LEV_ERROR, "input params invalid, Hashkey = %d, KeyLen=%d",  ptHashKey,ulHashkeyLen);
        return null_byte_dword;
    }

    ulMask = TINY_MASK(ulHashbit);

    for(i = 0; i < ulHashkeyLen; i++)
    {
        ulHashValue *= 16777619;
        ulHashValue ^= (uint32_t)(ptHashKey[i]);
    }

    return (((ulHashValue>>ulHashbit)^ulHashValue) & ulMask);
}

/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * Function Name ：THListHead
 * Description ：初始化hash桶的头结点
 * Input  ：
 *          THashManager *pstHash
 *          uint32_t ulBitWidth//key长度
 * Output  ：
 * Return  ：void
 * Mark :
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
uint32_t HashManagerInit(THashManager *pstHash, uint32_t ulBitWidth,HashFunc pfHashFunc)
{
    uint32_t index = 0;
    uint32_t ulsize = 0;
    THashHead *ptHashHead = null_ptr;

    if (null_ptr == pstHash)
    {
        // LOG_RECORD(LOG_LEV_ERROR,"pstHash is null");
        return proc_fail;
    }

    if (( 0 == ulBitWidth) || ( ulBitWidth > MAX_BIT_WIDTH))
    {
        // LOG_RECORD(LOG_LEV_ERROR,"ulBitWidth is invalid");
        return proc_fail;
    }

    ulsize = HASH_BUCKET_NUM(ulBitWidth);
    ptHashHead = (THashHead *)malloc(ulsize * sizeof(THashHead));
    if(null_ptr == ptHashHead)
    {
        // LOG_RECORD(LOG_LEV_ERROR, "malloc the hashhead fail \r\n");
        return proc_fail;
    }

    pstHash->ulBitWidth = ulBitWidth;
    pstHash->pstHashHead = ptHashHead;
    pstHash->ulNumUsed = 0;
    pstHash->pHashFunc = pfHashFunc;

    for (index=0; index<ulsize; index++)
    {
        HListInitHead(&ptHashHead->hlistfirst);
        ptHashHead->usSize = 0;
        ptHashHead ++;
    }
    return proc_succ;
}
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * Function Name ：HashManagerGetBucketHead
 * Description ：根据hash 值找到对应的桶节点
 * Input  ：
 *          THashManager *pstHash //哈希
 *          uint8_t *ptHashKey //哈希key
 *          uint32_t ulHashkeyLen//key长度
 * Output  ：
 * Return  ：void
 * Mark :
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
THashHead* HashManagerGetBucketHead(THashManager *pstHash,  uint8_t * pucKey, uint32_t ulKeyLen)
{
    uint32_t ulHashValue = 0;

    ulHashValue = pstHash->pHashFunc(pucKey, ulKeyLen,pstHash->ulBitWidth);
    return (pstHash->pstHashHead) + ulHashValue; //获取对应Hash值对应的桶
}

/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * Function Name ：HashManagerInsert
 * Description ：插入hash数据
 * Input  ：
 *          THashManager *pstHash //哈希
 *          uint8_t *ptHashKey //哈希key
 *          uint32_t ulHashkeyLen//key长度
 *          uint64_t ulData //哈希表存储的数据，一般情况是一个表的索引
 * Output  ：
 * Return  ：void
 * Mark :
 * * * * * ** * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
bool_t HashManagerInsert(THashManager *ptHash, uint8_t *pcKey, uint32_t ulKeyLen, uint64_t ulData )
{
    THashElem *ptHashElem ;
    THashHead *ptHashHead ;

    if ((null_ptr == ptHash) || (null_ptr == pcKey) )
    {
        // LOG_RECORD(LOG_LEV_ERROR, "input params invalid,pstHash = %d, pucKey = %d, ulData = %d", ptHash, pcKey, ulData);
        return proc_fail;
    }

    //加keylen的长度，是因为这里要存储key的值。
    ptHashElem = (THashElem * )malloc(sizeof(THashElem)+ulKeyLen);
    if (null_ptr == ptHashElem)
    {
        // LOG_RECORD(LOG_LEV_ERROR, "malloc hashnode mem failed");
        return proc_fail;
    }

    ptHashElem->ulData = ulData;
    ptHashElem->ulKeyLen = ulKeyLen;

    //存储key
    memcpy_s(ptHashElem->pucKey,ulKeyLen,pcKey,ulKeyLen);
    //找到桶节点的头
    ptHashHead = HashManagerGetBucketHead(ptHash,pcKey,ulKeyLen);
    //将新的节点插入到桶里面
    HlistAddHead(&ptHashElem->hlistnode,&ptHashHead->hlistfirst);
    ptHashHead->usSize ++;
    ptHash->ulNumUsed ++;

    return proc_succ;
}

/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * Function Name ：HashManagerLookup
 * Description ：查找hash，返回存储的data
 * Input  ：
 *          THashManager *pstHash //哈希
 *          uint8_t *ptHashKey //哈希key
 *          uint32_t ulHashkeyLen//key长度
 * Output  ：
 * Return  ：void
 * Mark :
 * * * * * ** * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
uint64_t HashManagerLookup(THashManager *ptHash, uint8_t *pcKey, uint32_t ulKeyLen)
{
    THashElem *ptHashElem;
    THashHead *ptHashHead;
    THListNode *pstListTemp;
    uint64_t ulHashData = null_byte_dword;

    ptHashHead = HashManagerGetBucketHead(ptHash,pcKey,ulKeyLen);

    HListForEach(pstListTemp,&ptHashHead->hlistfirst)
    {
        ptHashElem = HListEntryGet(pstListTemp,THashElem,hlistnode);
        if(0 == memcmp(ptHashElem->pucKey,pcKey,ulKeyLen))
        {
            ulHashData = ptHashElem->ulData;
            break;
        }
    }

    return ulHashData;
}

/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * Function Name ：HashManagerDelete
 * Description ： 删除hash节点
 * Input  ：
 *          THashManager *pstHash //哈希
 *          uint8_t *ptHashKey //哈希key
 *          uint32_t ulHashkeyLen//key长度
 * Output  ：
 * Return  ：void
 * Mark :
 * * * * * ** * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
uint64_t HashManagerDelete(THashManager *ptHash, uint8_t *pcKey, uint32_t ulKeyLen)
{
    THashElem* pstHashElem ;
    THashHead* pstHashHead ;
    THListNode *pstListTemp;
    THListNode *pstListSafe;
    bool_t bret = hash_false;

    if ((null_ptr == ptHash) || (null_ptr == pcKey) || (0 == ulKeyLen))
    {
        // LOG_RECORD(LOG_LEV_ERROR, "input params invalid,pstHash = %d, pucKey = %d, ulKeyLen = %d", ptHash, pcKey, ulKeyLen);
        return proc_fail;
    }

    pstHashHead = HashManagerGetBucketHead(ptHash,pcKey,ulKeyLen);

    HListForEachSafe(pstListTemp,pstListSafe,&pstHashHead->hlistfirst)
    {
        pstHashElem = HListEntryGet(pstListTemp,THashElem,hlistnode);
        if(0 == memcmp(pstHashElem->pucKey,pcKey,ulKeyLen))
        {
            pstHashHead->usSize --;
            HListDelInit(&pstHashElem->hlistnode);
            free(pstHashElem);
            pstHashElem = null_ptr;
            ptHash->ulNumUsed --;
            bret = hash_true;
            break;
        }
    }

    return bret;
}
```