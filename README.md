# Ansible Notes

## Overview

Inventory file:
* hosts:
  * ansible-web01
  * ansible-web02
  * ansible-db01
* Inventory Host var for private ssh key file
* Inventory Group var for ansible_user=vagrant

## Ansible from Commandline

```bash
# check connectivity
ansible all -i hosts -m ping
# Facts
ansible dbservers -i hosts -m setup
# Run a command on a group of servers
ansible all -i hosts -m command -a 'uptime'
# Install Apache (as root) - repeat shows idempotent
# -a - module argument
# -b - become - run with privilege esculation (default sudo)
ansible ansible-web01 -i hosts -m yum -a "name=httpd state=present" -b
# remove package
ansible ansible-web01 -i hosts -m yum -a "name=httpd state=absent" -b
```

## All-in-one playbook

a1_playbook:
* Uses variable to install multiple items
* Runs getenforce & captures output into variable sestatus
* Installs Apache and starts the service

```bash
ansible-playbook -i hosts a1_playbook.yml
```

A Playbook can contain 1 or more plays.

### Handlers
Tasks that execute once at end of a play, if notified. E.g.
```bash
tasks:
- name: install ngix
  yum:
    name: nginx
    state: latest
  notify: restart nginx

handlers:
- name: restart nginx
  service:
    name: nginx
    state: restarted
```

## Roles

Example roles at <http://galaxy.ansible.com>

`site.yml` playbook:
* Targets hosts with roles

```bash
# Create two roles
mkdir roles; cd roles
ansible-galaxy init common
ansible-galaxy init apache
```

Common tasks, handlers and template files:
* (new) `roles/common/tasks/selinux.yml`
* (new) `roles/common/tasks/ntp.yml`
* (mod) `roles/common/handlers/main.yml`
* (new) `roles/common/tempates/ntp.conf.j2`
  * Has ntpserver variable
* (new) `group_vars/all`
  * New dir and file
  * Contains ntpserver value
* (mod) `roles/common/tasks/main.yml`
  * put in epel repo

Files only have sequence sections for type. E.g. task sequences only

Apache role files:
* (mod) `roles/apache/tasks/main.yml`
  * Uses variable for apache_dirs
  * Uses var for dest apache_docroot
  * Uses var to select template based on OS family
* (new) `roles/apache/templates/httpd.conf-RedHat.j2`
* (new) `roles/apache/templates/index.html.j2`
  * Displays ansible_distribution and host names from the webservers group
* (mod) `roles/apache/handlers/main.yml`
  * Add restart apache handler
* (new) `group_vars/webservers`
  * Vars for apache etc

## Web Role - Built on other roles

```bash
cd roles
ansible-galaxy init web
```

## Notes from Webinar
https://www.ansible.com/resources/webinars-training/introduction-to-ansible

Does all these Use Cases:
* Configuration/State Management - Like Chef, Puppet and CFEngine
   * Security and compliance
* Application Deployment - Like Fabric, Capistrano and Nolio
* Workflow Orchestration - Like BMC, Mcollective and Chef Metal
* Provisioning - Like Cobbler, AWS and Juju
   * New VMs or cloud based services
* Orchestrate the application lifecycle
   * Continuous Delivery

### Installation
Preferred
```bash
pip install ansible
```

### How Ansible Works
Playbooks:
* Invoke modules, to;
* Execute tasks in sequence

Inventory:
* Can come from multiple sources

Plugin: E.g. Support for alternative to ssh or WINRM connections to services.

### Modules
https://docs.ansible.com/ansible/latest/modules/modules_by_category.html

Command modules:
* command - Not processed through the shell
* shell
* script
* raw - Raw ssh command - bypasses the python modules mechanism. Good for bootstrap, or Win powershell execution.