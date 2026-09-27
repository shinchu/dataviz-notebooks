# dataviz-notebooks

```
git worktree add ../dataviz-answer [hash]
git worktree remove ../dataviz-answer
```

The answers-worktree above checks out a commit that still has the answers.
Before publishing a notebook, remove its answer cells (code cells starting
with `# answer`, together with their outputs):

```
python3 scripts/strip_answers.py week_1/intro-colab-python.ipynb [...]
```

The script is idempotent. Run its test with `uvx pytest tests`.
