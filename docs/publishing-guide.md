# Publishing Guide

이 저장소는 개발 관련 원본 글과 네이버 블로그 게시용 콘텐츠를 함께 관리합니다.

## 기본 구조

```text
posts/<category>/<post>/
├─ post.md
├─ naver.md
└─ images/
```

## 파일 역할

- `post.md`: GitHub에서 관리하는 원본/상세 버전
- `naver.md`: 네이버 블로그 복사·게시용 버전
- `images/`: 해당 글에서만 사용하는 PNG 도식과 이미지

## 이미지 규칙

- 도식은 PNG 사용을 기본으로 합니다.
- 파일명은 영문 소문자, 숫자, 하이픈을 사용합니다.
- 글 하나의 이미지는 해당 글의 `images/` 폴더에서 관리합니다.
- Markdown에서는 상대경로로 이미지를 연결합니다.

예:

```markdown
![Git 기본 흐름](./images/01-git-storage-flow.png)
```

## 게시 순서

1. `post.md` 원본 작성
2. 도식 및 이미지 생성
3. `naver.md` 게시용 문장/이미지 순서 점검
4. 네이버 블로그에 본문 복사
5. PNG 파일을 순서대로 첨부
6. 게시 후 필요하면 `post.md`의 `naver_url`과 `status` 갱신
