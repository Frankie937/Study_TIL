최근 파이썬 생태계에서는 기존 `requirements.txt` 기반 방식에서 **`pyproject.toml` + `uv**` 조합으로 빠르게 패러다임이 전환되고 있습니다. 신입 개발자의 눈높이에 맞춰 이 방식이 왜 쓰이고, 기존 방식 대비 어떤 장점이 있는지 체계적으로 설명해 드리겠습니다.

---

### 1. `pyproject.toml`이란?

과거 파이썬 프로젝트는 설정 파일이 수없이 파편화되어 있었습니다.

* 패키지 빌드 설정: `setup.py`, `setup.cfg`
* 의존성 관리: `requirements.txt`, `requirements-dev.txt`
* Linter/Formatter 설정: `.eslintrc`, `flake8`, `black.toml` 등

**`pyproject.toml`은 파이썬 표준화 기구(PEP 518, PEP 621)에서 제정한 단일 통합 설정 파일**입니다. 프로젝트의 메타데이터, 의존성 라이브러리, 각종 개발 도구(Ruff, Mypy, Pytest) 설정을 **단 하나의 파일**에서 모두 관리합니다.

---

### 2. 이 `pyproject.toml` 파일 구조 톺아보기

제공해주신 설정 파일의 핵심 구성을 하나씩 살펴보겠습니다.

* **`[project]`**: 프로젝트명(`adca`), 파이썬 최소 버전(`>=3.12`), 기본 실행에 필요한 핵심 라이브러리(`fastapi`, `langgraph`, `pydantic` 등)가 선언되어 있습니다.
* **`[project.optional-dependencies]`**: 선택적 의존성 그룹입니다. 예를 들어 LLM 서비스 없이 로컬 모드로만 돌릴 때는 굳이 heavy한 `openai`나 `anthropic` SDK를 안 깔아도 되게끔 분리해둔 것입니다.
* **`[dependency-groups]` (dev)**: 테스트(`pytest`), 코드 정적 분석(`ruff`, `mypy`)처럼 **실제 배포 환경(운영)에는 필요 없고 개발자 컴퓨터에서만 필요한 라이브러리**를 명확히 구별해 둔 최신 표준 규격입니다.
* **`[project.scripts]`**: `adca = "adca.cli:main"` 구문을 통해 터미널에서 `pip install` 또는 `uv pip install` 후 바로 `adca`라는 명령어로 CLI 프로그램을 실행할 수 있게 등록해 줍니다.
* **`[tool.ruff]`, `[tool.mypy]`, `[tool.pytest.ini_options]**`: 코드 포맷터(Ruff), 타입 검사기(Mypy), 테스트 프레임워크(Pytest)의 개별 설정값을 한 파일에서 깔끔하게 관리합니다.

---

### 3. `uv`는 무엇이고, 왜 같이 쓸까?

`uv`는 Rust 언어로 작성된 **초고속 파이썬 패키지 관리자**입니다 (Ruff를 만든 Astral사 개발). 기존의 `pip`, `virtualenv`, `poetry`, `pipenv` 등을 완벽히 대체하고 있습니다.

* **압도적인 속도**: C++ / Rust 기반으로 제작되어 기존 `pip`나 `poetry`보다 **10~100배 이상 빠릅니다**. (초단위가 아니라 밀리초 단위로 의존성을 해결)
* **통합 관리**: 파이썬 설치(`uv python`), 가상환경 생성, 패키지 설치(`uv sync`), 잠금 파일 생성(`uv lock`)을 `uv` 하나로 다 처리합니다.

---

### 4. `requirements.txt` 방식 대비 무엇이 더 좋을까?

| 구분 | 기존 방식 (`requirements.txt`) | 현대적 방식 (`pyproject.toml` + `uv`) |
| --- | --- | --- |
| **설정 파일 파편화** | `requirements.txt`, `requirements-dev.txt`, `setup.py`, `pytest.ini` 등 수많은 파일로 분산 | `pyproject.toml` **단 1개 파일로 통합** |
| **개발/운영 분리** | 파일별로 직접 나눠 작성해야 하고 관리가 번거로움 | `dependencies`와 `dependency-groups.dev`로 표준화되어 명확히 분리 |
| **의존성 충돌 예방** | 라이브러리 간 하위 의존성(Transitive Dependencies) 충돌 해결 능력이 약함 | 강력한 Resolver와 `uv.lock` 파일 제공으로 **어느 컴퓨터에서 설치해도 100% 동일한 실행 환경 보장** |
| **설치 속도** | 패키지가 많아지면 설치 및 빌드 시간이 수 분 이상 소요 | Rust 기반 엔진 덕분에 병렬 다운로드와 캐싱으로 **수 초 만에 설치 완료** |
| **파이썬 버전 관리** | `pyenv` 등을 별도로 설치해서 파이썬 버전을 맞춰야 함 | `requires-python = ">=3.12"` 선언 시 `uv`가 파이썬 3.12 환경까지 알아서 세팅함 |

---

### 5. 실제 개발 workflow (가이드)

팀에 합류해서 이 프로젝트를 전달받았을 때, `uv`를 사용하면 다음과 같은 단 몇 줄의 명령어만으로 개발 환경 구축부터 실행까지 끝납니다.

```bash
# 1. 프로젝트에 필요한 가상환경 생성 및 의존성 자동 설치 (pyproject.toml 읽어서 처리)
uv sync

# 2. LLM 옵션 기능까지 포함해서 설치하고 싶을 때
uv sync --extra llm

# 3. 가상환경 진입 없이 프로젝트 CLI 명령어 실행
uv run adca

# 4. 새 패키지 추가 시 (pyproject.toml에 자동으로 추가되고 설치됨)
uv add langchain

```

### 요약

현재 IT 업계(특히 AI 및 백엔드 분야)에서는 "파이썬 표준 규격인 `pyproject.toml`로 프로젝트를 정의하고, 초고속 도구인 `uv`로 패키지 및 가상환경을 관리하는 방식"이 대세로 자리 잡았습니다. 단일 파일 관리의 편리함, 명확한 개발/배포 환경 분리, 빠른 빌드 속도 덕분에 대규모 서비스 및 AI 시스템 개발 시 필수적인 선택이 되고 있습니다.
