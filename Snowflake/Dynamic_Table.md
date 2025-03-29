### Dynamic Table이란?
- Dynamic Table은 Snowflake에서 자동으로 최신 데이터를 유지하는 테이블로, ETL(Extract, Transform, Load) 작업을 단순화하고 데이터 동기화를 쉽게 수행할 수 있도록 설계되었음
- 기존 Materialized View와 비슷하지만, 자동 업데이트 주기를 설정할 수 있어 더 효율적임.
- 트리거 없이 최신 데이터 유지가 가능하며, ETL 파이프라인을 간소화하는 데 유용함.

### Dynamic Table의 주요 기능 및 장점
1) 자동 데이터 갱신:
TARGET_LAG 설정을 통해 테이블을 자동으로 업데이트할 수 있음.

2) ETL 간소화:
복잡한 배치 작업 없이 실시간 또는 일정 주기별 업데이트 가능.

3) 쿼리 성능 최적화:
최신 데이터를 저장해두고 조회하기 때문에 복잡한 조인을 최소화할 수 있음.

4) 변환(Transformation) 자동화:
원본 데이터에서 변환된 데이터를 지속적으로 유지하는 테이블 생성 가능.

### Dynamic Table 생성 예제
(1) 기본 Dynamic Table 생성
```sql
CREATE OR REPLACE DYNAMIC TABLE sales_summary
TARGET_LAG = '5 minutes'
WAREHOUSE = my_warehouse
AS
SELECT customer_id, SUM(amount) AS total_spent
FROM raw_sales
GROUP BY customer_id;
```
- sales_summary 테이블은 raw_sales 테이블에서 최신 데이터를 반영
- TARGET_LAG = '5 minutes' → 최대 5분 간격으로 자동 업데이트
- WAREHOUSE = my_warehouse → 데이터 처리를 위한 컴퓨팅 리소스 지정

(2) Dynamic Table을 활용한 변환(Transformation)
```sql
CREATE OR REPLACE DYNAMIC TABLE daily_sales_report
TARGET_LAG = '1 hour'
WAREHOUSE = compute_wh
AS
SELECT 
    DATE(order_date) AS order_day, 
    SUM(amount) AS total_sales, 
    COUNT(order_id) AS order_count
FROM orders
GROUP BY order_day;
```
* 활용 상황
  - 실시간 분석 대시보드: 최신 일일 매출 데이터를 유지하며, BI 툴과 연동 가능
  - 데이터 정제 및 집계: 원본 orders 테이블에서 날짜별 매출 집계를 자동으로 생성

(3) Dynamic Table을 활용한 다중 테이블 조인
```sql
CREATE OR REPLACE DYNAMIC TABLE customer_order_summary
TARGET_LAG = '15 minutes'
WAREHOUSE = analytics_wh
AS
SELECT 
    c.customer_id, 
    c.name, 
    COUNT(o.order_id) AS total_orders, 
    SUM(o.amount) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;
```
* 활용 상황
  - 고객별 주문 현황을 지속적으로 최신 상태로 유지
  - BI 툴과 연결하여 실시간 리포트 제공

### Dynamic Table 활용 사례
1) 활용 사례 1: 실시간 데이터 분석
TARGET_LAG = '1 minute'로 설정하여 거의 실시간으로 데이터 분석 가능
(BI 대시보드에서 최신 매출 정보 제공 가능)

2) 활용 사례 2: ETL(Extract, Transform, Load) 자동화
데이터 웨어하우스에서 변환된 데이터를 저장할 때 기존 ETL 작업 대신 Dynamic Table 사용
데이터 스케줄링 없이 자동 업데이트 가능

3) 활용 사례 3: 데이터 마트(Data Mart) 구축
Dynamic Table을 사용하여 부서별 맞춤 데이터 마트 생성
예: finance_sales, marketing_campaign_performance 등

### Dynamic Table vs. 기존 방법 비교
![image](https://github.com/user-attachments/assets/75521f00-6718-4cb0-a7c0-316ffcefd503)

### 결론
- Dynamic Table은 자동 업데이트 기능을 제공하여, 실시간 분석과 ETL 작업을 간소화할 수 있음
- Materialized View보다 더 유연하고, 주기적인 데이터 동기화가 필요할 때 유리함
- 특히 데이터 마트 구축, 실시간 분석, BI 보고서 최적화 등에 효과적

