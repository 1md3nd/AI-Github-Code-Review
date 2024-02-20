from Github import GithubWrapper

g = GithubWrapper()


repo = 'pypa/pip'

res = g.fetch_repo(repo)

print("Get the repo raw data")
print(res)
print("repo description")
print(res.description)
print('Raw data')
print(res.raw_data)

# print('Repo tree')

# tree = g.get_tree(repo)
# print(tree)