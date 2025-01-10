from github import Github
from collections import defaultdict
from datetime import datetime
import os
import sys
import traceback

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
            print("Error: GT_TOKEN not found in environment variables")
            sys.exit(1)

        print("GitHub 연결 시도 중...")
        g = Github(token)
        user = g.get_user()
        
        # TimeTable 저장소 가져오기
        repo = g.get_repo(f"{user.login}/TimeTable")  # TimeTable 저장소 지정
        
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

        # README.md 내용 생성 (시간대별 커밋 분석만)
        readme_content = '## ⏰ 시간대별 커밋 분석\n\n'
        readme_content += '```text\n'
        
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
            
            readme_content += f'{i} {emoji} {period:<8} {count:3d} commits {bar} {percentage:4.1f}%\n'
        
        readme_content += '```\n\n'
        readme_content += f'마지막 업데이트: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'

        try:
            # TimeTable의 README.md 파일 생성 또는 업데이트
            try:
                contents = repo.get_contents("README.md")
                repo.update_file(
                    path="README.md",
                    message="📊 커밋 통계 자동 업데이트",
                    content=readme_content,
                    sha=contents.sha
                )
            except:
                repo.create_file(
                    path="README.md",
                    message="📊 커밋 통계 초기 생성",
                    content=readme_content
                )
            print("README.md 파일 업데이트 완료!")

        except Exception as e:
            print(f"README.md 업데이트 중 에러: {str(e)}")
            sys.exit(1)

    except Exception as e:
        print(f"에러 발생: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 

    