import datetime
import os
from utils.github import get_pull_requests_data, GithubStats, get_reviewer_description

github_token = os.getenv('GITHUB_TOKEN', None)
developers = {"debiff": ["Simone Biffi", True],
                      "Undermaken": ["Matteo Boschi", True],
                      "thisisjp": ["Jacopo Pompilii", True],
                      "pp - ps": ["Pietro Stroia", True],
                      "fabriziofff": ["Fabrizio Filizola", True],
                      "pietro909": ["Pietro Grandi", True],
                      "CrisTofani": ["Cristiano Tofani", True]}
end = datetime.datetime.now()
start = end - datetime.timedelta(days=60)
# it assumes that each item is a valid project inside pagopa org (https://github.com/pagopa)
stats_for_projects = ['io-app']
for project in stats_for_projects:
    pr_created = get_pull_requests_data(github_token, project, start, end)
    pr_reviews = get_pull_requests_data(github_token, project, start, end, 'closed', 'updated')
    stats = GithubStats(pr_created, pr_reviews)
    if stats.total_pr_reviewed == 0 and stats.total_pr_created == 0:
        continue
    # collect reviewers and sort by performance
    reviewers = list(reversed(sorted(filter(lambda k: developers.get(k, (k, False))[1], stats.data.keys()),
                                     key=lambda k: stats.data[k].contribution_ratio)))
    # collect not reviewers
    not_reviewers = list(filter(lambda k: k not in reviewers, stats.data.keys()))
    # put not reviewer at the end
    reviewers.extend(not_reviewers)
    for key in reviewers:
        value = stats.data[key]
        developer, is_reviewer = developers.get(key, (key, False))
        msg = f'{developer}\n'
        if is_reviewer:
            msg += f'{get_reviewer_description(value)}\n'
        msg += f'PR created: {value.pr_created_count}\n'
        msg += f'PR created contribution: {value.pr_created_contribution}\n'
        msg += f'PR reviewed: {value.pr_review_count}\n'
        msg += f'PR reviewed contribution: {value.pr_review_contribution}\n'
        print(msg)