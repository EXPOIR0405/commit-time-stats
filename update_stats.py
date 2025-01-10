from github import Github
from collections import defaultdict
from datetime import datetime, timezone, timedelta
import os
import sys

def get_time_period(hour):
    if 6 <= hour < 12:
        return "Morning", "🌞"
    elif 12 <= hour < 18:
        return "Daytime", "🏢"
    elif 18 <= hour < 24:
        return "Evening", "🌆"
    else:
        return "Night", "🌙"

def main():
    try:
        token = os.getenv('GT_TOKEN')
        if not token:
            print("Error: GT_TOKEN not found")
            sys.exit(1)

        g = Github(token)
        user = g.get_user()
        
        # 커밋 통계 수집
        period_commits = defaultdict(int)
        total_commits = 0
        
        for repo in user.get_repos():
            try:
                commits = repo.get_commits(author=user.login)
                for commit in commits:
                    commit_time = commit.commit.author.date
                    period = get_time_period(commit_time.hour)[0]  # [0]으로 period만 가져오기
                    period_commits[period] += 1
                    total_commits += 1
            except:
                continue

        # max_commits 계산을 여기서 수행
        max_commits = max(period_commits.values()) if period_commits else 1

        try:
            profile_repo = g.get_repo(f"{user.login}/{user.login}")
            contents = profile_repo.get_contents("README.md")
            current_content = contents.decoded_content.decode('utf-8')
            
            # hits 배지 찾기
            hits_marker = "hits&edge_flat=false"
            hits_index = current_content.find(hits_marker)
            
            if hits_index != -1:
                # hits 배지 끝나는 부분 찾기
                insert_position = current_content.find("</p>", hits_index) + 4
                
                # 기존 통계 섹션 제거 (있다면)
                old_stats_start = current_content.find("## ⏰ 시간대별 커밋 분석")
                if old_stats_start != -1:
                    old_stats_end = current_content.find("---", old_stats_start) + 4 if current_content.find("---", old_stats_start) != -1 else len(current_content)
                    current_content = current_content[:old_stats_start] + current_content[old_stats_end:]
                
                # 통계 섹션 생성
                stats_section = '\n## ⏰ 시간대별 커밋 분석\n\n'
                stats_section += '```text\n'
                
                for period, emoji in [
                    ("Morning", "🌞"),
                    ("Daytime", "🏢"),
                    ("Evening", "🌆"),
                    ("Night", "🌙")
                ]:
                    count = period_commits[period]
                    percentage = (count / total_commits * 100) if total_commits > 0 else 0
                    bar_length = int((count / max_commits) * 20)
                    bar = '█' * bar_length + '⋅' * (20 - bar_length)
                    
                    stats_section += f'{emoji} {period:<8} {count:3d} commits {bar} {percentage:4.1f}%\n'
                
                stats_section += '```\n\n'
                
                # 한국 시간으로 변환
                kst = timezone(timedelta(hours=9))
                current_time = datetime.now(kst)
                
                stats_section += f'마지막 업데이트: {current_time.strftime("%Y-%m-%d %H:%M:%S")} (KST)\n\n---\n\n'
                
                # 새로운 내용 조합
                new_content = (
                    current_content[:insert_position] + 
                    '\n' + stats_section + 
                    current_content[insert_position:]
                )
                
                # README.md 업데이트
                profile_repo.update_file(
                    path="README.md",
                    message="📊 커밋 통계 자동 업데이트",
                    content=new_content,
                    sha=contents.sha
                )
                print("프로필 README.md 업데이트 완료!")
            else:
                print("hits 배지를 찾을 수 없습니다.")
                
        except Exception as e:
            print(f"에러 발생: {str(e)}")
            sys.exit(1)

    except Exception as e:
        print(f"에러 발생: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 

    