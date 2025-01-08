from github import Github
from collections import defaultdict
from datetime import datetime
import os
import sys

def main():
    # 토큰 확인
    token = os.getenv('GH_TOKEN')
    if not token:
        print("Error: GH_TOKEN not found")
        sys.exit(1)

    print("GitHub 연결 시도 중...")
    g = Github(token)

    try:
        # 현재 사용자 가져오기
        user = g.get_user()
        print(f"사용자 {user.login} 으로 연결됨")

        # EXPOIR0405 저장소 가져오기
        repo = g.get_repo(f"{user.login}/EXPOIR0405")
        print(f"저장소 연결됨: {repo.name}")

        # 커밋 시간 통계를 저장할 딕셔너리
        commit_hours = defaultdict(int)
        total_commits = 0

        # 사용자의 모든 저장소들을 순회
        print("커밋 분석 시작...")
        for user_repo in user.get_repos():
            try:
                print(f"저장소 분석 중: {user_repo.name}")
                commits = user_repo.get_commits(author=user.login)
                for commit in commits:
                    commit_time = commit.commit.author.date
                    hour = commit_time.hour
                    commit_hours[hour] += 1
                    total_commits += 1
            except Exception as e:
                print(f"저장소 {user_repo.name} 처리 중 에러: {str(e)}")
                continue

        print(f"총 {total_commits}개의 커밋 분석됨")

        # README.md 내용 생성
        readme_content = '# 📊 나의 GitHub 활동 통계\n\n'
        readme_content += '## 🕒 커밋 시간대 분석\n\n'
        readme_content += '```text\n'
        
        max_commits = max(commit_hours.values()) if commit_hours else 1
        
        for hour in range(24):
            count = commit_hours.get(hour, 0)
            bar_length = int((count / max_commits) * 20)
            bar = '█' * bar_length
            readme_content += f'{hour:02d}:00 {bar} {count:3d}\n'
        
        readme_content += '```\n\n'
        readme_content += f'총 분석된 커밋 수: {total_commits}\n'
        readme_content += f'\n마지막 업데이트: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'

        # README.md 파일 업데이트
        try:
            # 기존 README.md 파일 가져오기
            contents = repo.get_contents("README.md")
            repo.update_file(
                path="README.md",
                message="📊 커밋 통계 자동 업데이트",
                content=readme_content,
                sha=contents.sha
            )
            print("README.md 파일 업데이트 완료!")
        except Exception as e:
            # README.md 파일이 없는 경우 새로 생성
            repo.create_file(
                path="README.md",
                message="📊 커밋 통계 초기 생성",
                content=readme_content
            )
            print("README.md 파일 생성 완료!")

    except Exception as e:
        print(f"에러 발생: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 