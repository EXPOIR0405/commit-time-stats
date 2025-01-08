from github import Github
from collections import defaultdict
from datetime import datetime
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
    token = os.getenv('GH_TOKEN')
    if not token:
        print("Error: GH_TOKEN not found")
        sys.exit(1)

    print("GitHub 연결 시도 중...")
    g = Github(token)

    try:
        user = g.get_user()
        print(f"사용자 {user.login} 으로 연결됨")
        repo = g.get_repo(f"{user.login}/EXPOIR0405")
        
        # 시간대별 커밋 수 저장
        period_commits = {
            "Morning": 0,
            "Daytime": 0,
            "Evening": 0,
            "Night": 0
        }
        total_commits = 0

        print("커밋 분석 시작...")
        for user_repo in user.get_repos():
            try:
                print(f"저장소 분석 중: {user_repo.name}")
                commits = user_repo.get_commits(author=user.login)
                for commit in commits:
                    hour = commit.commit.author.date.hour
                    period, _ = get_time_period(hour)
                    period_commits[period] += 1
                    total_commits += 1
            except Exception as e:
                print(f"저장소 {user_repo.name} 처리 중 에러: {str(e)}")
                continue

        print(f"총 {total_commits}개의 커밋 분석됨")

        # 기존 README.md 읽기
        contents = repo.get_contents("README.md")
        existing_content = contents.decoded_content.decode('utf-8')
        
        # GitHub Stats 섹션 찾기
        stats_section_marker = "## ✍️ GitHub Stats ✍️"
        stats_index = existing_content.find(stats_section_marker)
        
        # 다음 섹션(Contact) 찾기
        contact_section = "## 📧 Contact 📧"
        contact_index = existing_content.find(contact_section)
        
        if stats_index == -1 or contact_index == -1:
            print("필요한 섹션을 찾을 수 없습니다.")
            return
        
        # GitHub Stats 섹션의 끝 부분 찾기 (Contact 섹션 직전)
        insert_position = contact_index
        
        # 새로운 통계 섹션 생성
        commit_stats_section = '\n## ⏰ 시간대별 커밋 분석\n\n'
        commit_stats_section += '```text\n'
        
        max_commits = max(period_commits.values()) if period_commits else 1
        
        for i, (period, emoji) in enumerate([
            ("Morning", "🌞"),
            ("Daytime", "🏢"),
            ("Evening", "🌆"),
            ("Night", "🌙")
        ], 1):
            count = period_commits[period]
            percentage = (count / total_commits * 100) if total_commits > 0 else 0
            bar_length = int((count / max_commits) * 20)
            bar = '█' * bar_length + '⋅' * (20 - bar_length)
            
            commit_stats_section += f'{i} {emoji} {period:<8} {count:3d} commits {bar} {percentage:4.1f}%\n'
        
        commit_stats_section += '```\n'
        commit_stats_section += f'\n마지막 업데이트: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n'
        commit_stats_section += "---\n\n"  # 구분선 추가
        
        # 새로운 README 내용 조합
        new_content = (
            existing_content[:insert_position] + 
            commit_stats_section + 
            existing_content[insert_position:]
        )

        # README.md 업데이트
        repo.update_file(
            path="README.md",
            message="📊 커밋 통계 자동 업데이트",
            content=new_content,
            sha=contents.sha
        )
        print("README.md 파일 업데이트 완료!")

    except Exception as e:
        print(f"에러 발생: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 

    