# NoSQL数据库

## 概述

!!! note "NoSQL数据库"
    非关系型数据库,适合大规模数据存储。

## NoSQL特点

<div style="background-color: #E3F2FD; padding: 15px; margin: 10px 0; border-left: 4px solid #2196F3; border-radius: 5px;">
    <strong>NoSQL特点</strong>
    <ul style="margin: 5px 0;">
        <li><strong>灵活的数据模型</strong>: 无固定模式</li>
        <li><strong>水平扩展</strong>: 易于扩展</li>
        <li><strong>高性能</strong>: 高吞吐量</li>
        <li><strong>弱一致性</strong>: 最终一致性</li>
    </ul>
</div>

## NoSQL类型

### 键值存储

!!! tip "键值存储"
    简单的键值对存储。

**代表:** Redis、Memcached

**应用:** 缓存、会话存储

### 文档存储

<div style="background-color: #E8F5E9; padding: 15px; margin: 10px 0; border-left: 4px solid #4CAF50; border-radius: 5px;">
    <strong>文档存储</strong>
    <p style="margin: 5px 0;">存储JSON或XML文档。</p>
</div>

**代表:** MongoDB、CouchDB

**应用:** 内容管理、日志存储

### 列族存储

!!! info "列族存储"
    按列族存储数据。

**代表:** HBase、Cassandra

**应用:** 大数据分析

### 图数据库

<div style="background-color: #FFF3E0; padding: 15px; margin: 10px 0; border-left: 4px solid #FF9800; border-radius: 5px;">
    <strong>图数据库</strong>
    <p style="margin: 5px 0;">存储图结构数据。</p>
</div>

**代表:** Neo4j、JanusGraph

**应用:** 社交网络、推荐系统

## CAP理论

!!! warning "CAP理论"
    - **C(一致性)**: 所有节点数据一致
    - **A(可用性)**: 每个请求都有响应
    - **P(分区容错)**: 网络分区时系统仍工作

**结论:** 最多只能同时满足两个

## 参考资料

- [NoSQL 百度百科](https://baike.baidu.com/item/NoSQL)
