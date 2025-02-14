# Final Project

# Part 1: Creating a Flask API (with a database and AI integration) and deploying using Ansible (with git and jenkins)
## Steps needed to complete part 1
### Creating 4 New Virtual Machines
1. **`ansible_project`** for `ansible` that will control the other three (`192.168.2.140`)
2. **`jenkins_git_project`** / **`jenkins_git_node`**  for `git` and `jenkins`. (`192.168.2.141`)
3. **`flask_project`** / **`flask_node`** (`httpd` / `nginx`) (`192.168.2.142`)
4. **`db_project`** for the database (`mysql`) (`192.168.2.143`)
