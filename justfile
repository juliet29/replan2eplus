
push:
  rm -rf dist && source .env && uv version --bump patch && uv build && uv publish 


update-deps:
  uv add ~/_UILCode/gqe-phd/fpopt/utils4plans/
  uv add ~/_UILCode/gqe-phd/fpopt/geomeppy/

add-local-geomeppy:
  uv add --editable "geomeppyupdated @ /Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/geomeppyupdated"
# update-geomeppy:
#   uv add ~/_UILCode/gqe-phd/fpopt/geomeppy/


test-ops:
  uv run pytest tests/test_ops


################### 
################### 
# TRIALS
################### 

study-case:
  uv run replan studies study-case



publish-tag end:
  @echo "Have you updated the version number for pushing to pypi?" 
  @read status;


  @echo "Have you pushed the code with this new version number?" 
  @read status;

  git tag -a v0.1.{{end}} -m v0.1.{{end}}
  git push --tag
  sleep 2
  gh run list
