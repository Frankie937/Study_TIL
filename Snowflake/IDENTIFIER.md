### IDENTIFIER() 함수 용도 
* IDENTIFIER() 함수는 동적으로 테이블, 컬럼, 스키마 등의 객체 이름을 변수처럼 처리할 때 사용
* Snowflake에서는 SQL을 실행할 때 문자열 값을 그대로 객체 이름으로 사용하지 않기 때문에, 동적으로 변수를 사용하여 SQL을 작성하려면 IDENTIFIER()를 활용
* 사용 목적 
  - 동적 SQL 생성: 프로시저나 스크립트에서 변수로 테이블 또는 컬럼 이름을 설정할 때 활용
  - 메타데이터 기반 처리: 다른 테이블에서 가져온 값(예: 테이블 이름)을 기반으로 SQL 실행
  - 파라미터 기반 쿼리 작성: 변수 기반으로 테이블이나 컬럼을 지정하여 유연한 쿼리 작성 가능

### 활용예제 
(1) 변수로 테이블 이름을 지정하여 데이터 조회
```sql
DECLARE table_name STRING;
SET table_name = 'orders';

SELECT * FROM IDENTIFIER($table_name);
```
- table_name 변수에 orders 테이블을 저장
- IDENTIFIER($table_name)를 사용해 SELECT * FROM orders;와 동일한 쿼리 실행

(2) 변수로 컬럼 이름을 지정하여 특정 컬럼 조회
```sql
DECLARE column_name STRING;
SET column_name = 'customer_id';

SELECT IDENTIFIER($column_name) FROM orders;
```
- column_name 변수에 customer_id 컬럼을 저장
- IDENTIFIER($column_name)를 사용해 SELECT customer_id FROM orders;와 동일한 쿼리 실행

(3) 프로시저에서 테이블과 컬럼 동적으로 설정
```sql
CREATE OR REPLACE PROCEDURE dynamic_select(table_name STRING, column_name STRING)
RETURNS TABLE()
LANGUAGE SQL
AS
$$
    BEGIN
        RETURN TABLE(SELECT IDENTIFIER(column_name) FROM IDENTIFIER(table_name));
    END;
$$;

CALL dynamic_select('orders', 'customer_id');

```
- table_name과 column_name을 입력 받아 해당 테이블과 컬럼을 조회하는 프로시저
- CALL dynamic_select('orders', 'customer_id'); 실행 시 SELECT customer_id FROM orders;와 동일한 결과 반환

(4) 동적으로 테이블 생성
```sql
DECLARE table_name STRING;
SET table_name = 'new_sales_data';

CREATE TABLE IDENTIFIER($table_name) (
    id INT,
    amount NUMBER(10,2),
    created_at TIMESTAMP
);

```
- 변수 table_name에 테이블명을 저장하고, IDENTIFIER()를 이용해 해당 테이블을 생성
- 실행 결과: new_sales_data라는 테이블이 생성됨

### 결론 
- IDENTIFIER() 함수는 Snowflake에서 변수 기반으로 동적 SQL을 실행할 때 필수적
- 프로시저, 스크립트, 또는 동적 쿼리에서 테이블명, 컬럼명 등을 유연하게 지정해야 할 때 IDENTIFIER()를 활용하면 유용함

