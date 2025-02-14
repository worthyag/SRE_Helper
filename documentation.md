# Final Project

# Part 1: Creating a Flask API (with a database and AI integration) and deploying using Ansible (with git and jenkins)
## Steps needed to complete part 1
### Creating 4 New Virtual Machines
1. **`ansible_project`** for `ansible` that will control the other three (`192.168.2.140`)
2. **`jenkins_git_project`** / **`jenkins_git_node`**  for `git` and `jenkins`. (`192.168.2.141`)
3. **`flask_project`** / **`flask_node`** (`httpd` / `nginx`) (`192.168.2.142`)
4. **`db_project`** for the database (`mysql`) (`192.168.2.143`)

### Create an Application that integrates the Gemini API.
1. Create a repo for the app and create a local db (keep the code, you will make something similar on **`db_project`**).
2. Write the code and commit often (it will be a flask app, find a reason for it to need a db).
    1. Keep track of any libraries you’ve had to download (they will be in the jenkins pipeline or the ansible playbook)
3. Check that it runs properly.
   1. Format the output of the request (etc).
5. Make sure that it has a good UI.
6. Push it to GitHub.

### Download ansible onto ansible_project VM and set up PLA.
1. Download `ansible`.
    1. Install pip (`yum install pip`)
    2. Install `ansible` (`yum install ansible`)
2. Set up PLA to the other VMs (**`jenkins_git_project`**, **`flask_project`**, **`db_project`**).
    1. Add aliases to the `/etc/hosts`.
    2. Use `ssh-add` (you will have to add the key again every time you start a new session).
    3. Test the connections.

## Applying the steps
