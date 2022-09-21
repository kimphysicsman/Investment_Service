# [Investment_service](https://www.notion.so/kimphysicsman/89c7875b6a0b4235b8eb983aaa15ea80)

> 투자 조회 및 입금 서비스

<br />

## 🔑 MVP

- 데이터 조회 : 투자화면, 투자상세 화면, 투자종목 화면
- 투자금 입금
  - Phase1 : 입금 거래 정보를 서버에 등록
  - Phase2 : phase1 에서 등록한 거래정보 검증 후 실제 고객의 자산을 업데이트

<br />

## 📖 과제 해석

### 1. 고객 관리

`고객`은 본인의 `투자(계좌)` 및 `종목`을 조회할 수 있다.

> - `고객` 정보
>   - 고객명
>   - 패스워드
> - 주요 기능
>   - 로그인

### 2. 투자 관리

`투자(계좌)`는 `고객`에 의해 조회될 수 있다.

> - `투자(계좌)` 정보
>   - `고객` - FK
>   - `증권사` - FK
>   - 계좌명
>   - 계좌번호
>   - 투자원금
>   - 계좌 총 자산
> - 주요 기능
>   - 투자 조회
>   - 투자 상세 조회

### 3. 종목 관리

`종목`은 하나의 `투자(계좌)`에 여러개가 등록될 수 있다. **_(ManyToMany 관계)_**

> - `종목` 정보
>   - `자산그룹` - FK
>   - 종목 이름
>   - 현재가
>   - ISIN
> - `투자종목` 정보
>   - `종목` - FK
>   - `투자(계좌)` - FK
>   - 보유 수량
> - 주요기능
>   - 보유종목 조회

### 4. 투자금 입금 관리

`입금`은 서버에 등록된 입금거래정보를 의미하며 `고객`과 `투자(계좌)`정보를 포함한다. 투

> - '투자금 입금 Phase 1'에서 서버 등록시 DB에 생성된다.
> - '투자금 입금 Phase 2'에서 검증 실패시 DB에서 삭제된다.
> - `입금` 정보
>   - `고객` - FK
>   - `투자(계좌)` - FK
>   - 거래 금액
>   - 거래정보 식별자

<br />

## 🔍 고려항목

### 1. 고객관리 - 로그인

> 요구사항에는 포함되어있지 않지만 **투자 조회(또는 투자금 입금) 시 고객이 본인의 투자를 조회(또는 투자금 입금)한다고 가정하고** JWT를 통한 로그인 기능을 구현하고 고객인증을 통해 본인의 투자(계좌)만을 조회(또는 투자금 입금)할 수 있도록 계획
>
> - 고객 데이터 생성시 비밀번호는 기본 고정값으로 설정, 비밀번호 기본 고정값은 .env파일에서 관리

### 2. 고객 - 투자(계좌) 관계

> 제공된 데이터셋에는 1명의 고객에 1개의 투자(계좌)로만 구성되었지만 구조적으로 **1개 이상의 투자(계좌)를 가질 수 있다고 가정하고 FK로 계획**, 따라서 투자 조회시 본인이 가진 투자(계좌)를 리스트로 조회할 수 있다.
>
> - 투자 조회 정리  
>   (고객 로그인)  
>   -> 고객 본인의 투자(계좌) 리스트 조회  
>   -> 그중에 하나 선택 시 해당 투자(계좌)에 대한 상세 조회  
>   -> 보유 종목 선택시 해당 투자(계좌)의 종목 리스트 조회

### 3. '투자 조회', '보유 종목 조회' -> 응답 데이터에 id 포함

> '투자 상세 조회'를 제외한 '투자 조회'와 '보유 종목 조회' 기능은 여러개가 리스트로 조회될 수 있으므로 **Front에서 각각의 개체를 식별할 수 있는 고유 id값을 응답 데이터에 포함**시킬 계획

<br />

## 💡 기타 추가사항

### 1. Batch

> `apscheduler`/`django-apscheduler`를 이용한 매일 0시 Bacth 함수 실행  
> [대표 코드 보기](https://github.com/kimphysicsman/Investment_Service/blob/2e008ce032a659aa008f2412ee41c36559041ef8/investment/scheduler/updater.py#L1)  
>
> `pandas.read_excel`를 이용한 데이터셋 업데이트  
> [대표 코드 보기](https://github.com/kimphysicsman/Investment_Service/blob/2e008ce032a659aa008f2412ee41c36559041ef8/investment/scheduler/functions.py#L19)  

### 2. 적절한 오류/예외 처리

> `service` / `view` layer구분으로 에러 핸들링 통일성 유지  
> `try/except` / `status`를 이용한 에러 핸들링  
> [대표 코드 보기](https://github.com/kimphysicsman/Investment_Service/blob/2e008ce032a659aa008f2412ee41c36559041ef8/deposit/views.py#L20)

### 3. 원본 데이터와 응답 값에 일관성(Consistency) 이 유지

> `transaction.atomic`을 이용한 Bacth와 투자금입금 적용 함수에 transaction 보장  
> [대표 코드 보기](https://github.com/kimphysicsman/Investment_Service/blob/2e008ce032a659aa008f2412ee41c36559041ef8/deposit/views.py#L65)

### 4. 투자금입금 정보 해시화

> `make_password` / `check_password`를 이용하여 간단하게 해쉬/검증
> [대표 코드 보러가기](https://github.com/kimphysicsman/Investment_Service/blob/2e008ce032a659aa008f2412ee41c36559041ef8/deposit/services/deposit_service.py#L73)


<br />

## ✏ 주요 기능

### 1. 고객 관리

- 로그인 : JWT 토큰 인증

### 2. 투자 관리

- 테이터 조회

  - **투자 화면**
    > - 계좌명
    > - 증권사
    > - 계좌번호
    > - 계좌 총 자산
  - **투자 상세 화면**
    > - 계좌명
    > - 증권사
    > - 계좌번호
    > - 계좌 총 자산
    > - 투자 원금
    > - 총 수익금 (총 자산 - 투자 원금)
    > - 수익률 (총 수익금 / 투자 원금 \* 100)
  - **보유 종목 화면**
    > - 보유 종목명
    > - 보유 종목의 자산군
    > - 보유 종목의 평가 금액 (종목 보유 수량 \* 종목 현재가)
    > - 보유 종목 ISIN

- 투자금 입금

  - **Phase 1**  
     입금 거래 정보들을 서버에 등록합니다.

    > **요청 데이터**
    >
    > > - 계좌번호
    > > - 고객명
    > > - 거래 금액
    >
    > **응답 데이터**
    >
    > > - 거래정보 식별자 - 요청 데이터 묶음을 식별할 수 있는 key 값

  - **Phase 2**  
     phase1 에서 등록한 거래정보 검증 후 실제 고객의 자산을 업데이트합니다.
    거래 정보를 hashing 하여 서버에 phase2 요청을 하면 서버에서는 phase1 에서 등록하여 저장된 데이터를 hashing 하여
    동일한 데이터에 대한 요청인지 검증을 합니다.
    검증에 성공하면 고객의 총 자산을 업데이트하고 성공 응답을 하고, 검증 실패 시 자산 업데이트 없이 실패 응답을 합니다.

    > **요청 데이터**
    >
    > > - phase1 요청 데이터 계좌번호, 고객명, 거래 금액 순서로 연결한 string 을 hash한 string.
    > > - phase1 에서 응답받은 거래정보 식별자
    >
    > **응답 데이터**
    >
    > > - 입금 거래 결과

<br />

## 💻 기술 스택

`Python` `Django` `DRF`

<br />

## 👉 ERD

> <img width="600" src="https://user-images.githubusercontent.com/68724828/191544952-9ecbbe52-6c3b-4ed5-b229-d16211d9a6ed.png" />

<br />

## 🙏 API 문서

> ![](https://user-images.githubusercontent.com/68724828/191545068-1d5c2dd4-5cd4-4896-b159-2e53dd0ad5f0.png)
>
> ### [상세보기](https://www.notion.so/kimphysicsman/664b9f1e8c0c41c792e801f80ced948f?v=84e97738b1ac49ac82bef79aacd1615b)

<br />

## 📌 컨벤션

### ❓ Commit Message

- feat/ : 새로운 기능 추가/수정/삭제
- enhan/ : 기존 코드에 기능을 추가하거나 기능을 강화할 때
- refac/ : 코드 리팩토링,버그 수정
- test/ : 테스트 코드/기능 추가
- edit/ : 파일을 수정한 경우(파일위치변경, 파일이름 변경, 삭제)

### ❓ Naming

- Class : Pascal
- Variable : Snake
- Function : Snake
- Constant : Pascal + Snake

### ❓ 주석

- Docstring을 활용하여 클래스와 함수단위에 설명을 적어주도록 하자.
- input/output을 명시하여 문서 없이 코드만으로 어떠한 결과가 나오는지 알 수 있도록 하자.

### 🚷 벼락치기의 규칙

- 컨벤션 지키기
- Commit 단위 지키기
- 말 이쁘게하기
- 문제를 마주하여 트러블을 겪었다면, 어떻게 해결을 했는지 공유를 해주기
- 각자의 작업을 미리 작성을 하여서 각자의 작업을 공유하기

<br />

## 📄 기획문서

#### [노션 - 디셈버앤컴퍼니 기업과제](https://www.notion.so/kimphysicsman/89c7875b6a0b4235b8eb983aaa15ea80)
