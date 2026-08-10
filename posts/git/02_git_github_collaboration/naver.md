# 2장 통합 실습: GitHub 협업 프로젝트의 전체 흐름과 형상관리 이해하기

> **대상:** Git의 기본 동작을 학습한 초보자  
> **선행 학습:** 「1장 통합 실습: Git의 동작 원리와 안전한 저장소 시작」  
> **권장 환경:** Windows 10/11, PowerShell, Git, VS Code, GitHub

지난 1장에서는 `Working Directory → Staging Area → Local Repository`의 흐름을 학습했습니다. 이번 장에서는 이 구조를 GitHub 원격 저장소와 팀 프로젝트 협업까지 확장합니다.

![Git의 기본 흐름과 저장 구조](./images/01-git-storage-flow.png)

이번 장에서 계속 생각할 질문은 하나입니다.

> **지금 내가 만든 변경은 어디에 있는가?**

---

## 1. 파일 변경은 지금 어디에 있을까?

![파일 변경은 지금 어디에 있을까](./images/02-change-location-by-stage.png)

`app.py`를 수정했다고 가정합니다.

- 파일 수정 직후: 변경은 Working Directory에 있습니다.
- `git add` 후: 선택한 변경이 Staging Area에 staged 됩니다.
- `git commit` 후: 새로운 Commit이 Local Repository에 생성됩니다.
- `git push` 후: Local Commit이 GitHub Remote Repository에 공유됩니다.

```powershell
git add app.py
git commit -m "feat: update dashboard"
git push
```

Staging Area는 Commit 후 단순히 “비어 있다”고 외우기보다 **새로 staged된 변경이 없고 현재 Commit과 같은 상태**라고 이해하는 것이 좋습니다.

---

## 2. Git과 GitHub, 그리고 clone

![Git과 GitHub 그리고 clone](./images/03-git-vs-github-clone.png)

Git은 버전 관리 도구이고 GitHub는 Git 저장소를 온라인에서 공유하고 협업할 수 있도록 도와주는 서비스입니다.

`git clone`은 단순한 ZIP 다운로드와 다릅니다.

```powershell
git clone <팀 저장소 URL>
```

clone을 하면 프로젝트 파일뿐 아니라 Commit 이력, Branch 정보, 원격 저장소 연결 정보까지 함께 준비됩니다.

---

## 3. 브랜치와 HEAD 이해하기

![브랜치와 HEAD 이해하기](./images/04-branch-and-head.png)

Branch는 폴더 복사본이 아니라 Commit을 가리키는 이름 또는 포인터입니다.

```powershell
git switch -c feature/dashboard
git branch --show-current
```

처음에는 `main`과 새 Branch가 같은 Commit을 가리킵니다. 새 Branch에서 Commit을 만들면 작업선이 갈라집니다.

```text
A --- B --- C                  <- main
           \
            D --- E            <- feature/dashboard
```

HEAD는 보통 현재 작업 중인 Branch를 가리킵니다.

---

## 4. 팀 프로젝트 전체 형상관리 흐름

![팀 프로젝트 전체 형상관리 흐름](./images/05-team-configuration-flow.png)

팀 프로젝트의 기본 흐름은 다음과 같습니다.

```text
Issue
-> 최신 main 확인
-> 개인 Branch
-> 파일 수정
-> Add
-> Commit
-> Push
-> Pull Request
-> Review
-> 수정
-> 다시 Commit / Push
-> Merge
-> Pull
```

`main`은 팀이 검토하고 통합한 현재의 공식 프로젝트 버전으로 이해하면 좋습니다.

---

## 5. 프로젝트를 시작할 때의 기본 시나리오

![프로젝트 시작 기본 시나리오](./images/06-project-start-scenario.png)

처음 프로젝트를 받습니다.

```powershell
cd C:\dev
git clone <팀 저장소 URL>
cd <저장소명>
```

상태를 확인합니다.

```powershell
git status
git log --oneline -5
git branch
git remote -v
```

새 작업 전에는 최신 main을 받습니다.

```powershell
git switch main
git pull origin main
```

그리고 최신 main에서 개인 작업 Branch를 만듭니다.

```powershell
git switch -c feature/analysis-metrics
```

---

## 6. 작업 브랜치에서 수정하고 Commit하기

![작업 브랜치에서 수정하고 Commit하기](./images/07-work-branch-commit.png)

파일을 수정한 뒤 먼저 확인합니다.

```powershell
git status
git diff
```

다음 Commit에 넣을 변경을 선택합니다.

```powershell
git add src/analysis.py
```

Commit을 만듭니다.

```powershell
git commit -m "feat: add category sales calculation"
```

새 Commit은 먼저 Local Repository에 만들어집니다. 아직 GitHub에는 없을 수 있습니다.

---

## 7. Push, Pull Request, Review, 수정 반영

![Push Pull Request Review 수정 반영](./images/08-push-pr-review.png)

처음 Push합니다.

```powershell
git push -u origin feature/analysis-metrics
```

중요한 점은 **Push와 Merge는 다르다**는 것입니다. Push는 개인 Branch를 GitHub에 공유한 것이며 아직 main에 포함된 것은 아닙니다.

GitHub에서 Pull Request를 생성합니다.

```text
base: main
compare: feature/analysis-metrics
```

다른 팀원은 `Files changed`를 확인하고 가능하면 직접 실행한 뒤 Comment, Approve 또는 Request changes를 선택합니다.

리뷰에서 수정 요청을 받았다면 같은 Branch에서 수정합니다.

```powershell
git add src/analysis.py
git commit -m "fix: handle empty category result"
git push
```

같은 Branch에 새 Commit을 Push하면 기존 PR이 자동으로 갱신됩니다.

---

## 8. Merge 후 최신화와 origin/main

![Merge 후 최신화와 원격 추적](./images/09-merge-pull-origin-main.png)

Review가 끝난 변경을 Merge하면 공식 main에 포함됩니다.

하지만 GitHub에서 Merge했다고 다른 팀원의 PC까지 자동으로 바뀌는 것은 아닙니다.

```powershell
git switch main
git pull origin main
```

세 이름을 구분해 봅니다.

- `main`: 내 PC의 로컬 Branch
- `origin/main`: 마지막으로 확인한 원격 main 상태를 나타내는 로컬의 원격 추적 참조
- GitHub main: 실제 GitHub Remote Repository의 main

`git fetch`는 원격 최신 정보를 가져오고, `git pull`은 원격 변경을 받아 현재 Local Branch에 반영합니다.

---

## 9. Merge Conflict와 팀 동시 작업

![Merge Conflict와 팀 동시 작업](./images/10-merge-conflict-team-work.png)

Conflict는 Git의 오류가 아닙니다. 두 변경 중 무엇을 최종 결과로 사용할지 자동 판단하기 어려워 사람이 결정해야 하는 상태입니다.

충돌을 줄이려면 다음 습관이 중요합니다.

1. 역할과 파일 범위를 먼저 정합니다.
2. 최신 main에서 Branch를 만듭니다.
3. PR을 너무 크게 만들지 않습니다.
4. 오래 끌지 말고 자주 Merge합니다.
5. 같은 파일을 수정할 때 미리 소통합니다.
6. Merge 후 최신 main을 다시 Pull합니다.

---

## 10. 길을 잃었을 때 먼저 확인할 명령

```powershell
pwd
git status
git branch --show-current
git log --oneline --decorate --graph -10
git remote -v
```

무작정 명령을 실행하기보다 **현재 폴더, 변경 상태, 현재 Branch, Commit 이력, Remote 주소**를 먼저 확인합니다.

---

## 11. 최종 정리

```text
Working Directory
-> Staging Area
-> Local Repository
-> Remote feature branch
-> Pull Request
-> Review
-> Merge
-> Remote main
-> Local main
```

프로젝트 전체 협업 순서는 다음과 같습니다.

```text
Issue
-> Branch
-> 수정
-> Add
-> Commit
-> Push
-> Pull Request
-> Review
-> 수정 / 추가 Commit
-> Merge
-> Pull
-> 다음 작업
```

명령어를 외우는 것보다 **파일, Commit, Branch와 원격 저장소 사이의 관계를 이해하는 것**이 먼저입니다.

---

## 네이버 블로그 태그

#Git #GitHub #Git초보 #Git협업 #형상관리 #브랜치 #PullRequest #코드리뷰 #Merge #팀프로젝트
