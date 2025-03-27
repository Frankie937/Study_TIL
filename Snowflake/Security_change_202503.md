( 현재 다니고 있는 회사에서 Snowflake DB를 사용하는데, 보안정책이 강화됨에 따라 계정의 보안 인증 방식에 대한 정리) 


### 인증 방식
1) PASSWORD + MFA적용 : 패스워드를 통해 사용자 인증 (패스워드는 snowflake 내에 암호화 되어 안전하게 보관)
-> MFA를 이용한 2차 인증이 필수사항으로 변경 
2) SAML SOO : 회사가 보유하고 있는 External idP와 인증을 통하여 사용자 인증 
3) OAuth : 회사가 보유하고 있는 External idP와 인증을 통하여 사용자 인증 
4) KEY-PAIR :  Public/Private key를 통해서 사용자 인증  

### 사용자 Type이 생김 - Person / Service / (Legacy_Service --임시) 
* Person
  - PASSWORD + MFA적용
  - SAML SOO
  - OAuth
* Service 
  - KEY-PAIR 
  - OAuth
 
  
