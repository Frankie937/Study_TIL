( 현재 다니고 있는 회사에서 Snowflake DB를 사용하는데, 보안정책이 강화됨에 따라 계정의 보안 인증 방식에 대한 정리) 


### 인증 방식
1) PASSWORD + MFA적용 : 패스워드를 통해 사용자 인증 (패스워드는 snowflake 내에 암호화 되어 안전하게 보관)
-> MFA를 이용한 2차 인증이 필수사항으로 변경 
2) SAML SOO : 회사가 보유하고 있는 External idP와 인증을 통하여 사용자 인증 
3) OAuth : 회사가 보유하고 있는 External idP와 인증을 통하여 사용자 인증 
  - Snowflake는 integration을 통해 클라이언트에 대한 OAuth를 활성화 함. 
  (**integration은 snowflake와 서드파티 서비스 간의 인터페이스를 제공하는 snowflake 오브젝트이다.
  - 관리자(DBA)는 클라이언트가 사용자를 인증 페이지로 리다이렉션하고, snowflake에 액세스하기 위한 액세스 토큰과 선택적으로 새로고침 토큰을 생성하기 위해 OAuth를 지원할 수 있도록 OAuth를 구성
  - OAuth(Open Authorization) 프로토콜을 사용하여 인증을 수행하는 방식
  - Snowflake 자체 OAuth 서버 또는 외부 IDP(예: Okta, Google, Azure AD)를 사용할 수 있음
  - 비밀번호 없이 토큰을 이용한 인증이 가능
    ``` sql
    # OAuth 보안 통합(Security Integration) 생성
    CREATE SECURITY INTEGRATION my_oauth_integration
    TYPE = OAUTH
    AUTH_CLIENT = 'TABLEAU'
    ENABLED = TRUE;

    # OAuth 인증 URL 확인 및 발급
    SELECT SYSTEM$SHOW_OAUTH_AUTHORIZATION_URL('my_oauth_integration');
    ```
  - OAuth를 사용하는 계정 등록
    - 애플리케이션(Tableau 등)에서 OAuth 인증 설정
    - Access Token을 이용하여 접속 
4) KEY-PAIR :  Public/Private key를 통해서 사용자 인증  

### 사용자 Type이 생김 - Person / Service / (Legacy_Service --임시) 
* Person
  - PASSWORD + MFA적용
  - SAML SOO
  - OAuth
* Service 
  - KEY-PAIR 
  - OAuth
 

  
