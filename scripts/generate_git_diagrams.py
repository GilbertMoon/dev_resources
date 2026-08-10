from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path('posts/git/02_git_github_collaboration/images')
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1600, 1000
NAVY = '#123A8C'
BLUE = '#1F5CC4'
LIGHT = '#F5F8FD'
PALE = '#EAF2FF'
GREEN = '#218739'
RED = '#C83D32'
GRAY = '#5A6472'
DARK = '#111827'
WHITE = '#FFFFFF'
BORDER = '#B8C8E6'

FONT_CANDIDATES = [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJKkr-Regular.otf',
    '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
]
BOLD_CANDIDATES = [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJKkr-Bold.otf',
    '/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
]

def find_font(candidates):
    for p in candidates:
        if Path(p).exists():
            return p
    return candidates[-1]

REG = find_font(FONT_CANDIDATES)
BOLD = find_font(BOLD_CANDIDATES)

def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else REG, size)

def text_size(draw, text, f):
    box = draw.textbbox((0, 0), text, font=f)
    return box[2] - box[0], box[3] - box[1]

def center_text(draw, box, text, f, fill=DARK):
    x1, y1, x2, y2 = box
    tw, th = text_size(draw, text, f)
    draw.text(((x1+x2-tw)/2, (y1+y2-th)/2-2), text, font=f, fill=fill)

def rounded(draw, box, fill=WHITE, outline=NAVY, width=3, radius=20):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def line(draw, pts, fill=NAVY, width=5):
    draw.line(pts, fill=fill, width=width)

def arrow(draw, start, end, fill=BLUE, width=6, head=16):
    x1,y1=start; x2,y2=end
    draw.line((x1,y1,x2,y2), fill=fill, width=width)
    import math
    ang=math.atan2(y2-y1,x2-x1)
    a1=ang+2.55; a2=ang-2.55
    p1=(x2+head*math.cos(a1), y2+head*math.sin(a1))
    p2=(x2+head*math.cos(a2), y2+head*math.sin(a2))
    draw.polygon([(x2,y2),p1,p2], fill=fill)

def title(draw, t, sub=''):
    center_text(draw, (50,25,W-50,105), t, font(52, True), NAVY)
    if sub:
        center_text(draw, (80,105,W-80,158), sub, font(25), DARK)

def label(draw, xy, t, size=24, bold=False, fill=DARK):
    draw.text(xy, t, font=font(size,bold), fill=fill)

def box_text(draw, box, t, size=26, fill=WHITE, outline=NAVY, color=DARK, bold=False):
    rounded(draw, box, fill, outline, 3, 16)
    center_text(draw, box, t, font(size,bold), color)

def node(draw, x, y, txt, r=34, fill=WHITE, outline=NAVY):
    draw.ellipse((x-r,y-r,x+r,y+r), fill=fill, outline=outline, width=4)
    center_text(draw, (x-r,y-r,x+r,y+r), txt, font(25,True), NAVY)

def commit_chain(draw, xs, y, labels, branch=None, branch_x=None):
    for i in range(len(xs)-1):
        line(draw, (xs[i]+34,y,xs[i+1]-34,y), NAVY, 4)
    for x,t in zip(xs,labels): node(draw,x,y,t)
    if branch:
        bx = branch_x if branch_x is not None else xs[-1]+65
        arrow(draw, (bx+120,y), (xs[-1]+40,y), NAVY, 4, 13)
        box_text(draw,(bx,y-32,bx+120,y+32),branch,19,PALE,NAVY,NAVY,True)

def save(img, name):
    img.save(OUT/name, 'PNG', optimize=True)

# 1. Git storage flow
img=Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)
title(d,'Git의 기본 흐름과 저장 구조','Working Directory → Staging Area → Local Repository → GitHub Remote Repository')
box_text(d,(475,200,1125,310),'Working Directory',36,PALE,NAVY,NAVY,True)
arrow(d,(800,310),(800,395)); label(d,(835,340),'git add',28,True,NAVY)
box_text(d,(475,395,1125,505),'Staging Area',36,PALE,NAVY,NAVY,True)
arrow(d,(800,505),(800,590)); label(d,(835,535),'git commit',28,True,NAVY)
box_text(d,(475,590,1125,700),'Local Repository (.git)',36,PALE,NAVY,NAVY,True)
arrow(d,(800,700),(800,790)); label(d,(835,730),'git push',28,True,NAVY)
box_text(d,(475,790,1125,900),'GitHub Remote Repository',34,LIGHT,NAVY,NAVY,True)
label(d,(80,920),'핵심: add는 스테이징, commit은 로컬 기록, push는 원격 공유입니다.',26,True,DARK)
save(img,'01-git-storage-flow.png')

# 2. change location by stage
img=Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)
title(d,'파일 변경은 지금 어디에 있을까?','수정 → add → commit → push 단계에서 변경이 존재하는 위치')
cols=[35,420,805,1190]
heads=['1. 파일 수정 직후','2. git add 후','3. git commit 후','4. git push 후']
for x,h in zip(cols,heads):
    rounded(d,(x,180,x+350,900),LIGHT,BORDER,2,18)
    box_text(d,(x+20,200,x+330,260),h,22,NAVY,NAVY,WHITE,True)
# col1
box_text(d,(60,300,360,390),'Working Directory\napp.py : 수정됨',22,PALE,NAVY,DARK,True)
box_text(d,(60,440,360,550),'Staging Area\nstaged 변경 없음\nHEAD와 동일',20,WHITE,NAVY,DARK)
box_text(d,(60,610,360,700),'Local Repository\nCommit A',20,WHITE,NAVY,DARK)
box_text(d,(60,755,360,845),'GitHub\nCommit A',20,WHITE,NAVY,DARK)
# col2
box_text(d,(445,300,745,390),'Working Directory\napp.py : 수정됨',22,PALE,NAVY,DARK,True)
box_text(d,(445,440,745,550),'Staging Area\napp.py 변경 staged\n다음 Commit 후보',20,PALE,GREEN,DARK)
box_text(d,(445,610,745,700),'Local Repository\nCommit A',20,WHITE,NAVY,DARK)
box_text(d,(445,755,745,845),'GitHub\nCommit A',20,WHITE,NAVY,DARK)
# col3
box_text(d,(830,300,1130,390),'Working Directory\nCommit B와 동일',21,WHITE,NAVY,DARK)
box_text(d,(830,440,1130,550),'Staging Area\nstaged 변경 없음\nCommit B와 동일',20,WHITE,NAVY,DARK)
box_text(d,(830,610,1130,700),'Local Repository\nCommit A → Commit B',20,PALE,GREEN,DARK,True)
box_text(d,(830,755,1130,845),'GitHub\nCommit A (Push 전)',20,WHITE,NAVY,DARK)
# col4
box_text(d,(1215,300,1515,390),'Working Directory\nCommit B와 동일',21,WHITE,NAVY,DARK)
box_text(d,(1215,440,1515,550),'Staging Area\nstaged 변경 없음',20,WHITE,NAVY,DARK)
box_text(d,(1215,610,1515,700),'Local Repository\nCommit A → Commit B',20,WHITE,NAVY,DARK)
box_text(d,(1215,755,1515,845),'GitHub\nCommit A → Commit B',20,PALE,GREEN,DARK,True)
save(img,'02-change-location-by-stage.png')

# 3 Git vs GitHub and clone
img=Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)
title(d,'Git과 GitHub, 그리고 clone 이해하기','Git은 버전 관리 도구, GitHub는 원격 협업 서비스입니다.')
rounded(d,(70,190,740,520),LIGHT,NAVY,3,20); rounded(d,(860,190,1530,520),LIGHT,NAVY,3,20)
center_text(d,(90,205,720,265),'Git',font(38,True),NAVY); center_text(d,(880,205,1510,265),'GitHub',font(38,True),NAVY)
label(d,(130,300),'status   add   commit   branch   switch',25,False,DARK)
label(d,(130,350),'merge    log   fetch    pull     push',25,False,DARK)
label(d,(930,300),'Remote Repository   Collaborator',25,False,DARK)
label(d,(930,350),'Issue   Pull Request   Review   Merge',25,False,DARK)
box_text(d,(120,615,620,800),'GitHub Remote Repository\n파일 + Commit 이력 + Branch 정보',25,PALE,NAVY,DARK,True)
arrow(d,(650,705),(940,705),NAVY,8,24); label(d,(735,650),'git clone',34,True,NAVY)
box_text(d,(980,615,1480,800),'내 PC\nWorking Directory\nLocal Repository (.git)\norigin 설정',24,PALE,NAVY,DARK,True)
label(d,(215,850),'ZIP 다운로드는 현재 파일 중심, git clone은 저장소 이력과 원격 연결 정보까지 함께 가져옵니다.',24,True,DARK)
save(img,'03-git-vs-github-clone.png')

# 4 branch and HEAD
img=Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)
title(d,'브랜치와 HEAD 이해하기','브랜치는 폴더 복사가 아니라 Commit을 가리키는 포인터입니다.')
label(d,(90,190),'1) main만 있을 때',28,True,NAVY)
commit_chain(d,[250,430,610],285,['A','B','C'],'main',690)
label(d,(90,380),'2) feature/dashboard 생성 직후',28,True,NAVY)
commit_chain(d,[250,430,610],475,['A','B','C'],'main',690)
box_text(d,(690,530,970,590),'feature/dashboard',22,PALE,NAVY,NAVY,True); arrow(d,(690,560),(635,490),NAVY,4,13)
label(d,(90,665),'3) feature에서 D, E Commit 생성',28,True,NAVY)
commit_chain(d,[200,350,500],755,['A','B','C'],'main',580)
line(d,(525,775,610,830),NAVY,4); line(d,(610,830,735,830),NAVY,4); node(d,610,830,'D'); node(d,735,830,'E')
box_text(d,(840,795,1125,860),'feature/dashboard',21,PALE,NAVY,NAVY,True); arrow(d,(840,828),(775,830),NAVY,4,13)
box_text(d,(1160,795,1310,860),'HEAD',22,WHITE,GREEN,GREEN,True); arrow(d,(1160,828),(780,845),GREEN,4,13)
label(d,(1010,900),'HEAD는 현재 작업 중인 브랜치를 따라갑니다.',24,True,DARK)
save(img,'04-branch-and-head.png')

# 5 team configuration flow
img=Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)
title(d,'팀 프로젝트의 전체 형상관리 흐름','Local 작업이 GitHub를 거쳐 공식 main으로 통합되는 과정')
rounded(d,(70,180,745,900),LIGHT,NAVY,3,20); rounded(d,(855,180,1530,900),LIGHT,NAVY,3,20)
box_text(d,(205,205,610,270),'내 컴퓨터 - Local',30,NAVY,NAVY,WHITE,True)
left=[('파일 수정',315),('Working Directory',395),('Staging Area',505),('Local Repository',615),('Local feature branch',725)]
for t,y in left: box_text(d,(190,y,625,y+65),t,23,WHITE,NAVY,DARK,True)
for y,txt in [(380,'git add'),(490,'git commit'),(710,'')]: pass
arrow(d,(407,380),(407,395)); label(d,(430,365),'git add',20,True,NAVY)
arrow(d,(407,470),(407,505)); label(d,(430,475),'git add',20,True,NAVY)
arrow(d,(407,570),(407,615)); label(d,(430,585),'git commit',20,True,NAVY)
arrow(d,(407,680),(407,725));
box_text(d,(990,205,1395,270),'GitHub - Remote',30,NAVY,NAVY,WHITE,True)
right=[('Issue',315),('Remote feature branch',395),('Pull Request',485),('Review',575),('Merge',690),('main',780)]
for t,y in right: box_text(d,(970,y,1415,y+60),t,23,WHITE,NAVY,DARK,True)
for a,b in [(375,395),(455,485),(545,575),(635,690),(750,780)]: arrow(d,(1192,a),(1192,b))
arrow(d,(625,757),(970,425),NAVY,6,18); label(d,(690,650),'git push',23,True,NAVY)
arrow(d,(1192,840),(600,860),GREEN,6,18); label(d,(810,865),'Merge 후 다른 팀원은 git pull',22,True,GREEN)
label(d,(110,925),'핵심: Issue → Branch → Commit → Push → PR → Review → Merge → Pull',27,True,DARK)
save(img,'05-team-configuration-flow.png')

# 6 project start scenario
img=Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)
title(d,'프로젝트를 시작할 때의 기본 시나리오','Clone부터 최신 main 동기화, Issue 확인, 개인 브랜치 생성까지')
steps=['원격 저장소 확인','Clone','Issue 확인','최신 main Pull','개인 Branch 생성','파일 수정','Status / Diff 확인','Add','Commit','Push','Pull Request','Review','수정','다시 Commit / Push','Merge','최신 main Pull','다음 작업']
y=185
for i,s in enumerate(steps):
    box_text(d,(125,y,675,y+42),s,20,PALE if i<5 else WHITE,NAVY,DARK,i in {0,1,2,3,4,15})
    if i < len(steps)-1: arrow(d,(400,y+42),(400,y+53),NAVY,3,8)
    y += 47
rounded(d,(800,190,1490,890),LIGHT,NAVY,3,20)
label(d,(850,225),'새 작업 전 최신 main 받기',30,True,NAVY)
label(d,(850,295),'GitHub main',24,True,DARK); commit_chain(d,[980,1160,1340],360,['A','B','C'],'main',1410)
label(d,(850,455),'Local main (pull 전)',24,True,DARK); commit_chain(d,[1020,1210],520,['A','B'],'main',1280)
arrow(d,(1170,580),(1170,650),GREEN,7,20); label(d,(1210,605),'git pull',26,True,GREEN)
label(d,(850,685),'Local main (pull 후)',24,True,DARK); commit_chain(d,[980,1160,1340],750,['A','B','C'],'main',1410)
label(d,(870,835),'새 Branch는 가능한 한 최신 main에서 시작합니다.',24,True,DARK)
save(img,'06-project-start-scenario.png')

# 7 work branch commit
img=Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)
title(d,'작업 브랜치에서 수정하고 Commit하기','파일 수정 → status/diff 확인 → add → commit')
# four quadrants
quads=[(50,180,780,500),(820,180,1550,500),(50,540,780,900),(820,540,1550,900)]
for q in quads: rounded(d,q,LIGHT,NAVY,3,20)
box_text(d,(70,195,360,250),'1. 개인 브랜치 생성',22,NAVY,NAVY,WHITE,True)
commit_chain(d,[180,330,480],345,['A','B','C'],'main',560); box_text(d,(540,400,745,460),'feature/analysis',19,PALE,NAVY,NAVY,True); arrow(d,(540,430),(510,370),NAVY,4,12)
box_text(d,(840,195,1080,250),'2. 파일 수정',22,NAVY,NAVY,WHITE,True)
box_text(d,(900,300,1470,380),'Working Directory\nsrc/analysis.py : 수정됨',24,PALE,GREEN,DARK,True); label(d,(960,415),'git status     git diff',25,True,NAVY)
box_text(d,(70,555,260,610),'3. git add',22,NAVY,NAVY,WHITE,True)
box_text(d,(100,680,350,790),'Working Directory\n수정됨',22,WHITE,NAVY,DARK); arrow(d,(380,735),(480,735),NAVY,6,18); label(d,(395,690),'git add',22,True,NAVY); box_text(d,(510,680,750,790),'Staging Area\n변경 staged',22,PALE,GREEN,DARK,True)
box_text(d,(840,555,1070,610),'4. git commit',22,NAVY,NAVY,WHITE,True)
commit_chain(d,[940,1080,1220],730,['A','B','C'],'main',1290); line(d,(1245,745,1320,690),NAVY,4); node(d,1320,690,'D',34,PALE,GREEN); box_text(d,(1365,655,1520,720),'feature',20,PALE,NAVY,NAVY,True); arrow(d,(1365,688),(1355,690),NAVY,4,11)
label(d,(920,815),'Commit D는 아직 Local Repository에만 존재',22,True,DARK)
save(img,'07-work-branch-commit.png')

# 8 push PR review
img=Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)
title(d,'Push, Pull Request, Review, 수정 반영','개인 브랜치를 공유하고 기존 PR에 수정 Commit을 계속 반영하는 흐름')
boxes=[(50,185,770,500),(830,185,1550,500),(50,545,770,905),(830,545,1550,905)]
for b in boxes: rounded(d,b,LIGHT,NAVY,3,20)
box_text(d,(70,200,260,255),'1. Push',23,NAVY,NAVY,WHITE,True)
label(d,(100,295),'Local feature branch',22,True,DARK); commit_chain(d,[150,275,400,525],350,['A','B','C','D'],'feature',590)
arrow(d,(400,415),(400,460),NAVY,5,15); label(d,(430,425),'git push',22,True,NAVY); label(d,(100,465),'Push ≠ main Merge',24,True,RED)
box_text(d,(850,200,1120,255),'2. Pull Request',23,NAVY,NAVY,WHITE,True)
box_text(d,(900,300,1480,370),'base: main      compare: feature/analysis',22,PALE,NAVY,DARK,True)
for i,t in enumerate(['변경된 Commit과 파일 확인','작업 목적과 실행 방법','검증 결과와 리뷰 의견','최종 Merge 여부']): label(d,(930,410+i*42),f'- {t}',22,False,DARK)
box_text(d,(70,560,260,615),'3. Review',23,NAVY,NAVY,WHITE,True)
for i,t in enumerate(['Files changed 확인','코드 읽기','직접 실행','결과 확인','Comment / Approve / Request changes']): box_text(d,(110,650+i*45,650,686+i*45),t,19,WHITE,BORDER,DARK,i==4)
box_text(d,(850,560,1090,615),'4. 리뷰 반영',23,NAVY,NAVY,WHITE,True)
label(d,(900,665),'수정 전',21,True,DARK); commit_chain(d,[1030,1150,1270,1390],705,['A','B','C','D'],'feature',1440)
arrow(d,(1200,755),(1200,800),GREEN,6,17); label(d,(1230,765),'commit + push',21,True,GREEN)
label(d,(900,820),'수정 후',21,True,DARK); commit_chain(d,[1030,1150,1270,1390,1495],855,['A','B','C','D','E'])
label(d,(950,920),'같은 Branch에 Push하면 기존 PR이 자동 갱신됩니다.',23,True,DARK)
save(img,'08-push-pr-review.png')

# 9 merge pull origin/main
img=Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)
title(d,'Merge 후 최신화와 원격 추적 이해','main, origin/main, GitHub main의 차이와 pull의 역할')
rounded(d,(50,180,770,480),LIGHT,NAVY,3,20); rounded(d,(830,180,1550,480),LIGHT,NAVY,3,20)
box_text(d,(70,200,245,255),'1. Merge',22,NAVY,NAVY,WHITE,True)
label(d,(90,300),'Merge 전',22,True,DARK); commit_chain(d,[230,370,510],335,['A','B','C'],'main',575); line(d,(535,350,600,400),NAVY,4); node(d,600,400,'D'); node(d,720,400,'E'); line(d,(634,400,686,400),NAVY,4)
label(d,(90,430),'Merge 후: 검토된 변경이 공식 main에 포함',21,True,DARK)
box_text(d,(850,200,1220,255),'2. 다른 팀원의 PC',22,NAVY,NAVY,WHITE,True)
label(d,(875,300),'GitHub main: A - B - C - M',22,True,NAVY); label(d,(875,345),'Local main : A - B - C',22,True,DARK); arrow(d,(1130,380),(1130,425),GREEN,6,16); label(d,(1170,390),'git pull',22,True,GREEN); label(d,(875,440),'Local main : A - B - C - M',22,True,DARK)
rounded(d,(50,525,1550,900),LIGHT,NAVY,3,20); box_text(d,(70,545,520,600),'3. main / origin/main / GitHub main',22,NAVY,NAVY,WHITE,True)
headers=['fetch 전','fetch 후','pull 후']; xs=[160,600,1040]
for x,h in zip(xs,headers): label(d,(x,640),h,23,True,NAVY)
# rows
for y,t in [(700,'Local main'),(755,'origin/main'),(810,'GitHub main')]: label(d,(80,y),t,21,True,DARK)
vals=[['A-B','A-B','A-B-C'],['A-B','A-B-C','A-B-C'],['A-B-C','A-B-C','A-B-C']]
for c,x in enumerate(xs):
    for r,y in enumerate([690,745,800]): box_text(d,(x,y,x+310,y+48),vals[c][r],18,WHITE,BORDER,DARK,False)
arrow(d,(500,760),(570,760),NAVY,5,15); arrow(d,(940,760),(1010,760),NAVY,5,15)
label(d,(190,875),'origin/main은 원격 main의 상태를 로컬에서 추적하는 참조입니다.',23,True,DARK)
save(img,'09-merge-pull-origin-main.png')

# 10 conflict and team work
img=Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(img)
title(d,'Merge Conflict와 팀 동시 작업 이해하기','공통 조상에서 갈라진 브랜치와 충돌을 줄이는 협업 방법')
rounded(d,(50,180,1030,520),LIGHT,NAVY,3,20); rounded(d,(1070,180,1550,900),LIGHT,NAVY,3,20)
box_text(d,(70,200,360,255),'1. 충돌이 생기는 구조',22,NAVY,NAVY,WHITE,True)
commit_chain(d,[180,330,480],345,['A','B','C']); line(d,(505,330,630,270),NAVY,4); node(d,650,260,'D'); node(d,790,260,'E'); line(d,(684,260,756,260),NAVY,4); label(d,(850,245),'팀원 A',22,True,NAVY)
line(d,(505,360,630,430),NAVY,4); node(d,650,440,'F'); node(d,790,440,'G'); line(d,(684,440,756,440),NAVY,4); label(d,(850,425),'팀원 B',22,True,NAVY)
label(d,(390,385),'C = 공통 조상',21,True,GREEN)
rounded(d,(50,560,1030,900),LIGHT,NAVY,3,20); box_text(d,(70,580,360,635),'2. 네 명이 동시에 작업',22,NAVY,NAVY,WHITE,True)
label(d,(110,690),'C에서 각 작업 Branch가 시작',22,True,DARK)
for i,(a,b,n) in enumerate([('D1','D2','feature/data-check'),('A1','A2','feature/analysis'),('S1','S2','feature/app'),('R1','R2','docs/readme')]):
    y=720+i*45
    box_text(d,(430,y,510,y+34),a,16,WHITE,NAVY,NAVY,True); arrow(d,(515,y+17),(565,y+17),NAVY,3,9); box_text(d,(570,y,650,y+34),b,16,WHITE,NAVY,NAVY,True); label(d,(680,y+2),n,18,False,DARK)
box_text(d,(1090,200,1495,255),'3. 충돌을 줄이는 방법',22,NAVY,NAVY,WHITE,True)
tips=['역할과 파일 범위 먼저 정하기','최신 main에서 Branch 만들기','PR을 너무 크게 만들지 않기','오래 끌지 말고 자주 Merge하기','같은 파일 수정 전 미리 소통하기','Merge 후 최신 main 다시 pull하기']
for i,t in enumerate(tips,1):
    box_text(d,(1110,305+(i-1)*85,1160,355+(i-1)*85),str(i),20,NAVY,NAVY,WHITE,True); label(d,(1190,313+(i-1)*85),t,20,True,DARK)
label(d,(115,925),'핵심: Conflict는 Git의 오류가 아니라 사람이 최종 선택을 내려야 하는 상황입니다.',25,True,DARK)
save(img,'10-merge-conflict-team-work.png')

print(f'generated {len(list(OUT.glob("*.png")))} diagrams in {OUT}')
